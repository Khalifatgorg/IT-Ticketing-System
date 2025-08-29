from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base, UserMixin):
__tablename__ = 'users'
id = Column(Integer, primary_key=True)
email = Column(String(120), unique=True, nullable=False)
name = Column(String(120), nullable=False)
role = Column(String(20), nullable=False) # 'head', 'admin', 'user'
employee_id = Column(String(50))
branch = Column(String(120))
branch_code = Column(String(50))
department = Column(String(120))
created_at = Column(DateTime, default=datetime.utcnow)


class Ticket(Base):
__tablename__ = 'tickets'
id = Column(Integer, primary_key=True)
title = Column(String(200))
description = Column(Text)
issue_type = Column(String(50))
attachment = Column(String(300))
created_by_id = Column(Integer, ForeignKey('users.id'))
created_by = relationship('User', foreign_keys=[created_by_id])
created_at = Column(DateTime, default=datetime.utcnow)
status = Column(String(50), default='New') # New, Accepted-by-Head, Assigned, In-Progress, Resolved, Rejected
head_approved = Column(Boolean, default=False)
assigned_admin_id = Column(Integer, ForeignKey('users.id'), nullable=True)
assigned_admin = relationship('User', foreign_keys=[assigned_admin_id])
history = Column(Text, default='')


class Notification(Base):
__tablename__ = 'notifications'
id = Column(Integer, primary_key=True)
content = Column(Text)
created_by_id = Column(Integer, ForeignKey('users.id'))
created_by = relationship('User')
created_at = Column(DateTime, default=datetime.utcnow)
