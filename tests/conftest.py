"""
Pytest configuration for jane-website tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def docs_dir(project_root: Path) -> Path:
    """Return the documentation directory."""
    return project_root / "fashion-website-docs"
