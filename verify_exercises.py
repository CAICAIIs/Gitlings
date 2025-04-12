#!/usr/bin/env python3
import subprocess
import toml
from pathlib import Path

def verify_exercise(exercise_dir: Path):
    meta = toml.load(exercise_dir / "meta.toml")
    verify_cmd = meta.get("verify", "true")
    
    try:
        subprocess.run(verify_cmd, shell=True, check=True)
        print(f"✅ {exercise_dir.name} passed")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {exercise_dir.name} failed")
        return False

if __name__ == "__main__":
    exercises = Path("exercises").glob("*/*")
    results = [verify_exercise(ex) for ex in exercises if (ex / "meta.toml").exists()]
    print(f"\nSummary: {sum(results)}/{len(results)} exercises passed")
