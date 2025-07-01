"""
Humano - AI Text Humanization Package

A Python package for humanizing AI-generated or robotic text using research-proven techniques
including DIPPER paraphrasing, HMGC framework, and ADAT adversarial methods.
"""

__version__ = "0.1.0"
__author__ = "Khushiyant"
__email__ = "khushiyant2002@gmail.com"

# Public API - only expose the convenience function
__all__ = ["humanize"]

# Convenience function for quick access
def humanize(content: str, strength: str = "medium") -> dict:
    """
    Convenience function to humanize text content.
    
    Args:
        content (str): The text content to humanize
        strength (str): Humanization strength ("low", "medium", "high")
        
    Returns:
        dict: Result with success status and humanized content
    """
    from .main import HumanizerService
    service = HumanizerService()
    return service.humanize_content(content, strength)