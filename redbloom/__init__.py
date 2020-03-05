from flask_security import current_user
from taozi.models import Post, Event, Issue
from flask import Blueprint, render_template, abort

routes = Blueprint('redbloom', __name__)

@routes.route('/')
def index():
    featured = Post.query.filter(Post.published, Post.issue.has(slug='general'), Post.tags.contains('featured')).first()
    posts = Post.query.filter(Post.published, Post.issue.has(slug='general'), Post.event==None).limit(3)
    events = Post.query.filter(Post.published, Post.issue.has(slug='general'), Post.event!=None).limit(3)
    return render_template('index.html', featured=featured, posts=posts, events=events)

@routes.route('/<issue>/<slug>')
def post(issue, slug):
    post = Post.query.filter(Post.slug==slug, Post.issue.has(slug=issue)).first_or_404()
    if not post.published and not current_user.is_authenticated:
        abort(404)
    return render_template('post.html', post=post)

@routes.route('/events')
def events():
    events = [e.post for e in Event.query.order_by(Event.start.desc(), Event.end.desc()).all() if e.post.published]
    events.reverse()
    return render_template('events.html', events=events)

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/donate')
def donate():
    return render_template('donate.html')

@routes.route('/get-involved')
def get_involved():
    return render_template('get_involved.html')

