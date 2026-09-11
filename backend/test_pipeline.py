import asyncio, uuid, datetime
from app.core.database import AsyncSessionLocal
from app.services.prediction_engine import run_pipeline
from app.models.symptom import SymptomSubmission, SymptomMaster
from sqlalchemy import select

async def test():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(SymptomMaster.id).limit(1))
        sym_id = res.scalar_one_or_none()
        
        # Create a new submission directly
        submission = SymptomSubmission(
            patient_id=uuid.UUID('e15c990bc1404db388415b3983831d05'),  # valid patient id from earlier
            submitted_symptoms=[sym_id],
            status='submitted'
        )
        db.add(submission)
        await db.commit()
        await db.refresh(submission)
        
        print('Created submission:', submission.id)
        
        try:
            res = await run_pipeline(
                db=db,
                submission_id=submission.id,
                patient_id=submission.patient_id,
                submitted_symptom_ids=[sym_id]
            )
            print('Pipeline success!')
        except Exception as e:
            print('Pipeline failed:', type(e), e)
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test())
