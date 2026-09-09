import asyncio
from app.core.database import AsyncSessionLocal
from app.models.symptom import SymptomMaster
from app.db.seed import SYMPTOMS_DATA, normalize_code

async def seed_symptoms():
    async with AsyncSessionLocal() as db:
        for category, symptoms in SYMPTOMS_DATA.items():
            for s_name in symptoms:
                s_code = normalize_code(s_name)
                # Check if it exists
                # In SQLAlchemy 2.0 with async:
                # result = await db.execute(select(SymptomMaster).filter_by(symptom_code=s_code))
                # if not result.scalar_one_or_none():
                db.add(SymptomMaster(
                    symptom_code=s_code,
                    display_name=s_name,
                    category=category,
                    synonyms=[s_name.lower()]
                ))
        try:
            await db.commit()
            print('Symptoms seeded successfully!')
        except Exception as e:
            print('Error:', e)

if __name__ == '__main__':
    asyncio.run(seed_symptoms())
