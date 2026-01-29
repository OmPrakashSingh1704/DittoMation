"""
Gesture Executor - Executes gestures via ADB input commands.

Provides functions to perform taps, swipes, long presses, and other
input events on the Android device.
"""

import os
import sys
import time
from typing import Any, Dict, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.logging_config import get_logger
from core.validators import (
    validate_chunk_size,
    validate_coordinates,
    validate_phone_number,
    validate_swipe_coordinates,
    validate_text_input,
)
from recorder.adb_wrapper import run_adb

# Module logger
logger = get_logger("executor")


def _escape_text_for_shell(text: str) -> str:
    """
    Escape text for safe shell input.

    Args:
        text: Raw text to escape

    Returns:
        Escaped text safe for shell command
    """
    escaped_parts = []
    for char in text:
        # Replace control characters with a space to avoid breaking the shell command
        if char in "\n\r\t":
            escaped_parts.append("%s")
        elif char == " ":
            escaped_parts.append("%s")
        elif char in "'\"&<>()|;\\`$!#*?[]{}.":
            # Add backslash escaping for shell-sensitive chars
            escaped_parts.append("\\" + char)
        else:
            # Only allow printable ASCII characters
            code_point = ord(char)
            if 32 <= code_point < 127:
                escaped_parts.append(char)
            # Skip non-printable characters for security
    return "".join(escaped_parts)


def _clear_text_field() -> None:
    """Clear the current text field by moving to the end and long-pressing delete."""
    run_adb(["shell", "input", "keyevent", "KEYCODE_MOVE_END"])
    run_adb(["shell", "input", "keyevent", "--longpress", "KEYCODE_DEL"])
    time.sleep(0.2)


def _parse_coordinates(coord: Any, default: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """
    Parse coordinates from various formats.

    Args:
        coord: Coordinate value in various formats (typically list/tuple [x, y])
        default: Default coordinate if parsing fails

    Returns:
        Tuple of (x, y) coordinates
    """
    if isinstance(coord, (list, tuple)) and len(coord) >= 2:
        return coord[0], coord[1]
    logger.warning(f"Invalid coordinates: {coord}, using default {default}")
    return default


def _calculate_relative_end(start_x: int, start_y: int, gesture: Dict[str, Any]) -> Tuple[int, int]:
    """
    Calculate end coordinates relative to a new start position.

    Args:
        start_x: New start X coordinate
        start_y: New start Y coordinate
        gesture: Gesture dict containing original start/end

    Returns:
        Tuple of (end_x, end_y) coordinates
    """
    orig_start = gesture.get("start", [0, 0])
    end = gesture.get("end", [start_x, start_y])

    # Calculate delta if both coordinates are valid
    if (
        isinstance(orig_start, (list, tuple))
        and len(orig_start) >= 2
        and isinstance(end, (list, tuple))
        and len(end) >= 2
    ):
        dx = end[0] - orig_start[0]
        dy = end[1] - orig_start[1]
        return start_x + dx, start_y + dy

    # Fallback to original end coordinates
    return _parse_coordinates(end, (start_x, start_y))


def tap(x: int, y: int) -> bool:
    """
    Execute tap gesture.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        True if successful
    """
    try:
        # Validate coordinates
        x, y = validate_coordinates(x, y)

        run_adb(["shell", "input", "tap", str(x), str(y)])
        return True
    except Exception as e:
        logger.error(f"Tap failed: {e}")
        return False


def long_press(x: int, y: int, duration_ms: int = 1000) -> bool:
    """
    Execute long press gesture.

    Uses swipe from point to same point with duration to simulate long press.

    Args:
        x: X coordinate
        y: Y coordinate
        duration_ms: Press duration in milliseconds

    Returns:
        True if successful
    """
    try:
        # Validate coordinates
        x, y = validate_coordinates(x, y)

        # Long press is simulated as a swipe with same start/end point
        run_adb(["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)])
        return True
    except Exception as e:
        logger.error(f"Long press failed: {e}")
        return False


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
    """
    Execute swipe gesture.

    Args:
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate
        duration_ms: Swipe duration in milliseconds

    Returns:
        True if successful
    """
    try:
        # Validate coordinates
        x1, y1, x2, y2 = validate_swipe_coordinates(x1, y1, x2, y2)

        run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)])
        return True
    except Exception as e:
        logger.error(f"Swipe failed: {e}")
        return False


