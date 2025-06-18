"""Tests for core utilities."""

import pytest
from pathlib import Path
import tempfile
import os

from ai_assist.core import (
    validate_project_root,
    get_ai_directory_path,
    ensure_ai_directory,
    is_ai_directory_initialized,
    get_project_name,
    ProjectRootError,
    AIDirectoryError
)


class TestProjectRootValidation:
    """Test cases for project root validation."""
    
    def test_validate_empty_directory(self):
        """Test validation fails in empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ProjectRootError) as exc_info:
                validate_project_root(temp_dir)
            assert "project root" in str(exc_info.value).lower()
    
    def test_validate_with_git(self):
        """Test validation succeeds with .git directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / ".git").mkdir()
            
            result = validate_project_root(temp_dir)
            assert result == temp_path.resolve()
    
    def test_validate_with_readme(self):
        """Test validation succeeds with README.md."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "README.md").touch()
            
            result = validate_project_root(temp_dir)
            assert result == temp_path.resolve()
    
    def test_validate_with_setup_py(self):
        """Test validation succeeds with setup.py."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "setup.py").touch()
            
            result = validate_project_root(temp_dir)
            assert result == temp_path.resolve()
    
    def test_validate_current_directory(self):
        """Test validation with current directory."""
        # Assuming tests are run from project root with project indicators
        original_cwd = os.getcwd()
        try:
            # This should succeed if run from project root
            result = validate_project_root()
            assert isinstance(result, Path)
        except ProjectRootError:
            # If it fails, create a temporary project-like directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                (temp_path / "README.md").touch()
                os.chdir(temp_dir)
                
                result = validate_project_root()
                assert result == temp_path.resolve()
        finally:
            os.chdir(original_cwd)


class TestAIDirectory:
    """Test cases for AI directory operations."""
    
    def test_get_ai_directory_path(self):
        """Test getting AI directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            ai_dir = get_ai_directory_path(temp_path)
            
            assert ai_dir == temp_path / "AI"
            assert not ai_dir.exists()  # Should not exist yet
    
    def test_ensure_ai_directory_creates(self):
        """Test ensuring AI directory creates it."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            ai_dir = ensure_ai_directory(temp_path)
            assert ai_dir.exists()
            assert ai_dir.is_dir()
            assert ai_dir == temp_path / "AI"
    
    def test_ensure_ai_directory_exists(self):
        """Test ensuring AI directory when it already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            ai_dir = temp_path / "AI"
            ai_dir.mkdir()
            
            result = ensure_ai_directory(temp_path)
            assert result == ai_dir
            assert ai_dir.exists()
    
    def test_is_ai_directory_initialized(self):
        """Test checking if AI directory is initialized."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Not initialized
            assert not is_ai_directory_initialized(temp_path)
            
            # Create AI directory but no context file
            ai_dir = temp_path / "AI"
            ai_dir.mkdir()
            assert not is_ai_directory_initialized(temp_path)
            
            # Create context file
            (ai_dir / "AI_CONTEXT.yaml").touch()
            assert is_ai_directory_initialized(temp_path)
    
    def test_get_project_name(self):
        """Test getting project name from directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_name = get_project_name(temp_path)
            
            assert project_name == temp_path.name