"""Tests for CLI interface."""

import pytest
from click.testing import CliRunner
from pathlib import Path
import tempfile
import os

from ai_assist.cli import main
from ai_assist.core import AIAssistError


class TestCLI:
    """Test cases for CLI commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_main_help(self):
        """Test main command help output."""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'AI Project Assistant' in result.output
        assert 'init' in result.output
        assert 'preamble' in result.output
        assert 'log-query' in result.output
    
    def test_version(self):
        """Test version command."""
        result = self.runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    def test_init_outside_project_root(self):
        """Test init command fails outside project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to empty directory (no project indicators)
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                result = self.runner.invoke(main, ['init'])
                assert result.exit_code == 1
                assert 'Error:' in result.output
                assert 'project root' in result.output.lower()
            finally:
                os.chdir(original_cwd)
    
    def test_init_in_project_root(self):
        """Test init command succeeds in project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a project indicator file
            (temp_path / "README.md").touch()
            
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                result = self.runner.invoke(main, ['init'])
                assert result.exit_code == 0
                assert 'Project root detected' in result.output
                assert 'AI directory ready' in result.output
                assert 'Initialization complete' in result.output
                
                # Check that AI directory and context file were created
                ai_dir = temp_path / "AI"
                assert ai_dir.exists()
                assert (ai_dir / "AI_CONTEXT.yaml").exists()
            finally:
                os.chdir(original_cwd)
    
    def test_init_force_overwrite(self):
        """Test init command with --force flag."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create project indicator and existing AI structure
            (temp_path / "README.md").touch()
            ai_dir = temp_path / "AI"
            ai_dir.mkdir()
            context_file = ai_dir / "AI_CONTEXT.yaml"
            context_file.write_text("existing content")
            
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Test without --force (should warn)
                result = self.runner.invoke(main, ['init'])
                assert result.exit_code == 0
                assert 'already exists' in result.output
                assert context_file.read_text() == "existing content"
                
                # Test with --force (should overwrite)
                result = self.runner.invoke(main, ['init', '--force'])
                assert result.exit_code == 0
                assert 'Initialization complete' in result.output
                assert context_file.read_text() != "existing content"
            finally:
                os.chdir(original_cwd)
    
    def test_status_command(self):
        """Test status command output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "README.md").touch()
            
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Test status before init
                result = self.runner.invoke(main, ['status'])
                assert result.exit_code == 0
                assert 'AI Project Assistant Status' in result.output
                assert 'AI Directory Exists: No' in result.output
                
                # Test status after init
                self.runner.invoke(main, ['init'])
                result = self.runner.invoke(main, ['status'])
                assert result.exit_code == 0
                assert 'AI Directory Exists: Yes' in result.output
                assert 'AI_CONTEXT.yaml: Yes' in result.output
            finally:
                os.chdir(original_cwd)
    
    def test_preamble_without_init(self):
        """Test preamble command fails without initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "README.md").touch()
            
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                result = self.runner.invoke(main, ['preamble', '--topic', 'api'])
                assert result.exit_code == 1
                assert 'AI directory not found' in result.output
            finally:
                os.chdir(original_cwd)
    
    def test_log_query_without_init(self):
        """Test log-query command fails without initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "README.md").touch()
            
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                result = self.runner.invoke(main, [
                    'log-query', 
                    '--model', 'gpt-4', 
                    '--prompt', 'test prompt'
                ])
                assert result.exit_code == 1
                assert 'AI directory not found' in result.output
            finally:
                os.chdir(original_cwd)
