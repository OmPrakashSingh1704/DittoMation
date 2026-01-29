"""Tests for the validators module."""

import pytest

from core.validators import (
    validate_chunk_size,
    validate_coordinates,
    validate_phone_number,
    validate_swipe_coordinates,
    validate_text_input,
)


class TestValidateCoordinates:
    """Tests for validate_coordinates function."""

    def test_positive_coordinates(self):
        """Test that positive coordinates are returned unchanged."""
        x, y = validate_coordinates(100, 200)
        assert x == 100
        assert y == 200

    def test_negative_x_coordinate(self):
        """Test that negative X is clamped to 0."""
        x, y = validate_coordinates(-10, 200)
        assert x == 0
        assert y == 200

    def test_negative_y_coordinate(self):
        """Test that negative Y is clamped to 0."""
        x, y = validate_coordinates(100, -20)
        assert x == 100
        assert y == 0

    def test_both_negative_coordinates(self):
        """Test that both negative coordinates are clamped to 0."""
        x, y = validate_coordinates(-10, -20)
        assert x == 0
        assert y == 0

    def test_zero_coordinates(self):
        """Test that zero coordinates are valid."""
        x, y = validate_coordinates(0, 0)
        assert x == 0
        assert y == 0


class TestValidateSwipeCoordinates:
    """Tests for validate_swipe_coordinates function."""

    def test_all_positive_coordinates(self):
        """Test that all positive coordinates are returned unchanged."""
        x1, y1, x2, y2 = validate_swipe_coordinates(10, 20, 30, 40)
        assert x1 == 10
        assert y1 == 20
        assert x2 == 30
        assert y2 == 40

    def test_negative_start_coordinates(self):
        """Test that negative start coordinates are clamped."""
        x1, y1, x2, y2 = validate_swipe_coordinates(-10, -20, 30, 40)
        assert x1 == 0
        assert y1 == 0
        assert x2 == 30
        assert y2 == 40

    def test_negative_end_coordinates(self):
        """Test that negative end coordinates are clamped."""
        x1, y1, x2, y2 = validate_swipe_coordinates(10, 20, -30, -40)
        assert x1 == 10
        assert y1 == 20
        assert x2 == 0
        assert y2 == 0

    def test_all_negative_coordinates(self):
        """Test that all negative coordinates are clamped to 0."""
        x1, y1, x2, y2 = validate_swipe_coordinates(-10, -20, -30, -40)
        assert x1 == 0
        assert y1 == 0
        assert x2 == 0
        assert y2 == 0


class TestValidatePhoneNumber:
    """Tests for validate_phone_number function."""

    def test_valid_phone_number(self):
        """Test a valid phone number."""
        is_valid, cleaned, error = validate_phone_number("1234567890")
        assert is_valid is True
        assert cleaned == "1234567890"
        assert error == ""

    def test_valid_international_number(self):
        """Test a valid international number with +."""
        is_valid, cleaned, error = validate_phone_number("+11234567890")
        assert is_valid is True
        assert cleaned == "+11234567890"
        assert error == ""

    def test_phone_number_with_formatting(self):
        """Test that formatting characters are removed."""
        is_valid, cleaned, error = validate_phone_number("(123) 456-7890")
        assert is_valid is True
        assert cleaned == "1234567890"
        assert error == ""

    def test_too_short_number(self):
        """Test that short numbers are rejected."""
        is_valid, cleaned, error = validate_phone_number("12")
        assert is_valid is False
        assert "Invalid phone number" in error

    def test_too_long_number(self):
        """Test that very long numbers are rejected."""
        is_valid, cleaned, error = validate_phone_number("1" * 25)
        assert is_valid is False
        assert "too long" in error

    def test_empty_number(self):
        """Test that empty numbers are rejected."""
        is_valid, cleaned, error = validate_phone_number("")
        assert is_valid is False

    def test_minimum_valid_length(self):
        """Test minimum valid length (3 digits)."""
        is_valid, cleaned, error = validate_phone_number("123")
        assert is_valid is True
        assert cleaned == "123"
        assert error == ""


class TestValidateTextInput:
    """Tests for validate_text_input function."""

    def test_normal_text(self):
        """Test that normal text is returned unchanged."""
        text = validate_text_input("Hello World")
        assert text == "Hello World"

    def test_empty_text(self):
        """Test that empty text is valid."""
        text = validate_text_input("")
        assert text == ""

    def test_text_at_max_length(self):
        """Test that text at max length is not truncated."""
        text = "A" * 5000
        result = validate_text_input(text)
        assert len(result) == 5000
        assert result == text

    def test_text_over_max_length(self):
        """Test that text over max length is truncated."""
        text = "A" * 6000
        result = validate_text_input(text)
        assert len(result) == 5000

    def test_custom_max_length(self):
        """Test custom max length parameter."""
        text = "A" * 100
        result = validate_text_input(text, max_length=50)
        assert len(result) == 50


class TestValidateChunkSize:
    """Tests for validate_chunk_size function."""

    def test_normal_chunk_size(self):
        """Test that normal chunk size is returned unchanged."""
        size = validate_chunk_size(10)
        assert size == 10

    def test_too_small_chunk_size(self):
        """Test that too small chunk size is clamped to minimum."""
        size = validate_chunk_size(0)
        assert size == 1

    def test_negative_chunk_size(self):
        """Test that negative chunk size is clamped to minimum."""
        size = validate_chunk_size(-5)
        assert size == 1

    def test_too_large_chunk_size(self):
        """Test that too large chunk size is clamped to maximum."""
        size = validate_chunk_size(100)
        assert size == 50

    def test_minimum_allowed_size(self):
        """Test minimum allowed size."""
        size = validate_chunk_size(1)
        assert size == 1

    def test_maximum_allowed_size(self):
        """Test maximum allowed size."""
        size = validate_chunk_size(50)
        assert size == 50

    def test_custom_bounds(self):
        """Test custom min and max bounds."""
        size = validate_chunk_size(15, min_size=5, max_size=20)
        assert size == 15

        size = validate_chunk_size(2, min_size=5, max_size=20)
        assert size == 5

        size = validate_chunk_size(25, min_size=5, max_size=20)
        assert size == 20
