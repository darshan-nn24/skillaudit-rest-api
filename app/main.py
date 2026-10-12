from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'tasks.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    priority = Column(String(20), nullable=False, default="medium")


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillAudit Task Management API",
    description="A simple CRUD REST API built for the SkillAudit internship task.",
    version="1.0.0",
)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: str = Field(default="pending", pattern="^(pending|in-progress|completed)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: str | None = Field(default=None, pattern="^(pending|in-progress|completed)$")
    priority: str | None = Field(default=None, pattern="^(low|medium|high)$")


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: str
    priority: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Health"])
def root():
    return {"message": "SkillAudit Task Management API is running", "docs": "/docs"}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Unable to create task")


@app.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK, tags=["Tasks"])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id.desc()).all()


@app.get("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = task_update.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
