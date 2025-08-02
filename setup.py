#!/usr/bin/env python3
"""
Simple setup script for MultiProdigy
"""

from setuptools import setup, find_packages

setup(
    name="MultiProdigy",
    version="0.1.0",
    description="Modular, schema-driven, multi-agent framework with observability",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0",
        "flask>=2.0.0",
        "prometheus-client>=0.14.0",
    ],
    extras_require={
        "full": [
            "redis>=4.5.0",
            "fastapi>=0.95.0",
            "uvicorn>=0.21.0",
            "python-multipart>=0.0.6",
            "structlog>=23.1.0",
            "pyyaml>=6.0",
            "python-dotenv>=1.0.0",
        ],
        "dev": [
            "pytest>=7.3.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.3.0",
            "mypy>=1.3.0",
            "isort>=5.12.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "multiprodigy-demo=demo.observability_demo:main",
        ],
    },
)