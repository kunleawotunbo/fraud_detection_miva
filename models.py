"""
Mobile Money Fraud Surveillance System in Nigeria
Module: models.py
Description: Defines the 4 machine learning and deep learning architectures evaluated:
1. Supervised Cost-Weighted XGBoost (scale_pos_weight=761.6, tree_method='hist')
2. Unsupervised PyTorch Symmetric Deep Autoencoder (10 -> 32 -> 16 -> 8 -> 16 -> 32 -> 10)
3. PyTorch Long Short-Term Memory (LSTM) Recurrent Sequence Tracker (2 layers, hidden_dim=32)
4. Unsupervised Baseline Scikit-Learn Isolation Forest
"""

import os
from typing import Tuple, Optional
import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

from sklearn.ensemble import IsolationForest


# ==========================================
# 1. PyTorch Symmetric Deep Autoencoder
# ==========================================
if TORCH_AVAILABLE:
    class DeepAutoencoder(nn.Module):
        """
        PyTorch Symmetric Deep Autoencoder for out-of-distribution anomaly detection.
        Architecture: 10 -> 32 -> 16 -> 8 -> 16 -> 32 -> 10
        Features BatchNorm1d and LeakyReLU(0.2) activations.
        """
        def __init__(self, input_dim: int = 10, latent_dim: int = 8):
            super().__init__()
            # Encoder
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, 32),
                nn.BatchNorm1d(32),
                nn.LeakyReLU(0.2),
                nn.Linear(32, 16),
                nn.BatchNorm1d(16),
                nn.LeakyReLU(0.2),
                nn.Linear(16, latent_dim),
            )
            # Decoder
            self.decoder = nn.Sequential(
                nn.Linear(latent_dim, 16),
                nn.BatchNorm1d(16),
                nn.LeakyReLU(0.2),
                nn.Linear(16, 32),
                nn.BatchNorm1d(32),
                nn.LeakyReLU(0.2),
                nn.Linear(32, input_dim),  # Purely linear output reconstruction
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            latent = self.encoder(x)
            reconstruction = self.decoder(latent)
            return reconstruction

        def compute_reconstruction_error(self, x: torch.Tensor) -> torch.Tensor:
            """Calculates per-sample Mean Squared Error (MSE) reconstruction loss."""
            self.eval()
            with torch.no_grad():
                recon = self.forward(x)
                mse = torch.mean((x - recon) ** 2, dim=1)
            return mse
else:
    class DeepAutoencoder:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for DeepAutoencoder. Install via pip install torch.")


# ==========================================
# 2. PyTorch LSTM Recurrent Sequence Tracker
# ==========================================
if TORCH_AVAILABLE:
    class LSTMSequenceTracker(nn.Module):
        """
        PyTorch LSTM sequence network (2 layers, hidden_dim=32)
        to capture temporal state transitions across transaction windows.
        """
        def __init__(self, input_dim: int = 10, hidden_dim: int = 32, num_layers: int = 2):
            super().__init__()
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            self.lstm = nn.LSTM(
                input_size=input_dim,
                hidden_size=hidden_dim,
                num_layers=num_layers,
                batch_first=True,
                dropout=0.2 if num_layers > 1 else 0.0,
            )
            self.classifier = nn.Sequential(
                nn.Linear(hidden_dim, 16),
                nn.LeakyReLU(0.2),
                nn.Linear(16, 1),
                nn.Sigmoid(),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # x shape: (batch_size, seq_len, input_dim) or (batch_size, input_dim)
            if x.dim() == 2:
                x = x.unsqueeze(1)  # seq_len = 1
            out, (hn, _) = self.lstm(x)
            # Use final time-step hidden state
            final_h = out[:, -1, :]
            prob = self.classifier(final_h)
            return prob.squeeze(-1)
else:
    class LSTMSequenceTracker:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for LSTMSequenceTracker. Install via pip install torch.")


# ==========================================
# 3. Supervised Cost-Weighted XGBoost Builder
# ==========================================
def build_xgboost_classifier(
    scale_pos_weight: float = 761.6,
    n_estimators: int = 100,
    max_depth: int = 6,
    learning_rate: float = 0.1,
    random_state: int = 42,
):
    """
    Constructs an XGBClassifier configured with cost-sensitive weighting
    and tree_method='hist' to handle extreme 0.13% class asymmetry.
    """
    if not XGB_AVAILABLE:
        raise ImportError("xgboost is not installed. Run `pip install xgboost`.")

    return XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        scale_pos_weight=scale_pos_weight,
        tree_method="hist",
        objective="binary:logistic",
        eval_metric="aucpr",
        random_state=random_state,
        n_jobs=-1,
    )


# ==========================================
# 4. Unsupervised Baseline: Isolation Forest
# ==========================================
def build_isolation_forest(
    n_estimators: int = 100,
    contamination: float = 0.0013,
    random_state: int = 42,
) -> IsolationForest:
    """
    Constructs an IsolationForest baseline parameterized to expected 0.13% contamination.
    """
    return IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )

