"""
Replayer Main - CLI entry point for replaying recorded workflows.

Usage:
    python -m replayer.main --workflow workflow.json --delay 500

Flow:
1. Load workflow JSON
2. For each step:
   a. Capture current UI
   b. Locate element using smart fallback
   c. Execute gesture at element center (or recorded coords if not found)
   d. Wait for delay between steps
3. Report success/failure for each step
"""

import argparse
import os
import signal
import sys
import time
from typing import Optional, List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recorder.adb_wrapper import check_device_connected, get_screen_size
from recorder.ui_dumper import capture_ui_fast
from recorder.workflow import WorkflowRecorder, WorkflowStep, format_step
from replayer.locator import ElementLocator, describe_location_result
from replayer.executor import GestureExecutor


class ReplaySession:
    """
    Manages a replay session.

    Coordinates workflow loading, element location, and gesture execution.
    """

    def __init__(
        self,
        workflow_path: str,
        delay_ms: int = 500,
        verbose: bool = False
    ):
        """
        Initialize replay session.

        Args:
            workflow_path: Path to workflow JSON file
            delay_ms: Delay between steps in milliseconds
            verbose: Enable verbose output
        """
        self.workflow_path = workflow_path
        self.delay_ms = delay_ms
        self.verbose = verbose

        # Components
        self.workflow: Optional[WorkflowRecorder] = None
        self.locator = ElementLocator()
        self.executor = GestureExecutor(delay_ms=delay_ms)

        # Results tracking
        self.results: List[Dict[str, Any]] = []
        self._running = False
        self._stop_requested = False

    def load(self) -> bool:
        """
        Load the workflow file.

        Returns:
            True if loaded successfully
        """
        try:
            self.workflow = WorkflowRecorder.load(self.workflow_path)
            print(f"Loaded workflow: {len(self.workflow)} steps")

            if self.verbose:
                print("\n" + self.workflow.summary())

            return True
        except FileNotFoundError:
            print(f"Error: Workflow file not found: {self.workflow_path}")
            return False
        except Exception as e:
            print(f"Error loading workflow: {e}")
            return False

    def run(self) -> bool:
        """
        Run the replay session.

        Returns:
            True if all steps succeeded
        """
        if not self.workflow:
            print("Error: No workflow loaded")
            return False

        if len(self.workflow) == 0:
            print("Warning: Workflow is empty")
            return True

        print("\n" + "=" * 50)
        print("Starting replay...")
        print("=" * 50 + "\n")

        self._running = True
        self.results = []

        for step in self.workflow:
            if self._stop_requested:
                print("\nReplay stopped by user")
                break

            result = self._replay_step(step)
            self.results.append(result)

            if not result["success"]:
                print(f"  [FAILED] {result.get('error', 'Unknown error')}")

        self._running = False
        return self._print_summary()

    def _replay_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """
        Replay a single workflow step.

        Args:
            step: WorkflowStep to replay

        Returns:
            Result dict with success status and details
        """
        result = {
            "step_id": step.step_id,
            "action": step.action,
            "success": False,
            "strategy_used": None,
            "fallback_level": 0,
            "error": None
        }

        print(f"Step {step.step_id}: {step.action.upper()}", end=" ")

        try:
            # Capture current UI
            ui_tree, elements = capture_ui_fast()

            if not elements:
                print("(no UI)")
                # Fall back to recorded coordinates
                coordinates = self._get_fallback_coordinates(step)
                success = self.executor.execute(step.gesture, coordinates)
                result["success"] = success
                result["strategy_used"] = "coordinates"
                result["fallback_level"] = 99
                return result

            # Find element using locator
            loc_result = self.locator.find_element(step.locator, elements)

            if loc_result.found:
                strategy_info = f"{loc_result.strategy_used}"
                if loc_result.fallback_level > 0:
                    strategy_info += f" (fallback #{loc_result.fallback_level})"
                print(f"({strategy_info})")
            else:
                print("(coordinates)")

            # Execute gesture
            success = self.executor.execute(step.gesture, loc_result.coordinates)

            result["success"] = success
            result["strategy_used"] = loc_result.strategy_used
            result["fallback_level"] = loc_result.fallback_level

            if self.verbose and loc_result.element:
                elem = loc_result.element
                print(f"    Element: {elem.get('class', '').split('.')[-1]}")
                if elem.get('resource_id'):
                    print(f"    ID: {elem['resource_id'].split('/')[-1]}")
                if elem.get('text'):
                    print(f"    Text: {elem['text'][:50]}")

        except Exception as e:
            result["error"] = str(e)
            print(f"(error: {e})")

        return result

    def _get_fallback_coordinates(self, step: WorkflowStep) -> tuple:
        """
        Get fallback coordinates from step.

        Args:
            step: WorkflowStep

        Returns:
            (x, y) coordinates
        """
        gesture = step.gesture
        start = gesture.get("start", [0, 0])
        return (start[0], start[1])

    def _print_summary(self) -> bool:
        """
        Print replay summary.

        Returns:
            True if all steps succeeded
        """
        print("\n" + "=" * 50)
        print("Replay Summary")
        print("=" * 50)

        total = len(self.results)
        success = sum(1 for r in self.results if r["success"])
        failed = total - success

        print(f"Total steps: {total}")
        print(f"Successful: {success}")
        print(f"Failed: {failed}")

        # Strategy breakdown
        strategy_counts: Dict[str, int] = {}
        fallback_counts: Dict[int, int] = {}

        for r in self.results:
            if r["success"]:
                strategy = r.get("strategy_used", "unknown")
                strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

                level = r.get("fallback_level", 0)
                fallback_counts[level] = fallback_counts.get(level, 0) + 1

        if strategy_counts:
            print("\nStrategies used:")
            for strategy, count in sorted(strategy_counts.items()):
                print(f"  {strategy}: {count}")

        if any(level > 0 for level in fallback_counts):
            print("\nFallback usage:")
            for level, count in sorted(fallback_counts.items()):
                if level == 0:
                    print(f"  Primary worked: {count}")
                else:
                    print(f"  Fallback #{level}: {count}")

        # Failed steps
        if failed > 0:
            print("\nFailed steps:")
            for r in self.results:
                if not r["success"]:
                    print(f"  Step {r['step_id']}: {r.get('error', 'Unknown')}")

        return failed == 0

    def stop(self) -> None:
        """Request stop of replay."""
        self._stop_requested = True


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Replay recorded Android workflows.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m replayer.main --workflow my_workflow.json
  python -m replayer.main -w test.json --delay 1000 --verbose

The replayer will:
1. Load the workflow file
2. For each step, find the target element using smart fallbacks
3. Execute the recorded gesture
4. Report success/failure for each step
        """
    )

    parser.add_argument(
        "-w", "--workflow",
        required=True,
        help="Workflow JSON file to replay"
    )

    parser.add_argument(
        "-d", "--delay",
        type=int,
        default=500,
        help="Delay between steps in milliseconds (default: 500)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )

    args = parser.parse_args()

    # Check device connection
    if not args.dry_run:
        if not check_device_connected():
            print("Error: No Android device connected.")
            print("Please connect a device or start an emulator.")
            sys.exit(1)

    # Create session
    session = ReplaySession(
        workflow_path=args.workflow,
        delay_ms=args.delay,
        verbose=args.verbose
    )

    # Handle signals
    def signal_handler(sig, frame):
        print("\nStopping replay...")
        session.stop()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Load workflow
    if not session.load():
        sys.exit(1)

    # Dry run mode
    if args.dry_run:
        print("\n[DRY RUN] Steps that would be executed:\n")
        for step in session.workflow:
            print(f"  {format_step(step)}")
        sys.exit(0)

    # Run replay
    success = session.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
