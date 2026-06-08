import json
from pathlib import Path
from typing import Dict, Optional
from backend.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
DISEASE_INFO_PATH = BASE_DIR / "data" / "disease_info.json"

_disease_db = None


def _load_disease_database() -> Dict:
    """Load disease information from JSON file once at startup"""
    global _disease_db
    
    if _disease_db is not None:
        return _disease_db
    
    try:
        with open(DISEASE_INFO_PATH, "r") as file:
            _disease_db = json.load(file)
        logger.info(f"Disease info database loaded: {len(_disease_db)} diseases")
        return _disease_db
    except FileNotFoundError:
        logger.error(f"Disease info file not found: {DISEASE_INFO_PATH}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing disease_info.json: {str(e)}")
        return {}


def get_disease_info(disease_name: str) -> Optional[Dict]:
    """
    Retrieve disease information by name.
    
    Args:
        disease_name: Name of the disease
        
    Returns:
        Dictionary with disease information or None if not found
    """
    db = _load_disease_database()
    
    if disease_name in db:
        return db[disease_name]
    
    logger.warning(f"Disease info not found: {disease_name}")
    return None


def get_disease_description(disease_name: str) -> str:
    """Get disease description with graceful fallback"""
    info = get_disease_info(disease_name)
    return info.get("description", "") if info else ""


def get_disease_advice(disease_name: str) -> list:
    """Get disease advice with graceful fallback"""
    info = get_disease_info(disease_name)
    return info.get("advice", []) if info else []


def get_disease_specialist(disease_name: str) -> str:
    """Get recommended specialist with graceful fallback"""
    info = get_disease_info(disease_name)
    return info.get("specialist", "General Physician") if info else "General Physician"
