from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskPaginatedResponse
from app.dependencies import get_current_user
from app.services import (
    create_task,
    update_task,
    get_task_by_id,
    get_all_tasks,
    assign_task,
    delete_task,
)
from app.models import User
from uuid import UUID

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
def create_task_router(
    project_id: UUID,
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_task(data, project_id, db)


@router.get("/", response_model=TaskPaginatedResponse)
def get_tasks_router(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0),
    limit: int = Query(10, gt=0),
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    sort_by: str = "created_at",
    order: str = "asc",
):
    return get_all_tasks(
        project_id, db, page, limit, search, status, priority, sort_by, order
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_router(
    task_id: UUID,
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_task_by_id(task_id, project_id, db)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_router(
    task_id: UUID,
    project_id: UUID,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_task(task_id, data, project_id, db)


@router.post("/{task_id}/assign/{user_id}", response_model=TaskResponse)
def assign_task_router(
    task_id: UUID,
    project_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return assign_task(task_id, project_id, user_id, db)


@router.delete("/{task_id}")
def delete_task_router(
    task_id: UUID,
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_task(task_id, project_id, db)
