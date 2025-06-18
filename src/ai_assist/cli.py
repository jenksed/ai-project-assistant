"""Main CLI interface for AI Project Assistant."""

import click
import sys
from pathlib import Path
from typing import Optional

from .core import (
    validate_project_root,
    ensure_ai_directory,
    get_ai_directory_path,
    AIAssistError
)


@click.group()
@click.version_option(version="0.1.0", prog_name="ai-assist")
@click.pass_context
def main(ctx):
    """AI Project Assistant - Maintain AI-ready project context and generate LLM preambles.
    
    This tool must be run from your project root directory and will create/manage
    an AI/ directory containing your project's AI context and generated files.
    """
    # Ensure that ctx.obj exists and is a dict (for sharing data between commands)
    ctx.ensure_object(dict)


@main.command()
@click.option('--force', is_flag=True, help='Overwrite existing AI_CONTEXT.yaml if it exists')
@click.pass_context
def init(ctx, force):
    """Initialize AI directory and create AI_CONTEXT.yaml template."""
    try:
        # Validate we're in a project root
        project_root = validate_project_root()
        click.echo(f"✓ Project root detected: {project_root}")
        
        # Create AI directory
        ai_dir = ensure_ai_directory(project_root)
        click.echo(f"✓ AI directory ready: {ai_dir}")
        
        # Create AI_CONTEXT.yaml (implementation will be in Phase 2)
        context_file = ai_dir / "AI_CONTEXT.yaml"
        if context_file.exists() and not force:
            click.echo(f"⚠️  AI_CONTEXT.yaml already exists. Use --force to overwrite.")
            return
        
        # For now, create a placeholder - full implementation in Phase 2
        click.echo("📝 Creating AI_CONTEXT.yaml template...")
        context_file.write_text("# AI_CONTEXT.yaml - Template (Phase 2 implementation pending)\n")
        click.echo(f"🎉 Initialization complete! AI context ready in {ai_dir}")
        
    except AIAssistError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--topic', required=True, help='Topic for the preamble (e.g., api, frontend, testing)')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'txt']), 
              help='Output format for the preamble')
@click.pass_context
def preamble(ctx, topic, format):
    """Generate AI preamble for a specific topic."""
    try:
        # Validate we're in a project root and AI directory exists
        project_root = validate_project_root()
        ai_dir = get_ai_directory_path(project_root)
        
        if not ai_dir.exists():
            raise AIAssistError(
                "AI directory not found. Run 'ai-assist init' first to initialize the project."
            )
        
        # Placeholder for Phase 3 implementation
        click.echo(f"🔄 Generating preamble for topic: {topic}")
        click.echo(f"📁 AI directory: {ai_dir}")
        click.echo("⏳ Preamble generation will be implemented in Phase 3")
        
    except AIAssistError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--model', required=True, help='AI model used (e.g., gpt-4, claude-3)')
@click.option('--prompt', required=True, help='The prompt sent to the AI model')
@click.option('--response', help='AI model response (optional, can be added later)')
@click.option('--format', default='markdown', type=click.Choice(['markdown', 'json']),
              help='Log format')
@click.pass_context
def log_query(ctx, model, prompt, response, format):
    """Log AI query and response for traceability."""
    try:
        # Validate we're in a project root and AI directory exists
        project_root = validate_project_root()
        ai_dir = get_ai_directory_path(project_root)
        
        if not ai_dir.exists():
            raise AIAssistError(
                "AI directory not found. Run 'ai-assist init' first to initialize the project."
            )
        
        # Placeholder for Phase 4 implementation
        click.echo(f"📝 Logging query for model: {model}")
        click.echo(f"📁 AI directory: {ai_dir}")
        click.echo("⏳ Query logging will be implemented in Phase 4")
        
    except AIAssistError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--key', required=True, help='Configuration key to update')
@click.option('--value', required=True, help='New value for the configuration key')
@click.pass_context
def update(ctx, key, value):
    """Update AI_CONTEXT.yaml configuration."""
    try:
        # Validate we're in a project root and AI directory exists
        project_root = validate_project_root()
        ai_dir = get_ai_directory_path(project_root)
        
        context_file = ai_dir / "AI_CONTEXT.yaml"
        if not context_file.exists():
            raise AIAssistError(
                "AI_CONTEXT.yaml not found. Run 'ai-assist init' first to initialize the project."
            )
        
        # Placeholder for Phase 2 implementation
        click.echo(f"🔄 Updating {key} = {value}")
        click.echo("⏳ Context updating will be implemented in Phase 2")
        
    except AIAssistError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.pass_context
def status(ctx):
    """Show current AI project status and configuration."""
    try:
        # Validate we're in a project root
        project_root = validate_project_root()
        ai_dir = get_ai_directory_path(project_root)
        
        click.echo("🔍 AI Project Assistant Status")
        click.echo(f"📁 Project Root: {project_root}")
        click.echo(f"📁 AI Directory: {ai_dir}")
        click.echo(f"✓ AI Directory Exists: {'Yes' if ai_dir.exists() else 'No'}")
        
        if ai_dir.exists():
            context_file = ai_dir / "AI_CONTEXT.yaml"
            click.echo(f"✓ AI_CONTEXT.yaml: {'Yes' if context_file.exists() else 'No'}")
            
            # List files in AI directory
            ai_files = list(ai_dir.glob("*"))
            if ai_files:
                click.echo("\n📄 Files in AI directory:")
                for file in sorted(ai_files):
                    click.echo(f"  • {file.name}")
            else:
                click.echo("\n📄 AI directory is empty")
        else:
            click.echo("\n💡 Run 'ai-assist init' to initialize the AI directory")
            
    except AIAssistError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()