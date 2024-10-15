# Scripts

## Database

These scripts fill the database and perform some computations. They have an order for running:

First, populate the database with the data:
- `fill_tableau_dashboard_v2_grades.py`
- `fill_tableau_dashboard_grades.py`
- `fill_pair_reports_grades.py`

Then run the computational scripts of the API:
- `compute_course_stats.py`
- `compute_course_v2_stats.py`
- `compute_course_educators.py`
- `compute_course_distributions.py`
- `compute_course_average_history.py`