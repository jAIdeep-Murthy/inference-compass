import json
import os
from dataclasses import dataclass
from typing import List


@dataclass
class ModelMetadata:
    """
    Represents metadata for an open-source model available on Featherless AI.
    """
    id: str
    name: str
    family: str
    size: str  # "small", "medium", "large"
    best_for: List[str]
    latency_tier: str  # "fast", "medium", "slow"
    cost_tier: str  # "cheap", "moderate", "expensive"
    context_length: int
    notes: str


def load_catalog(file_name: str = "model_catalog.json") -> List[ModelMetadata]:
    """
    Loads the model catalog JSON file from disk and parses it into ModelMetadata instances.
    
    Args:
        file_name (str): The filename of the JSON catalog. Defaults to 'model_catalog.json'.
        
    Returns:
        List[ModelMetadata]: A list of parsed model metadata objects.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_path = os.path.join(base_dir, file_name)
    
    if not os.path.exists(catalog_path):
        raise FileNotFoundError(f"Model catalog file not found at {catalog_path}")
        
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    models = []
    for item in data:
        models.append(ModelMetadata(**item))
        
    return models
