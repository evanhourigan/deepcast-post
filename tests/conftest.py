import pytest
import tempfile
import os
from unittest.mock import patch


@pytest.fixture
def sample_transcript():
    """Sample transcript content for testing."""
    return """[00:00:00] Speaker A: Welcome to the podcast everyone.
[00:00:05] Speaker B: Thanks for having us.
[00:00:10] Speaker A: Today we're discussing AI and its impact on society.
[00:00:15] Speaker B: It's a fascinating topic that affects us all.
[00:00:20] Speaker A: Let's dive into the main themes."""


@pytest.fixture
def sample_transcript_file(sample_transcript):
    """Create a temporary transcript file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_transcript)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    try:
        os.unlink(temp_file)
    except OSError:
        pass


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock_client:
        mock_response = mock_client.return_value.chat.completions.create.return_value
        mock_response.choices[0].message.content = "Generated deepcast breakdown content"
        yield mock_client


@pytest.fixture
def mock_environment():
    """Mock environment variables for testing."""
    env_vars = {
        "OPENAI_API_KEY": "test-api-key-12345",
        "OPENAI_MODEL": "gpt-4o-mini",
        "OPENAI_TEMPERATURE": "0.7"
    }
    
    with patch.dict(os.environ, env_vars, clear=True):
        yield env_vars


@pytest.fixture
def sample_deepcast_output():
    """Sample deepcast output for testing."""
    return """# Deepcast Breakdown

## Main Themes

- **AI Ethics:** Discussion of responsible AI development
- **Societal Impact:** How AI affects different communities
- **Future Outlook:** Predictions for AI advancement

## Speaker Notes

**Speaker A:** Host with technical background, leads discussion
**Speaker B:** Guest expert, provides industry insights

## Key Quotes

- "AI affects us all" [00:00:15]
- "Fascinating topic" [00:00:15]

## Executive Summary

- AI ethics crucial for responsible development
- Societal impact requires careful consideration
- Future outlook shows rapid advancement
- Need for balanced approach to AI integration"""


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    try:
        import shutil
        shutil.rmtree(temp_dir)
    except OSError:
        pass
