from dataclasses import dataclass
from pathlib import Path
import toml
from typing import List, Dict

@dataclass
class Exercise:
    id: str
    name: str
    description: str
    difficulty: int
    hints: List[str]
    checks: List[Dict[str, str]]
    
    @classmethod
    def load(cls, path: Path):
        """从上一级目录加载练习"""
        meta = toml.load(path / "meta.toml")
        with open(path / "exercise.md") as f:
            desc = f.read()
        with open(path / "hint.md") as f:
            hints = [h.strip() for h in f.read().split("---") if h.strip()]
        
        return cls(
            meta["exercise"]["id"],
            meta["exercise"]["name"],
            desc,
            meta["exercise"]["difficulty"],
            hints,
            meta["verification"]["checks"]
        )

    
    def load_exercise(exercise_path: str) -> dict:
        """加载练习数据"""
        base_path = Path(__file__).parent.parent.parent / "exercises"
        full_path = base_path / exercise_path
        
        meta = toml.load(full_path / "meta.toml")
        with open(full_path / "exercise.md") as f:
            description = f.read()
        with open(full_path / "hint.md") as f:
            hints = f.read().split("---")
        
        return {
            'id': exercise_path,
            'name': meta['exercise']['name'],
            'description': description,
            'hints': hints,
            'difficulty': meta['exercise'].get('difficulty', 1)
        }
