from sqlalchemy.orm import Session
from app.schemas import ProjectCreate, ProjectUpdate
from app.models import Project, User
from fastapi import HTTPException, status
from uuid import UUID


def create_project(user_id: UUID, data: ProjectCreate, db: Session) -> Project:
    new_project = Project(
        title=data.title,
        description=data.description,
        status=data.status,
        owner_id=user_id,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def get_project_by_id(project_id: UUID, db: Session) -> Project:
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return db_project


def update_project(
    project_id: UUID, current_user_id: UUID, data: ProjectUpdate, db: Session
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this project",
        )
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


def delete_project(project_id: UUID, current_user: User, db: Session) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    if project.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this project",
        )
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


def get_all_projects(current_user: User, db: Session) -> list[Project]:
    if current_user.role != "admin":
        return db.query(Project).filter(Project.owner_id == current_user.id).all()
    return db.query(Project).all()


def add_member(
    user_id: UUID, current_user_id: UUID, project_id: UUID, db: Session
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only project owner can add members",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user in project.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already a member"
        )
    project.members.append(user)
    db.commit()
    db.refresh(project)
    return project


def remove_member(
    user_id: UUID, current_user_id: UUID, project_id: UUID, db: Session
) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only project owner can remove member",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user in project.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a member"
        )
    project.members.remove(user)
    db.commit()
    db.refresh(project)
    return Project
