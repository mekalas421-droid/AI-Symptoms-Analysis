import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select

async def test():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(User).limit(1))
        user = res.scalar_one_or_none()
        if user:
            print('User role:', repr(user.role), type(user.role))
        else:
            print('No user')

if __name__ == '__main__':
    asyncio.run(test())
