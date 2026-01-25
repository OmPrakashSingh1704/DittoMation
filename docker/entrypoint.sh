#!/bin/bash
#
# DittoMation Docker Entrypoint Script
#
# This script handles:
# - Starting the Android emulator in headless mode
# - Waiting for emulator to boot
# - Running DittoMation commands
# - Graceful shutdown

set -e

# Configuration from environment
AVD_NAME="${AVD_NAME:-dittomation_avd}"
EMULATOR_TIMEOUT="${EMULATOR_TIMEOUT:-300}"
START_EMULATOR="${START_EMULATOR:-true}"
DITTO_EMULATOR_HEADLESS="${DITTO_EMULATOR_HEADLESS:-true}"
DITTO_EMULATOR_GPU="${DITTO_EMULATOR_GPU:-swiftshader_indirect}"
DITTO_EMULATOR_MEMORY="${DITTO_EMULATOR_MEMORY:-2048}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to start the emulator
start_emulator() {
    log_info "Starting Android emulator: ${AVD_NAME}"

    # Build emulator command
    EMULATOR_CMD="emulator -avd ${AVD_NAME}"

    if [ "${DITTO_EMULATOR_HEADLESS}" = "true" ]; then
        EMULATOR_CMD="${EMULATOR_CMD} -no-window"
    fi

    EMULATOR_CMD="${EMULATOR_CMD} -gpu ${DITTO_EMULATOR_GPU}"
    EMULATOR_CMD="${EMULATOR_CMD} -memory ${DITTO_EMULATOR_MEMORY}"
    EMULATOR_CMD="${EMULATOR_CMD} -no-audio"
    EMULATOR_CMD="${EMULATOR_CMD} -no-boot-anim"
    EMULATOR_CMD="${EMULATOR_CMD} -no-snapshot-save"

    # Start emulator in background
    log_info "Emulator command: ${EMULATOR_CMD}"
    ${EMULATOR_CMD} &
    EMULATOR_PID=$!

    log_info "Emulator started with PID: ${EMULATOR_PID}"
}

# Function to wait for emulator boot
wait_for_boot() {
    log_info "Waiting for emulator to boot (timeout: ${EMULATOR_TIMEOUT}s)..."

    local start_time=$(date +%s)
    local boot_completed=false

    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))

        if [ $elapsed -ge $EMULATOR_TIMEOUT ]; then
            log_error "Emulator boot timeout after ${EMULATOR_TIMEOUT}s"
            return 1
        fi

        # Check if emulator is visible to ADB
        if adb devices | grep -q "emulator-"; then
            # Check boot completion
            local boot_status=$(adb -e shell getprop sys.boot_completed 2>/dev/null || echo "")

            if [ "$boot_status" = "1" ]; then
                boot_completed=true
                break
            fi
        fi

        sleep 5
        log_info "Waiting for boot... (${elapsed}s elapsed)"
    done

    if [ "$boot_completed" = true ]; then
        log_info "Emulator boot completed successfully!"

        # Additional wait for system to stabilize
        sleep 5

        # Unlock screen
        adb -e shell input keyevent 82 2>/dev/null || true

        return 0
    fi

    return 1
}

# Function to stop emulator gracefully
stop_emulator() {
    log_info "Stopping emulator..."

    # Try graceful shutdown first
    adb -e emu kill 2>/dev/null || true

    # Wait for process to exit
    sleep 5

    # Force kill if still running
    if [ -n "$EMULATOR_PID" ] && kill -0 $EMULATOR_PID 2>/dev/null; then
        log_warn "Force killing emulator process"
        kill -9 $EMULATOR_PID 2>/dev/null || true
    fi

    log_info "Emulator stopped"
}

# Trap signals for graceful shutdown
cleanup() {
    log_info "Received shutdown signal"
    stop_emulator
    exit 0
}

trap cleanup SIGTERM SIGINT

# Main execution
main() {
    # Start ADB server
    log_info "Starting ADB server..."
    adb start-server

    # Check if we need to start the emulator
    if [ "${START_EMULATOR}" = "true" ]; then
        # Check if an emulator is already running
        if adb devices | grep -q "emulator-"; then
            log_info "Emulator already running"
        else
            start_emulator

            if ! wait_for_boot; then
                log_error "Failed to start emulator"
                exit 1
            fi
        fi
    fi

    # Check for connected devices
    log_info "Connected devices:"
    adb devices -l

    # Execute the command passed to the container
    if [ $# -gt 0 ]; then
        log_info "Executing command: $@"
        exec "$@"
    else
        log_info "No command specified. Starting interactive shell..."
        exec /bin/bash
    fi
}

main "$@"
