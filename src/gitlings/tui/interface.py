# src/gitlings/tui/interface.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

class GitTerminal(Static):
    """自定义终端模拟器"""
    content = reactive("")
    
    def __init__(self, executor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.executor = executor
        self.history = []
        self.history_index = 0
        self.current_dir = "~/git-practice"
        
    def on_mount(self) -> None:
        self.update_content("$ git status\nfatal: not a git repository (or any of the parent directories)")
    
    def update_content(self, new_text: str) -> None:
        self.content += "\n" + new_text
        self.refresh()
    
    def render(self) -> Panel:
        syntax = Syntax(
            self.content, 
            "bash", 
            theme="monokai", 
            line_numbers=False,
            word_wrap=True
        )
        return Panel(
            syntax,
            title=f"Git Terminal - {self.current_dir}",
            border_style="blue",
            subtitle="Press ↑/↓ for history"
        )

class ExercisePanel(Static):
    """练习说明面板"""
    def __init__(self, exercise, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise = exercise
    
    def render(self) -> Panel:
        table = Table.grid(padding=(0, 2))
        table.add_column(style="bold cyan")
        table.add_column()
        
        table.add_row("Exercise:", self.exercise['name'])
        table.add_row("Objective:", Text(self.exercise['description'], style="green"))
        
        return Panel(
            table,
            title="Current Exercise",
            border_style="green"
        )

class GitlingsApp(App):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 2fr 3fr;
        padding: 1;
    }
    
    #exercise-panel {
        height: 100%;
        border: round green;
    }
    
    #terminal-container {
        height: 100%;
        layout: vertical;
    }
    
    #terminal {
        height: 85%;
    }
    
    #input-container {
        height: 15%;
        border: round blue;
    }
    
    Input {
        width: 100%;
    }
    """

    def __init__(self, git_executor, exercise_data):
        super().__init__()
        self.git_executor = git_executor
        self.exercise_data = exercise_data
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield ExercisePanel(self.exercise_data, id="exercise-panel")
        with Container(id="terminal-container"):
            yield GitTerminal(self.git_executor, id="terminal")
            with Container(id="input-container"):
                yield Input(placeholder="Enter git command...", id="input")
        yield Footer()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            terminal = self.query_one(GitTerminal)
            result = self.git_executor(event.value)
            terminal.update_content(f"$ {event.value}\n{result}")
            self.query_one(Input).value = ""
            terminal.scroll_end()
    
    def on_key(self, event):
        terminal = self.query_one(GitTerminal)
        if event.key == "up":
            # 实现命令历史记录导航
            pass
        elif event.key == "down":
            pass
