"""
Test suite for Humano package.
"""

import pytest
from humano import humanize


class TestHumanizeFunction:
    """Test cases for the main humanize function."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_text = (
            "Furthermore, it is important to note that artificial intelligence "
            "has numerous applications in various domains. Additionally, machine "
            "learning algorithms can optimize complex processes efficiently."
        )
    
    def test_humanize_basic(self):
        """Test basic humanization functionality."""
        result = humanize(self.sample_text)
        
        assert 'success' in result
        assert result['success'] is True
        assert 'humanized_content' in result
        assert len(result['humanized_content']) > 0
        assert result['humanized_content'] != self.sample_text
    
    def test_humanize_strength_levels(self):
        """Test different strength levels."""
        for strength in ["low", "medium", "high"]:
            result = humanize(self.sample_text, strength=strength)
            assert result['success'] is True
            assert 'humanized_content' in result
            assert 'message' in result
            assert len(result['humanized_content']) > 0
    
    def test_humanize_short_text_error(self):
        """Test that short text returns error."""
        short_text = "Too short."
        result = humanize(short_text, "medium")
        
        assert result['success'] is False
        assert 'error' in result
        assert "too short" in result['error'].lower()
    
    def test_humanize_empty_text_error(self):
        """Test that empty text returns error."""
        result = humanize("", "medium")
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_humanize_invalid_strength(self):
        """Test that invalid strength level is handled gracefully."""
        result = humanize(self.sample_text, "invalid")
        # Should either work with default or return error
        assert 'success' in result


if __name__ == "__main__":
    pytest.main([__file__])
