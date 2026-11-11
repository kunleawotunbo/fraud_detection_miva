#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting Mobile Money Fraud Surveillance Microservices"
echo " Miva Open University - MIT 8313 Master's Project"
echo "=========================================================="

# Check if model artifacts exist; if not, generate sample data and run lightweight training
if [ ! -f "models/xgboost_model.joblib" ]; then
    echo "Model artifacts not detected. Initializing data generator and training pipeline..."
    python data_generator.py --n-samples 25000
    python train.py --quick
fi

# Start FastAPI server on port 8000 in background
echo "Launching FastAPI REST Gateway on port 8000..."
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Start Streamlit application on port 8501
echo "Launching Streamlit Dashboard Console on port 8501..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

