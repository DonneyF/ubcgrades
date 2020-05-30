from flask import Blueprint, g

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.url_value_preprocessor
def url_preprocessor(endpoint, values):
    # Fast check for yearsession preprocess
    yearsession = values.get('yearsession', None)
    if yearsession is not None:
        g.bad_yearsession = False
        if len(yearsession) < 5:
            g.bad_yearsession = True
        else:
            g.year = yearsession[0:4]
            g.session = yearsession[4]

    # Fast check for course detail
    course_detail = values.get('course', None)
    if course_detail is not None:
        if course_detail[-1].isalpha():
            g.course = course_detail[:-1]
            g.detail = course_detail[-1]
        else:
            g.course = course_detail
            g.detail = ''



from app.api import grades, filters, helpers, course_statistics
