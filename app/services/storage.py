import os
import shutil
from typing import List
from app.core.config import settings

class StorageService:
    def __init__(self, mount_point: str = settings.MOUNT_POINT):
        self.mount_point = mount_point
        # Ensure the mount point exists (mostly for local dev if not using fuse)
        # In cloud run with fuse, this path will be where the bucket is mounted
        if not os.path.exists(self.mount_point):
            try:
                os.makedirs(self.mount_point, exist_ok=True)
            except OSError:
                pass # Might not have permissions or it's a readonly mount

    def create_repository(self, repo_name: str) -> bool:
        repo_path = os.path.join(self.mount_point, repo_name)
        if os.path.exists(repo_path):
            return False
        os.makedirs(repo_path, exist_ok=True)
        # Create a README.md to initialize
        with open(os.path.join(repo_path, "README.md"), "w") as f:
            f.write(f"# {repo_name}\n")
        return True

    def list_repositories(self) -> List[str]:
        if not os.path.exists(self.mount_point):
            return []

        repos = []
        for name in os.listdir(self.mount_point):
            if os.path.isdir(os.path.join(self.mount_point, name)):
                repos.append(name)
        return repos

    def get_repository_files(self, repo_name: str) -> List[str]:
        repo_path = os.path.join(self.mount_point, repo_name)
        if not os.path.exists(repo_path):
            return []

        files = []
        for root, _, filenames in os.walk(repo_path):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), repo_path)
                files.append(rel_path)
        return files

storage_service = StorageService()
