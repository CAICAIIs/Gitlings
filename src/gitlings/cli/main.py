import click
from pathlib import Path
from gitlings.core.exercise import ExerciseManager
from typing import Optional

@click.group()
def cli():
    """Gitlings - Interactive Git learning tool"""
    pass

@cli.command()
def start():
    """Start the interactive learning session"""
    click.echo("🚀 Starting Gitlings interactive mode...")
    
    exercises_path = Path(__file__).parent.parent.parent / "exercises"
    
    try:
        manager = ExerciseManager(exercises_path)
    except Exception as e:
        return
    
    # 显示第一个练习
    if manager.current_exercise:
        click.echo(f"\n📝 Exercise: {manager.current_exercise.name}")
        click.echo(manager.current_exercise.description)
    else:
        click.echo("No valid exercises found!", err=True)

if __name__ == "__main__":
    cli()
