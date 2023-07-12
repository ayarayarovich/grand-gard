from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Post, PermissionsEnum


class PostDAL:
    """Data Access Layer for operating posts info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self, post_name: str, permissions: list[PermissionsEnum]
    ) -> Post:
        new_post = Post(name=post_name, permissions=[p.value for p in permissions])
        self.session.add(new_post)
        await self.session.flush()
        return new_post

    async def delete_post(
        self, post_id: int = None, post_name: int = None
    ) -> int | None:
        query = delete(Post).where(Post.id == post_id).returning(Post.id)
        res = await self.session.execute(query)
        deleted_post_id = res.scalar_one_or_none()
        return deleted_post_id

    async def get_post_by_id(self, post_id: int) -> Post | None:
        query = select(Post).where(Post.id == post_id)

        res = await self.session.execute(query)
        post = res.scalar_one_or_none()
        return post

    async def get_post_by_name(self, post_name: str) -> Post | None:
        query = select(Post).where(Post.name == post_name)
        res = await self.session.execute(query)
        post = res.scalar_one_or_none()
        return post

    async def get_posts(self, offset: int, limit: int) -> list[Post]:
        query = select(Post).offset(offset).limit(limit)

        res = await self.session.execute(query)
        posts = res.scalars().unique()

        return list(posts)

    async def update_post(self, post_id: int, **kwargs):
        query = update(Post).where(Post.id == post_id).values(kwargs).returning(Post.id)
        res = await self.session.execute(query)
        updated_post_id = res.scalar_one_or_none()
        return updated_post_id
