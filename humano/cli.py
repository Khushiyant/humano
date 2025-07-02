#!/usr/bin/env python3
"""
Command-line interface for Humano text humanization.
"""

import argparse
import sys
import os
from typing import Optional

from .main import HumanizerService


def read_input(input_source: Optional[str] = None) -> str:
    """Read input from file, stdin, or direct argument."""
    if input_source:
        if os.path.isfile(input_source):
            # Read from file
            with open(input_source, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Treat as direct text input
            return input_source
    else:
        # Read from stdin
        return sys.stdin.read()


def write_output(content: str, output_file: Optional[str] = None) -> None:
    """Write output to file or stdout."""
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Output written to: {output_file}")
    else:
        print(content)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Humanize AI-generated text using research-proven techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  humano "Your AI-generated text here"
  humano "Text" --strength high --personality confident
  humano input.txt -o output.txt --personality casual
  echo "Text to humanize" | humano --strength medium
  humano -i input.txt --strength high --personality analytical
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input text or file path. If not provided, reads from stdin.'
    )
    
    parser.add_argument(
        '-i', '--input-file',
        help='Input file path (alternative to positional argument)'
    )
    
    parser.add_argument(
        '-o', '--output-file',
        help='Output file path. If not provided, writes to stdout.'
    )
    
    parser.add_argument(
        '-s', '--strength',
        choices=['low', 'medium', 'high'],
        default='medium',
        help='Humanization strength level (default: medium)'
    )
    
    parser.add_argument(
        '-p', '--personality',
        choices=['balanced', 'casual', 'confident', 'analytical'],
        default='balanced',
        help='Writing personality to inject (default: balanced)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Humano 0.1.0'
    )
    
    parser.add_argument(
        '--check-status',
        action='store_true',
        help='Check if the humanizer service is available'
    )
    
    args = parser.parse_args()
    
    # Initialize service
    service = HumanizerService()
    
    # Check status if requested
    if args.check_status:
        status = service.check_api_status()
        if status['success']:
            print("Service available")
        else:
            print("Service not available")
        return
    
    # Determine input source
    input_source = args.input_file or args.input
    
    try:
        # Read input
        content = read_input(input_source)
        
        if not content.strip():
            print("Error: No input content provided", file=sys.stderr)
            sys.exit(1)
        
        # Humanize content
        result = service.humanize_content(content.strip(), args.strength, args.personality)
        
        if result['success']:
            # Write output
            write_output(result['humanized_content'], args.output_file)
            
            # Show additional info if verbose
            if args.output_file is None:  # Only show extra info when outputting to stdout
                print(f"\n[Transformations: {result.get('transformations_applied', 0)}, "
                      f"Context: {result.get('context_detected', {}).get('formality', 0):.2f} formality]", 
                      file=sys.stderr)
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
