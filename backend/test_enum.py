import enum
from sqlalchemy import create_engine, Enum, String, Column, Integer
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class SeverityLevel(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"

class TestTable(Base):
    __tablename__ = "test_enum"
    id = Column(Integer, primary_key=True)
    severity = Column(Enum(SeverityLevel, values_callable=lambda x: [e.value for e in x]))

engine = create_engine('sqlite:///:memory:', echo=False)
Base.metadata.create_all(engine)

with Session(engine) as session:
    session.execute(TestTable.__table__.insert().values(id=1, severity='moderate'))
    session.commit()
    try:
        obj = session.query(TestTable).first()
        print('Loaded:', obj.severity)
    except Exception as e:
        print('Error:', repr(e))
