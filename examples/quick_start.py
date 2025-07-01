#!/usr/bin/env python3
"""
Quick start example for Humano package.
"""

import humano

def main():
    # Sample AI-generated text
    ai_text = """
    Furthermore, it is important to note that artificial intelligence has numerous applications 
    in various domains. Additionally, machine learning algorithms can optimize complex processes 
    efficiently. Moreover, the implementation of these technologies facilitates enhanced 
    productivity. In conclusion, AI represents a paradigm shift in computational methodologies.
    """

    print("Original AI-generated text:")
    print(ai_text.strip())
    print("\n" + "="*60 + "\n")

    # Test different strength levels
    for strength in ["low", "medium", "high"]:
        print(f"Humanization Strength: {strength.upper()}")
        print("-" * 30)
        
        result = humano.humanize(ai_text.strip(), strength=strength)
        
        if result['success']:
            print(f"SUCCESS: {result['message']}")
            print(f"Humanized text: {result['humanized_content']}")
        else:
            print(f"ERROR: {result['error']}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
