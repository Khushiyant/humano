# Humano - Advanced AI Text Humanization

A sophisticated Python package for transforming AI-generated text into natural, human-like content using advanced NLP techniques and context-aware processing.

## Features

- **Context-Aware Processing**: Automatically detects and adapts to academic, business, technical, or casual content types
- **Multi-Phase Humanization**: Core transformations → Structural improvements → Advanced techniques
- **Personality Injection**: Choose from casual, confident, analytical, or balanced writing styles
- **Sophisticated Pattern Recognition**: Targets specific AI-generated patterns and phrases
- **Natural Flow Enhancement**: Creates sentence rhythm variation and natural imperfections
- **Smart Contractions**: Context-sensitive application based on formality level
- **Semantic Intelligence**: Uses clustering for intelligent word replacements

## Installation

```bash
pip install humano
```

## Quick Start

### Python API

```python
import humano

# Basic usage
result = humano.humanize("Your AI-generated text here", strength="medium")
print(result['humanized_content'])

# Advanced usage with personality
result = humano.humanize(
    "Your AI-generated text here", 
    strength="high",
    personality="casual"
)

# Check detailed results
if result['success']:
    print(f"Humanized: {result['humanized_content']}")
    print(f"Context detected: {result['context_detected']}")
    print(f"Transformations applied: {result['transformations_applied']}")
else:
    print(f"Error: {result['error']}")
```

### Command Line

```bash
# Basic usage
humano "Your AI-generated text here"

# Advanced options
humano "Your text" --strength high --personality confident

# From file with custom settings
humano input.txt -o output.txt --strength medium --personality analytical
```

## API Reference

### `humanize(content, strength="medium", personality="balanced")`

**Parameters:**
- `content` (str): Text to humanize (minimum 20 characters)
- `strength` (str): Humanization intensity
  - `"low"`: Core transformations only (pattern removal, word replacement, contractions)
  - `"medium"`: + Sentence restructuring, personality injection, flow enhancement
  - `"high"`: + Semantic enhancement, advanced burstiness, natural imperfections
- `personality` (str): Writing style to inject
  - `"balanced"`: Mix of all personality types (default)
  - `"casual"`: Informal, conversational tone
  - `"confident"`: Assertive, direct communication
  - `"analytical"`: Thoughtful, measured approach

**Returns:**
```python
{
    "success": bool,
    "humanized_content": str,      # If successful
    "context_detected": dict,      # Content analysis results
    "transformations_applied": int,# Number of changes made
    "message": str,               # Status message
    "error": str                  # If failed
}
```

## How It Works

### 1. Context Analysis
Humano analyzes your text to detect:
- **Content Type**: Academic, business, technical, or general
- **Formality Level**: Determines transformation intensity
- **Writing Patterns**: Identifies AI-generated structures

### 2. Multi-Phase Processing

#### Phase 1: Core Transformations (All Levels)
- **Pattern Removal**: Targets AI phrases like "Furthermore," "In conclusion"
- **Contextual Word Replacement**: Swaps formal terms for natural alternatives
- **Smart Contractions**: Applies contractions based on context formality

#### Phase 2: Structural Improvements (Medium+)
- **Sentence Restructuring**: Transforms rigid sentence patterns
- **Personality Injection**: Adds human-like communication styles
- **Flow Enhancement**: Creates natural rhythm and connectivity

#### Phase 3: Advanced Techniques (High Only)
- **Semantic Enhancement**: Intelligent phrase replacements
- **Burstiness Control**: Varies sentence lengths naturally
- **Natural Imperfections**: Adds subtle human-like hesitations
- **Contextual Emphasis**: Strategic word emphasis

## Troubleshooting

### Common Issues

- **Minimum Text Length**: Text must be at least 20 characters
- **Memory Usage**: Large texts may require more memory for processing
- **Randomization**: Results may vary slightly between runs due to probabilistic transformations

## Examples

### Academic Text Transformation

**Input:**
```
Furthermore, it is important to note that the methodology utilized in this research demonstrates significant advantages. The implementation of these techniques facilitates comprehensive analysis and subsequently yields substantial improvements in overall performance metrics.
```

**Output (High Strength, Casual Personality):**
```
Plus, here's the thing - the method we used in this research shows some real benefits. Using these techniques helps us do thorough analysis and ends up giving us major improvements in how well everything performs.
```

### Business Content Humanization

**Input:**
```
We must leverage our core competencies to optimize synergies and streamline operational paradigms. This strategic approach will facilitate scalable solutions and maximize actionable insights across all stakeholder touchpoints.
```

**Output (Medium Strength, Confident Personality):**
```
Look, we need to use our strengths to improve how different parts work together and simplify our operations. This approach will help us create flexible solutions and get the most useful insights for everyone involved.
```

## License

MIT License - see LICENSE file for details.
