# src/gitlings/cli/main.py
import click
from gitlings.core.virtual_git import VirtualGit
from gitlings.tui.interface import GitlingsApp
from gitlings.core.exercise import Exercise

@click.group()
def cli():
    """Gitlings - Interactive Git learning tool"""
    pass

@cli.command()
@click.option("--exercise", default="basic/01_init", help="Exercise to start with")
def start(exercise):
    """Start the interactive TUI"""
    git_simulator = VirtualGit()
    exercise_data = Exercise.load_exercise(exercise)
    app = GitlingsApp(git_simulator.run_command, exercise_data)
    app.run()
