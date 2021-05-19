from app.api import bp
from app.models import TableauDashboardGrade, PAIRReportsGrade
from app.api.errors import error_response, bad_request
from flask import jsonify, g
from sqlalchemy.orm.exc import NoResultFound


# Routes for Tableau Dashboard
@bp.route('/v2/grades/<string:campus>/<yearsession:ys>', methods=['GET'])
def get_grades_v2_l1(campus, ys):
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<yearsession:ys>/<string:subject>', methods=['GET'])
def get_grades_v2_l2(campus, ys, subject):
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<yearsession:ys>/<string:subject>/<string:course>', methods=['GET'])
def get_grades_v2_l3(campus, ys, subject, course):
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<yearsession:ys>/<string:subject>/<string:course>/<string:section>', methods=['GET'])
def get_grades_v2_yearsession_subject_course_section(campus, ys, subject, course, section):
    try:
        result = TableauDashboardGrade.query.filter_by(campus=campus, year=ys.year, session=ys.session, subject=subject,
                                                       course=g.course, detail=g.detail, section=section).one().to_dict()
        return jsonify(result)
    except NoResultFound:
        return error_response(404, "Not Found")


# Route for PAIR Reports
@bp.route('/v1/grades/<string:campus>/<yearsession:ys>', methods=['GET'])
def get_grades_v1_l1(campus, ys):
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<yearsession:ys>/<string:subject>', methods=['GET'])
def get_grades_v1_l2(campus, ys, subject):
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<yearsession:ys>/<string:subject>/<string:course>', methods=['GET'])
def get_grades_v1_l3(campus, ys, subject, course):
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=ys.year, session=ys.session, subject=subject, course=g.course, detail=g.detail).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<yearsession:ys>/<string:subject>/<string:course>/<string:section>', methods=['GET'])
def get_grades_v1_yearsession_subject_course_section(campus, ys, subject, course, section):
    try:
        result = PAIRReportsGrade.query.filter_by(campus=campus, year=ys.year, session=ys.session, subject=subject,
                                                       course=g.course, detail=g.detail, section=section).one().to_dict()
        return jsonify(result)
    except NoResultFound:
        return error_response(404, "Not Found")
