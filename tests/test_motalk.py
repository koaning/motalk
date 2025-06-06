"""Tests for motalk package"""

import motalk


def test_version():
    """Test that the package has a version"""
    assert hasattr(motalk, "__version__")
    assert isinstance(motalk.__version__, str)