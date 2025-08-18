import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open
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
            assert generator.model == "gpt-4o-mini"
            assert generator.temperature == 0.7
            assert generator.verbose is False
    
    def test_init_with_custom_parameters(self):
        """Test initialization with custom model and temperature."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator(model="gpt-4", temperature=0.5, verbose=True)
            assert generator.model == "gpt-4"
            assert generator.temperature == 0.5
            assert generator.verbose is True
    
    def test_init_with_environment_overrides(self):
        """Test initialization with environment variable overrides."""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "OPENAI_MODEL": "gpt-3.5-turbo",
            "OPENAI_TEMPERATURE": "0.3"
        }):
            generator = DeepcastGenerator()
            assert generator.model == "gpt-3.5-turbo"
            assert generator.temperature == 0.3
    
    def test_load_transcript_file_not_found(self):
        """Test loading transcript from non-existent file."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            with pytest.raises(FileNotFoundError, match="Transcript file not found: non-existent-file.txt"):
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
    
    def test_load_transcript_encoding_error(self):
        """Test loading transcript with encoding issues."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            # Mock open to raise an encoding error
            with patch('builtins.open', mock_open()) as mock_file:
                mock_file.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, 'Invalid byte')
                
                with pytest.raises(Exception, match="Error reading transcript file:"):
                    generator.load_transcript("test.txt")
    
    def test_build_prompt(self):
        """Test prompt building."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            transcript = "Test transcript"
            prompt = generator.build_prompt(transcript)
            
            assert "Test transcript" in prompt
            assert "thematic breakdown" in prompt
            assert "Markdown" in prompt
            assert "Speaker-organized notes" in prompt
            assert "Extracted quotes" in prompt
            assert "executive summary" in prompt
            assert "NOTION COMPATIBILITY" in prompt
    
    def test_build_prompt_with_long_transcript(self):
        """Test prompt building with longer transcript content."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            transcript = "A" * 1000  # Long transcript
            prompt = generator.build_prompt(transcript)
            
            assert len(prompt) > 1000
            assert transcript in prompt
    
    @patch('openai.OpenAI')
    def test_get_deepcast_breakdown_success(self, mock_openai):
        """Test successful API call to OpenAI."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            # Mock the OpenAI response
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices[0].message.content = "Generated deepcast breakdown"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            result = generator.get_deepcast_breakdown("Test prompt")
            
            assert result == "Generated deepcast breakdown"
            mock_client.chat.completions.create.assert_called_once()
    
    @patch('openai.OpenAI')
    def test_get_deepcast_breakdown_api_error(self, mock_openai):
        """Test OpenAI API error handling."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            # Mock the OpenAI client to raise an error
            mock_client = MagicMock()
            mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")
            mock_openai.return_value = mock_client
            
            with pytest.raises(Exception, match="OpenAI API error: API rate limit exceeded"):
                generator.get_deepcast_breakdown("Test prompt")
    
    @patch('openai.OpenAI')
    def test_get_deepcast_breakdown_correct_parameters(self, mock_openai):
        """Test that OpenAI API is called with correct parameters."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator(model="gpt-4", temperature=0.5)
            
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            generator.get_deepcast_breakdown("Test prompt")
            
            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == "gpt-4"
            assert call_args[1]['temperature'] == 0.5
            assert call_args[1]['messages'][0]['role'] == "system"
            assert call_args[1]['messages'][1]['role'] == "user"
            assert call_args[1]['messages'][1]['content'] == "Test prompt"
    
    @patch('deepcast_post.core.Progress')
    @patch('deepcast_post.core.DeepcastGenerator.get_deepcast_breakdown')
    @patch('deepcast_post.core.DeepcastGenerator.load_transcript')
    def test_generate_breakdown_success(self, mock_load, mock_get_breakdown, mock_progress):
        """Test successful breakdown generation workflow."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator(verbose=True)
            
            # Mock dependencies
            mock_load.return_value = "Test transcript content"
            mock_get_breakdown.return_value = "# Generated Breakdown\n\nContent here"
            
            # Mock progress bar
            mock_progress_instance = MagicMock()
            mock_progress.return_value.__enter__.return_value = mock_progress_instance
            mock_progress_instance.add_task.return_value = "task_id"
            
            # Mock file writing
            with patch('builtins.open', mock_open()) as mock_file:
                result = generator.generate_breakdown("input.txt", "output.md")
                
                # Verify transcript was loaded
                mock_load.assert_called_once_with("input.txt")
                
                # Verify breakdown was generated
                mock_get_breakdown.assert_called_once()
                
                # Verify file was written
                mock_file.assert_called_once_with("output.md", "w", encoding="utf-8")
    
    @patch('deepcast_post.core.DeepcastGenerator.load_transcript')
    def test_generate_breakdown_default_output_path(self, mock_load):
        """Test that default output path is generated correctly."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            # Mock transcript loading
            mock_load.return_value = "Test content"
            
            # Mock OpenAI API call
            with patch.object(generator, 'get_deepcast_breakdown', return_value="Generated content"):
                # Mock file writing
                with patch('builtins.open', mock_open()) as mock_file:
                    generator.generate_breakdown("my-transcript.txt")
                    
                    # Should generate default output path
                    expected_path = "my-transcript-deepcast.md"
                    mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
    
    @patch('deepcast_post.core.DeepcastGenerator.load_transcript')
    def test_generate_breakdown_file_write_error(self, mock_load):
        """Test handling of file write errors."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator()
            
            # Mock transcript loading
            mock_load.return_value = "Test content"
            
            # Mock OpenAI API call
            with patch.object(generator, 'get_deepcast_breakdown', return_value="Generated content"):
                # Mock file writing to raise an error
                with patch('builtins.open', mock_open()) as mock_file:
                    mock_file.side_effect = PermissionError("Permission denied")
                    
                    with pytest.raises(Exception, match="Error writing output file: Permission denied"):
                        generator.generate_breakdown("input.txt", "output.md")
    
    def test_generate_breakdown_with_verbose_output(self):
        """Test that verbose mode shows progress messages."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator(verbose=True)
            
            # Mock all dependencies
            with patch.object(generator, 'load_transcript', return_value="Test content"):
                with patch.object(generator, 'get_deepcast_breakdown', return_value="Generated content"):
                    with patch.object(generator.console, 'print') as mock_print:
                        with patch('builtins.open', mock_open()):
                            generator.generate_breakdown("input.txt")
                            
                            # Should print verbose messages
                            assert mock_print.call_count >= 1
    
    def test_generate_breakdown_without_verbose_output(self):
        """Test that non-verbose mode doesn't show progress messages."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            generator = DeepcastGenerator(verbose=False)
            
            # Mock all dependencies
            with patch.object(generator, 'load_transcript', return_value="Test content"):
                with patch.object(generator, 'get_deepcast_breakdown', return_value="Generated content"):
                    with patch.object(generator.console, 'print') as mock_print:
                        with patch('builtins.open', mock_open()):
                            generator.generate_breakdown("input.txt")
                            
                            # In non-verbose mode, we should only see:
                            # 1. Progress bar output (from Rich Progress)
                            # 2. Success panel
                            # The verbose messages (loading transcript, sending to OpenAI) should not appear
                            assert mock_print.call_count == 2  # Progress + success panel
                            
                            # Verify that verbose messages were not printed
                            # Check that no verbose messages appear in the calls
                            for call in mock_print.call_args_list:
                                args = call[0]  # Get the positional arguments
                                if args:  # If there are arguments
                                    message = str(args[0])
                                    # These verbose messages should not appear
                                    assert "📖 Loading transcript from:" not in message
                                    assert "📡 Sending to OpenAI" not in message 