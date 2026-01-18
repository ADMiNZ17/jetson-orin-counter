#!/bin/bash

# --- COLORS FOR OUTPUT ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Jetson Orin Nano Dependency Installer ===${NC}"

# --- 1. CHECK PLATFORM ---
if [ -f /etc/nv_tegra_release ]; then
    echo -e "${GREEN}[✔] Jetson Platform Detected.${NC}"
    grep -oP 'R\d+\s+\(release\s+\K\d+\.\d+' /etc/nv_tegra_release | xargs -I {} echo "    L4T Version: {}"
else
    echo -e "${RED}[✘] Error: Not a Jetson device (Tegra release not found).${NC}"
    echo "    This script is intended for Jetson Orin Nano/NX/AGX."
    exit 1
fi

# --- 2. UPDATE PACKAGE LISTS (Only if needed) ---
# We check if apt-get update has been run recently (last 24h) to save time
if [ -z "$(find /var/cache/apt/pkgcache.bin -mtime -1 2>/dev/null)" ]; then
    echo -e "${YELLOW}Updating Apt Cache...${NC}"
    sudo apt-get update
else
    echo -e "${GREEN}[✔] Apt cache is up to date.${NC}"
fi

# --- 3. SYSTEM DEPENDENCIES (APT) ---
DEPENDENCIES=(
    "python3-pip"
    "libopenblas-dev"
    "libopenmpi-dev"
    "libgl1-mesa-glx"
    "libglib2.0-0"
    "git"
)

echo -e "\n${YELLOW}Checking System Libraries...${NC}"
for pkg in "${DEPENDENCIES[@]}"; do
    if dpkg -l | grep -q "^ii  $pkg "; then
        echo -e "    [✔] $pkg is already installed."
    else
        echo -e "    ${YELLOW}[Installing] $pkg...${NC}"
        sudo apt-get install -y $pkg
    fi
done

# --- 4. PYTHON ENVIRONMENT CHECK ---
echo -e "\n${YELLOW}Checking Python Environment...${NC}"

# Function to check pip package
check_pip_install() {
    PACKAGE=$1
    VERSION_REQ=$2 # Optional

    if python3 -m pip show "$PACKAGE" > /dev/null 2>&1; then
        echo -e "    [✔] Python package '$PACKAGE' is installed."
    else
        echo -e "    ${YELLOW}[Installing] $PACKAGE...${NC}"
        python3 -m pip install "$PACKAGE"
    fi
}

# --- 5. CRITICAL: PYTORCH & TORCHVISION ---
# On Jetson, we CANNOT simply 'pip install torch'. It installs the CPU version.
# We must verify the Nvidia GPU version is present.

if python3 -c "import torch; print(torch.cuda.is_available())" | grep -q "True"; then
    echo -e "    [✔] PyTorch with CUDA is detected."
else
    echo -e "${RED}[!] WARNING: PyTorch with CUDA is NOT detected.${NC}"
    echo -e "    Standard 'pip install torch' does not work on Jetson."
    echo -e "    Installing standard version will break GPU acceleration."
    echo -e "    Please follow the Nvidia dusty-nv guide or use the Docker container."
    read -p "    Do you want to continue installing other libs? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# --- 6. INSTALL PROJECT LIBRARIES ---
# We install these one by one to avoid dependency hell
check_pip_install "numpy" "<2" # Ultralytics requires numpy < 2.0
check_pip_install "shapely"
check_pip_install "psutil"
check_pip_install "seaborn"

# Install Ultralytics (YOLO)
# We use --no-deps for torch/torchvision to prevent it from overwriting the Jetson version
if python3 -m pip show "ultralytics" > /dev/null 2>&1; then
    echo -e "    [✔] Ultralytics is already installed."
else
    echo -e "    ${YELLOW}[Installing] Ultralytics (YOLOv8)...${NC}"
    # Critical: Do not upgrade torch automatically
    python3 -m pip install ultralytics 
fi

# Install Supervision (for better drawing/counting)
check_pip_install "supervision"

echo -e "\n${GREEN}=== Installation Complete! ===${NC}"
echo -e "You can now run your project using: ${YELLOW}python3 camera_live.py${NC}"