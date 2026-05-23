# axentx-audio-gain-teams

A Python package that installs a background service to intercept Microsoft Teams
desktop client audio on Windows and keep the audio level within a target RMS
value, even when Teams performs automatic gain control (AGC).

## Windows‑specific setup

1. **Prerequisites**
   - Windows 10 (1809) or later, 64‑bit.
   - Python 3.9 or newer (download from the official installer, ensure *Add to PATH* is checked).
   - Administrative rights (required to install the service).

2. **Install the package**