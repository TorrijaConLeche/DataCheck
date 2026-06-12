import os

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STORAGE_DIR = os.path.join(BACKEND_DIR, "storage")
DATASETS_DIR = os.path.join(STORAGE_DIR, "datasets")
RESULTS_DIR = os.path.join(STORAGE_DIR, "results")


def dataset_path(dataset_id: str) -> str:
    return os.path.join(DATASETS_DIR, f"{dataset_id}.csv")


def rules_path(dataset_id: str) -> str:
    return os.path.join(DATASETS_DIR, f"{dataset_id}-rules.json")
