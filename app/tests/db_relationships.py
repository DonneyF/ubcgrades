"""
Imports data from Tableau Dashboard into the database. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import TableauDashboardGrade, Subjects
import unittest


class TestCase(unittest.TestCase):

    def test_relationship(self):
        app, db = create_app(Config)

        with app.app_context():
            subject = Subjects.query.filter_by(subject_code="MATH", campus="UBCV").one()
            entry = TableauDashboardGrade(campus="UBCV", year="2018", session="W",
                                          subject=subject, course="201", detail="", section="102")
            db.session.add(entry)

            section = TableauDashboardGrade.query.filter_by(subject_code="MATH").first()

            self.assertEqual(section.subject.subject_code, "MATH")
            self.assertEqual(section.subject.faculty_title, "Faculty of Science")
            print(subject.sections)


if __name__ == "__main__":
    unittest.main()
