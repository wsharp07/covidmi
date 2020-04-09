from covidmi.app.data_parser import DataParser
import pytest


@pytest.mark.parametrize("test_input,expected", [
                        ("Other*", False),
                        ("Out of State", False),
                        ("Unknown", False),
                        ("Total", False),
                        ("County", False)])
def test_isvalid_invalid_input_expect_false(test_input, expected):
    parser = DataParser()
    assert parser.is_valid(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
                        ("Oakland", True),
                        ("St Clair", True)])
def test_isvalid_valid_input_expect_true(test_input, expected):
    parser = DataParser()
    assert parser.is_valid(test_input) == expected
