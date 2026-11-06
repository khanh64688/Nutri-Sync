"""Unit tests for validating the Vietnamese Food Composition Table (FCT)

reference dataset: backend/app/data/nutrition_ref.json.
Part of NutriSync Phase 0 / Sprint 1 (TASK-0.3).
"""

import json
import re
from pathlib import Path
import pytest

DATA_FILE_PATH = Path(__file__).resolve().parent.parent / "app" / "data" / "nutrition_ref.json"

VALID_DISH_TYPES = {"dry_dish", "soup_dish", "snack"}
EXPECTED_COUNTS = {
    "dry_dish": 15,
    "soup_dish": 12,
    "snack": 3,
}
EXPECTED_PORTION_COEFFICIENTS = {
    "small": 0.8,
    "standard": 1.0,
    "large": 1.3,
}
EXPECTED_TOLERANCE = {
    "dry_dish": 12.0,
    "soup_dish": 20.0,
    "snack": 12.0,
}


@pytest.fixture(scope="module")
def nutrition_data() -> dict:
    """Fixture to load and parse nutrition_ref.json once for all tests."""
    assert DATA_FILE_PATH.exists(), f"Nutrition reference file not found at: {DATA_FILE_PATH}"
    with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@pytest.fixture(scope="module")
def dishes(nutrition_data: dict) -> list[dict]:
    """Fixture extracting dishes list."""
    assert "dishes" in nutrition_data, "Root JSON must contain 'dishes' list."
    return nutrition_data["dishes"]


class TestNutritionDataStructure:
    """Test suite for top-level JSON structure and metadata."""

    def test_file_exists(self):
        """Verify the nutrition_ref.json file is located at the expected path."""
        assert DATA_FILE_PATH.is_file(), f"File does not exist at {DATA_FILE_PATH}"

    def test_root_metadata(self, nutrition_data: dict):
        """Verify root metadata fields."""
        assert "version" in nutrition_data, "Missing 'version' field."
        assert "metadata" in nutrition_data, "Missing 'metadata' field."
        metadata = nutrition_data["metadata"]
        assert metadata.get("total_dishes") == 30, "Metadata total_dishes must be 30."
        assert "categories" in metadata
        assert metadata["categories"]["dry_dish"] == 15
        assert metadata["categories"]["soup_dish"] == 12
        assert metadata["categories"]["snack"] == 3


class TestDishesIntegrity:
    """Test suite for individual dishes data integrity."""

    def test_total_dishes_count(self, dishes: list[dict]):
        """Ensure exactly 30 dishes are provided."""
        assert len(dishes) == 30, f"Expected exactly 30 dishes, but found {len(dishes)}."

    def test_dish_category_distribution(self, dishes: list[dict]):
        """Ensure correct distribution: 15 dry, 12 soup, 3 snack."""
        counts = {}
        for d in dishes:
            dtype = d.get("dish_type")
            counts[dtype] = counts.get(dtype, 0) + 1

        assert counts == EXPECTED_COUNTS, (
            f"Category counts mismatch! Expected: {EXPECTED_COUNTS}, Got: {counts}"
        )

    def test_unique_snake_case_dish_ids(self, dishes: list[dict]):
        """Verify each dish_id is unique and follows snake_case naming format."""
        seen_ids = set()
        snake_case_pattern = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")

        for d in dishes:
            dish_id = d.get("dish_id")
            assert dish_id, f"Dish missing 'dish_id': {d}"
            assert dish_id not in seen_ids, f"Duplicate dish_id found: '{dish_id}'"
            assert snake_case_pattern.match(dish_id), (
                f"dish_id '{dish_id}' is not valid snake_case"
            )
            seen_ids.add(dish_id)

    def test_required_dish_fields(self, dishes: list[dict]):
        """Verify all mandatory fields are present in each dish."""
        required_fields = [
            "dish_id",
            "dish_name",
            "dish_type",
            "description",
            "tolerance_percentage",
            "base_portion",
            "portion_coefficients",
            "toppings",
            "standard_components",
        ]

        for d in dishes:
            dish_id = d.get("dish_id", "UNKNOWN")
            for field in required_fields:
                assert field in d, f"Dish '{dish_id}' is missing required field: '{field}'"
            assert isinstance(d["dish_name"], str) and len(d["dish_name"].strip()) > 0
            assert isinstance(d["description"], str) and len(d["description"].strip()) > 0
            assert d["dish_type"] in VALID_DISH_TYPES


