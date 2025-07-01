# Humano - AI Text Humanization

A Python package for humanizing AI-generated text using research-proven techniques.

## Features

- **Research-Based**: Implements DIPPER, HMGC, and ADAT techniques
- **Multiple Strength Levels**: Low, medium, or high humanization intensity
- **Easy Integration**: Simple API and command-line interface

## Installation

```bash
pip install humano
```

## Quick Start

### Python API

```python
import humano

result = humano.humanize("Your AI-generated text here", strength="medium")
print(result['humanized_content'])
```

### Command Line

```bash
# Direct text input
humano "Your AI-generated text here"

# From file
humano input.txt -o output.txt --strength high
```

## API Reference

### `humanize(content, strength="medium")`

**Parameters:**
- `content` (str): Text to humanize (minimum 50 characters)
- `strength` (str): Humanization level ("low", "medium", "high")

**Returns:**
```python
{
    "success": bool,
    "humanized_content": str,  # If successful
    "error": str,             # If failed
    "message": str            # Status message
}
```

## License

MIT License - see LICENSE file for details.
