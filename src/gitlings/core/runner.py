from pathlib import Path
from typing import List, Optional, Dict
from .exercise import Exercise
from .virtual_git import VirtualGit

class ExerciseRunner:
    def __init__(self, exercises_dir: Path):
        self.exercises = self._load_exercises(exercises_dir)
        self.current_index = 0
        self.git = VirtualGit()
        self.history = []
    
    def _load_exercises(self, root: Path) -> List[Exercise]:
        exercises = []
        for ex_dir in sorted(root.glob("*/*")):
            if (ex_dir / "meta.toml").exists():
                exercises.append(Exercise.load(ex_dir))
        return exercises
    
    @property
    def current_exercise(self) -> Optional[Exercise]:
        if self.current_index < len(self.exercises):
            return self.exercises[self.current_index]
        return None
    
    def next(self) -> bool:
        if self.current_index + 1 < len(self.exercises):
            self.current_index += 1
            self.git = VirtualGit()  # 重置Git环境
            return True
        return False
    
    def verify(self) -> Dict[str, bool]:
        if not self.current_exercise:
            return {}
        
        results = {}
        for check in self.current_exercise.checks:
            check_id, check_desc = check.split("@")
            check_id = check_id.strip()
            
            if check_id == "git init":
                results[check_desc.strip()] = self.git.state['repo_initialized']
            elif check_id == "hello.txt存在":
                results[check_desc.strip()] = "hello.txt" in self.git.state['working_dir']
            elif check_id == "提交信息规范":
                results[check_desc.strip()] = any(
                    "feat:" in c['message'] for c in self.git.state['commits']
                )
            elif check_id == "git merge":
                results[check_desc.strip()] = any(
                    "merge" in cmd for cmd in self.git.command_history
                )
            elif check_id == "解决README冲突":
                results[check_desc.strip()] = self.git.state['conflict'] is None
            else:
                results[check_desc.strip()] = False
        
        return results
    
    def execute(self, command: str) -> str:
        output = self.git.run_command(command)
        self.history.append((command, output))
        return output
