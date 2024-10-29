from app.backend.db import *

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()