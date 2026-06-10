from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import ProjectResponse, ProjectCreate, ProjectUpdate
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services import (
    create_project,
    update_project,
    get_all_projects,
    get_project_by_id,
    add_member,
    remove_member,
    delete_project,
)
from uuid import UUID

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project_router(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_project(current_user.id, data, db)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_router(
    project_id: UUID,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_project(project_id, current_user.id, data, db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_router(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_project_by_id(project_id, db)


@router.get("/", response_model=list[ProjectResponse])
def get_projects_router(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_all_projects(current_user, db)


@router.delete("/{project_id}")
def delete_project_router(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_project(project_id, current_user, db)


@router.post("/{project_id}/members/{user_id}", response_model=ProjectResponse)
def add_member_router(
    project_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return add_member(user_id, current_user.id, project_id, db)


@router.delete("/{project_id}/members/{user_id}", response_model=ProjectResponse)
def remove_member_router(
    project_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return remove_member(user_id, current_user.id, project_id, db)
