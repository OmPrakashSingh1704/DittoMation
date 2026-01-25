# DittoMation Docker Image
#
# This Dockerfile creates a containerized environment for running
# DittoMation automation workflows with an Android emulator.
#
# Build:
#   docker build -t dittomation .
#
# Run:
#   docker run --rm -it dittomation ditto run /app/workflows/test.json
#
# With emulator:
#   docker run --rm --privileged dittomation

FROM ubuntu:22.04

LABEL maintainer="DittoMation Team"
LABEL description="DittoMation Android Automation with Emulator Support"
LABEL version="1.0.0"

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set locale
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Android SDK configuration
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/emulator:/usr/local/bin:/root/.local/bin"

# Emulator configuration
ENV DITTO_EMULATOR_HEADLESS=true
ENV DITTO_EMULATOR_GPU=swiftshader_indirect
ENV DITTO_EMULATOR_MEMORY=2048
ENV DITTO_EMULATOR_CORES=2

# Default AVD configuration
ENV AVD_NAME=dittomation_avd
ENV AVD_DEVICE="pixel_6"
ENV AVD_API_LEVEL=33
ENV AVD_ABI=x86_64

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python
    python3.10 \
    python3-pip \
    python3.10-venv \
    # Java (required for Android SDK)
    openjdk-17-jdk-headless \
    # Core utilities
    wget \
    curl \
    unzip \
    git \
    # For emulator
    libgl1-mesa-glx \
    libpulse0 \
    libasound2 \
    libx11-6 \
    libxcursor1 \
    libxext6 \
    libxft2 \
    libxi6 \
    libxinerama1 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    # For hardware acceleration (KVM)
    qemu-kvm \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Java home
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Install Android Command Line Tools
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools \
    && cd ${ANDROID_HOME}/cmdline-tools \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip -O tools.zip \
    && unzip -q tools.zip \
    && rm tools.zip \
    && mv cmdline-tools latest

# Accept Android SDK licenses
RUN yes | sdkmanager --licenses || true

# Install Android SDK components
RUN sdkmanager --update \
    && sdkmanager \
        "platform-tools" \
        "platforms;android-${AVD_API_LEVEL}" \
        "system-images;android-${AVD_API_LEVEL};google_apis;${AVD_ABI}" \
        "emulator" \
        "build-tools;${AVD_API_LEVEL}.0.0"

# Create AVD
RUN echo "no" | avdmanager create avd \
    -n ${AVD_NAME} \
    -k "system-images;android-${AVD_API_LEVEL};google_apis;${AVD_ABI}" \
    -d "${AVD_DEVICE}" \
    --force

# Configure AVD for headless mode
RUN mkdir -p /root/.android/avd/${AVD_NAME}.avd \
    && echo "hw.gpu.enabled=yes" >> /root/.android/avd/${AVD_NAME}.avd/config.ini \
    && echo "hw.gpu.mode=swiftshader_indirect" >> /root/.android/avd/${AVD_NAME}.avd/config.ini \
    && echo "hw.ramSize=${DITTO_EMULATOR_MEMORY}" >> /root/.android/avd/${AVD_NAME}.avd/config.ini \
    && echo "hw.keyboard=yes" >> /root/.android/avd/${AVD_NAME}.avd/config.ini \
    && echo "disk.dataPartition.size=4G" >> /root/.android/avd/${AVD_NAME}.avd/config.ini

# Create app directory
WORKDIR /app

# Copy DittoMation source
COPY . /app/

# Install uv for fast package management
RUN pip3 install --no-cache-dir uv

# Install DittoMation and dependencies
RUN uv pip install --system . pyyaml

# Verify installation
RUN python3 -c "from core.cli import main; print('Import successful')"
RUN ditto --version

# Install optional cloud dependencies (commented out by default)
# RUN pip3 install --no-cache-dir boto3 google-cloud-storage

# Create directories for workflows and output
RUN mkdir -p /app/workflows /app/output /app/screenshots

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ADB port
EXPOSE 5555

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD adb devices | grep -q "device$" || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["ditto", "--help"]
