from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from .. import schemas, models, utils


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

#  Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
    user.password = utils.hash(user.password)
    users = models.User(name=user.name, username=user.username, email=user.email, password=user.password)
    db.add(users)
    db.commit()
    db.refresh(users)
    return users

# Read
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.UserOut)
def read_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} doesnot exist")
    return user
