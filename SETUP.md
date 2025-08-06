# Quick Setup Guide

## Environment Setup

Your `deepcast_post` project is now configured with the same environment management as your `diarized_transcriber` project:

### 1. Environment Variables

The project uses a `.env` file for configuration. Edit the `.env` file to add your OpenAI API key:

```bash
# Edit the .env file
nano .env
```

Replace `your-api-key-here` with your actual OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. Virtual Environment

The project uses:

- **direnv** for automatic environment loading
- **Poetry** for dependency management (optional)
- **pip** for dependency installation (fallback)

### 3. Dependencies

Dependencies are already installed. If you need to reinstall:

```bash
# Using pip (current setup)
python3 -m pip install python-dotenv openai rich

# Or using Poetry (if you prefer)
poetry install
```

## Usage

Once your API key is set in `.env`, you can use the tool:

```bash
# Basic usage
deepcast transcript.txt

# With custom output
deepcast transcript.txt --output-path breakdown.md

# With verbose output
deepcast transcript.txt --verbose
```

## Environment Configuration

The tool supports these environment variables in `.env`:

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `OPENAI_MODEL` (optional): Model to use (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE` (optional): Temperature for generation (default: 0.7)

## Workflow Integration

```bash
# Step 1: Transcribe and diarize
transcribe audio.wav --formats txt

# Step 2: Generate deepcast breakdown
deepcast audio-transcript.txt

# Step 3: Import to Notion (future tool)
# notion-import audio-deepcast.md
```
