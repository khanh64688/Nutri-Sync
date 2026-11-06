"""Unit tests for validating the Ground Truth benchmark dataset.

Part of NutriSync Phase 0 / Sprint 1 (TASK-0.2).
"""

import json
from pathlib import Path
import pytest

DATASET_DIR = Path(__file__).resolve().parent.parent.parent / "evaluation" / "dataset"
IMAGES_DIR = DATASET_DIR / "images"
GROUND_TRUTH_FILE = DATASET_DIR / "ground_truth.json"


@pytest.fixture(scope="module")
def ground_truth_data():
    """Load ground_truth.json."""
    assert GROUND_TRUTH_FILE.exists(), f"ground_truth.json not found at {GROUND_TRUTH_FILE}"
    with open(GROUND_TRUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


class TestGroundTruthDataset:
    """Validate Ground Truth benchmark dataset."""

    def test_metadata_and_counts(self, ground_truth_data: dict):
        """Ensure 60 total samples across 30 dishes."""
        assert ground_truth_data.get("total_samples") == 60
        assert ground_truth_data.get("total_dishes") == 30
        samples = ground_truth_data.get("samples", [])
        assert len(samples) == 60, f"Expected 60 samples, got {len(samples)}"

    def test_samples_integrity(self, ground_truth_data: dict):
        """Verify each sample record has all required fields and valid data."""
        samples = ground_truth_data.get("samples", [])
        seen_images = set()

        for s in samples:
            image_name = s.get("image_name")
            assert image_name, "Sample missing image_name"
            assert image_name not in seen_images, f"Duplicate image_name: {image_name}"
            seen_images.add(image_name)

            # Check image file exists on disk and is non-empty
            img_file = IMAGES_DIR / image_name
            assert img_file.exists(), f"Image file missing on disk: {img_file}"
            assert img_file.stat().st_size > 0, f"Empty image file: {img_file}"

            # Check dish info
            assert s.get("true_dish_id"), f"Missing true_dish_id in {image_name}"
            assert s.get("true_dish_name"), f"Missing true_dish_name in {image_name}"
            assert s.get("view_angle") in ["45_degree", "90_degree"]
            assert s.get("true_portion") in ["small", "standard", "large"]

            # Check calories and macros
            assert s.get("true_calories", 0) > 0, f"Invalid calories in {image_name}"
            macros = s.get("true_macronutrients", {})
            for m in ["protein_g", "carbs_g", "fat_g"]:
                assert m in macros, f"Missing macro '{m}' in {image_name}"
                assert macros[m] >= 0, f"Macro '{m}' cannot be negative in {image_name}"

