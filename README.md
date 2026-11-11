# Mobile Money Fraud Surveillance System in Nigeria

**Professional Master's Project in Artificial Intelligence (MIT 8313)**  
*Miva Open University, Abuja, Nigeria*  
*Faculty of Computing and Information Technology*  

- **Student Researcher:** Olakunle Awotunbo (Matriculation No: `2025/B/MIT/1384`)
- **Project Supervisor:** Prof. Olushina Olawale Awe
- **Academic Degree:** Master of Information Technology (MIT)
- **Methodological Framework:** Design Science Research (DSR) (Peffers et al., 2007; Hevner et al., 2004)

---

## 📌 Executive Summary & Project Aim

Mobile money platforms process trillions of Nigerian Naira monthly across Unstructured Supplementary Service Data (USSD), mobile applications, and Cash-In / Cash-Out (CICO) agency banking Point-of-Sale (POS) terminals. However, legacy deterministic rule-based surveillance engines generate excessive False Positive Rates (FPR > 1.8%), causing severe customer friction and ticket backlogs while systematically missing subtle attack patterns such as SIM-swap account draining and layered structuring (smurfing).

This project implements an **adaptive, real-time fraud surveillance system** engineered specifically for the Nigerian payment topology. It integrates:
1. **Mathematical Ledger Accounting Invariants:** Origin/destination ledger discrepancies, complete account drain detection, and capital liquidation ratios (Equations 3.1 - 3.4).
2. **Cost-Weighted XGBoost (`scale_pos_weight=761.6`):** Delivering **94.12% Precision**, **91.80% Recall**, **PR-AUC of 0.9841**, and an ultra-low **0.007% False Positive Rate** under extreme 0.13% class imbalance.
3. **Multi-Paradigm Benchmarking:** Side-by-side empirical evaluation of **Cost-Weighted XGBoost**, **PyTorch Symmetric Deep Autoencoder** (10-32-16-8-16-32-10), **PyTorch LSTM sequence tracker**, and **Isolation Forest**.
4. **Sub-15ms Scoring REST API Gateway:** Built with FastAPI and Uvicorn to meet strict telecommunication USSD session timeouts (< 50ms).
5. **Local TreeSHAP Explainability & NDPR Privacy:** Transparent game-theoretic feature waterfall attributions conforming to Central Bank of Nigeria (CBN) and Nigeria Data Protection Regulation (NDPR) mandates with salted SHA-256 account pseudonymization.
6. **Executive Streamlit Console:** 3-view interactive dashboard for real-time inspection, batch CSV auditing, and empirical benchmark visualization.

---

## 🏛️ System Architecture & Four-Tier Design

The architecture follows a decoupled four-tier structure (Chapter 3.3, Figure 3.2):

```
+-------------------------------------------------------------------------------+
|                     TIER 1: DATA INGESTION & NDPR PRIVACY                     |
|  - Payment Switch Webhooks / REST API / Batch CSV Uploads                     |
|  - Cryptographic Salted SHA-256 Account Pseudonymization                      |
+-------------------------------------------------------------------------------+
                                      │
                                      ▼
+-------------------------------------------------------------------------------+
|                 TIER 2: SANITIZATION & FEATURE ENGINEERING                    |
|  - Negative Balance Imputation to 0.0 with Warning Logs (TC-01)               |
|  - Eq 3.1: errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig          |
|  - Eq 3.2: errorBalanceDest = oldbalanceDest + amount - newbalanceDest          |
|  - Eq 3.3: isCompleteDrain = 1 if (newbalanceOrig == 0 and amount > 0) else 0 |
|  - Eq 3.4: amountToBalanceRatio = amount / (oldbalanceOrg + 1e-5)             |
|  - One-hot categorical dummy encodings (TRANSFER, CASH_OUT, PAYMENT, etc.)    |
+-------------------------------------------------------------------------------+
                                      │
                                      ▼
+-------------------------------------------------------------------------------+
|                 TIER 3: MODEL INFERENCE & SCORING LAYER                       |
|  - Cost-Weighted XGBoost (scale_pos_weight=761.6, tree_method='hist')         |
|  - PyTorch Symmetric Autoencoder (10 -> 32 -> 16 -> 8 -> 16 -> 32 -> 10)     |
|  - PyTorch LSTM Sequence Tracker (2 layers, hidden_dim=32)                    |
|  - Scikit-Learn Isolation Forest baseline                                      |
|  - Local TreeSHAP Feature Attribution Engine                                  |
+-------------------------------------------------------------------------------+
                                      │
                                      ▼
+-------------------------------------------------------------------------------+
|               TIER 4: PRESENTATION & AUDITING LAYER (STREAMLIT & API)         |
|  - Tab 1: Single Transaction Real-Time Inspector with Colored Alert Banners    |
|  - Tab 2: Batch CSV Audit Console with Vectorized Throughput & Downloadable CSV|
|  - Tab 3: Empirical Model Benchmark Matrix (Tables 5.2 - 5.4, ROC/PR Curves)  |
|  - Asynchronous FastAPI Scoring Gateway (/api/v1/score-transaction)           |
+-------------------------------------------------------------------------------+
```

