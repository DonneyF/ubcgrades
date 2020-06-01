from app.api import bp
from app.models import Course, TableauDashboardGrade as TDG, PAIRReportsGrade as PRG, CourseDistributions as CDist, \
    Professor, CourseAverageHistory
from app.api.errors import error_response, bad_request
from flask import jsonify, g


@bp.route('/v2/course-statistics/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_course_statistics(campus, subject, course):
    result = Course.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).one_or_none()
    return jsonify(result.to_dict()) if result is not None else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/<string:campus>/<string:subject>', methods=['GET'])
def get_course_statistics_no_subject(campus, subject):
    result = [row.to_dict() for row in Course.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/distributions/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_course_distributions(campus, subject, course):
    result = [row.to_dict() for row in CDist.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/distributions/<string:campus>/<string:subject>', methods=['GET'])
def get_course_distributions_no_subject(campus, subject):
    result = [row.to_dict() for row in CDist.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/professors/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_professors(campus, subject, course):
    result = [row.to_dict() for row in Professor.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/professors/<string:campus>/<string:subject>', methods=['GET'])
def get_professors_no_subject(campus, subject):
    result = [row.to_dict() for row in Professor.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/average-history/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_average_history(campus, subject, course):
    result = CourseAverageHistory.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).one_or_none()
    return jsonify(result.to_dict()) if result is not None else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/average-history/<string:campus>/<string:subject>', methods=['GET'])
def get_average_history_no_subject(campus, subject):
    result = [row.to_dict() for row in CourseAverageHistory.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")