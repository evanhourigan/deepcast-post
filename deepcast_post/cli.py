#!/usr/bin/env python3

import argparse
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from deepcast_post.core import DeepcastGenerator

# Load environment variables from .env file in project directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_dir, '.env')
load_dotenv(env_path)

console = Console()

def show_cost_warning():
    """Display cost information to the user."""
    console.print(Panel(
        "[yellow]💰 Cost Information:[/yellow]\n"
        "• Default model: GPT-4o-mini (~$0.004 per transcript)\n"
        "• GPT-4o: ~$0.11 per transcript\n"
        "• See COST_GUIDE.md for detailed pricing\n"
        "• Set OPENAI_MAX_INPUT_TOKENS to limit costs",
        title="Cost Warning",
        border_style="yellow"
    ))

def main():
    parser = argparse.ArgumentParser(
        prog="deepcast",
        description="Generate Deepcast Breakdown from diarized transcript",
        epilog="Example: deepcast transcript.txt"
    )
    parser.add_argument("transcript_path", help="Path to the diarized transcript file")
    parser.add_argument("--output-path", help="Path for output file (default: {transcript}-deepcast.md)")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model to use (default: gpt-4o-mini)")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation (default: 0.7)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-cost-warning", action="store_true", help="Suppress cost warning")
    
    args = parser.parse_args()
    
    # Show cost warning unless suppressed
    if not args.no_cost_warning:
        show_cost_warning()
    
    # Validate OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print(Panel(
            "[red]Error: OPENAI_API_KEY environment variable not set[/red]\n"
            "Please set your OpenAI API key:\n"
            "export OPENAI_API_KEY='your-api-key-here'",
            title="Configuration Error",
            border_style="red"
        ))
        sys.exit(1)
    
    try:
        generator = DeepcastGenerator(
            model=args.model,
            temperature=args.temperature,
            verbose=args.verbose
        )
        
        generator.generate_breakdown(
            transcript_path=args.transcript_path,
            output_path=args.output_path
        )
        
    except Exception as e:
        console.print(Panel(
            f"[red]Error: {str(e)}[/red]",
            title="Generation Failed",
            border_style="red"
        ))
        sys.exit(1)

if __name__ == "__main__":
    main() 