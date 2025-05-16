from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

# Created instance of FastAPI
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class choiceBase(BaseModel):
    choice_txt: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[choiceBase]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/")
def create_questions(questions: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=questions.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in questions.choices:
        db_choice = models.Choices(choice_text=choice.choice_txt, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    db.commit()