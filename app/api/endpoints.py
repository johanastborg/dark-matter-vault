from fastapi import APIRouter, HTTPException, status
from typing import List
from app.api.models import Repository, RepositoryCreate
from app.services.storage import storage_service
import uuid

router = APIRouter()

@router.get("/repositories", response_model=List[str])
def list_repositories():
    """
    List all repositories.
    """
    return storage_service.list_repositories()

@router.post("/repositories", response_model=Repository, status_code=status.HTTP_201_CREATED)
def create_repository(repo: RepositoryCreate):
    """
    Create a new repository.
    """
    success = storage_service.create_repository(repo.name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Repository already exists"
        )

    return Repository(
        id=str(uuid.uuid4()),
        owner="user", # Placeholder
        name=repo.name,
        description=repo.description,
        is_private=repo.is_private,
        files=["README.md"]
    )

@router.get("/repositories/{repo_name}/files", response_model=List[str])
def get_repository_files(repo_name: str):
    """
    List files in a repository.
    """
    files = storage_service.get_repository_files(repo_name)
    if not files and repo_name not in storage_service.list_repositories():
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found"
        )
    return files
