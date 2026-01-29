"""
Validators - Common validation utilities for coordinates, text, phone numbers, etc.

Centralizes validation logic to avoid duplication across modules.
"""

from typing import Tuple

from core.logging_config import get_logger

logger = get_logger("validators")


def validate_coordinates(x: int, y: int) -> Tuple[int, int]:
    """
    Validate and clamp coordinates to non-negative values.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        Tuple of validated (x, y) coordinates
    """
    if x < 0 or y < 0:
        logger.warning(f"Invalid negative coordinates ({x}, {y}), clamping to 0")
        x = max(0, x)
        y = max(0, y)
    return x, y


def validate_swipe_coordinates(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
    """
    Validate and clamp swipe coordinates to non-negative values.

    Args:
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate

    Returns:
        Tuple of validated (x1, y1, x2, y2) coordinates
    """
    if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
        logger.warning("Invalid negative coordinates, clamping to 0")
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = max(0, x2)
        y2 = max(0, y2)
    return x1, y1, x2, y2


def validate_phone_number(phone_number: str) -> Tuple[bool, str, str]:
    """
    Validate and clean a phone number.

    Args:
        phone_number: Raw phone number string

    Returns:
        Tuple of (is_valid, cleaned_number, error_message)
        - is_valid: True if valid, False otherwise
        - cleaned_number: Cleaned number with only digits and +
        - error_message: Error message if invalid, empty string if valid
    """
    # Clean the number - keep only digits and +
    cleaned = "".join(c for c in phone_number if c.isdigit() or c == "+")

    # Check for misplaced '+' character
    # '+' is only allowed at the start and at most once
    plus_count = cleaned.count("+")
    if plus_count > 1:
        return False, cleaned, f"Invalid phone number: multiple '+' characters: {phone_number}"
    if plus_count == 1 and not cleaned.startswith("+"):
        return False, cleaned, f"Invalid phone number: '+' must be at the start: {phone_number}"

    # Basic validation: must have at least 3 digits
    if len(cleaned.replace("+", "")) < 3:
        return False, cleaned, f"Invalid phone number: {phone_number}"

    # Limit length to prevent abuse
    if len(cleaned) > 20:
        return False, cleaned, f"Phone number too long: {phone_number}"

    return True, cleaned, ""


def validate_text_input(text: str, max_length: int = 5000) -> str:
    """
    Validate and truncate text input.

    Args:
        text: Input text
        max_length: Maximum allowed length

    Returns:
        Validated text (truncated if too long)
    """
    if not text:
        return text

    if len(text) > max_length:
        logger.warning(f"Text too long, truncating to {max_length} characters")
        text = text[:max_length]

    return text


def validate_chunk_size(chunk_size: int, min_size: int = 1, max_size: int = 50) -> int:
    """
    Validate and clamp chunk size to reasonable bounds.

    Args:
        chunk_size: Requested chunk size
        min_size: Minimum allowed size
        max_size: Maximum allowed size

    Returns:
        Validated chunk size
    """
    if chunk_size < min_size or chunk_size > max_size:
        clamped = max(min_size, min(chunk_size, max_size))
        logger.warning(
            f"Chunk size {chunk_size} out of range [{min_size}, {max_size}], "
            f"clamping to {clamped}"
        )
        return clamped
    return chunk_size
