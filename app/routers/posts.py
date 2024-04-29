from fastapi import status, Depends, APIRouter, HTTPException
from .. import schemas, models, oauth2
from ..database import get_db, engine
from sqlalchemy.orm import Session
from typing import Optional

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/posts',
    tags= ['Posts']
)
# Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # This makes sure that the post created is by an aunthenticated user and inserted according to the owner_id
    posts = models.Post(owner_id=current_user.id, title=post.title, content=post.content, published=post.published)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

# Read
# Query parameters (limit, Skip, Search)
# The search query is designed to fetch the query using the title keywords of the post
# Use the "%20" for spacing the keywords in the API.
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def read_posts(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = 0):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

# Update
@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.owner_id == current_user.id).first()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    post_to_update.title = post.title
    post_to_update.content = post.content
    post_to_update.published = post.published
    db.commit()
    db.refresh(post_to_update)
    return post_to_update

# Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # Making the post private 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return {"data": "The plug successfully deleted"}
 