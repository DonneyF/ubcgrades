from app.api import bp
from app.models import TableauDashboardGrade as TDG, PAIRReportsGrade as PRG
from app.api.errors import error_response, bad_request
from flask import jsonify, g


# Filters v2
@bp.route('/v2/sections/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_sections_v2(campus, yearsession, subject, course):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    result = [row.section for row in TDG.query.filter_by(
        campus=campus, year=g.year, session=g.session, subject=subject, course=g.course, detail=g.detail).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/courses/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_courses_v2(campus, yearsession, subject):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    query = TDG.query.with_entities(TDG.course, TDG.detail, TDG.course_title).filter_by(
        campus=campus, year=g.year, session=g.session, subject=subject).distinct()
    result = [{
        'course': row.course,
        'detail': row.detail,
        'course_title': row.course_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/courses/<string:campus>/<string:subject>', methods=['GET'])
def get_courses_no_yearsession_v2(campus, subject):
    query = TDG.query.with_entities(TDG.course, TDG.detail, TDG.course_title).filter_by(campus=campus, subject=subject).distinct()
    result = [{
        'course': row.course,
        'detail': row.detail,
        'course_title': row.course_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/subjects/<string:campus>/<string:yearsession>', methods=['GET'])
def get_subjects_v2(campus, yearsession):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    query = TDG.query.with_entities(TDG.subject, TDG.subject_title).filter_by(campus=campus, year=g.year,
                                                                              session=g.session).distinct()
    result = [{
        'subject': row.subject,
        'subject_title': row.subject_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/subjects/<string:campus>', methods=['GET'])
def get_subjects_no_yearsession_v2(campus):
    result = [row.subject for row in TDG.query.with_entities(TDG.subject).filter_by(
        campus=campus).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v2/yearsessions/<string:campus>', methods=['GET'])
def get_yearsessions_v2(campus):
    result = [row.year + row.session.name for row in
              TDG.query.with_entities(TDG.year, TDG.session).filter_by(
                  campus=campus).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


# Filters v2
@bp.route('/v1/sections/<string:campus>/<string:yearsession>/<string:subject>/<string:course>', methods=['GET'])
def get_sections_v1(campus, yearsession, subject, course):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    result = [row.section for row in PRG.query.filter_by(
        campus=campus, year=g.year, session=g.session, subject=subject, course=g.course, detail=g.detail).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/courses/<string:campus>/<string:yearsession>/<string:subject>', methods=['GET'])
def get_courses_v1(campus, yearsession, subject):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    query = PRG.query.with_entities(PRG.course, PRG.course_title).filter_by(campus=campus, year=g.year, session=g.session,
                                                          subject=subject).distinct()
    result = [{
        'course': row.course,
        'course_title': row.course_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/courses/<string:campus>/<string:subject>', methods=['GET'])
def get_courses_no_yearsession_v1(campus, subject):
    query = PRG.query.with_entities(PRG.course, PRG.course_title).filter_by(campus=campus, subject=subject).distinct()
    result = [{
        'course': row.course,
        'course_title': row.course_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/subjects/<string:campus>/<string:yearsession>', methods=['GET'])
def get_subjects_v1(campus, yearsession):
    if g.bad_yearsession:
        return bad_request("Bad yearsession")
    query = PRG.query.with_entities(PRG.subject, PRG.subject_title).filter_by(campus=campus, year=g.year,
                                                                              session=g.session).distinct()
    result = [{
        'subject': row.subject,
        'subject_title': row.subject_title
    } for row in query]
    return jsonify(result) if result != [] else error_response(404, "Not Found")


@bp.route('/v1/yearsessions/<string:campus>', methods=['GET'])
def get_yearsessions_v1(campus):
    result = [row.year + row.session.name for row in PRG.query.with_entities(PRG.year, PRG.session).filter_by(
        campus=campus).distinct()]
    return jsonify(result) if result != [] else error_response(404, "Not Found")
