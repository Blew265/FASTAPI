from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2
from ..database import get_db, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/votes',
    tags= ['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
  
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()   
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already voted on post {vote.post_id}")
        models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(vote)
        db.commit()
        return {"message": "successfully added vote"}   
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Votes not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
        