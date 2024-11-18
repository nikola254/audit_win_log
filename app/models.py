# Для работы с миграциями для начала необходимо создать репозиторий миграций
# flask db init
# Далее необходимо создать первую и последующую мигарцию
# flask db migrate -m "users table"
# Далее необходимо сгенерировать сценарий миграции
# flask db upgrade

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Criticals(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) 
    event_time: so.Mapped[datetime] = so.mapped_column()
    event_id: so.Mapped[int] = so.mapped_column(sa.Integer)
    event_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    event_info: so.Mapped[str] = so.mapped_column(sa.String(256))
    
class Error(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) 
    event_time: so.Mapped[datetime] = so.mapped_column()
    event_id: so.Mapped[int] = so.mapped_column(sa.Integer)
    event_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    event_info: so.Mapped[str] = so.mapped_column(sa.String(256))
    
class Warning(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) 
    event_time: so.Mapped[datetime] = so.mapped_column()
    event_id: so.Mapped[int] = so.mapped_column(sa.Integer)
    event_type: so.Mapped[str] = so.mapped_column(sa.String(256))
    event_info: so.Mapped[str] = so.mapped_column(sa.String(256))
    
class All_log_file(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True) 
    log_mode: so.Mapped[str] = so.mapped_column(sa.String(256))
    max_size: so.Mapped[int] = so.mapped_column(sa.Integer)
    record_count: so.Mapped[int] = so.mapped_column(sa.Integer)
    log_name: so.Mapped[str] = so.mapped_column(sa.String(256))
    