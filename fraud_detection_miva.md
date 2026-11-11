Here is the master prompt and step-by-step procedure to generate and scaffold the complete fraud detection system in Google Antigravity.
Part 1: The Master Prompt for Google Antigravity
Copy and paste the prompt below into Google Antigravity:



Markdown
Create a complete, production-grade Python project titled "Mobile Money Fraud Surveillance System in Nigeria" designed for high-throughput payment switches (USSD, Mobile Apps, Agency Banking POS).

Project Requirements & Specifications:

1. Architecture & Tech Stack:
   - Backend & Data Engine: Python 3.11, NumPy, Pandas, Scikit-Learn
   - Modeling: 
     a) Supervised: XGBoost (XGBClassifier) with scale_pos_weight=761.6 (handling 0.13% class imbalance) and tree_method='hist'.
     b) Unsupervised: PyTorch Symmetric Deep Autoencoder (dimensions: 10 -> 32 -> 16 -> 8 -> 16 -> 32 -> 10) with BatchNorm1d and LeakyReLU(0.2) activations.
     c) Recurrent: PyTorch LSTM sequence tracker (2 layers, hidden_dim=32).
     d) Baseline: Scikit-Learn IsolationForest.
   - Resampling: imbalanced-learn SMOTE applied strictly within training partitions (zero data leakage into test/validation folds).
   - Explainability: SHAP (TreeSHAP) with local waterfall attribution plots.
   - Frontend UI: Streamlit 1.32+ with a clean executive layout.
   - Scoring API: FastAPI + Uvicorn exposing an asynchronous endpoint for sub-15ms real-time scoring.
   - Security & Compliance: SHA-256 salted pseudonymization on account IDs conforming to NDPR & CBN guidelines.

2. Feature Engineering Logic:
   Implement the following mathematical formulations:
   - errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
   - errorBalanceDest = oldbalanceDest + amount - newbalanceDest
   - isCompleteDrain = 1 if (newbalanceOrig == 0 and amount > 0) else 0
   - amountToBalanceRatio = amount / (oldbalanceOrg + 1e-5)
   - One-hot encoding for transaction channels: TRANSFER, CASH_OUT, PAYMENT, CASH_IN, DEBIT.

3. Deliverables & File Structure:
   Generate all functional code files:
   - data_generator.py: Generates a realistic synthetic Nigerian mobile money dataset (100,000+ records) with 0.13% fraud prevalence containing account draining, midnight velocity spikes, and CICO cash-outs.
   - train.py: End-to-end pipeline training XGBoost, Autoencoder, LSTM, and Isolation Forest with 5-Fold Stratified Cross-Validation, saving metrics, benchmark comparison tables, and serializing model artifacts to a `models/` directory.
   - app.py: Streamlit dashboard with 3 primary views:
     Tab 1: Single Transaction Real-Time Inspector (input sliders/fields, immediate colored alert banner [GREEN/AMBER/RED], risk score, and an interactive SHAP waterfall plot).
     Tab 2: Batch CSV Audit Console (drag-and-drop CSV upload, batch latency calculation, anomaly percentage breakdown, Plotly distribution chart, and downloadable flagged CSV).
     Tab 3: Empirical Model Benchmark Matrix (displaying Precision, Recall, F1, PR-AUC, AUC-ROC, and latency comparison tables).
   - api.py: FastAPI application exposing POST `/api/v1/score-transaction` returning JSON {status, risk_score, risk_tier, action, inference_latency_ms, compliance}.
   - Dockerfile: Multi-stage container build packaging the FastAPI app and Streamlit interface.
   - requirements.txt: All pinned dependencies.
   - README.md: Setup, training, and execution instructions.

Make all scripts self-contained, modular, and immediately executable without missing imports or placeholder pseudo-code.


Part 2: Step-by-Step Execution Plan
Step 1: Initialize Workspace & Environment
In your local terminal or within Antigravity’s terminal workspace, create and enter the project folder:
Bash
mkdir -p fraud_surveillance_miva
cd fraud_surveillance_miva


Set up and activate a clean Python 3.11 virtual environment:
Bash
python3.11 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate


Install the dependencies generated in requirements.txt:
Bash
pip install --upgrade pip
pip install -r requirements.txt


Step 2: Generate the Dataset & Train Models
Generate the synthetic Nigerian mobile money transaction stream:
Bash
python data_generator.py

This outputs data/nigerian_mobile_money.csv containing severe class asymmetry (0.13% fraud).
Run the cross-validation training and serialization routine:
Bash
python train.py

This will:
Execute 5-Fold Stratified Cross-Validation with train-only SMOTE.
Train the cost-weighted XGBoost model (scale_pos_weight=761.6), PyTorch Autoencoder, LSTM, and Isolation Forest.
Serialize artifacts to models/ (xgboost_model.joblib, autoencoder.pt, scaler.joblib, explainer.joblib).
Output the comparative benchmark table matching Table 5.2 in your report.
Step 3: Run the Streamlit Dashboard (For Report Screenshots)
Start the Streamlit application:
Bash
streamlit run app.py


Open your browser at http://localhost:8501.
Capture your thesis screenshots:
Figure 4.2 (Single Transaction Inspector): Select TRANSFER or CASH_OUT, enter amount = 250,000, oldbalanceOrg = 250,000, newbalanceOrig = 0. Click Score Transaction to trigger the CRITICAL BLOCK (Red Banner).
Figure 4.4 (TreeSHAP Waterfall): Capture the feature contribution plot directly beneath the risk verdict displaying high positive attribution for isCompleteDrain and errorBalanceOrig.
Figure 4.3 (Batch CSV Audit): Navigate to Tab 2, upload a test CSV, and capture the aggregate anomaly pie chart, throughput rate, and the flagged records table.
Step 4: Run & Test the REST API Gateway
In a separate terminal tab, launch the FastAPI server:
Bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload


Verify interactive docs at http://localhost:8000/docs.
Open Postman (or use curl) to send a test request:
Method: POST
URL: http://localhost:8000/api/v1/score-transaction
Headers: Content-Type: application/json
Body (raw JSON):



JSON
{
  "step": 142,
  "type": "TRANSFER",
  "amount": 350000.0,
  "oldbalanceOrg": 350000.0,
  "newbalanceOrig": 0.0,
  "oldbalanceDest": 15000.0,
  "newbalanceDest": 365000.0
}


Capture Figure 4.6: Take a screenshot of Postman showing the 200 OK response payload, the "action": "BLOCK", and the response time showing < 20ms.
Step 5: Container Build & Runtime Verification
Build the Docker container:
Bash
docker build -t mobile-money-fraud-engine:v1 .


Run the containerized service:
Bash
docker run -d -p 8501:8501 -p 8000:8000 --name fraud_switch_instance mobile-money-fraud-engine:v1


Verify running containers:
Bash
docker ps


Capture Figure 4.5: Take a screenshot of your terminal showing the active container ID, image name, port mappings (0.0.0.0:8000->8000/tcp, 0.0.0.0:8501->8501/tcp), and healthy status.
Once you have these PNG/JPEG files saved in your screenshots/ directory, insert them directly into the designated (Place Figure X.X here) placeholders in your Google Doc.
