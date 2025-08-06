import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from deepcast_post.core import DeepcastGenerator


class TestDeepcastGenerator:
    def test_init_without_api_key(self):
        """Test initialization without OpenAI API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable not set"):
                DeepcastGenerator()
    
    def test_init_with_api_key(self):
        """Test initialization with OpenAI API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            assert generator.model == "gpt-4"
            assert generator.temperature == 0.7
            assert generator.verbose is False
    
    def test_load_transcript_file_not_found(self):
        """Test loading transcript from non-existent file."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            with pytest.raises(FileNotFoundError):
                generator.load_transcript("non-existent-file.txt")
    
    def test_load_transcript_success(self):
        """Test loading transcript from existing file."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("Test transcript content")
                temp_file = f.name
            
            try:
                content = generator.load_transcript(temp_file)
                assert content == "Test transcript content"
            finally:
                os.unlink(temp_file)
    
    def test_build_prompt(self):
        """Test prompt building."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            transcript = "Test transcript"
            prompt = generator.build_prompt(transcript)
            
            assert "Test transcript" in prompt
            assert "thematic breakdown" in prompt
            assert "Markdown" in prompt 