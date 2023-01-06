from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from schemas import *
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, utils, database, oauth2
from database import engine, SessionLocal, get_db
from typing import Optional, List
import oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])

my_posts = [{"title":"Lord of Rings", "content": "Rings of Power", "id":1},
           {"title":"Folsom Foods", "content":"Burger", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user), limit: int = 3,
skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post:PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                   (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}/", response_model=PostOut)
def get_post(id: int, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id= %s""",(str(id),))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id)\
            .filter(models.Post.id == id).first()

    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,    
                            detail=  f"post with id:{id} not found")
    
    return post

@router.put("/{id}/", response_model=Post)
def update_post(id: int, post:schemas.PostCreate, db:Session = Depends(get_db), current_user: int= 
Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s  WHERE id = %s RETURNING *""" , 
    #               (post.title, post.content, post.published, str(id)))
    # updated = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    
    if posts == None:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail = f"post with id: {id} does not exist")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail=f"Unauthorized to perform the action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return posts

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),) )
    # delete_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                      detail=f"Unauthorized to perform the action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)