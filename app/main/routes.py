from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', header_card_text="View Grades")


@bp.route('/statistics-by-course', methods=['GET'])
def statistics_by_course():
    return render_template('statistics_by_course.html', header_card_text="Statistics by Course")
