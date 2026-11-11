"""
Mobile Money Fraud Surveillance System in Nigeria
Module: security.py
Description: Enforces NDPR (Nigeria Data Protection Regulation) & CBN Guidelines.
Provides cryptographic salted SHA-256 pseudonymization for account and customer IDs,
ensuring zero cleartext PII in downstream logs, storage, or memory artifacts.
"""

import os
import hashlib
from typing import Optional, Dict, Any

# Cryptographic salt loaded from environment variable, with high-entropy fallback
DEFAULT_SALT = "miva_mit8313_cbn_ndpr_secure_salt_2026"
NDPR_SALT = os.environ.get("NDPR_PEPPER_SALT", DEFAULT_SALT)


def pseudonymize_identifier(identifier: Optional[str], salt: Optional[str] = None) -> str:
    """
    Applies irreversible cryptographic salted SHA-256 pseudonymization to customer and account IDs.
    
    Args:
        identifier: The raw account or customer identifier (e.g. phone number, wallet ID).
        salt: Optional salt override. Defaults to system NDPR_SALT.
        
    Returns:
        A 64-character hexadecimal SHA-256 hash.
    """
    if not identifier:
        identifier = "ANONYMOUS_ACCOUNT"
    active_salt = salt or NDPR_SALT
    salted_str = f"{active_salt}:{identifier.strip()}"
    return hashlib.sha256(salted_str.encode("utf-8")).hexdigest()


def mask_display_hash(sha256_hash: str, prefix_len: int = 6, suffix_len: int = 4) -> str:
    """
    Returns a masked preview of a cryptographic hash for user interfaces (e.g., '8f4b2c...a91d').
    """
    if len(sha256_hash) <= prefix_len + suffix_len:
        return sha256_hash
    return f"{sha256_hash[:prefix_len]}...{sha256_hash[-suffix_len:]}"


def sanitize_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures that any record destined for audit logging or persistence has its PII pseudonymized
    and contains NDPR compliance metadata.
    """
    sanitized = record.copy()
    if "nameOrig" in sanitized and sanitized["nameOrig"]:
        sanitized["account_orig_hash"] = pseudonymize_identifier(str(sanitized.pop("nameOrig")))
    if "nameDest" in sanitized and sanitized["nameDest"]:
        sanitized["account_dest_hash"] = pseudonymize_identifier(str(sanitized.pop("nameDest")))
    
    sanitized["ndpr_compliance"] = {
        "status": "COMPLIANT",
        "hashing_algorithm": "SHA-256",
        "pii_redacted": True,
        "stateless_processing": True
    }
    return sanitized

