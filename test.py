"""Unit tests."""

import os

import yaml

THIS_DIR = os.path.dirname(__file__)


def test_data():
    """Test data structure"""
    with open(os.path.join(THIS_DIR, "data", "data.yml"), encoding="utf-8") as file:
        data = yaml.load(file, yaml.CLoader)

    for values in data.values():

        if values["tips"] is not None:
            assert os.path.exists(values["image"])
            assert isinstance(values["location"], str)
            assert len(values["tips"]) == 5
