import pytest
import os
import tempfile
from unittest.mock import patch, mock_open
from deepcast_post.core import DeepcastGenerator


class TestIntegration:
    """Integration tests for the complete deepcast generation workflow."""
    
    @pytest.mark.integration
    def test_full_workflow_success(self, sample_transcript_file, mock_environment, temp_output_dir):
        """Test the complete workflow from transcript to output file."""
        output_path = os.path.join(temp_output_dir, "output-deepcast.md")
        
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI response
            mock_client = mock_openai.return_value
            mock_response = mock_client.chat.completions.create.return_value
            mock_response.choices[0].message.content = "# Generated Deepcast\n\nContent here"
            
            # Run the full workflow
            generator = DeepcastGenerator(verbose=False)
            generator.generate_breakdown(sample_transcript_file, output_path)
            
            # Verify OpenAI was called
            mock_client.chat.completions.create.assert_called_once()
            
            # Verify output file was created
            assert os.path.exists(output_path)
            
            # Verify file content
            with open(output_path, 'r') as f:
                content = f.read()
                assert "# Generated Deepcast" in content
    
    @pytest.mark.integration
    def test_full_workflow_with_default_output_path(self, sample_transcript_file, mock_environment):
        """Test workflow with automatic output path generation."""
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI response
            mock_client = mock_openai.return_value
            mock_response = mock_client.chat.completions.create.return_value
            mock_response.choices[0].message.content = "# Generated Deepcast\n\nContent here"
            
            # Run workflow without specifying output path
            generator = DeepcastGenerator(verbose=False)
            generator.generate_breakdown(sample_transcript_file)
            
            # Verify default output file was created
            # The filename is based on the actual temp file name, not "sample_transcript"
            base_name = os.path.splitext(os.path.basename(sample_transcript_file))[0]
            expected_output = f"{base_name}-deepcast.md"
            assert os.path.exists(expected_output)
            
            # Cleanup
            try:
                os.unlink(expected_output)
            except OSError:
                pass
    
    @pytest.mark.integration
    def test_workflow_with_verbose_output(self, sample_transcript_file, mock_environment):
        """Test workflow with verbose output enabled."""
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI response
            mock_client = mock_openai.return_value
            mock_response = mock_client.chat.completions.create.return_value
            mock_response.choices[0].message.content = "# Generated Deepcast\n\nContent here"
            
            # Create generator and mock its console
            generator = DeepcastGenerator(verbose=True)
            with patch.object(generator.console, 'print') as mock_console:
                generator.generate_breakdown(sample_transcript_file, "verbose-output.md")
                
                # Verify verbose messages were printed
                assert mock_console.call_count >= 2  # Loading + success messages
    
    @pytest.mark.integration
    def test_workflow_with_custom_model_and_temperature(self, sample_transcript_file, mock_environment):
        """Test workflow with custom model and temperature settings."""
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI response
            mock_client = mock_openai.return_value
            mock_response = mock_client.chat.completions.create.return_value
            mock_response.choices[0].message.content = "# Generated Deepcast\n\nContent here"
            
            # Run workflow with custom parameters
            generator = DeepcastGenerator(model="gpt-4", temperature=0.3, verbose=False)
            generator.generate_breakdown(sample_transcript_file, "custom-output.md")
            
            # Verify OpenAI was called with custom parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == "gpt-4"
            assert call_args[1]['temperature'] == 0.3
    
    @pytest.mark.integration
    def test_workflow_error_handling(self, sample_transcript_file, mock_environment):
        """Test workflow error handling when OpenAI API fails."""
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI to raise an error
            mock_client = mock_openai.return_value
            mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")
            
            # Run workflow and expect error
            generator = DeepcastGenerator(verbose=False)
            
            with pytest.raises(Exception, match="OpenAI API error: API rate limit exceeded"):
                generator.generate_breakdown(sample_transcript_file, "error-output.md")
    
    @pytest.mark.integration
    def test_workflow_with_large_transcript(self, mock_environment, temp_output_dir):
        """Test workflow with a large transcript file."""
        # Create a large transcript
        large_transcript = "Speaker A: " + "This is a test sentence. " * 1000
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(large_transcript)
            large_file = f.name
        
        try:
            output_path = os.path.join(temp_output_dir, "large-output-deepcast.md")
            
            with patch('openai.OpenAI') as mock_openai:
                # Mock OpenAI response
                mock_client = mock_openai.return_value
                mock_response = mock_client.chat.completions.create.return_value
                mock_response.choices[0].message.content = "# Large Transcript Breakdown\n\nContent here"
                
                # Run workflow with large transcript
                generator = DeepcastGenerator(verbose=False)
                generator.generate_breakdown(large_file, output_path)
                
                # Verify OpenAI was called with large prompt
                call_args = mock_client.chat.completions.create.call_args
                prompt = call_args[1]['messages'][1]['content']
                assert len(prompt) > 10000  # Large prompt
                assert large_transcript in prompt
                
                # Verify output file was created
                assert os.path.exists(output_path)
        
        finally:
            # Cleanup
            try:
                os.unlink(large_file)
            except OSError:
                pass
    
    @pytest.mark.integration
    def test_workflow_output_format_validation(self, sample_transcript_file, mock_environment, temp_output_dir):
        """Test that the output format matches expected structure."""
        output_path = os.path.join(temp_output_dir, "format-test-deepcast.md")
        
        with patch('openai.OpenAI') as mock_openai:
            # Mock OpenAI response with structured content
            mock_client = mock_openai.return_value
            mock_response = mock_client.chat.completions.create.return_value
            mock_response.choices[0].message.content = """# Deepcast Breakdown

## Main Themes
- **Theme 1:** Description
- **Theme 2:** Description

## Speaker Notes
**Speaker A:** Description
**Speaker B:** Description

## Executive Summary
- Point 1
- Point 2"""
            
            # Run workflow
            generator = DeepcastGenerator(verbose=False)
            generator.generate_breakdown(sample_transcript_file, output_path)
            
            # Verify output file structure
            with open(output_path, 'r') as f:
                content = f.read()
                
                # Check for expected sections
                assert "## Main Themes" in content
                assert "## Speaker Notes" in content
                assert "## Executive Summary" in content
                
                # Check for proper markdown formatting
                assert "**Speaker A:**" in content
                assert "- **Theme 1:**" in content
                assert "- Point 1" in content
