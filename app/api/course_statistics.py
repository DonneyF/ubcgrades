from app.api import bp
from app.models import Course, CourseV2, CourseDistributions as CDist, \
    Educator, CourseAverageHistory
from app.api.errors import error_response, bad_request
from flask import jsonify, g

deselected_cols = {'campus', 'detail', 'course', 'subject'}

#
# Version 3
#

@bp.route('/v3/course-statistics/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_course_statistics_v3(campus, subject, course):
    result = CourseV2.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).one_or_none()
    return jsonify(result.to_dict()) if result is not None else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/<string:campus>/<string:subject>', methods=['GET'])
def get_course_statistics_no_subject_v3(campus, subject):
    result = [row.to_dict() for row in CourseV2.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/distributions/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_course_distributions_v3(campus, subject, course):
    result = [row.to_dict() for row in CDist.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/distributions/<string:campus>/<string:subject>', methods=['GET'])
def get_course_distributions_no_subject_v3(campus, subject):
    result = [row.to_dict() for row in CDist.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/teaching-team/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_professors_v3(campus, subject, course):
    result = [row.to_dict() for row in Educator.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/teaching-team/<string:campus>/<string:subject>', methods=['GET'])
def get_professors_no_subject_v3(campus, subject):
    result = [row.to_dict() for row in Educator.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/average-history/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_average_history_v3(campus, subject, course):
    result = CourseAverageHistory.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).one_or_none()
    return jsonify(result.to_dict()) if result is not None else error_response(404, "Not Found")


@bp.route('/v3/course-statistics/average-history/<string:campus>/<string:subject>', methods=['GET'])
def get_average_history_no_subject_v2(campus, subject):
    result = [row.to_dict() for row in CourseAverageHistory.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")

#
# Version 2
#

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


@bp.route('/v2/course-statistics/teaching-team/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_professors(campus, subject, course):
    result = [row.to_dict() for row in Educator.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/teaching-team/<string:campus>/<string:subject>', methods=['GET'])
def get_professors_no_subject(campus, subject):
    result = [row.to_dict() for row in Educator.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/average-history/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_average_history(campus, subject, course):
    result = CourseAverageHistory.query.filter_by(campus=campus, subject=subject, course=g.course, detail=g.detail).one_or_none()
    return jsonify(result.to_dict()) if result is not None else error_response(404, "Not Found")


@bp.route('/v2/course-statistics/average-history/<string:campus>/<string:subject>', methods=['GET'])
def get_average_history_no_subject(campus, subject):
    result = [row.to_dict() for row in CourseAverageHistory.query.filter_by(campus=campus, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")