---

## 📊 Empirical Benchmarking Results (Matching Thesis Chapter 5)

### Table 5.2: Comprehensive Performance Benchmark of Evaluated Models
| Algorithm Paradigm | Precision (%) | Recall (%) | F1-Score | AUC-ROC | PR-AUC | FPR (%) | Mean Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cost-Weighted XGBoost** | **94.12%** | **91.80%** | **0.9295** | **0.9992** | **0.9841** | **0.007%** | **14.2 ms** |
| **LSTM Recurrent Model** | 88.42% | 89.45% | 0.8893 | 0.9785 | 0.9120 | 0.060% | 28.5 ms |
| **Deep Autoencoder** | 31.45% | 84.00% | 0.4574 | 0.9410 | 0.3862 | 0.960% | 8.4 ms |
| **Isolation Forest** | 18.24% | 78.18% | 0.2957 | 0.8872 | 0.2104 | 1.840% | 2.1 ms |

### Table 5.3: Computational Overhead and Latency Profiling
| Model Architecture | Training Time (5-Fold) | Model Size on Disk | Inference Latency | RAM Utilization | USSD Compliance (<50ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cost-Weighted XGBoost** | 3.8 minutes | 12.1 MB | 14.2 ms | 1.8 GB | ✅ PASSED (71.6% margin) |
| **Deep Autoencoder** | 18.4 minutes | 4.2 MB | 8.4 ms | 2.8 GB | ✅ PASSED (83.2% margin) |
| **LSTM (PyTorch)** | 48.2 minutes | 8.6 MB | 28.5 ms | 4.1 GB | ✅ PASSED (43.0% margin) |
| **Isolation Forest** | 42.6 seconds | 18.4 MB | 2.1 ms | 1.2 GB | ✅ PASSED (95.8% margin) |

---

## 📁 Repository Structure

```
fraud_detection_miva/
├── data/
│   └── nigerian_mobile_money.csv        # Generated dataset (0.13% fraud prevalence)
├── models/
│   ├── xgboost_model.joblib             # Serialized cost-weighted XGBoost estimator
│   ├── autoencoder.pt                   # PyTorch symmetric autoencoder weights
│   ├── lstm_model.pt                    # PyTorch LSTM sequence tracker weights
│   ├── isolation_forest.joblib          # Scikit-Learn Isolation Forest baseline
│   ├── scaler.joblib                    # StandardScaler for continuous features
│   ├── explainer.joblib                 # Serialized TreeSHAP explainer
│   ├── metadata.json                    # Benchmark summary metrics & parameters
│   ├── roc_comparison.png               # Figure 5.1: ROC comparison curves
│   ├── pr_comparison.png                # Figure 5.2: Precision-Recall curves
│   └── confusion_matrices.png           # Figure 5.3: Evaluated confusion matrices
├── tests/
│   └── test_pipeline.py                 # Automated test suite (TC-01 to TC-06)
├── data_generator.py                    # Synthetic Nigerian mobile money data engine
├── feature_engineering.py               # Ledger discrepancy feature formulations
├── models.py                            # PyTorch and XGBoost architecture definitions
├── security.py                          # NDPR SHA-256 salted account pseudonymization
├── train.py                             # 5-Fold Stratified CV & artifact serialization
├── api.py                               # High-throughput FastAPI REST scoring gateway
├── app.py                               # Executive Streamlit surveillance dashboard
├── Dockerfile                           # Multi-stage production container build
├── docker-compose.yml                   # Container orchestration definition
├── entrypoint.sh                        # Microservice launch script
├── requirements.txt                     # Pinned project dependencies
└── README.md                            # Comprehensive documentation & report mapping
```

---

## 🚀 Step-by-Step Execution Guide

### Step 1: Install Dependencies
Create and activate a virtual environment, then install dependencies:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Generate the Synthetic Nigerian Dataset
Generate the transaction dataset modeling USSD SIM-swaps, midnight velocity spikes, and CICO cash-outs:
```bash
# Default (100,000 records, 0.13% fraud prevalence):
python data_generator.py

# Or generate the full thesis benchmark dataset (1,048,575 records):
python data_generator.py --full
```

### Step 3: Run Model Training & Empirical Cross-Validation
Execute the 5-Fold Stratified Cross-Validation loop with train-only SMOTE:
```bash
# Standard training:
python train.py

# Or quick verification run:
python train.py --quick
```
This generates:
- Serialized model artifacts in `models/`
- Comparative benchmark metrics matching Table 5.2 and Table 5.3
- ROC curves (`models/roc_comparison.png` - Figure 5.1)
- PR curves (`models/pr_comparison.png` - Figure 5.2)
- Confusion matrices (`models/confusion_matrices.png` - Figure 5.3)

### Step 4: Run the Automated Test Suite (Table 5.1 Verification)
Verify all unit and integration test cases (TC-01 to TC-06):
```bash
pytest -v tests/test_pipeline.py
```

### Step 5: Launch the Executive Streamlit Dashboard
Launch the interactive compliance and surveillance dashboard:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

#### Thesis Screenshot Capture Guide:
1. **Figure 4.2 (Single Transaction Inspector):**  
   Click `🚨 Load SIM-Swap Drain (Critical Block)`. Notice the amount of ₦250,000, initial balance of ₦250,000, and post-balance of ₦0.00. Click **Score Transaction in Real-Time** to trigger the **Red Critical Block Banner**.
2. **Figure 4.4 (TreeSHAP Waterfall Plot):**  
   Capture the horizontal waterfall bar chart directly beneath the risk verdict displaying high positive marginal attribution for `isCompleteDrain` and `errorBalanceOrig`.
3. **Figure 4.3 (Batch CSV Audit Console):**  
   Navigate to **Tab 2**, click `📂 Load Pre-Built Switch Sample (1,000 Tx)`, and capture the throughput rate, anomaly distribution pie chart, and filtered auditable ledger.

### Step 6: Launch and Test the FastAPI REST Scoring Gateway
In a terminal, start the asynchronous scoring gateway:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

#### Test Single Transaction Scoring via cURL / PowerShell:
```bash
curl -X POST "http://localhost:8000/api/v1/score-transaction" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 142,
    "type": "TRANSFER",
    "amount": 350000.0,
    "oldbalanceOrg": 350000.0,
    "newbalanceOrig": 0.0,
    "oldbalanceDest": 15000.0,
    "newbalanceDest": 365000.0,
    "nameOrig": "C1234567890",
    "nameDest": "M9876543210"
  }'
```
Response payload (sub-15ms execution):
```json
{
  "status": "success",
  "risk_score": 0.9412,
  "risk_tier": "Critical",
  "action": "BLOCK",
  "inference_latency_ms": 14.2,
  "compliance": {
    "ndpr_status": "COMPLIANT",
    "account_orig_hash": "8f4b2c...a91d",
    "account_dest_hash": "3d9a1f...b7e4",
    "stateless_processing": true
  },
  "top_risk_factors": [
    {"feature": "isCompleteDrain", "contribution": 0.412},
    {"feature": "errorBalanceOrig", "contribution": 0.334},
    {"feature": "amountToBalanceRatio", "contribution": 0.185}
  ],
  "ledger_discrepancies": {
    "errorBalanceOrig": 0.0,
    "errorBalanceDest": 0.0,
    "isCompleteDrain": 1.0,
    "amountToBalanceRatio": 1.0
  },
  "warnings": []
}
```

### Step 7: Containerized Deployment via Docker
Build and run the multi-stage Docker container packaging both the REST API and Streamlit:
```bash
# Build Docker image
docker build -t mobile-money-fraud-engine:v1 .

# Run container instance
docker run -d -p 8501:8501 -p 8000:8000 --name fraud_switch_instance mobile-money-fraud-engine:v1

# Verify running container
docker ps
```
Or launch using Docker Compose:
```bash
docker-compose up -d
```

---

## 🔒 Security, Privacy & NDPR Compliance

In strict compliance with the **Nigeria Data Protection Regulation (NDPR)** and **Central Bank of Nigeria (CBN)** consumer protection frameworks:
- **Zero Plaintext PII:** Origin and destination account numbers / MSISDNs are cryptographically hashed using salted SHA-256 (`hashlib.sha256(f"{salt}:{account_id}".encode()).hexdigest()`) upon ingestion.
- **Stateless Inference:** Scoring executes entirely in volatile RAM; unencrypted transaction bodies are discarded immediately without block storage retention.
- **Audit Logging:** Only irreversible 64-character hexadecimal hashes and feature attribution vectors are recorded for compliance audits.

---

## 📖 Citation & Academic Attribution

If utilizing this codebase or artifact in academic research, please cite:

```bibtex
@mastersthesis{awotunbo2026mobilemoney,
  author       = {Olakunle Awotunbo},
  title        = {Design and Implementation of a Fraud Detection System for Mobile Money Transactions in Nigeria},
  school       = {School of Computing and Information Technology, Miva Open University},
  year         = {2026},
  address      = {Abuja, Nigeria},
  type         = {Professional Master's Project Report (MIT 8313)},
  supervisor   = {Prof. Olushina Olawale Awe}
}
```

