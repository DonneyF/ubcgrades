from app.api import bp
from app.models import TableauDashboardGrade, PAIRReportsGrade
from app.api.errors import error_response, bad_request
from flask import jsonify


def get_yearsession(yearsession):
    if len(yearsession) < 5:
        return bad_request("Bad yearsession")

    return yearsession[0:4], yearsession[4]


# Filters v2
@bp.route('/v2/sections/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_sections_v2(campus, yearsession, subject, course):
    year, session = get_yearsession(yearsession)
    result = [row.section for row in TableauDashboardGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject, course=course).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/courses/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_courses_v2(campus, yearsession, subject):
    year, session = get_yearsession(yearsession)
    result = [row.course for row in TableauDashboardGrade.query.with_entities(TableauDashboardGrade.course).filter_by(
        campus=campus, year=year, session=session, subject=subject).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/courses/<string:campus>/<string:subject>', methods=['GET'])
def get_courses_no_yearsession_v2(campus, subject):
    result = [row.course for row in
              TableauDashboardGrade.query.with_entities(TableauDashboardGrade.course).filter_by(
                  campus=campus, subject=subject).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/subjects/<string:campus>/<string:yearsession>', methods=['GET'])
def get_subjects_v2(campus, yearsession):
    year, session = get_yearsession(yearsession)
    result = [row.subject for row in
              TableauDashboardGrade.query.with_entities(TableauDashboardGrade.subject).filter_by(
                  campus=campus, year=year, session=session).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/yearsessions/<string:campus>', methods=['GET'])
def get_yearsessions_v2(campus):
    result = [row.year + row.session.name for row in TableauDashboardGrade.query.with_entities(TableauDashboardGrade.year,
        TableauDashboardGrade.session).filter_by(campus=campus).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


# Filters v2
@bp.route('/v1/sections/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_sections_v1(campus, yearsession, subject, course):
    year, session = get_yearsession(yearsession)
    result = [row.section for row in PAIRReportsGrade.query.filter_by(
        campus=campus, year=year, session=session, subject=subject, course=course).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/courses/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_courses_v1(campus, yearsession, subject):
    year, session = get_yearsession(yearsession)
    result = [row.course for row in PAIRReportsGrade.query.with_entities(PAIRReportsGrade.course).filter_by(
        campus=campus, year=year, session=session, subject=subject).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/courses/<string:campus>/<string:subject>', methods=['GET'])
def get_courses_no_yearsession_v1(campus, subject):
    result = [row.course for row in PAIRReportsGrade.query.with_entities(PAIRReportsGrade.course).filter_by(
                  campus=campus, subject=subject).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/subjects/<string:campus>/<string:yearsession>', methods=['GET'])
def get_subjects_v1(campus, yearsession):
    year, session = get_yearsession(yearsession)
    result = [row.subject for row in PAIRReportsGrade.query.with_entities(PAIRReportsGrade.subject).filter_by(
                  campus=campus, year=year, session=session).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/yearsessions/<string:campus>', methods=['GET'])
def get_yearsessions_v1(campus):
    result = [row.year + row.session.name for row in PAIRReportsGrade.query.with_entities(PAIRReportsGrade.year,
        PAIRReportsGrade.session).filter_by(campus=campus).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")
