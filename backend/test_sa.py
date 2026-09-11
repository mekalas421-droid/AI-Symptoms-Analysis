import asyncio, uuid
from app.core.database import AsyncSessionLocal
from app.models.symptom import SymptomMaster
from sqlalchemy import select

async def test():
    async with AsyncSessionLocal() as db:
        # Get one directly via string
        res = await db.execute(select(SymptomMaster).limit(1))
        sym = res.scalar_one_or_none()
        print('Fetched sym id:', sym.id, type(sym.id))

        # Try to look it up by its UUID object
        uid = sym.id
        res2 = await db.execute(select(SymptomMaster).where(SymptomMaster.id == uid))
        sym2 = res2.scalar_one_or_none()
        print('Found by UUID object:', sym2 is not None)

        # Try to look it up by its UUID object inside in_
        res3 = await db.execute(select(SymptomMaster).where(SymptomMaster.id.in_([uid])))
        sym3 = res3.scalars().all()
        print('Found by in_([UUID]):', len(sym3) > 0)

if __name__ == '__main__':
    asyncio.run(test())
