#!/bin/bash
set -e

# =============================================================================
# KiCAD FreeRouter Plugin Installation Script
# =============================================================================
# This script installs the KiCAD FreeRouter plugin on Linux and Windows (MSYS2/Cygwin).
# It handles dependency installation, OS detection, and proper plugin placement.
# =============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# OS Detection
# =============================================================================
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || \
         [[ -n "$MSYSTEM" && ("$MSYSTEM" == "MINGW64" || "$MSYSTEM" == "MINGW32" || "$MSYSTEM" == "MSYS") ]]; then
        echo "windows"
    else
        echo "unsupported"
    fi
}

# =============================================================================
# Dependency Installation
# =============================================================================
install_dependencies_linux() {
    log_info "Installing dependencies for Linux..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip git
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip git
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python python-pip git
    else
        log_warn "No supported package manager found. Please install python3, pip, and git manually."
    fi
    
    # Install kicad-freerouter Python package if available
    if pip3 show kicad-freerouter &> /dev/null; then
        log_info "kicad-freerouter package already installed"
    else
        pip3 install --user kicad-freerouter || log_warn "pip package installation failed, continuing with manual installation"
    fi
}

install_dependencies_windows() {
    log_info "Installing dependencies for Windows (MSYS2/MinGW)..."
    
    # Check for Chocolatey
    if command -v choco &> /dev/null; then
        choco install -y python git
    else
        log_warn "Chocolatey not found. Please install Python and Git manually."
    fi
    
    # Install kicad-freerouter Python package
    pip install kicad-freerouter || log_warn "pip package installation failed, continuing with manual installation"
}

# =============================================================================
# Plugin Installation
# =============================================================================
install_plugin_linux() {
    local kicad_version="${1:-7}"
    local plugin_dir="$HOME/.local/share/kicad/${kicad_version}/plugins"
    
    log_info "Installing plugin to: $plugin_dir"
    mkdir -p "$plugin_dir"
    
    if [ -d "./kicad_freerouter_plugin" ]; then
        cp -r ./kicad_freerouter_plugin/* "$plugin_dir/"
        log_info "Plugin files copied successfully"
    elif [ -d "./freerouter" ]; then
        cp -r ./freerouter "$plugin_dir/"
        log_info "Freerouter directory copied successfully"
    else
        log_error "Plugin directory not found. Expected ./kicad_freerouter_plugin or ./freerouter"
        return 1
    fi
}

install_plugin_windows() {
    local kicad_version="${1:-7}"
    local plugin_dir="$USERPROFILE/AppData/Roaming/KiCad/${kicad_version}/plugins"
    
    log_info "Installing plugin to: $plugin_dir"
    mkdir -p "$plugin_dir"
    
    if [ -d "./kicad_freerouter_plugin" ]; then
        cp -r ./kicad_freerouter_plugin/* "$plugin_dir/"
        log_info "Plugin files copied successfully"
    elif [ -d "./freerouter" ]; then
        cp -r ./freerouter "$plugin_dir/"
        log_info "Freerouter directory copied successfully"
    else
        log_error "Plugin directory not found. Expected ./kicad_freerouter_plugin or ./freerouter"
        return 1
    fi
}

# =============================================================================
# Main Execution
# =============================================================================
main() {
    local os_type
    os_type=$(detect_os)
    
    log_info "Detected OS: $os_type"
    
    case "$os_type" in
        linux)
            install_dependencies_linux
            install_plugin_linux "$@"
            ;;
        windows)
            install_dependencies_windows
            install_plugin_windows "$@"
            ;;
        macos)
            log_warn "macOS support is experimental"
            install_dependencies_linux  # Similar to Linux
            install_plugin_linux "$@"
            ;;
        *)
            log_error "Unsupported operating system: $OSTYPE"
            exit 1
            ;;
    esac
    
    log_info "Installation completed!"
    log_info "Please restart KiCAD to see the plugin in the Tools menu."
}

# Run main with all arguments
main "$@"