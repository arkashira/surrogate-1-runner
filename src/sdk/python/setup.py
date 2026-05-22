from setuptools import setup

setup(
    name="axentx-smartgrid-sdk",
    version="0.1.0",
    packages=['smartgrid'],
    install_requires=['paho-mqtt>=1.6.1', 'json'],
)