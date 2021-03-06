import json
import calendar
from datetime import datetime
from collections import defaultdict
from flask_security import current_user
from taozi.models import Post, Event, Issue
from flask import Blueprint, render_template, abort, current_app

routes = Blueprint('redbloom', __name__)

@routes.route('/news')
def news():
    featured = Post.query.filter(Post.published, Post.tags.contains('featured'), Post.issue.has(slug='red-bloom')).all()
    posts = Post.query.filter(Post.published, Post.event==None, Post.issue.has(slug='red-bloom')).limit(20)
    return render_template('index.html', featured=featured, posts=posts)

@routes.route('/working-groups')
def working_groups():
    working_groups = Issue.query.filter(Issue.published, Issue.slug != 'red-bloom').all()
    return render_template('working_groups.html', working_groups=working_groups)

@routes.route('/working-groups/<slug>')
def working_group(slug):
    working_group = Issue.query.filter(Issue.published, Issue.slug==slug).first_or_404()
    return render_template('issue.html', issue=working_group)

@routes.route('/<issue>/<slug>')
def post(issue, slug):
    post = Post.query.filter(Post.slug==slug, Post.issue.has(slug=issue)).first_or_404()
    if not post.published and not current_user.is_authenticated:
        abort(404)
    return render_template('post.html', post=post)

@routes.route('/events')
def events():
    today = datetime.now()
    month = today.month
    year = today.year
    first_weekday, num_days = calendar.monthrange(year, month)
    start = datetime(year, month, 1)
    end = datetime(year, month, num_days)
    events = [e for e in Event.query.filter(Event.start.between(start, end)).order_by(Event.start.asc(), Event.end.desc()).all() if e.post.published]
    events_by_day = defaultdict(list)
    for event in events:
        events_by_day[event.start.day].append(event)
    return render_template('events.html',
            events_by_day=events_by_day,
            month=month, year=year,
            first_weekday=first_weekday,
            month_name=calendar.month_name[month],
            num_days=num_days)

@routes.route('/')
def about():
    return render_template('about.html')

@routes.route('/points-of-unity')
def points_of_unity():
    return render_template('points_of_unity.html')

@routes.route('/get-involved')
def get_involved():
    return render_template('get_involved.html')

@routes.context_processor
def inject_user():
    wgs = Issue.query.filter(Issue.published, Issue.slug != 'red-bloom').all()
    wgs_json = json.dumps([{
        'name': wg.name,
        'slug': wg.slug,
        'style': wg['style'],
        'color': wg['color']
    } for wg in wgs])
    return dict(wgs=wgs, wgs_json=wgs_json)
