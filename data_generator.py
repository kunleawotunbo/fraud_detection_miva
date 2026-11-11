"""
Mobile Money Fraud Surveillance System in Nigeria
Module: data_generator.py
Description: Generates realistic synthetic Nigerian mobile money transactions
with severe class imbalance (0.13% fraud prevalence) modeling USSD account draining,
midnight velocity spikes (1 AM - 5 AM), and CICO agency banking cash-outs.
"""

import os
import argparse
import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DataGenerator")


def generate_nigerian_mobile_money_data(
    n_samples: int = 100000,
    fraud_ratio: float = 0.0013,
    random_state: int = 42,
    output_path: str = "data/nigerian_mobile_money.csv",
) -> pd.DataFrame:
    """
    Synthesizes a realistic mobile money transaction dataset matching Nigerian switch dynamics.
    
    Args:
        n_samples: Total number of records (default 100,000; full benchmark is 1,048,575).
        fraud_ratio: Target fraud prevalence (default 0.0013, i.e. 0.13%).
        random_state: Seed for reproducibility.
        output_path: Destination path for the generated CSV.
        
    Returns:
        Generated Pandas DataFrame.
    """
    np.random.seed(random_state)
    logger.info(f"Generating {n_samples:,} mobile money records with {fraud_ratio*100:.2f}% fraud target...")

    n_fraud = int(np.round(n_samples * fraud_ratio))
    n_legit = n_samples - n_fraud

    logger.info(f"Target distribution: {n_legit:,} Legitimate ({(n_legit/n_samples)*100:.2f}%), {n_fraud:,} Fraud ({(n_fraud/n_samples)*100:.2f}%)")

    # 1. Generate Legitimate Transactions
    # Hours across 30 days (steps 1 to 720 hours)
    # Legitimate transactions peak during daytime (8 AM - 9 PM)
    hours = np.random.choice(
        np.concatenate([
            np.random.randint(8, 22, size=int(n_legit * 0.85)),
            np.random.randint(0, 24, size=int(n_legit * 0.15)),
        ])
    )
    days = np.random.randint(0, 30, size=n_legit)
    step_legit = days * 24 + hours

    channel_choices = ["PAYMENT", "CASH_OUT", "CASH_IN", "TRANSFER", "DEBIT"]
    channel_probs = [0.35, 0.35, 0.18, 0.10, 0.02]
    type_legit = np.random.choice(channel_choices, size=n_legit, p=channel_probs)

    # Legitimate transaction amounts (log-normal distribution in NGN, typical ₦500 to ₦150,000)
    amount_legit = np.random.lognormal(mean=8.5, sigma=1.2, size=n_legit)
    amount_legit = np.clip(amount_legit, 100.0, 500000.0)

    # Origin balances for legitimate users (higher than amount in almost all cases)
    oldbalanceOrg_legit = amount_legit * np.random.uniform(1.1, 8.0, size=n_legit) + np.random.uniform(1000.0, 50000.0, size=n_legit)
    
    # In legitimate transactions, balance reconciles cleanly: new = old - amount (for outgoing) or new = old + amount (for CASH_IN)
    newbalanceOrig_legit = np.zeros(n_legit, dtype=np.float64)
    for i, t in enumerate(type_legit):
        if t in ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"]:
            newbalanceOrig_legit[i] = max(0.0, oldbalanceOrg_legit[i] - amount_legit[i])
        else:  # CASH_IN
            newbalanceOrig_legit[i] = oldbalanceOrg_legit[i] + amount_legit[i]

    # Destination balances
    oldbalanceDest_legit = np.random.lognormal(mean=9.0, sigma=1.5, size=n_legit)
    oldbalanceDest_legit = np.clip(oldbalanceDest_legit, 0.0, 2000000.0)
    newbalanceDest_legit = np.zeros(n_legit, dtype=np.float64)
    for i, t in enumerate(type_legit):
        if t in ["TRANSFER", "CASH_IN"]:
            newbalanceDest_legit[i] = oldbalanceDest_legit[i] + amount_legit[i]
        elif t == "CASH_OUT":
            # Cash out agent pays out physical cash, so wallet balance might decrease or adjust
            newbalanceDest_legit[i] = max(0.0, oldbalanceDest_legit[i] - amount_legit[i])
        else:
            newbalanceDest_legit[i] = oldbalanceDest_legit[i]

    isFraud_legit = np.zeros(n_legit, dtype=int)

    # 2. Generate Fraudulent Transactions (SIM-swap, Account Drain, Midnight Velocity, Mule Cash-outs)
    # Fraud occurs predominantly during nocturnal windows (1 AM - 5 AM)
    fraud_hours = np.random.choice([1, 2, 3, 4, 5], size=n_fraud, p=[0.25, 0.30, 0.25, 0.10, 0.10])
    fraud_days = np.random.randint(0, 30, size=n_fraud)
    step_fraud = fraud_days * 24 + fraud_hours

    # Nigerian mobile fraud almost exclusively targets TRANSFER and CASH_OUT
    type_fraud = np.random.choice(["TRANSFER", "CASH_OUT"], size=n_fraud, p=[0.60, 0.40])

    # Fraud amounts: typically high value, targeting complete account drainage
    # Range ₦100,000 to ₦3,000,000
    amount_fraud = np.random.lognormal(mean=12.2, sigma=0.8, size=n_fraud)
    amount_fraud = np.clip(amount_fraud, 50000.0, 3500000.0)

    # In SIM-swap and account takeovers:
    # 75% are total account drains: oldbalanceOrg == amount, newbalanceOrig = 0.0
    # 25% are balance tampering / ledger mismatch: old balance lower than amount or zero post-balance
    oldbalanceOrg_fraud = np.zeros(n_fraud, dtype=np.float64)
    newbalanceOrig_fraud = np.zeros(n_fraud, dtype=np.float64)

    drain_mask = np.random.rand(n_fraud) < 0.75
    # Total account drains
    oldbalanceOrg_fraud[drain_mask] = amount_fraud[drain_mask]
    newbalanceOrig_fraud[drain_mask] = 0.0

    # Ledger discrepancy / tampering cases (balance not reconciling properly)
    non_drain_indices = np.where(~drain_mask)[0]
    for idx in non_drain_indices:
        oldbalanceOrg_fraud[idx] = amount_fraud[idx] * np.random.uniform(0.5, 1.2)
        # Violates ledger balance preservation
        newbalanceOrig_fraud[idx] = 0.0 if np.random.rand() < 0.6 else max(0.0, oldbalanceOrg_fraud[idx] - amount_fraud[idx] * 0.5)

    # Destination balances for fraud:
    # Frequently zero initial balance (freshly registered synthetic mule wallets)
    oldbalanceDest_fraud = np.zeros(n_fraud, dtype=np.float64)
    has_prior_bal = np.random.rand(n_fraud) < 0.20
    oldbalanceDest_fraud[has_prior_bal] = np.random.uniform(100.0, 25000.0, size=has_prior_bal.sum())

    # In many fraud cash-outs, destination post-balance remains 0 or fails to increment (immediate POS cash withdrawal)
    newbalanceDest_fraud = np.zeros(n_fraud, dtype=np.float64)
    immediate_cashout = np.random.rand(n_fraud) < 0.70
    newbalanceDest_fraud[immediate_cashout] = 0.0
    newbalanceDest_fraud[~immediate_cashout] = oldbalanceDest_fraud[~immediate_cashout] + amount_fraud[~immediate_cashout]

    isFraud_fraud = np.ones(n_fraud, dtype=int)

    # Combine into unified dataset
    step_all = np.concatenate([step_legit, step_fraud])
    type_all = np.concatenate([type_legit, type_fraud])
    amount_all = np.concatenate([amount_legit, amount_fraud])
    old_orig_all = np.concatenate([oldbalanceOrg_legit, oldbalanceOrg_fraud])
    new_orig_all = np.concatenate([newbalanceOrig_legit, newbalanceOrig_fraud])
    old_dest_all = np.concatenate([oldbalanceDest_legit, oldbalanceDest_fraud])
    new_dest_all = np.concatenate([newbalanceDest_legit, newbalanceDest_fraud])
    is_fraud_all = np.concatenate([isFraud_legit, isFraud_fraud])

    # Account ID generation
    account_ids_orig = [f"C{np.random.randint(100000000, 999999999)}" for _ in range(n_samples)]
    account_ids_dest = [
        f"M{np.random.randint(100000000, 999999999)}" if t == "PAYMENT" else f"C{np.random.randint(100000000, 999999999)}"
        for t in type_all
    ]

    df = pd.DataFrame({
        "step": step_all.astype(int),
        "type": type_all,
        "amount": np.round(amount_all, 2),
        "nameOrig": account_ids_orig,
        "oldbalanceOrg": np.round(old_orig_all, 2),
        "newbalanceOrig": np.round(new_orig_all, 2),
        "nameDest": account_ids_dest,
        "oldbalanceDest": np.round(old_dest_all, 2),
        "newbalanceDest": np.round(new_dest_all, 2),
        "isFraud": is_fraud_all,
    })

    # Shuffle the dataset to emulate continuous arriving stream
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Dataset successfully serialized to: {output_path}")
    logger.info(f"Dataset Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    logger.info(f"Actual Fraud Count: {df['isFraud'].sum():,} ({df['isFraud'].mean()*100:.3f}%)")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic Nigerian Mobile Money Transaction Data")
    parser.add_argument("--n-samples", type=int, default=100000, help="Number of records to generate (default: 100,000)")
    parser.add_argument("--full", action="store_true", help="Generate full thesis benchmark dataset of 1,048,575 records")
    parser.add_argument("--output", type=str, default="data/nigerian_mobile_money.csv", help="Output CSV path")
    args = parser.parse_args()

    samples = 1048575 if args.full else args.n_samples
    generate_nigerian_mobile_money_data(n_samples=samples, output_path=args.output)

