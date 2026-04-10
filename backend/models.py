"""
models.py - SQLAlchemy Database Models
Includes image_url on Post for cover image support.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    bio        = db.Column(db.String(300), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts    = db.relationship("Post",    backref="author",    lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="commenter", lazy=True, cascade="all, delete-orphan")
    likes    = db.relationship("Like",    backref="liker",     lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":         self.id,
            "username":   self.username,
            "email":      self.email,
            "bio":        self.bio,
            "created_at": self.created_at.isoformat(),
            "post_count": len(self.posts), # type: ignore
        }


class Post(db.Model):
    __tablename__ = "posts"

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text,        nullable=False)
    summary    = db.Column(db.String(500), default="")
    tags       = db.Column(db.String(200), default="")
    image_url  = db.Column(db.String(500), default="")   # ← cover image URL
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship("Comment", backref="post", lazy=True, cascade="all, delete-orphan")
    likes    = db.relationship("Like",    backref="post", lazy=True, cascade="all, delete-orphan")

    def to_dict(self, include_content=True):
        data = {
            "id":            self.id,
            "title":         self.title,
            "summary":       self.summary or self.content[:150] + "…",
            "tags":          [t.strip() for t in self.tags.split(",") if t.strip()],
            "image_url":     self.image_url,   # ← included in every response
            "author":        self.author.username, # type: ignore
            "author_id":     self.user_id,
            "created_at":    self.created_at.isoformat(),
            "updated_at":    self.updated_at.isoformat(),
            "like_count":    len(self.likes), # type: ignore
            "comment_count": len(self.comments), # type: ignore
        }
        if include_content:
            data["content"] = self.content
        return data


class Comment(db.Model):
    __tablename__ = "comments"

    id         = db.Column(db.Integer, primary_key=True)
    body       = db.Column(db.Text, nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id    = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":         self.id,
            "body":       self.body,
            "author":     self.commenter.username, # type: ignore
            "author_id":  self.user_id,
            "post_id":    self.post_id,
            "created_at": self.created_at.isoformat(),
        }


class Like(db.Model):
    __tablename__ = "likes"

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "post_id", name="unique_like"),)
