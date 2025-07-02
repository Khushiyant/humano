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
        if not result['success']:
            print(f"Error: {result.get('error', 'Unknown error')}")
        assert result['success'] is True, f"Humanization failed: {result.get('error', 'Unknown error')}"
        assert 'humanized_content' in result
        assert 'context_detected' in result
        assert 'transformations_applied' in result
        assert len(result['humanized_content']) > 0
        assert result['humanized_content'] != self.sample_text
    
    def test_humanize_strength_levels(self):
        """Test different strength levels."""
        for strength in ["low", "medium", "high"]:
            result = humanize(self.sample_text, strength=strength)
            if not result['success']:
                print(f"Error for strength {strength}: {result.get('error', 'Unknown error')}")
            assert result['success'] is True, f"Humanization failed for strength {strength}: {result.get('error', 'Unknown error')}"
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
    
    def test_humanize_personality_types(self):
        """Test different personality types."""
        personalities = ["balanced", "casual", "confident", "analytical"]
        
        for personality in personalities:
            result = humanize(self.sample_text, strength="medium", personality=personality)
            if not result['success']:
                print(f"Error for personality {personality}: {result.get('error', 'Unknown error')}")
            assert result['success'] is True, f"Humanization failed for personality {personality}"
            assert 'humanized_content' in result
            assert len(result['humanized_content']) > 0
    
    def test_context_detection(self):
        """Test that context detection works."""
        result = humanize(self.sample_text)
        
        assert result['success'] is True
        assert 'context_detected' in result
        context = result['context_detected']
        assert isinstance(context, dict)
        assert 'formality' in context
        assert isinstance(context['formality'], (int, float))
    
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