def scroll(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500) -> bool:
    """
    Execute scroll gesture.

    Same as swipe but with longer default duration for smoother scroll.

    Args:
        x1: Start X coordinate
        y1: Start Y coordinate
        x2: End X coordinate
        y2: End Y coordinate
        duration_ms: Scroll duration in milliseconds

    Returns:
        True if successful
    """
    return swipe(x1, y1, x2, y2, duration_ms)


def pinch(center_x: int, center_y: int, scale: float, duration_ms: int = 500) -> bool:
    """
    Execute pinch gesture (zoom in/out).

    Note: This is a simplified approximation using multiple swipes.
    For accurate pinch, sendevent would be needed.

    Args:
        center_x: Center X of pinch
        center_y: Center Y of pinch
        scale: Scale factor (>1 zoom in, <1 zoom out)
        duration_ms: Gesture duration

    Returns:
        True if successful
    """
    try:
        # Calculate pinch parameters
        base_distance = 200
        if scale > 1:
            # Zoom in: fingers move apart
            start_dist = int(base_distance / scale)
            end_dist = base_distance
        else:
            # Zoom out: fingers move together
            start_dist = base_distance
            end_dist = int(base_distance * scale)

        # Execute as two simultaneous swipes (approximation)
        # This is a simplified version - real pinch needs sendevent

        # First finger: left to right of center
        run_adb(
            [
                "shell",
                "input",
                "swipe",
                str(center_x - start_dist // 2),
                str(center_y),
                str(center_x - end_dist // 2),
                str(center_y),
                str(duration_ms),
            ]
        )

        # Brief delay
        time.sleep(0.05)

        # Second finger: right to left of center (opposite direction)
        run_adb(
            [
                "shell",
                "input",
                "swipe",
                str(center_x + start_dist // 2),
                str(center_y),
                str(center_x + end_dist // 2),
                str(center_y),
                str(duration_ms),
            ]
        )

        return True
    except Exception as e:
        logger.error(f"Pinch failed: {e}")
        return False


def input_text(text: str, chunk_size: int = 10, clear_first: bool = False) -> bool:
    """
    Input text string.

    Args:
        text: Text to input
        chunk_size: Characters per chunk (smaller = slower but more reliable)
        clear_first: If True, clear the field before typing

    Returns:
        True if successful
    """
    try:
        # Validate input
        if not text:
            return True  # Empty string is valid, just return success

        text = validate_text_input(text)
        chunk_size = validate_chunk_size(chunk_size)

        # Optionally clear existing text first
        if clear_first:
            _clear_text_field()

        # Type in chunks to avoid dropped characters
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            escaped = _escape_text_for_shell(chunk)
            run_adb(["shell", "input", "text", escaped])

            # Small delay between chunks
            if i + chunk_size < len(text):
                time.sleep(0.15)

        return True
    except Exception as e:
        logger.error(f"Input text failed: {e}")
        return False


def press_key(keycode: str) -> bool:
    """
    Press a key by keycode.

    Common keycodes:
    - KEYCODE_HOME (3)
    - KEYCODE_BACK (4)
    - KEYCODE_MENU (82)
    - KEYCODE_ENTER (66)
    - KEYCODE_DEL (67) - Backspace

    Args:
        keycode: Key code name or number

    Returns:
        True if successful
    """
    try:
        run_adb(["shell", "input", "keyevent", str(keycode)])
        return True
    except Exception as e:
        logger.error(f"Key press failed: {e}")
        return False


def press_back() -> bool:
    """Press back button."""
    return press_key("KEYCODE_BACK")


def press_home() -> bool:
    """Press home button."""
    return press_key("KEYCODE_HOME")


def press_enter() -> bool:
    """Press enter key."""
    return press_key("KEYCODE_ENTER")


def make_call(phone_number: str) -> bool:
    """
    Make a phone call.

    Args:
        phone_number: Number to call (e.g., "1234567890")

    Returns:
        True if successful
    """
    try:
        # Validate the number
        is_valid, number, error_msg = validate_phone_number(phone_number)
        if not is_valid:
            logger.error(error_msg)
            return False

        run_adb(["shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{number}"])
        return True
    except Exception as e:
        logger.error(f"Call failed: {e}")
        return False


def end_call() -> bool:
    """End the current phone call."""
    return press_key("KEYCODE_ENDCALL")


def dial_number(phone_number: str) -> bool:
    """
    Open dialer with number (doesn't start call).

    Args:
        phone_number: Number to dial

    Returns:
        True if successful
    """
    try:
        # Validate the number
        is_valid, number, error_msg = validate_phone_number(phone_number)
        if not is_valid:
            logger.error(error_msg)
            return False

        run_adb(["shell", "am", "start", "-a", "android.intent.action.DIAL", "-d", f"tel:{number}"])
        return True
    except Exception as e:
        logger.error(f"Dial failed: {e}")
        return False


def execute_gesture(gesture: Dict[str, Any], coordinates: Optional[Tuple[int, int]] = None) -> bool:
    """
    Execute a gesture from workflow step.

    Args:
        gesture: Gesture dict from workflow
        coordinates: Override coordinates (from element location)

    Returns:
        True if successful
    """
    gesture_type = gesture.get("type", "tap")

    # Get start coordinates (use override or gesture coordinates)
    if coordinates:
        x, y = coordinates
    else:
        x, y = _parse_coordinates(gesture.get("start", [0, 0]), (0, 0))

    # Get end coordinates for swipe/scroll gestures
    end_x, end_y = _parse_coordinates(gesture.get("end", [x, y]), (x, y))

    # Get duration
    duration_ms = gesture.get("duration_ms", 100)

    # Execute based on type
    if gesture_type == "tap":
        return tap(x, y)

    elif gesture_type == "long_press":
        press_duration = max(duration_ms, 500)
        return long_press(x, y, press_duration)

    elif gesture_type == "swipe":
        # Calculate end point relative to new start if coordinates were overridden
        if coordinates:
            end_x, end_y = _calculate_relative_end(x, y, gesture)
        swipe_duration = max(duration_ms, 200)
        return swipe(x, y, end_x, end_y, swipe_duration)

    elif gesture_type == "scroll":
        # Calculate end point relative to new start if coordinates were overridden
        if coordinates:
            end_x, end_y = _calculate_relative_end(x, y, gesture)
        scroll_duration = max(duration_ms, 300)
        return scroll(x, y, end_x, end_y, scroll_duration)

    elif gesture_type == "pinch":
        scale = gesture.get("scale", 1.0)
        return pinch(x, y, scale, duration_ms)

    else:
        logger.warning(f"Unknown gesture type: {gesture_type}")
        return False


class GestureExecutor:
    """
    Stateful gesture executor with delay control.

    Manages delays between gestures and tracks execution.
    """

    def __init__(self, delay_ms: int = 500):
        """
        Initialize executor.

        Args:
            delay_ms: Delay between gestures in milliseconds
        """
        self.delay_ms = delay_ms
        self.executed_count = 0
        self.failed_count = 0

    def execute(
        self, gesture: Dict[str, Any], coordinates: Optional[Tuple[int, int]] = None
    ) -> bool:
        """
        Execute gesture with delay handling.

        Args:
            gesture: Gesture dict
            coordinates: Target coordinates

        Returns:
            True if successful
        """
        success = execute_gesture(gesture, coordinates)

        if success:
            self.executed_count += 1
        else:
            self.failed_count += 1

        # Wait after gesture
        time.sleep(self.delay_ms / 1000.0)

        return success

    def reset_stats(self) -> None:
        """Reset execution statistics."""
        self.executed_count = 0
        self.failed_count = 0

    @property
    def stats(self) -> Dict[str, int]:
        """Get execution statistics."""
        return {
            "executed": self.executed_count,
            "failed": self.failed_count,
            "total": self.executed_count + self.failed_count,
        }
