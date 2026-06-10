from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskUpdate
from app.models import Task
from fastapi import HTTPException, status
import math
from uuid import UUID


def create_task(data: TaskCreate, project_id: UUID, db: Session) -> Task:
    new_task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        project_id=project_id,
        priority=data.priority,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(task_id: UUID, data: TaskUpdate, project_id: UUID, db: Session) -> Task:
    existing_task = get_task_by_id(task_id, project_id, db)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)
    return existing_task


def delete_task(task_id: UUID, project_id: UUID, db: Session) -> dict:
    existing_task = get_task_by_id(task_id, project_id, db)
    db.delete(existing_task)
    db.commit()
    return {"message": "Task deleted successfully"}


def get_all_tasks(
    project_id: UUID,
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    sort_by: str = "created_at",
    order: str = "asc",
) -> dict:
    # return db.query(Task).filter(Task.project_id == project_id).all()
    query = db.query(Task).filter(Task.project_id == project_id)

    # search
    if search is not None:
        query = query.filter(Task.title.ilike(f"{search}"))

    # filter
    if status is not None:
        query = query.filter(Task.status == status)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    column = getattr(Task, sort_by, Task.created_at)
    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    count = query.count()
    skip = (page - 1) * limit
    total_pages = math.ceil(count / limit)
    query = query.offset(skip).limit(limit)
    tasks = query.all()
    return {
        "data": tasks,
        "total": count,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


# we use , for and operation and or_() for or operation
# check task by comparing task id and project id
def get_task_by_id(task_id: UUID, project_id: UUID, db: Session) -> Task:
    existing_task = (
        db.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
    )
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return existing_task


def assign_task(task_id: UUID, project_id: UUID, user_id: UUID, db: Session) -> Task:
    existing_task = get_task_by_id(task_id, project_id, db)
    if existing_task.assigned_to is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task already assigned to a member",
        )
    existing_task.assigned_to = user_id
    db.commit()
    db.refresh(existing_task)
    return existing_task