class TestNutritionalValues:
    """Test suite for macronutrients, calories, and mathematical sanity."""

    def test_base_portion_and_macronutrients(self, dishes: list[dict]):
        """Validate base portion weight, calories, and macronutrient sanity."""
        for d in dishes:
            dish_id = d["dish_id"]
            base = d["base_portion"]

            # Weight and calories checks
            assert base.get("weight_gram", 0) > 0, f"Weight must be > 0 in '{dish_id}'"
            calories = base.get("calories", 0)
            assert calories > 0, f"Calories must be > 0 in '{dish_id}'"

            # Macros checks
            macros = base.get("macronutrients", {})
            for macro in ["protein_g", "carbs_g", "fat_g", "fiber_g"]:
                assert macro in macros, f"Missing macro '{macro}' in '{dish_id}'"
                assert macros[macro] >= 0, f"Macro '{macro}' cannot be negative in '{dish_id}'"

            # Calorie sanity check: 4 * P + 4 * C + 9 * F ~ Calories (within 20% margin)
            calc_calories = (
                macros["protein_g"] * 4.0
                + macros["carbs_g"] * 4.0
                + macros["fat_g"] * 9.0
            )
            relative_diff = abs(calc_calories - calories) / calories
            assert relative_diff < 0.20, (
                f"Calorie sanity check failed for '{dish_id}': declared={calories}, "
                f"calculated from macros={calc_calories:.1f} (diff={relative_diff:.1%})"
            )

    def test_portion_coefficients(self, dishes: list[dict]):
        """Verify portion coefficients match standard specifications."""
        for d in dishes:
            dish_id = d["dish_id"]
            coeffs = d.get("portion_coefficients", {})
            assert coeffs == EXPECTED_PORTION_COEFFICIENTS, (
                f"Invalid portion_coefficients in '{dish_id}': {coeffs}"
            )

    def test_tolerance_rules(self, dishes: list[dict]):
        """Verify tolerance percentage is 12% for dry/snack and 20% for soup."""
        for d in dishes:
            dish_id = d["dish_id"]
            dish_type = d["dish_type"]
            expected_tol = EXPECTED_TOLERANCE[dish_type]
            assert d["tolerance_percentage"] == expected_tol, (
                f"Tolerance for '{dish_id}' ({dish_type}) should be {expected_tol}%, "
                f"got {d['tolerance_percentage']}%"
            )


class TestToppingsAndComponents:
    """Test suite for toppings, modifiers, and standard components."""

    def test_toppings_structure_and_sanity(self, dishes: list[dict]):
        """Verify each dish has valid toppings with positive calories."""
        snake_case_pattern = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")

        for d in dishes:
            dish_id = d["dish_id"]
            toppings = d.get("toppings", [])
            assert len(toppings) >= 2, f"Dish '{dish_id}' should have at least 2 toppings."

            topping_ids = set()
            for t in toppings:
                tid = t.get("topping_id")
                assert tid, f"Topping missing 'topping_id' in '{dish_id}'"
                assert tid not in topping_ids, f"Duplicate topping_id '{tid}' in '{dish_id}'"
                assert snake_case_pattern.match(tid), f"topping_id '{tid}' is not snake_case"
                topping_ids.add(tid)

                assert t.get("name"), f"Topping missing name in '{dish_id}'"
                assert t.get("additional_calories", 0) > 0, (
                    f"Topping '{tid}' in '{dish_id}' has non-positive calories"
                )

                macros = t.get("additional_macronutrients", {})
                for m in ["protein_g", "carbs_g", "fat_g"]:
                    assert m in macros, f"Topping '{tid}' missing macro '{m}'"
                    assert macros[m] >= 0, f"Topping '{tid}' macro '{m}' cannot be negative"

    def test_standard_components(self, dishes: list[dict]):
        """Verify each dish has a non-empty list of standard components for VLM."""
        for d in dishes:
            dish_id = d["dish_id"]
            components = d.get("standard_components", [])
            assert len(components) >= 3, (
                f"Dish '{dish_id}' must have at least 3 standard components, got {len(components)}"
            )
            for c in components:
                assert isinstance(c, str) and len(c.strip()) > 0, (
                    f"Empty component string found in '{dish_id}'"
                )

