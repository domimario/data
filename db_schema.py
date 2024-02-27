# db_schema.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Nationality(Base):
    __tablename__ = 'nationalities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Championship(Base):
    __tablename__ = 'championships'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nationality_id = Column(Integer, ForeignKey('nationalities.id'))
    nationality = relationship('Nationality')

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    championship_id = Column(Integer, ForeignKey('championships.id'))
    championship = relationship('Championship')
    players = relationship('Player', back_populates='team')
    trophies = relationship('Trophy', back_populates='team')

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    number = Column(Integer)
    nationality_id = Column(Integer, ForeignKey('nationalities.id'))
    nationality = relationship('Nationality')
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates='players')
    goals = relationship('Goal', back_populates='player')

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    match_type = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    player = relationship('Player', back_populates='goals')

class Trophy(Base):
    __tablename__ = 'trophies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates='trophies')

# Create an SQLite database in memory for testing
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
