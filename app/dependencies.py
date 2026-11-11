from .database import SessionaLocal

def get_db():
    db=SessionaLocal()
    try:
        yield db
    finally:
        db.close()