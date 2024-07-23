from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declared_attr

from auth.models.base import Base
from auth.db.type_utils import EnumAsString
from auth.enums import TeamRoles, OrgRoles

# Association Tables
user_organizations = Table('user_organizations', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('role', EnumAsString(OrgRoles))
)

user_teams = Table('user_teams', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('role', EnumAsString(TeamRoles))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    organizations = relationship('Organization', secondary=user_organizations, back_populates='users')
    teams = relationship('Team', secondary=user_teams, back_populates='members')

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship('User', secondary=user_organizations, back_populates='organizations')
    teams = relationship('Team', back_populates='organization')

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    organization = relationship('Organization', back_populates='teams')
    members = relationship('User', secondary=user_teams, back_populates='teams')

class Workflow(Base):
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_exported = Column(Boolean, default=False)

    creator = relationship('User')

