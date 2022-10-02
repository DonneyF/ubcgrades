# Scripts

## Database (`db_`)

These scripts fill the database and perform some computations. They have an order for running:

First, populate the database with the data:
- `db_fill_tableau_dashboard_v2_grades.py`
- `db_fill_tableau_dashboard_grades.py`
- `db_fill_pair_reports_grades.py`

Then run the computational scripts of the API:
- `db_compute_course_stats.py`
- `db_compute_course_v2_stats.py`
- `db_fill_course_educators.py`
- `db_fill_course-distributions.py`
- `db_fill_course_average_history.py`