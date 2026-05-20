"""
Tests for ex11_check_blackholes.py

Run with: pytest tests/test_ex11_check_blackholes.py -v
"""

import sys
import os
import json
import tempfile
import pytest

# Add exercises folder to path so we can import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'exercises'))

from ex11_check_blackholes import Blackhole


# --- Fixtures: reusable test data ---

@pytest.fixture
def sample_routes_with_blackholes():
    """Routes that contain blackholes."""
    return [
        {"RouteTableId": "rtb-111", "Destination": "10.0.0.0/16", "Target": "tgw-abc", "State": "active"},
        {"RouteTableId": "rtb-222", "Destination": "10.99.0.0/16", "Target": "tgw-dead000", "State": "blackhole"},
        {"RouteTableId": "rtb-333", "Destination": "172.16.0.0/16", "Target": "tgw-dead111", "State": "blackhole"},
        {"RouteTableId": "rtb-444", "Destination": "192.168.0.0/16", "Target": "tgw-xyz", "State": "active"},
    ]


@pytest.fixture
def sample_routes_no_blackholes():
    """All routes are active — no blackholes."""
    return [
        {"RouteTableId": "rtb-111", "Destination": "10.0.0.0/16", "Target": "tgw-abc", "State": "active"},
        {"RouteTableId": "rtb-222", "Destination": "172.16.0.0/16", "Target": "tgw-def", "State": "active"},
    ]


@pytest.fixture
def temp_json_file(sample_routes_with_blackholes):
    """Write sample data to a temp JSON file and return the path."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(sample_routes_with_blackholes, f)
    f.close()
    yield f.name
    os.unlink(f.name)  # cleanup after test


@pytest.fixture
def temp_json_no_blackholes(sample_routes_no_blackholes):
    """Temp JSON file with no blackholes."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(sample_routes_no_blackholes, f)
    f.close()
    yield f.name
    os.unlink(f.name)


# --- Tests ---

class TestBlackhole:
    """Test the Blackhole class."""

    def test_finds_blackholes(self, temp_json_file):
        """Should find 2 blackhole routes in sample data."""
        bh = Blackhole()
        result = bh.blackhole(temp_json_file)
        assert len(result) == 2

    def test_blackhole_contains_correct_data(self, temp_json_file):
        """Each result should have the right keys and values."""
        bh = Blackhole()
        result = bh.blackhole(temp_json_file)
        assert result[0]["RouteTableId"] == "rtb-222"
        assert result[0]["Destination"] == "10.99.0.0/16"
        assert result[0]["Target"] == "tgw-dead000"
        assert result[0]["State"] == "blackhole"

    def test_no_blackholes_returns_empty(self, temp_json_no_blackholes):
        """Should return empty list when no blackholes exist."""
        bh = Blackhole()
        result = bh.blackhole(temp_json_no_blackholes)
        assert result == []

    def test_file_not_found(self):
        """Should handle missing file gracefully."""
        bh = Blackhole()
        result = bh.blackhole("nonexistent_file.json")
        assert result is None

    def test_str_with_blackholes(self, temp_json_file):
        """__str__ should format output with BLACKHOLE prefix."""
        bh = Blackhole()
        bh.blackhole(temp_json_file)
        output = str(bh)
        assert "BLACKHOLE:" in output
        assert "rtb-222" in output
        assert "Total number of blackholes: 2" in output

    def test_str_no_blackholes(self, temp_json_no_blackholes):
        """__str__ should show 'not found' message when empty."""
        bh = Blackhole()
        bh.blackhole(temp_json_no_blackholes)
        output = str(bh)
        assert "No blackhole routes found!" in output
