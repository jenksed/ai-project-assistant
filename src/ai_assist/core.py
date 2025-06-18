"""Core utilities and validation for AI Project Assistant."""

import os
from pathlib import Path
from typing import Optional, Union


class AIAssistError(Exception):
    """Base exception for AI Assistant errors."""
    pass


class ProjectRootError(AIAssistError):
    """Raised when project root validation fails."""
    pass


class AIDirectoryError(AIAssistError):
    """Raised when AI directory operations fail."""
    pass


def validate_project_root(path: Optional[Union[str, Path]] = None) -> Path:
    """Validate that we're running from a project root directory.
    
    Args:
        path: Optional path to validate. Defaults to current working directory.
        
    Returns:
        Path: Validated project root path
        
    Raises:
        ProjectRootError: If not in a valid project root
    """
    if path is None:
        path = Path.cwd()
    else:
        path = Path(path)
    
    # Check if we're in a directory that looks like a project root
    # Common indicators of project root:
    project_indicators = [
        # Version control
        '.git',
        '.gitignore',
        # Python projects
        'setup.py', 'pyproject.toml', 'requirements.txt', 'Pipfile',
        # Node.js projects
        'package.json',
        # Other common project files
        'README.md', 'README.rst', 'README.txt',
        'Makefile', 'docker-compose.yml', 'Dockerfile',
        # Source directories
        'src', 'lib',
    ]
    
    # Check if any indicators exist
    has_indicators = any((path / indicator).exists() for indicator in project_indicators)
    
    if not has_indicators:
        raise ProjectRootError(
            f"Current directory '{path}' doesn't appear to be a project root. "
            f"Expected to find at least one of: {', '.join(project_indicators[:5])}... "
            f"Please run ai-assist from your project root directory."
        )
    
    return path.resolve()


def get_ai_directory_path(project_root: Union[str, Path]) -> Path:
    """Get the path to the AI directory for a project.
    
    Args:
        project_root: Path to the project root
        
    Returns:
        Path: Path to the AI directory (may not exist yet)
    """
    return Path(project_root) / "AI"


def ensure_ai_directory(project_root: Union[str, Path]) -> Path:
    """Ensure the AI directory exists, creating it if necessary.
    
    Args:
        project_root: Path to the project root
        
    Returns:
        Path: Path to the AI directory
        
    Raises:
        AIDirectoryError: If directory cannot be created
    """
    ai_dir = get_ai_directory_path(project_root)
    
    try:
        ai_dir.mkdir(exist_ok=True)
        return ai_dir
    except OSError as e:
        raise AIDirectoryError(f"Failed to create AI directory '{ai_dir}': {e}")


def is_ai_directory_initialized(project_root: Union[str, Path]) -> bool:
    """Check if the AI directory is properly initialized.
    
    Args:
        project_root: Path to the project root
        
    Returns:
        bool: True if AI directory exists and has AI_CONTEXT.yaml
    """
    ai_dir = get_ai_directory_path(project_root)
    context_file = ai_dir / "AI_CONTEXT.yaml"
    
    return ai_dir.exists() and context_file.exists()


def get_project_name(project_root: Union[str, Path]) -> str:
    """Attempt to determine the project name from the directory or common files.
    
    Args:
        project_root: Path to the project root
        
    Returns:
        str: Best guess at project name
    """
    project_root = Path(project_root)
    
    # Try to get name from directory
    return project_root.name