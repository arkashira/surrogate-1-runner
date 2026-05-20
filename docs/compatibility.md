#!/bin/bash
# /opt/axentx/surrogate-1/scripts/check-compatibility.sh
# Runtime compatibility checker and fixer for surrogate-1

set -e

echo "=== Surrogate-1 Compatibility Checker ==="
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Error: Cannot detect Linux distribution"
    exit 1
fi

echo "Detected distribution: $DISTRO"
echo ""

case "$DISTRO" in
    ubuntu)
        echo "Applying Ubuntu compatibility fixes..."
        
        # Fix libssl dependency
        echo "[*] Checking libssl..."
        if ! dpkg -l | grep -q libssl1.1; then
            echo "[+] Installing libssl1.1..."
            sudo apt-get update -qq
            sudo apt-get install -y libssl1.1 || \
            sudo apt-get install -y libssl3 || true
        fi
        
        # Fix Python venv
        echo "[*] Checking Python venv support..."
        sudo apt-get install -y python3-venv python3-pip
        
        # Upgrade pip
        echo "[+] Upgrading pip..."
        pip3 install --upgrade pip --break-system-packages 2>/dev/null || \
        pip3 install --upgrade pip || true
        ;;
        
    fedora)
        echo "Applying Fedora compatibility fixes..."
        
        # Fix missing gcc-c++
        echo "[*] Checking gcc-c++..."
        if ! rpm -q gcc-c++ &>/dev/null; then
            echo "[+] Installing gcc-c++..."
            sudo dnf install -y gcc-c++
        fi
        
        # Install Python development tools
        sudo dnf install -y python3-pip python3-venv
        ;;
        
    debian)
        echo "Applying Debian compatibility fixes..."
        
        # Fix outdated pip
        echo "[*] Checking pip..."
        sudo apt-get update -qq
        sudo apt-get install -y python3-pip
        pip3 install --upgrade pip --break-system-packages 2>/dev/null || \
        pip3 install --upgrade pip || true
        ;;
        
    *)
        echo "Warning: Unsupported distribution: $DISTRO"
        echo "Supported: ubuntu, fedora, debian"
        exit 1
        ;;
esac

echo ""
echo "=== Compatibility check complete ==="
echo ""
echo "To install surrogate-1, run:"
echo "  git clone https://github.com/axentx/surrogate-1.git"
echo "  cd surrogate-1"
echo "  ./install.sh"