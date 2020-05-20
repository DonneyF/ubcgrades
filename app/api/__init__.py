from flask import Blueprint, g

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.url_value_preprocessor
def check_yearsession(endpoint, values):
    # Fast check for yearsession preprocess
    yearsession = values.get('yearsession', None)
    if yearsession is not None:
        g.bad_yearsession = False
        if len(yearsession) < 5:
            g.bad_yearsession = True
        else:
            g.year = yearsession[0:4]
            g.session = yearsession[4]


from app.api import grades, filters, helpers
