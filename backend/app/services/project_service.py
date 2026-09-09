from sqlalchemy.orm import Session

from backend.app.models.project import Project
from backend.app.schemas.project import ProjectCreate


def list_projects(db: Session) -> list[Project]:
    return db.query(Project).all()


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
