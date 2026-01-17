"""
Recorder Main - CLI entry point for recording Android interactions.

Usage:
    python -m recorder.main --output workflow.json

Flow:
1. Initialize ADB connection
2. Detect touch device and calibration values
3. Start event listener
4. On TOUCH_DOWN: capture UI snapshot
5. On gesture complete: match element, classify gesture, add step
6. On Ctrl+C: save workflow and exit
"""

import argparse
import signal
import sys
import time
from typing import Optional, Dict, Any, List

try:
    from recorder.adb_wrapper import check_device_connected, get_screen_size, wait_for_device
    from recorder.event_listener import TouchEventListener, TouchEvent
    from recorder.ui_dumper import capture_ui, find_scrollable_parent, get_all_elements, pretty_print_element
    from recorder.element_matcher import match_element_at_point, describe_match
    from recorder.gesture_classifier import GestureClassifier, Gesture, describe_gesture
    from recorder.workflow import WorkflowRecorder, format_step
except ImportError:
    from adb_wrapper import check_device_connected, get_screen_size, wait_for_device
    from event_listener import TouchEventListener, TouchEvent
    from ui_dumper import capture_ui, find_scrollable_parent, get_all_elements, pretty_print_element
    from element_matcher import match_element_at_point, describe_match
    from gesture_classifier import GestureClassifier, Gesture, describe_gesture
    from workflow import WorkflowRecorder, format_step


class RecordingSession:
    """
    Manages a recording session.

    Coordinates event listening, UI capture, gesture classification,
    and workflow recording.
    """

    def __init__(self, output_path: str, output_dir: str = "output"):
        """
        Initialize recording session.

        Args:
            output_path: Path for workflow JSON output
            output_dir: Directory for UI snapshots
        """
        self.output_path = output_path
        self.output_dir = output_dir

        # Components
        self.listener: Optional[TouchEventListener] = None
        self.classifier: Optional[GestureClassifier] = None
        self.workflow: Optional[WorkflowRecorder] = None

        # State
        self._running = False
        self._pending_ui_tree = None
        self._pending_elements: List[Dict[str, Any]] = []
        self._touch_down_time: float = 0

    def _on_touch_event(self, event: TouchEvent) -> None:
        """
        Handle incoming touch events.

        Args:
            event: TouchEvent from listener
        """
        # On touch down, capture UI snapshot
        if event.type == 'touch_down':
            self._touch_down_time = time.time()
            try:
                step_num = len(self.workflow) + 1
                xml_path = self.workflow.get_ui_snapshot_path(step_num)
                self._pending_ui_tree, self._pending_elements = capture_ui(xml_path)
                print(f"  UI captured ({len(self._pending_elements)} elements)")
            except Exception as e:
                print(f"  Warning: UI capture failed: {e}")
                self._pending_ui_tree = None
                self._pending_elements = []

        # Feed event to classifier
        self.classifier.feed(event)

        # Check for completed gesture
        gesture = self.classifier.get_gesture()
        if gesture:
            self._on_gesture_complete(gesture)

    def _on_gesture_complete(self, gesture: Gesture) -> None:
        """
        Handle completed gesture.

        Args:
            gesture: Classified Gesture
        """
        print(f"\n{describe_gesture(gesture)}")

        # Match element at gesture start point
        x, y = gesture.start
        element, locator = match_element_at_point(self._pending_elements, x, y)

        if element:
            print(f"  Element: {pretty_print_element(element)}")
            print(f"  Locator: {describe_match(element, locator)}")
        else:
            print(f"  No element matched at ({x}, {y})")

        # Add step to workflow
        step_num = len(self.workflow) + 1
        xml_path = self.workflow.get_ui_snapshot_path(step_num)

        step = self.workflow.add_step(
            gesture=gesture,
            element=element,
            locator=locator,
            ui_xml_file=xml_path
        )

        print(f"  -> {format_step(step)}")

    def _check_scrollable(self, x: int, y: int) -> bool:
        """Check if coordinates are in a scrollable container."""
        if not self._pending_elements:
            return False

        scrollable = find_scrollable_parent(self._pending_elements, x, y)
        return scrollable is not None

    def start(self) -> None:
        """Start the recording session."""
        print("=" * 50)
        print("Android Recorder")
        print("=" * 50)

        # Check device connection
        if not check_device_connected():
            print("No device detected. Waiting for device...")
            if not wait_for_device(timeout=60):
                print("Error: No Android device connected.")
                print("Please connect a device or start an emulator.")
                sys.exit(1)

        # Get screen info (with retry for slow boot)
        width, height = get_screen_size()
        print(f"Screen size: {width}x{height}")

        # Initialize components
        self.workflow = WorkflowRecorder(output_dir=self.output_dir)
        self.classifier = GestureClassifier(scrollable_checker=self._check_scrollable)
        self.listener = TouchEventListener()

        # Register event callback
        self.listener.on_event(self._on_touch_event)

        # Start listening
        print("\nStarting touch event capture...")
        self.listener.start()
        self._running = True

        print("\n" + "=" * 50)
        print("Recording started. Interact with the device.")
        print("Press Ctrl+C to stop and save.")
        print("=" * 50 + "\n")

    def stop(self) -> None:
        """Stop the recording session and save workflow."""
        self._running = False

        if self.listener:
            self.listener.stop()

        if self.workflow and len(self.workflow) > 0:
            print("\n" + "=" * 50)
            print("Recording stopped.")
            print("=" * 50)

            # Deduplicate
            removed = self.workflow.deduplicate()
            if removed > 0:
                print(f"Removed {removed} duplicate step(s)")

            # Save workflow
            self.workflow.save(self.output_path)

            # Print summary
            print("\n" + self.workflow.summary())
        else:
            print("\nNo steps recorded.")

    def wait(self) -> None:
        """Wait for recording to complete (Ctrl+C)."""
        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Record Android touch interactions to a workflow file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m recorder.main --output my_workflow.json
  python -m recorder.main -o test.json --output-dir ./snapshots

The recorder will:
1. Capture touch events from the connected Android device
2. Match taps to UI elements
3. Classify gestures (tap, long_press, swipe, scroll, pinch)
4. Save a replayable workflow file
        """
    )

    parser.add_argument(
        "-o", "--output",
        default="workflow.json",
        help="Output workflow file path (default: workflow.json)"
    )

    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for UI snapshots (default: output)"
    )

    args = parser.parse_args()

    # Create session
    session = RecordingSession(
        output_path=args.output,
        output_dir=args.output_dir
    )

    # Handle signals
    def signal_handler(sig, frame):
        session.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run recording
    try:
        session.start()
        session.wait()
    finally:
        session.stop()


if __name__ == "__main__":
    main()
