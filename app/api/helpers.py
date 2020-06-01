#
# Website specific endpoints. Not for general use.
#

from app.api import bp
from app.models import TableauDashboardGrade, PAIRReportsGrade
from app.api.errors import error_response, bad_request
from flask import jsonify, g


recent_section_averages_keys = ['campus', 'year', 'session', 'average']


# Retrieve up to five most recently populated section averages
@bp.route('/recent-section-averages/<string:campus>/<string:subject>/<string:course>', methods=['GET'])
def get_recent_section_averages(campus, subject, course):
    result = [row for row in TableauDashboardGrade.query.filter_by(
        campus=campus, subject=subject, course=g.course, detail=g.detail).filter(TableauDashboardGrade.section != "OVERALL")
        .order_by(TableauDashboardGrade.year.desc()).limit(5).all()]

    # Then convert to dictionaries
    result = [{
        'campus': entry.campus.name,
        'year': entry.year,
        'session': entry.session.name,
        'course': entry.course,
        'detail': entry.detail,
        'section': entry.section,
        'average': entry.average
    } for entry in result]
    return jsonify(result) if result != [] else error_response(404, "Not Found")
