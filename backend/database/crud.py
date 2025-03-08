from sqlalchemy.orm import Session
from .models import User, League
from .database import Base, engine, SessionLocal

def create_user(db: Session, name: str, email: str):
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to get updated data
    return new_user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def initialize_leagues():
    """Create tables and insert initial data if they do not exist."""
    print("Initializing database and creating tables...")
    Base.metadata.create_all(bind=engine)  # Ensure tables exist
    db = SessionLocal()
    try:
        if not db.query(League).first():  # Check if table is empty
            league1 = League(name="Premier League")
            league2 = League(name="La Liga")
            db.add_all([league1, league2])
            db.commit()
            print("Inserted initial data.")
    finally:
        db.close()