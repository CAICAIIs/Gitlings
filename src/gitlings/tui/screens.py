from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.widgets import Header, Footer, Static, Button, Input
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from typing import Dict

class ExerciseScreen(ScrollableContainer):
    
    def __init__(self, runner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runner = runner
    
    def compose(self) -> ComposeResult:
        exercise = self.runner.current_exercise
        
        yield Static(
            Panel.fit(
                f"[b]{exercise.name}[/b] (难度: {'★' * exercise.difficulty})\n\n"
                f"{exercise.description}",
                title="练习描述"
            )
        )
        
        table = Table.grid(padding=(0, 2))
        table.add_column("验证条件", style="cyan")
        for check in exercise.checks:
            _, desc = check.split("@")
            table.add_row(f"◻ {desc.strip()}")
        
        yield Static(Panel.fit(table, title="验证条件"))
        
        yield Static("\n输入Git命令或选择操作:", classes="prompt")
        yield Input(placeholder="输入git命令...", id="command_input")
        yield Container(
            Button("验证 (V)", variant="primary", id="verify"),
            Button("提示 (H)", variant="warning", id="hint"),
            Button("下一个 (N)", variant="success", id="next"),
            classes="buttons"
        )
        
        yield Static(id="output", markup=False)

class GitlingsApp(App):
    
    CSS = """
    Screen {
        layout: vertical;
    }
    .buttons {
        layout: horizontal;
        margin: 1 0;
    }
    #output {
        border: solid $accent;
        padding: 1;
        height: 10;
        overflow-y: auto;
    }
    """
    
    def __init__(self, runner):
        super().__init__()
        self.runner = runner
    
    def on_mount(self) -> None:
        self.push_screen(ExerciseScreen(self.runner))
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "verify":
            await self._run_verification()
        elif event.button.id == "hint":
            await self._show_hint()
        elif event.button.id == "next":
            if self.runner.next():
                self.push_screen(ExerciseScreen(self.runner))
            else:
                self.notify("🎉 恭喜完成所有练习!", severity="success")
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            output = self.runner.execute(event.value)
            await self.query_one("#output").update(output)
            event.input.value = ""
    
    async def _run_verification(self):
        results = self.runner.verify()
        exercise = self.runner.current_exercise
        
        table = Table.grid(padding=(0, 2))
        table.add_column("验证结果", style="bold")
        
        for check in exercise.checks:
            _, desc = check.split("@")
            desc = desc.strip()
            status = "✓" if results.get(desc, False) else "✗"
            color = "green" if status == "✓" else "red"
            table.add_row(f"[{color}]{status}[/] {desc}")
        
        await self.query_one("#output").update(
            Panel.fit(table, title="验证结果")
        )
    
    async def _show_hint(self):
        exercise = self.runner.current_exercise
        if exercise.hints:
            hint = exercise.hints[0]  # 简化版：只显示第一个提示
            await self.query_one("#output").update(
                Panel.fit(f"[yellow]💡 提示:[/]\n\n{hint}", title="帮助")
            )
