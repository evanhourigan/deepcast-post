import openai
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

class DeepcastGenerator:
    """Generates deepcast breakdowns from diarized transcripts using OpenAI API."""
    
    def __init__(self, model=None, temperature=None, verbose=False):
        self.console = Console()
        
        # Load configuration from environment variables with defaults
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature or float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.verbose = verbose
        
        # Set OpenAI API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
    
    def load_transcript(self, transcript_path):
        """Load transcript from file."""
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Transcript file not found: {transcript_path}")
        except Exception as e:
            raise Exception(f"Error reading transcript file: {str(e)}")
    
    def build_prompt(self, transcript):
        """Build the prompt for OpenAI API."""
        return f"""
This is the diarized transcript of a podcast episode. I want a deep, structured breakdown that goes far beyond a summary. Your output should include:

1. A full thematic breakdown of the episode's main ideas and arguments, organized by topic or theme.  
2. Timestamped key takeaways for each major point.  
3. Speaker-organized notes — identify each speaker and summarize their contributions, perspective, and tone.  
4. Extracted quotes — especially insightful or memorable lines with timestamps.  

Please format the output in **Markdown**, using:
- `##` for section headings  
- `**Speaker Name:**` for speaker notes  
- Bulleted lists with consistent formatting
- Timestamps in `[mm:ss]` or `[hh:mm:ss]` format where appropriate

**CRITICAL FORMATTING RULES FOR NOTION COMPATIBILITY:**
- Use `- **Label:** Text` format for bullet points with labels
- Do NOT use inline bullet points like `**Label:** * Text * More text`
- Keep bullet points simple: one label per bullet, one description per bullet
- Use proper markdown: `**bold**` for emphasis, `- ` for lists
- Ensure all markdown syntax is properly closed and escaped
- Use consistent spacing and formatting throughout

End with a 5–7 bullet executive summary suitable for a slide or internal briefing.

Here is the diarized transcript:
{transcript}
"""
    
    def get_deepcast_breakdown(self, prompt):
        """Generate deepcast breakdown using OpenAI API."""
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior podcast analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_breakdown(self, transcript_path, output_path=None):
        """Generate deepcast breakdown from transcript."""
        # Determine output path
        if output_path is None:
            base = os.path.splitext(os.path.basename(transcript_path))[0]
            output_path = f"{base}-deepcast.md"
        
        # Load transcript
        if self.verbose:
            self.console.print(f"📖 Loading transcript from: {transcript_path}")
        transcript = self.load_transcript(transcript_path)
        
        # Generate breakdown
        if self.verbose:
            self.console.print(f"📡 Sending to OpenAI (Deepcast Breakdown)...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("Generating deepcast breakdown...", total=None)
            
            prompt = self.build_prompt(transcript)
            markdown = self.get_deepcast_breakdown(prompt)
        
        # Save output
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown)
        except Exception as e:
            raise Exception(f"Error writing output file: {str(e)}")
        
        # Success message
        self.console.print(Panel(
            f"[green]✅ Deepcast Markdown saved to: {output_path}[/green]",
            title="Success",
            border_style="green"
        )) 