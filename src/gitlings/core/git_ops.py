from git import Repo
import os
from typing import Optional


class GitManager:
    def __init__(self, path: str = "."):
        self.path = os.path.abspath(path)
        self.repo: Optional[Repo] = None

    def init_repo(self):
        """Initialize a new git repository"""
        try:
            self.repo = Repo.init(self.path)
            return True
        except Exception as e:
            print(f"Failed to init repo: {e}")
            return False

    def get_status(self):
        """Get current git status"""
        if not self.repo:
            return "No repository initialized"
        return self.repo.git.status()
