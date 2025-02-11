from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    value = Column(Float)
    icon = Column(String)

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    week = Column(String)
    weight_lost = Column(Float)
    calories_burned = Column(Float)

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    progress = Column(Float, default=0.0)
    duration = Column(Integer)
    calories_burned = Column(Integer)

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    duration = Column(Integer)  # Duration in minutes
    calories_burned = Column(Float)

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    progress = Column(Float)  # Progress percentage

class Trainer(Base):
    __tablename__ = "trainers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    contact = Column(String)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)

from sqlalchemy.orm import Session

def populate_sample_data(session: Session):
    try:
        # Add trainers
        trainers = []
        for i in range(1, 6):
            trainer = Trainer(
                name=f"Trainer {i}",
                specialization=f"Specialization {i}",
                contact=f"trainer{i}@example.com"
            )
            trainers.append(trainer)
        session.add_all(trainers)
        session.flush()
        
        # Add users
        users = []
        for i in range(1, 6):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                hashed_password="password",  # In production, hash passwords properly
                created_at=datetime.utcnow(),
                is_active=True,
                is_admin=False
            )
            users.append(user)
        session.add_all(users)
        session.flush()
        
        # Add workouts
        workouts = []
        for i in range(1, 6):
            workout = Workout(
                name=f"Workout {i}",
                description=f"Description for workout {i}",
                duration=30 + i * 5,
                calories_burned=100 + i * 20
            )
            workouts.append(workout)
        session.add_all(workouts)
        session.flush()
        
        # Add user progress
        user_progress = []
        for i in range(1, 6):
            progress = UserProgress(
                user_id=users[i-1].id,
                workout_id=workouts[i-1].id,
                progress=i * 20
            )
            user_progress.append(progress)
        session.add_all(user_progress)
        session.flush()
        
        # Add feedback
        feedbacks = []
        for i in range(1, 6):
            feedback = Feedback(
                user_id=users[i-1].id,
                trainer_id=trainers[i-1].id,
                rating=i,
                comment=f"Feedback {i}",
                created_at=datetime.utcnow(),
                is_active=True,
                is_resolved=False
            )
            feedbacks.append(feedback)
        session.add_all(feedbacks)
        
        session.commit()
        print("Sample data added to the database successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error populating sample data: {str(e)}")
