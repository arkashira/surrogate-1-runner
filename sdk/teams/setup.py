import pathlib
from setuptools import setup, find_packages

# Read the long description from README.md
this_directory = pathlib.Path(__file__).parent
readme_path = this_directory / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="axentx-audio-gain-teams",
    version="0.1.0",
    description="Hooks into Microsoft Teams desktop client audio to deliver gain‑stable stream on Windows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Axentx Team",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "axentx-audio-gain-teams=axentx_audio_gain_teams.service:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)