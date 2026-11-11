"""
Mobile Money Fraud Surveillance System in Nigeria
Module: feature_engineering.py
Description: Implements domain-specific bilateral ledger accounting features,
data sanitization, negative-balance imputation, and channel one-hot encoding
as formalized in Chapter 3 (Equations 3.1 - 3.4) and Table 3.3.
"""

import logging
from typing import Dict, Any, Tuple, List, Union
import numpy as np
import pandas as pd

logger = logging.getLogger("FeatureEngineering")
logging.basicConfig(level=logging.INFO)

# Standard payment primitives defined in Nigerian switch topology
PAYMENT_TYPES = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]

# 10 core continuous/domain indicators (used by Neural Autoencoder & sequence tracking)
NUMERIC_FEATURES_10 = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "errorBalanceOrig",
    "errorBalanceDest",
    "isCompleteDrain",
    "amountToBalanceRatio",
]

# Full 15-dimensional feature set including one-hot channel primitives (used by XGBoost)
ALL_FEATURES_15 = NUMERIC_FEATURES_10 + [f"type_{t}" for t in PAYMENT_TYPES]


def sanitize_payload(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Validates and sanitizes an incoming raw transaction dictionary.
    Imputes negative balances to 0.0 with warning logs (conforming to TC-01).
    Casts numeric parameters to float32.
    """
    warnings = []
    sanitized = {}

    # Step validation
    raw_step = payload.get("step", 1)
    try:
        sanitized["step"] = float(np.float32(raw_step))
    except (ValueError, TypeError):
        sanitized["step"] = 1.0
        warnings.append("Malformed 'step' received; defaulted to 1.0")

    # Type validation
    raw_type = str(payload.get("type", "TRANSFER")).upper().strip()
    if raw_type not in PAYMENT_TYPES:
        warnings.append(f"Unrecognized channel '{raw_type}'; defaulting to TRANSFER")
        raw_type = "TRANSFER"
    sanitized["type"] = raw_type

    # Balance and Amount parsing with negative-balance protection
    for field in ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]:
        raw_val = payload.get(field, 0.0)
        try:
            val = float(np.float32(raw_val))
        except (ValueError, TypeError):
            val = 0.0
            warnings.append(f"Invalid numeric value for {field}; imputed to 0.0")

        if val < 0.0:
            warnings.append(f"Negative balance detected in {field} ({val}); imputed to 0.0 per TC-01")
            logger.warning(f"Negative balance detected in {field} ({val}); imputed to 0.0 per TC-01")
            val = 0.0

        sanitized[field] = val

    # Optional account identifiers
    sanitized["nameOrig"] = payload.get("nameOrig", "C_UNKNOWN")
    sanitized["nameDest"] = payload.get("nameDest", "M_UNKNOWN")

    return sanitized, warnings


def compute_domain_features_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes mathematical ledger discrepancy features for a single transaction dictionary.
    Formulas:
      - errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig (Equation 3.1)
      - errorBalanceDest = oldbalanceDest + amount - newbalanceDest (Equation 3.2)
      - isCompleteDrain = 1 if (newbalanceOrig == 0 and amount > 0) else 0 (Equation 3.3)
      - amountToBalanceRatio = amount / (oldbalanceOrg + 1e-5) (Equation 3.4)
    """
    amount = float(data.get("amount", 0.0))
    old_orig = float(data.get("oldbalanceOrg", 0.0))
    new_orig = float(data.get("newbalanceOrig", 0.0))
    old_dest = float(data.get("oldbalanceDest", 0.0))
    new_dest = float(data.get("newbalanceDest", 0.0))

    # Eq 3.1: Origin Ledger Discrepancy
    error_balance_orig = old_orig - amount - new_orig

    # Eq 3.2: Destination Ledger Discrepancy
    error_balance_dest = old_dest + amount - new_dest

    # Eq 3.3: Binary Complete Account Drain Indicator
    is_complete_drain = 1.0 if (new_orig == 0.0 and amount > 0.0) else 0.0

    # Eq 3.4: Capital Liquidation Ratio with smoothing epsilon
    amount_to_balance_ratio = amount / (old_orig + 1e-5)

    features = dict(data)
    features["errorBalanceOrig"] = float(np.float32(error_balance_orig))
    features["errorBalanceDest"] = float(np.float32(error_balance_dest))
    features["isCompleteDrain"] = float(np.float32(is_complete_drain))
    features["amountToBalanceRatio"] = float(np.float32(amount_to_balance_ratio))

    # One-hot categorical dummy encodings
    tx_type = str(data.get("type", "TRANSFER")).upper().strip()
    for pt in PAYMENT_TYPES:
        features[f"type_{pt}"] = 1.0 if tx_type == pt else 0.0

    return features


def engineer_features_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vectorized feature engineering on a Pandas DataFrame for batch processing.
    Downcasts continuous columns to float32 to conserve RAM.
    """
    df = df.copy()

    # Negative balance handling
    balance_cols = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    for col in balance_cols:
        if col in df.columns:
            neg_mask = df[col] < 0
            if neg_mask.any():
                logger.warning(f"Detected {neg_mask.sum()} negative values in {col}; imputing to 0.0")
                df.loc[neg_mask, col] = 0.0
            df[col] = df[col].astype(np.float32)

    if "step" in df.columns:
        df["step"] = df["step"].astype(np.float32)

    # Eq 3.1: errorBalanceOrig
    df["errorBalanceOrig"] = (df["oldbalanceOrg"] - df["amount"] - df["newbalanceOrig"]).astype(np.float32)

    # Eq 3.2: errorBalanceDest
    df["errorBalanceDest"] = (df["oldbalanceDest"] + df["amount"] - df["newbalanceDest"]).astype(np.float32)

    # Eq 3.3: isCompleteDrain
    df["isCompleteDrain"] = ((df["newbalanceOrig"] == 0.0) & (df["amount"] > 0.0)).astype(np.float32)

    # Eq 3.4: amountToBalanceRatio
    df["amountToBalanceRatio"] = (df["amount"] / (df["oldbalanceOrg"] + 1e-5)).astype(np.float32)

    # One-hot encoding for channel types
    if "type" in df.columns:
        for pt in PAYMENT_TYPES:
            col_name = f"type_{pt}"
            df[col_name] = (df["type"].str.upper() == pt).astype(np.float32)
    else:
        for pt in PAYMENT_TYPES:
            col_name = f"type_{pt}"
            if col_name not in df.columns:
                df[col_name] = 0.0

    return df


def extract_feature_vector(
    payload: Dict[str, Any], feature_set: str = "all"
) -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Sanitizes payload, derives features, and returns a numeric NumPy array (shape 1, D).
    
    Args:
        payload: raw transaction payload
        feature_set: '10' for the 10 continuous/domain features,
                     'all' for 15 features including channel one-hot dummies.
                     
    Returns:
        (feature_array, feature_names, warnings)
    """
    sanitized, warnings = sanitize_payload(payload)
    feat_dict = compute_domain_features_dict(sanitized)

    cols = NUMERIC_FEATURES_10 if feature_set == "10" else ALL_FEATURES_15
    vec = np.array([[feat_dict.get(c, 0.0) for c in cols]], dtype=np.float32)
    return vec, cols, warnings

