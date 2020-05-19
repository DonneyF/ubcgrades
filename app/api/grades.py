from app.api import bp
from app.models import TableauDashboardGrade, PAIRReportsGrade
from app.api.errors import error_response, bad_request
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound


def get_yearsession(yearsession):
    if len(yearsession) < 5:
        return bad_request("Bad yearsession")

    return yearsession[0:4], yearsession[4]


# Routes for Tableau Dashboard
@bp.route('/v2/grades/<string:campus>/<string:yearsession>', methods=['GET'])
def get_grades_v2_l1(campus, yearsession):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=year, session=session).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_grades_v2_l2(campus, yearsession, subject):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_grades_v2_l3(campus, yearsession, subject, course):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject, course=course).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/grades/<string:campus>/<string:yearsession>/<string:subject>/<string:course>/<string:section>', methods=['GET'])
def get_grades_v2_yearsession_subject_course_section(campus, yearsession, subject, course, section):
    year, session = get_yearsession(yearsession)
    try:
        result = TableauDashboardGrade.query.filter_by(campus=campus, year=year, session=session, subject=subject,
                                                       course=course, section=section).one().to_dict()
        return jsonify(result)
    except NoResultFound:
        return error_response(404, "Not Found")


# Route for PAIR Reports
@bp.route('/v1/grades/<string:campus>/<string:yearsession>', methods=['GET'])
def get_grades_v1_l1(campus, yearsession):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=year, session=session).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_grades_v1_l2(campus, yearsession, subject):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_grades_v1_l3(campus, yearsession, subject, course):
    year, session = get_yearsession(yearsession)
    result = [row.to_dict() for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject, course=course).all()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/grades/<string:campus>/<string:yearsession>/<string:subject>/<string:course>/<string:section>', methods=['GET'])
def get_grades_v1_yearsession_subject_course_section(campus, yearsession, subject, course, section):
    year, session = get_yearsession(yearsession)
    try:
        result = PAIRReportsGrade.query.filter_by(campus=campus, year=year, session=session, subject=subject,
                                                       course=course, section=section).one().to_dict()
        return jsonify(result)
    except NoResultFound:
        return error_response(404, "Not Found")
