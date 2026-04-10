"""
routes/posts.py - Blog Post Routes
Full CRUD + image upload + comments + likes + search + pagination.
"""

import os
from flask import Blueprint, request, jsonify, send_from_directory
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from models import db, Post, Comment, Like
from routes.auth import token_required

posts_bp = Blueprint("posts", __name__)

POSTS_PER_PAGE = 6
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── GET /posts ─────────────────────────────────────────────────────────────
@posts_bp.route("/posts", methods=["GET"])
def get_posts():
    page     = request.args.get("page",     1, type=int)
    per_page = request.args.get("per_page", POSTS_PER_PAGE, type=int)
    search   = request.args.get("search",   "").strip()
    tag      = request.args.get("tag",      "").strip()

    query = Post.query.order_by(Post.created_at.desc())

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Post.title.ilike(like_pattern),
                Post.summary.ilike(like_pattern),
                Post.content.ilike(like_pattern),
                Post.tags.ilike(like_pattern),
            )
        )
    if tag:
        query = query.filter(Post.tags.ilike(f"%{tag}%"))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "posts":        [p.to_dict(include_content=False) for p in paginated.items],
        "total":        paginated.total,
        "pages":        paginated.pages,
        "current_page": page,
        "has_next":     paginated.has_next,
        "has_prev":     paginated.has_prev,
    }), 200


# ── GET /posts/<id> ────────────────────────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id, description="Post not found")
    post_data = post.to_dict()
    post_data["comments"] = [
        c.to_dict() for c in
        Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    ]
    return jsonify({"post": post_data}), 200


# ── POST /posts ────────────────────────────────────────────────────────────
@posts_bp.route("/posts", methods=["POST"])
@token_required
def create_post(current_user):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    title   = (data.get("title")   or "").strip()
    content = (data.get("content") or "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if len(title) > 200:
        return jsonify({"error": "Title must be under 200 characters"}), 400
    if not content or len(content) < 10:
        return jsonify({"error": "Content must be at least 10 characters"}), 400

    summary   = (data.get("summary")   or "").strip()
    tags      = (data.get("tags")      or "").strip()
    image_url = (data.get("image_url") or "").strip()

    if not summary:
        summary = content[:200] + ("…" if len(content) > 200 else "")

    post = Post(
        title=title, # pyright: ignore[reportCallIssue]
        content=content, # type: ignore
        summary=summary,# type: ignore
        tags=tags, # type: ignore
        image_url=image_url, # type: ignore
        user_id=current_user.id, # type: ignore
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created successfully!", "post": post.to_dict()}), 201


# ── PUT /posts/<id> ────────────────────────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>", methods=["PUT"])
@token_required
def update_post(current_user, post_id):
    post = Post.query.get_or_404(post_id, description="Post not found")
    if post.user_id != current_user.id:
        return jsonify({"error": "You are not authorized to edit this post"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return jsonify({"error": "Title cannot be empty"}), 400
        post.title = title
    if "content" in data:
        content = data["content"].strip()
        if len(content) < 10:
            return jsonify({"error": "Content must be at least 10 characters"}), 400
        post.content = content
    if "summary"   in data: post.summary   = data["summary"].strip()
    if "tags"      in data: post.tags      = data["tags"].strip()
    if "image_url" in data: post.image_url = data["image_url"].strip()

    from datetime import datetime
    post.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Post updated successfully!", "post": post.to_dict()}), 200


# ── DELETE /posts/<id> ─────────────────────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@token_required
def delete_post(current_user, post_id):
    post = Post.query.get_or_404(post_id, description="Post not found")
    if post.user_id != current_user.id:
        return jsonify({"error": "You are not authorized to delete this post"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200


# ── POST /posts/<id>/like ──────────────────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>/like", methods=["POST"])
@token_required
def toggle_like(current_user, post_id):
    post = Post.query.get_or_404(post_id, description="Post not found")
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"message": "Post unliked", "liked": False, "like_count": len(post.likes)}), 200
    else:
        db.session.add(Like(user_id=current_user.id, post_id=post_id)) # type: ignore
        db.session.commit()
        return jsonify({"message": "Post liked!", "liked": True, "like_count": len(post.likes)}), 200


# ── POST /posts/<id>/comments ──────────────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@token_required
def add_comment(current_user, post_id):
    Post.query.get_or_404(post_id, description="Post not found")
    data = request.get_json()
    body = (data.get("body") or "").strip() if data else ""

    if not body:
        return jsonify({"error": "Comment body is required"}), 400
    if len(body) > 1000:
        return jsonify({"error": "Comment must be under 1000 characters"}), 400

    comment = Comment(body=body, user_id=current_user.id, post_id=post_id) # type: ignore
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added!", "comment": comment.to_dict()}), 201


# ── DELETE /posts/<id>/comments/<cid> ─────────────────────────────────────
@posts_bp.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE"])
@token_required
def delete_comment(current_user, post_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first_or_404(
        description="Comment not found"
    )
    if comment.user_id != current_user.id:
        return jsonify({"error": "Not authorized to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200


# ── POST /upload  (image upload) ───────────────────────────────────────────
@posts_bp.route("/upload", methods=["POST"])
@token_required
def upload_image(current_user):
    """Upload a cover image. Returns the public URL."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only PNG, JPG, JPEG, GIF, WEBP files allowed"}), 400

    # Save with unique name: userID_originalname
    filename    = secure_filename(file.filename) # type: ignore
    unique_name = f"{current_user.id}_{filename}"

    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, unique_name))

    image_url = f"http://127.0.0.1:5000/static/uploads/{unique_name}"
    return jsonify({"image_url": image_url}), 200
