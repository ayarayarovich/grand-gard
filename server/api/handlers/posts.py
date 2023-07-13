from typing import Annotated
from fastapi import APIRouter, Depends
from api.schemes import PostShow, PostCreate, PostUpdate
from database.dals import PostDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception

from database.models import  PermissionsEnum


posts_router = APIRouter()
@posts_router.post("/")
async def create_post(
    post: PostCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        post_dal = PostDAL(session)

        new_post = await post_dal.create_post(
            post_name=post.name,
            permissions=[p for p in post.permissions],
        )

        return new_post

@posts_router.get("/{id}", response_model=PostShow) #предоставление информации
async def get_post_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        post_dal = PostDAL(session)

        post = await post_dal.get_post_by_id(id)
        if post is None:
            raise create_http_exception(
                status_code=404, reason="post with provided id does not exist", id=id
            )
        return post



@posts_router.put("/{id}", response_model=PostShow) #обновление
async def update_post(
    id: int,
    values_to_update: PostUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    async with session.begin():
        post_dal = PostDAL(session)
        updated_post = await post_dal.update_post(
            id, **values_to_update.dict(exclude_unset=True)
        )

        post = await post_dal.get_post_by_id(id)
        if post is None:
            raise create_http_exception(
                status_code=404, reason="post with provided id does not exist", id=id
            )

        return updated_post



#----------------------

@posts_router.get("/", response_model=list[PostShow])
async def get_post(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
         post_dal = PostDAL(session)
         post = await post_dal.get_posts(offset, limit)
         if limit > 10:
             raise create_http_exception(
                 status_code=416, reason="you cannot output more than 10 posts ", id=id
             )
         return post



@posts_router.delete("/{id}")
async def delete_post(id: int, session: Annotated[AsyncSession, Depends(get_db_session)]):

    async with session.begin():
        post_dal = PostDAL(session)

        post = await post_dal.get_post_by_id(id)
        if post is None:
            raise create_http_exception(
                status_code=404, reason="post with provided id does not exist", id=id
            )
        deleted_post_id=await post_dal.delete_post(id)
        return {deleted_post_id: "is deleted"}

