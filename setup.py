#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script for the qBittorrent client package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="qbittorrent-client",
    version="0.1.0",
    author="Tushar Sudake",
    author_email="etushar89@gmail.com",
    description="A Python client for the qBittorrent Web API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/etushar89/qbittorrent-client",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "qbt=qbittorrent_client.cli:main",
        ],
    },
)
