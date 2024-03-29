from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/statistics-by-course', methods=['GET'])
def statistics_by_course():
    return render_template('statistics_by_course.html')


# @bp.route('/statistics-by-subject', methods=['GET'])
# def statistics_by_subject():
#     return render_template('statistics_by_subject.html')
#
#
# @bp.route('/statistics-by-faculty', methods=['GET'])
# def statistics_by_faculty():
#     return render_template('statistics_by_faculty.html')

@bp.route('/about-help', methods=['GET'])
def about_help():
    return render_template('about_help.html')


@bp.route('/api-reference', methods=['GET'])
def api_index():
    return render_template('api/api_index.html')


@bp.route('/api-reference/v1', methods=['GET'])
def api_v1():
    return render_template('api/v1.html')


@bp.route('/api-reference/v2', methods=['GET'])
def api_v2():
    return render_template('api/v2.html')


@bp.route('/api-reference/v3', methods=['GET'])
def api_v3():
    return render_template('api/v3.html')
