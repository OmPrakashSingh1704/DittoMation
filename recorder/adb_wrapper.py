"""
ADB Wrapper - Foundation for all ADB interactions.

Provides utilities for executing ADB commands, detecting device info,
capturing UI hierarchy, and streaming shell output.
"""

import os
import re
import subprocess
import xml.etree.ElementTree as ET
from typing import Optional, Tuple, List, Generator


def get_adb_path() -> str:
    """
    Auto-detect ADB location.

    Checks in order:
    1. ANDROID_HOME/platform-tools/adb.exe
    2. User's local Android SDK
    3. System PATH

    Returns:
        Path to adb executable

    Raises:
        FileNotFoundError: If ADB cannot be found
    """
    # Check ANDROID_HOME environment variable
    android_home = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if android_home:
        adb_path = os.path.join(android_home, 'platform-tools', 'adb.exe')
        if os.path.exists(adb_path):
            return adb_path

    # Check common Windows location
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if local_app_data:
        adb_path = os.path.join(local_app_data, 'Android', 'Sdk', 'platform-tools', 'adb.exe')
        if os.path.exists(adb_path):
            return adb_path

    # Check user profile path
    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        adb_path = os.path.join(user_profile, 'AppData', 'Local', 'Android', 'Sdk', 'platform-tools', 'adb.exe')
        if os.path.exists(adb_path):
            return adb_path

    # Try system PATH
    try:
        result = subprocess.run(['where', 'adb'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass

    raise FileNotFoundError(
        "ADB not found. Please set ANDROID_HOME environment variable or add adb to PATH."
    )


# Cache ADB path after first detection
_adb_path: Optional[str] = None


def _get_adb() -> str:
    """Get cached ADB path."""
    global _adb_path
    if _adb_path is None:
        _adb_path = get_adb_path()
    return _adb_path


def run_adb(args: List[str], timeout: Optional[int] = 30) -> str:
    """
    Execute ADB command and return output.

    Args:
        args: List of arguments to pass to adb
        timeout: Command timeout in seconds (None for no timeout)

    Returns:
        Command stdout as string

    Raises:
        subprocess.CalledProcessError: If command fails
        subprocess.TimeoutExpired: If command times out
    """
    adb = _get_adb()
    cmd = [adb] + args

    result = subprocess.run(
        cmd,
        capture_output=True,
        timeout=timeout
    )

    # Decode with UTF-8, ignoring errors for special characters
    stdout = result.stdout.decode('utf-8', errors='ignore')
    stderr = result.stderr.decode('utf-8', errors='ignore')

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            stdout,
            stderr
        )

    return stdout


def get_device_serial() -> Optional[str]:
    """
    Get the serial number of the connected device.

    Returns:
        Device serial or None if no device connected
    """
    try:
        output = run_adb(['devices'])
        lines = output.strip().split('\n')
        for line in lines[1:]:  # Skip header
            if '\tdevice' in line:
                return line.split('\t')[0]
    except Exception:
        pass
    return None


def get_screen_size() -> Tuple[int, int]:
    """
    Get device screen size.

    Returns:
        Tuple of (width, height) in pixels

    Raises:
        RuntimeError: If screen size cannot be determined
    """
    # Try wm size first
    try:
        output = run_adb(['shell', 'wm', 'size'])
        # Output format: "Physical size: 1080x2340"
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
    except subprocess.CalledProcessError:
        pass

    # Fallback: try SurfaceFlinger (works on Android 13+)
    try:
        output = run_adb(['shell', 'dumpsys', 'SurfaceFlinger'])
        # Look for "size=[1080 2400]" pattern
        match = re.search(r'size=\[(\d+)\s+(\d+)\]', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        # Look for "w/h:1080x2400" pattern
        match = re.search(r'w/h:(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
    except subprocess.CalledProcessError:
        pass

    # Fallback: try dumpsys display
    try:
        output = run_adb(['shell', 'dumpsys', 'display'])
        match = re.search(r'mDisplayWidth=(\d+).*?mDisplayHeight=(\d+)', output, re.DOTALL)
        if match:
            return int(match.group(1)), int(match.group(2))
        # Alternative pattern
        match = re.search(r'(\d+)\s*x\s*(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
    except subprocess.CalledProcessError:
        pass

    # Fallback: try getprop
    try:
        width_out = run_adb(['shell', 'getprop', 'persist.sys.lcd_density_width'])
        height_out = run_adb(['shell', 'getprop', 'persist.sys.lcd_density_height'])
        if width_out.strip() and height_out.strip():
            return int(width_out.strip()), int(height_out.strip())
    except (subprocess.CalledProcessError, ValueError):
        pass

    # Fallback: common default sizes
    print("Warning: Could not detect screen size, using default 1080x1920")
    return 1080, 1920


def get_input_devices() -> List[dict]:
    """
    Get list of input devices.

    Returns:
        List of device info dicts with 'path' and 'name' keys
    """
    output = run_adb(['shell', 'getevent', '-pl'])
    devices = []
    current_device = None

    for line in output.split('\n'):
        if line.startswith('add device'):
            # Parse: "add device 1: /dev/input/event1"
            match = re.search(r'/dev/input/event\d+', line)
            if match:
                current_device = {'path': match.group(0), 'name': ''}
        elif 'name:' in line and current_device:
            # Parse: '  name:     "device_name"'
            match = re.search(r'name:\s+"([^"]+)"', line)
            if match:
                current_device['name'] = match.group(1)
                devices.append(current_device)
                current_device = None

    return devices


def get_input_device() -> str:
    """
    Find the primary touch input device path.

    Returns:
        Device path like '/dev/input/event1'

    Raises:
        RuntimeError: If no touch device found
    """
    devices = get_input_devices()

    # Sort by event number to prefer lower numbered devices (usually the primary)
    def get_event_num(d):
        match = re.search(r'event(\d+)', d['path'])
        return int(match.group(1)) if match else 999

    devices.sort(key=get_event_num)

    # Look for touch-related devices
    touch_keywords = ['touch', 'touchscreen', 'ts', 'input']

    for device in devices:
        name_lower = device['name'].lower()
        if any(kw in name_lower for kw in touch_keywords):
            return device['path']

    # Fallback: return first event device
    if devices:
        return devices[0]['path']

    raise RuntimeError("No touch input device found")


def get_input_max_values(device: str) -> Tuple[int, int]:
    """
    Get max X/Y values for coordinate scaling from input device.

    Args:
        device: Device path like '/dev/input/event1'

    Returns:
        Tuple of (max_x, max_y)
    """
    output = run_adb(['shell', 'getevent', '-pl'])

    max_x = 0
    max_y = 0
    in_device_section = False

    for line in output.split('\n'):
        if device in line:
            in_device_section = True
        elif line.startswith('add device') and in_device_section:
            break
        elif in_device_section:
            # Look for ABS_MT_POSITION_X or ABS_MT_POSITION_Y
            if 'ABS_MT_POSITION_X' in line or '0035' in line:
                match = re.search(r'max\s+(\d+)', line)
                if match:
                    max_x = int(match.group(1))
            elif 'ABS_MT_POSITION_Y' in line or '0036' in line:
                match = re.search(r'max\s+(\d+)', line)
                if match:
                    max_y = int(match.group(1))

    # Fallback to screen size if not found
    if max_x == 0 or max_y == 0:
        width, height = get_screen_size()
        return width, height

    return max_x, max_y


def dump_ui(output_path: Optional[str] = None, max_retries: int = 5, retry_delay: float = 1.0) -> ET.Element:
    """
    Capture UI hierarchy XML and return parsed tree.

    Args:
        output_path: Optional path to save raw XML
        max_retries: Number of retries if UI dump fails (for loading screens)
        retry_delay: Seconds to wait between retries

    Returns:
        Root element of parsed XML tree
    """
    import time

    adb = _get_adb()
    device_path = '/sdcard/window_dump.xml'

    last_error = None

    for attempt in range(max_retries):
        try:
            # Kill any stuck uiautomator process before trying
            if attempt > 0:
                subprocess.run(
                    [adb, 'shell', 'pkill', '-f', 'uiautomator'],
                    capture_output=True,
                    timeout=5
                )
                time.sleep(0.5)

            # Dump UI - use quoted command to avoid path escaping issues
            dump_result = subprocess.run(
                [adb, 'shell', f'uiautomator dump {device_path}'],
                capture_output=True,
                timeout=60  # Increased timeout
            )

            dump_stdout = dump_result.stdout.decode('utf-8', errors='ignore')
            dump_stderr = dump_result.stderr.decode('utf-8', errors='ignore')

            # Check for common errors indicating UI not ready
            if 'null root node' in dump_stdout or 'null root node' in dump_stderr:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue

            # Pull the file content
            cat_result = subprocess.run(
                [adb, 'shell', f'cat {device_path}'],
                capture_output=True,
                timeout=10
            )

            xml_content = cat_result.stdout.decode('utf-8', errors='ignore')
            cat_stderr = cat_result.stderr.decode('utf-8', errors='ignore')

            if not xml_content or not xml_content.strip().startswith('<?xml'):
                last_error = f"{dump_stderr} {cat_stderr}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise RuntimeError(f"UI dump failed: {last_error}")

            # Clean up device file (ignore errors)
            subprocess.run(
                [adb, 'shell', f'rm {device_path}'],
                capture_output=True,
                timeout=5
            )

            # Save to output if requested
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)

            # Parse and return
            return ET.fromstring(xml_content)

        except ET.ParseError as e:
            last_error = f"XML parse error: {e}"
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue

        except subprocess.TimeoutExpired as e:
            last_error = f"Timeout: {e}"
            # Kill stuck uiautomator on timeout
            subprocess.run(
                [adb, 'shell', 'pkill', '-f', 'uiautomator'],
                capture_output=True,
                timeout=5
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue

    raise RuntimeError(f"UI dump failed after {max_retries} attempts: {last_error}")


def shell_stream(cmd: str) -> Generator[str, None, None]:
    """
    Stream output from shell command (for getevent).

    Args:
        cmd: Shell command to execute

    Yields:
        Lines of output from the command
    """
    adb = _get_adb()
    full_cmd = [adb, 'shell', cmd]

    process = subprocess.Popen(
        full_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            yield line.rstrip('\n\r')
    finally:
        process.terminate()
        process.wait()


def get_current_app() -> Tuple[str, str]:
    """
    Get current foreground app package and activity.

    Returns:
        Tuple of (package_name, activity_name)
    """
    output = run_adb(['shell', 'dumpsys', 'activity', 'activities'])

    # Look for mResumedActivity or mFocusedActivity
    for pattern in [r'mResumedActivity.*?(\S+)/(\S+)', r'mFocusedActivity.*?(\S+)/(\S+)']:
        match = re.search(pattern, output)
        if match:
            return match.group(1), match.group(2)

    # Alternative: use window focus
    output = run_adb(['shell', 'dumpsys', 'window', 'windows'])
    match = re.search(r'mCurrentFocus.*?(\S+)/(\S+)', output)
    if match:
        return match.group(1), match.group(2)

    return '', ''


def check_device_connected() -> bool:
    """Check if a device is connected and ready."""
    try:
        output = run_adb(['devices'])
        return '\tdevice' in output
    except Exception:
        return False


def wait_for_device(timeout: int = 60) -> bool:
    """
    Wait for device to be fully booted.

    Args:
        timeout: Max seconds to wait

    Returns:
        True if device is ready, False if timeout
    """
    import time

    print("Waiting for device...")

    # First wait for device to appear
    try:
        run_adb(['wait-for-device'], timeout=timeout)
    except Exception:
        return False

    # Then wait for boot to complete
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            output = run_adb(['shell', 'getprop', 'sys.boot_completed'])
            if output.strip() == '1':
                print("Device ready.")
                return True
        except subprocess.CalledProcessError:
            pass
        time.sleep(1)

    print("Timeout waiting for device boot.")
    return False
