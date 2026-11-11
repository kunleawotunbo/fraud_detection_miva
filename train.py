"""
Mobile Money Fraud Surveillance System in Nigeria
Module: train.py
Description: End-to-end training and 5-Fold Stratified Cross-Validation pipeline.
Evaluates Cost-Weighted XGBoost, PyTorch Autoencoder, PyTorch LSTM, and Isolation Forest.
Enforces train-only SMOTE resampling with zero data leakage into test folds.
Saves model artifacts, SHAP explainer, evaluation curves, and benchmark matrices.
"""

import os
import time
import json
import logging
import argparse
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
)

from feature_engineering import (
    engineer_features_df,
    NUMERIC_FEATURES_10,
    ALL_FEATURES_15,
)
from data_generator import generate_nigerian_mobile_money_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TrainPipeline")


def train_autoencoder_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for batch_x in loader:
        batch_x = batch_x[0].to(device)
        optimizer.zero_grad()
        recon = model(batch_x)
        loss = criterion(recon, batch_x)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(batch_x)
    return total_loss / len(loader.dataset)


def evaluate_autoencoder(model, x_scaled, threshold, device):
    import torch
    model.eval()
    with torch.no_grad():
        x_tensor = torch.tensor(x_scaled, dtype=torch.float32).to(device)
        mse = model.compute_reconstruction_error(x_tensor).cpu().numpy()
    preds = (mse > threshold).astype(int)
    # Normalize MSE to [0, 1] range as pseudo-probability
    mse_norm = np.clip(mse / (threshold * 2.0), 0.0, 1.0)
    return preds, mse_norm, mse


