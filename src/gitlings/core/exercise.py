from dataclasses import dataclass
from pathlib import Path
import toml
from typing import List, Optional

@dataclass
class Exercise:
    path: Path
    name: str
    description: str
    
    @classmethod
    def load(cls, path: Path):
        """Load exercise from directory"""
        try:
            meta = toml.load(path / "meta.toml")
            with open(path / "exercise.md") as f:
                description = f.read()
            
            if "exercise" not in meta or "name" not in meta["exercise"]:
                raise ValueError("Invalid meta.toml structure")
                
            return cls(path, meta["exercise"]["name"], description)
        except Exception as e:
            print(f"Error loading exercise at {path}: {e}")
            return None

class ExerciseManager:
    def __init__(self, exercises_root: Path):
        self.exercises_root = exercises_root
        self.current_index = 0
        self.exercises = self._load_exercises()
    
    def _load_exercises(self) -> List[Exercise]:
        """Load all exercises from the exercises directory"""
        exercises = []
        
        # 递归查找所有包含meta.toml的目录
        for meta_file in self.exercises_root.rglob("meta.toml"):
            exercise_dir = meta_file.parent
            if exercise_dir.is_dir():
                exercise = Exercise.load(exercise_dir)
                if exercise:
                    exercises.append(exercise)
        
        # 按路径排序保证顺序
        exercises.sort(key=lambda x: str(x.path))
        return exercises
    
    @property
    def current_exercise(self) -> Optional[Exercise]:
        if self.current_index < len(self.exercises):
            return self.exercises[self.current_index]
        return None