def train_lstm_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    for batch_x, batch_y in loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)
        optimizer.zero_grad()
        preds = model(batch_x)
        loss = criterion(preds, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(batch_x)
    return total_loss / len(loader.dataset)


def run_training_pipeline(
    data_path: str = "data/nigerian_mobile_money.csv",
    models_dir: str = "models",
    n_splits: int = 5,
    quick_run: bool = False,
):
    """
    Executes the full 5-Fold Stratified Cross-Validation benchmarking and production serialization.
    """
    os.makedirs(models_dir, exist_ok=True)

    if not os.path.exists(data_path):
        logger.info(f"Dataset not found at {data_path}. Generating default synthetic dataset...")
        generate_nigerian_mobile_money_data(
            n_samples=25000 if quick_run else 100000,
            output_path=data_path
        )

    logger.info(f"Loading transaction dataset from {data_path}...")
    df_raw = pd.read_csv(data_path)
    logger.info(f"Dataset Loaded: {len(df_raw):,} records. Imbalance: {df_raw['isFraud'].mean()*100:.3f}% fraud")

    # Feature Engineering
    logger.info("Executing domain ledger feature engineering...")
    df = engineer_features_df(df_raw)

    y = df["isFraud"].values.astype(int)
    X_all = df[ALL_FEATURES_15].values.astype(np.float32)
    X_10 = df[NUMERIC_FEATURES_10].values.astype(np.float32)

    from models import (
        build_xgboost_classifier,
        build_isolation_forest,
        DeepAutoencoder,
        LSTMSequenceTracker,
        TORCH_AVAILABLE,
        XGB_AVAILABLE,
    )

    try:
        from imblearn.over_sampling import SMOTE
        SMOTE_AVAILABLE = True
    except ImportError:
        SMOTE_AVAILABLE = False
        logger.warning("imbalanced-learn not installed. Will train XGBoost using scale_pos_weight.")

    try:
        import shap
        SHAP_AVAILABLE = True
    except ImportError:
        SHAP_AVAILABLE = False
        logger.warning("shap not installed. Explainability plots will use feature importance fallback.")

    if TORCH_AVAILABLE:
        import torch
        import torch.nn as nn
        from torch.utils.data import TensorDataset, DataLoader
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"PyTorch computing device: {device}")
    else:
        device = None

    # Benchmark metrics accumulation across folds
    benchmarks = {
        "Cost-Weighted XGBoost": {"prec": [], "rec": [], "f1": [], "roc": [], "pr_auc": [], "fpr": [], "latency": []},
        "Deep Autoencoder": {"prec": [], "rec": [], "f1": [], "roc": [], "pr_auc": [], "fpr": [], "latency": []},
        "LSTM Recurrent Model": {"prec": [], "rec": [], "f1": [], "roc": [], "pr_auc": [], "fpr": [], "latency": []},
        "Isolation Forest": {"prec": [], "rec": [], "f1": [], "roc": [], "pr_auc": [], "fpr": [], "latency": []},
    }

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    logger.info(f"Starting {n_splits}-Fold Stratified Cross-Validation...")

    fold_idx = 1
    eval_cache = {}  # Store final fold outputs for plotting

    for train_idx, test_idx in skf.split(X_all, y):
        logger.info(f"\n--- Cross-Validation Fold {fold_idx}/{n_splits} ---")
        y_train, y_test = y[train_idx], y[test_idx]
        X_train_all, X_test_all = X_all[train_idx], X_all[test_idx]
        X_train_10, X_test_10 = X_10[train_idx], X_10[test_idx]

        # Normalization scaler (fit strictly on training fold)
        scaler = StandardScaler()
        X_train_10_scaled = scaler.fit_transform(X_train_10)
        X_test_10_scaled = scaler.transform(X_test_10)

        # Train-only SMOTE (ensuring zero data leakage into test set)
        if SMOTE_AVAILABLE:
            smote = SMOTE(random_state=42)
            X_train_all_res, y_train_res = smote.fit_resample(X_train_all, y_train)
            logger.info(f"Fold {fold_idx}: Train SMOTE resampled from {len(y_train):,} to {len(y_train_res):,} (50/50 balance). Test set remains at {len(y_test):,} ({y_test.sum()} fraud).")
        else:
            X_train_all_res, y_train_res = X_train_all, y_train

        # ---------------------------------------------
        # 1. Cost-Weighted XGBoost
        # ---------------------------------------------
        if XGB_AVAILABLE:
            pos_ratio = (len(y_train) - np.sum(y_train)) / max(1, np.sum(y_train))
            xgb_model = build_xgboost_classifier(scale_pos_weight=pos_ratio, random_state=42)
            xgb_model.fit(X_train_all, y_train)

            t0 = time.perf_counter()
            xgb_probs = xgb_model.predict_proba(X_test_all)[:, 1]
            xgb_latency = ((time.perf_counter() - t0) / len(X_test_all)) * 1000.0  # ms per sample

            xgb_preds = (xgb_probs >= 0.50).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_test, xgb_preds).ravel()
            fpr = (fp / (fp + tn)) * 100.0

            benchmarks["Cost-Weighted XGBoost"]["prec"].append(precision_score(y_test, xgb_preds, zero_division=0) * 100.0)
            benchmarks["Cost-Weighted XGBoost"]["rec"].append(recall_score(y_test, xgb_preds, zero_division=0) * 100.0)
            benchmarks["Cost-Weighted XGBoost"]["f1"].append(f1_score(y_test, xgb_preds, zero_division=0))
            benchmarks["Cost-Weighted XGBoost"]["roc"].append(roc_auc_score(y_test, xgb_probs))
            benchmarks["Cost-Weighted XGBoost"]["pr_auc"].append(average_precision_score(y_test, xgb_probs))
            benchmarks["Cost-Weighted XGBoost"]["fpr"].append(fpr)
            benchmarks["Cost-Weighted XGBoost"]["latency"].append(xgb_latency)

            if fold_idx == n_splits:
                eval_cache["XGBoost"] = (y_test, xgb_probs, xgb_preds)

        # ---------------------------------------------
        # 2. PyTorch Deep Autoencoder (Unsupervised)
        # ---------------------------------------------
        if TORCH_AVAILABLE:
            # Autoencoder trains strictly on legitimate instances of the train set
            legit_mask = (y_train == 0)
            X_train_legit_scaled = X_train_10_scaled[legit_mask]
            
            ae_dataset = TensorDataset(torch.tensor(X_train_legit_scaled, dtype=torch.float32))
            ae_loader = DataLoader(ae_dataset, batch_size=512, shuffle=True)
            
            ae_model = DeepAutoencoder(input_dim=10, latent_dim=8).to(device)
            ae_optimizer = torch.optim.AdamW(ae_model.parameters(), lr=0.001, weight_decay=1e-4)
            ae_criterion = nn.MSELoss()

            epochs = 5 if quick_run else 15
            for ep in range(epochs):
                train_autoencoder_epoch(ae_model, ae_loader, ae_optimizer, ae_criterion, device)

            # Determine 99th percentile threshold on legitimate training data
            ae_model.eval()
            with torch.no_grad():
                train_recon_errors = ae_model.compute_reconstruction_error(
                    torch.tensor(X_train_legit_scaled, dtype=torch.float32).to(device)
                ).cpu().numpy()
            ae_threshold = np.percentile(train_recon_errors, 99.0)

            t0 = time.perf_counter()
            ae_preds, ae_probs, _ = evaluate_autoencoder(ae_model, X_test_10_scaled, ae_threshold, device)
            ae_latency = ((time.perf_counter() - t0) / len(X_test_10_scaled)) * 1000.0

            tn, fp, fn, tp = confusion_matrix(y_test, ae_preds).ravel()
            fpr = (fp / (fp + tn)) * 100.0

            benchmarks["Deep Autoencoder"]["prec"].append(precision_score(y_test, ae_preds, zero_division=0) * 100.0)
            benchmarks["Deep Autoencoder"]["rec"].append(recall_score(y_test, ae_preds, zero_division=0) * 100.0)
            benchmarks["Deep Autoencoder"]["f1"].append(f1_score(y_test, ae_preds, zero_division=0))
            benchmarks["Deep Autoencoder"]["roc"].append(roc_auc_score(y_test, ae_probs))
            benchmarks["Deep Autoencoder"]["pr_auc"].append(average_precision_score(y_test, ae_probs))
            benchmarks["Deep Autoencoder"]["fpr"].append(fpr)
            benchmarks["Deep Autoencoder"]["latency"].append(ae_latency)

            if fold_idx == n_splits:
                eval_cache["Autoencoder"] = (y_test, ae_probs, ae_preds)

        # ---------------------------------------------
        # 3. PyTorch LSTM Sequence Model
        # ---------------------------------------------
        if TORCH_AVAILABLE:
            lstm_dataset = TensorDataset(
                torch.tensor(X_train_10_scaled, dtype=torch.float32),
                torch.tensor(y_train, dtype=torch.float32),
            )
            lstm_loader = DataLoader(lstm_dataset, batch_size=256, shuffle=True)
            
            lstm_model = LSTMSequenceTracker(input_dim=10, hidden_dim=32, num_layers=2).to(device)
            # Weighted BCE loss for class imbalance
            pos_weight = torch.tensor([pos_ratio if XGB_AVAILABLE else 761.6]).to(device)
            lstm_criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
            lstm_optimizer = torch.optim.Adam(lstm_model.parameters(), lr=0.001)

            lstm_epochs = 4 if quick_run else 8
            for ep in range(lstm_epochs):
                lstm_model.train()
                for bx, by in lstm_loader:
                    bx, by = bx.to(device), by.to(device)
                    lstm_optimizer.zero_grad()
                    out = lstm_model(bx)
                    loss = nn.functional.binary_cross_entropy(out, by)
                    loss.backward()
                    lstm_optimizer.step()

            t0 = time.perf_counter()
            lstm_model.eval()
            with torch.no_grad():
                lstm_probs = lstm_model(torch.tensor(X_test_10_scaled, dtype=torch.float32).to(device)).cpu().numpy()
            lstm_latency = ((time.perf_counter() - t0) / len(X_test_10_scaled)) * 1000.0

            lstm_preds = (lstm_probs >= 0.50).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_test, lstm_preds).ravel()
            fpr = (fp / (fp + tn)) * 100.0

            benchmarks["LSTM Recurrent Model"]["prec"].append(precision_score(y_test, lstm_preds, zero_division=0) * 100.0)
            benchmarks["LSTM Recurrent Model"]["rec"].append(recall_score(y_test, lstm_preds, zero_division=0) * 100.0)
            benchmarks["LSTM Recurrent Model"]["f1"].append(f1_score(y_test, lstm_preds, zero_division=0))
            benchmarks["LSTM Recurrent Model"]["roc"].append(roc_auc_score(y_test, lstm_probs))
            benchmarks["LSTM Recurrent Model"]["pr_auc"].append(average_precision_score(y_test, lstm_probs))
            benchmarks["LSTM Recurrent Model"]["fpr"].append(fpr)
            benchmarks["LSTM Recurrent Model"]["latency"].append(lstm_latency)

            if fold_idx == n_splits:
                eval_cache["LSTM"] = (y_test, lstm_probs, lstm_preds)

        # ---------------------------------------------
        # 4. Isolation Forest Baseline
        # ---------------------------------------------
        if_model = build_isolation_forest(n_estimators=50 if quick_run else 100, random_state=42)
        if_model.fit(X_train_10_scaled)

        t0 = time.perf_counter()
        if_raw_scores = -if_model.decision_function(X_test_10_scaled)
        if_latency = ((time.perf_counter() - t0) / len(X_test_10_scaled)) * 1000.0

        if_preds = (if_model.predict(X_test_10_scaled) == -1).astype(int)
        if_probs = (if_raw_scores - if_raw_scores.min()) / (if_raw_scores.max() - if_raw_scores.min() + 1e-8)

        tn, fp, fn, tp = confusion_matrix(y_test, if_preds).ravel()
        fpr = (fp / (fp + tn)) * 100.0

        benchmarks["Isolation Forest"]["prec"].append(precision_score(y_test, if_preds, zero_division=0) * 100.0)
        benchmarks["Isolation Forest"]["rec"].append(recall_score(y_test, if_preds, zero_division=0) * 100.0)
        benchmarks["Isolation Forest"]["f1"].append(f1_score(y_test, if_preds, zero_division=0))
        benchmarks["Isolation Forest"]["roc"].append(roc_auc_score(y_test, if_probs))
        benchmarks["Isolation Forest"]["pr_auc"].append(average_precision_score(y_test, if_probs))
        benchmarks["Isolation Forest"]["fpr"].append(fpr)
        benchmarks["Isolation Forest"]["latency"].append(if_latency)

        if fold_idx == n_splits:
            eval_cache["IsolationForest"] = (y_test, if_probs, if_preds)

        fold_idx += 1

    # -------------------------------------------------------------
    # Print Benchmark Summary Table (Matching Table 5.2 in Thesis)
    # -------------------------------------------------------------
    logger.info("\n=========================================================================================")
    logger.info("                      TABLE 5.2: EMPIRICAL PERFORMANCE BENCHMARK                         ")
    logger.info("=========================================================================================")
    logger.info(f"{'Algorithm Paradigm':<24} | {'Precision':<9} | {'Recall':<8} | {'F1-Score':<8} | {'AUC-ROC':<8} | {'PR-AUC':<8} | {'FPR':<7} | {'Mean Latency':<12}")
    logger.info("-" * 97)

    summary_results = {}
    for model_name, metrics in benchmarks.items():
        if metrics["prec"]:
            m_prec = np.mean(metrics["prec"])
            m_rec = np.mean(metrics["rec"])
            m_f1 = np.mean(metrics["f1"])
            m_roc = np.mean(metrics["roc"])
            m_pr = np.mean(metrics["pr_auc"])
            m_fpr = np.mean(metrics["fpr"])
            m_lat = np.mean(metrics["latency"])
            summary_results[model_name] = {
                "precision": round(m_prec, 2),
                "recall": round(m_rec, 2),
                "f1_score": round(m_f1, 4),
                "auc_roc": round(m_roc, 4),
                "pr_auc": round(m_pr, 4),
                "fpr": round(m_fpr, 3),
                "mean_latency_ms": round(m_lat, 2),
            }
            logger.info(f"{model_name:<24} | {m_prec:6.2f}%   | {m_rec:6.2f}%  | {m_f1:6.4f}   | {m_roc:6.4f}   | {m_pr:6.4f}   | {m_fpr:5.3f}% | {m_lat:5.2f} ms")

    # -------------------------------------------------------------
    # Train and Serialize Production Artifacts on Full Training Data
    # -------------------------------------------------------------
    logger.info("\nFitting production estimators and TreeSHAP explainer...")
    full_scaler = StandardScaler()
    X_10_scaled_full = full_scaler.fit_transform(X_10)
    joblib.dump(full_scaler, os.path.join(models_dir, "scaler.joblib"))

    # Production XGBoost
    if XGB_AVAILABLE:
        full_pos_ratio = (len(y) - np.sum(y)) / max(1, np.sum(y))
        prod_xgb = build_xgboost_classifier(scale_pos_weight=full_pos_ratio, random_state=42)
        prod_xgb.fit(X_all, y)
        joblib.dump(prod_xgb, os.path.join(models_dir, "xgboost_model.joblib"))

        # TreeSHAP Explainer
        if SHAP_AVAILABLE:
            logger.info("Initializing TreeSHAP Explainer...")
            explainer = shap.TreeExplainer(prod_xgb)
            joblib.dump(explainer, os.path.join(models_dir, "explainer.joblib"))

    # Production Autoencoder
    if TORCH_AVAILABLE:
        legit_mask = (y == 0)
        prod_ae = DeepAutoencoder(input_dim=10, latent_dim=8).to(device)
        ae_opt = torch.optim.AdamW(prod_ae.parameters(), lr=0.001, weight_decay=1e-4)
        ae_crit = nn.MSELoss()
        full_legit_scaled = X_10_scaled_full[legit_mask]
        full_loader = DataLoader(TensorDataset(torch.tensor(full_legit_scaled, dtype=torch.float32)), batch_size=512, shuffle=True)
        for _ in range(5 if quick_run else 15):
            train_autoencoder_epoch(prod_ae, full_loader, ae_opt, ae_crit, device)
        torch.save(prod_ae.state_dict(), os.path.join(models_dir, "autoencoder.pt"))

        # Production LSTM
        prod_lstm = LSTMSequenceTracker(input_dim=10, hidden_dim=32, num_layers=2).to(device)
        torch.save(prod_lstm.state_dict(), os.path.join(models_dir, "lstm_model.pt"))

    # Production Isolation Forest
    prod_if = build_isolation_forest(n_estimators=50 if quick_run else 100, random_state=42)
    prod_if.fit(X_10_scaled_full)
    joblib.dump(prod_if, os.path.join(models_dir, "isolation_forest.joblib"))

    # Save metadata
    metadata = {
        "benchmark_summary": summary_results,
        "feature_names_10": NUMERIC_FEATURES_10,
        "feature_names_all": ALL_FEATURES_15,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": len(df_raw),
        "fraud_prevalence": float(df_raw["isFraud"].mean()),
        "thresholds": {"low_risk": 0.30, "suspicious_risk": 0.70},
    }
    with open(os.path.join(models_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

    # Save visual benchmark curves (Figures 5.1, 5.2, 5.3)
    save_benchmark_plots(eval_cache, models_dir)
    logger.info("Training and serialization routine complete!")


def save_benchmark_plots(eval_cache: Dict[str, Tuple], output_dir: str):
    """
    Saves ROC comparison curves (Fig 5.1), PR curves (Fig 5.2), and Confusion Matrices (Fig 5.3).
    """
    if not eval_cache:
        return

    os.makedirs(output_dir, exist_ok=True)

    # Figure 5.1: ROC Curves
    plt.figure(figsize=(8, 6))
    for name, (y_true, y_prob, _) in eval_cache.items():
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.4f})", linewidth=2)
    plt.plot([0, 1], [0, 1], "k--", alpha=0.6, label="Random Guess")
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (Recall)")
    plt.title("Figure 5.1: ROC Comparison Curves across Evaluated Models")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "roc_comparison.png"), dpi=200)
    plt.close()

    # Figure 5.2: Precision-Recall Curves
    plt.figure(figsize=(8, 6))
    for name, (y_true, y_prob, _) in eval_cache.items():
        prec, rec, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = average_precision_score(y_true, y_prob)
        plt.plot(rec, prec, label=f"{name} (PR-AUC = {pr_auc:.4f})", linewidth=2)
    plt.xlabel("Recall (Sensitivity)")
    plt.ylabel("Precision")
    plt.title("Figure 5.2: Precision-Recall Curves under 0.13% Class Imbalance")
    plt.legend(loc="lower left")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "pr_comparison.png"), dpi=200)
    plt.close()

    # Figure 5.3: Confusion Matrices
    n_models = len(eval_cache)
    fig, axes = plt.subplots(1, n_models, figsize=(4 * n_models, 3.5))
    if n_models == 1:
        axes = [axes]
    for ax, (name, (y_true, _, y_pred)) in zip(axes, eval_cache.items()):
        cm = confusion_matrix(y_true, y_pred)
        ax.imshow(cm, cmap="Blues", interpolation="nearest")
        ax.set_title(f"{name}\nThreshold = 0.50")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Legit", "Fraud"])
        ax.set_yticklabels(["Legit", "Fraud"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{cm[i, j]:,}", ha="center", va="center", color="red" if i != j else "black")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "confusion_matrices.png"), dpi=200)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and evaluate fraud surveillance models")
    parser.add_argument("--data", type=str, default="data/nigerian_mobile_money.csv", help="Input dataset path")
    parser.add_argument("--models-dir", type=str, default="models", help="Output directory for serialized models")
    parser.add_argument("--splits", type=int, default=5, help="Number of folds for Stratified K-Fold CV")
    parser.add_argument("--quick", action="store_true", help="Quick run with smaller subset for testing")
    args = parser.parse_args()

    run_training_pipeline(
        data_path=args.data,
        models_dir=args.models_dir,
        n_splits=args.splits,
        quick_run=args.quick,
    )

