"""
Preprocessor and data importer for professors and their courses. Uses a combination of PAIR Reports and Tableau
Dashboard data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, Course, Professor, CampusEnum
from multiprocessing import Pool
from nameparser import HumanName
from nameparser.util import u


CAMPUSES = [CampusEnum.UBCV, CampusEnum.UBCO]


class HumanNameHashable(HumanName):
    def __hash__(self):
        return hash((u(self)).lower())


def get_sections_separated(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections_TDG = [row for row in TDG.query.with_entities(TDG.year, TDG.session, TDG.professor, TDG.section).filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject,
                                                                    course=course.course, detail=course.detail)]

    sections_PRG = [row for row in PRG.query.with_entities(PRG.year, PRG.session, PRG.professor, PRG.section).filter(PRG.section != "OVERALL").filter(PRG.year < '2014') \
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail)]

    return sections_TDG, sections_PRG


def main():
    app, db = create_app(Config)
    with app.app_context():
        db.create_all()
        bulk_objects = []
        # In the database, we have a sections -> professor. We wish to create course -> professor, yearsessions they are active
        # Get all the courses
        courses = [row for row in
                   Course.query.with_entities(Course.campus, Course.subject, Course.course, Course.detail).all()]

        # Get all the yearsessions
        year_sessions = set([row for row in TDG.query.with_entities(TDG.year, TDG.session).distinct()])
        year_sessions = year_sessions.union(
            set([row for row in PRG.query.with_entities(PRG.year, PRG.session).distinct()]))

        N = len(courses)
        for index, course in enumerate(courses):
            if index % 100 == 0:
                print(f'{index}/{N}')
            # Get all the sections
            sections_TDG, sections_PRG = get_sections_separated(course)
            # Dictionary that maps a professor to a dictionary that maps a yearsession to the number of sections the
            # professor was active in that yearsession
            prof_map = {}

            # Sections have Professor fields that contain a list of names. Sections from PRG can have names that
            # are in all-caps. We check equality between names using nameparser
            for section in sections_TDG + sections_PRG:
                section_ys = f'{section.year}{section.session.name}'
                prof_str = section.professor
                for prof in prof_str.split(";"):
                    prof_name = HumanNameHashable(prof)
                    if prof_name not in prof_map:
                        prof_map[prof_name] = {}

                    try:
                        prof_map[prof_name][section_ys] += 1
                    except KeyError:
                        prof_map[prof_name][section_ys] = 1

            for prof, ys_map in prof_map.items():
                prof_entry = Professor(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail,
                                       professor=str(prof))

                for yearsession_result in year_sessions:
                    yearsession = f'{yearsession_result.year}{yearsession_result.session.name}'
                    if yearsession in ys_map:
                        setattr(prof_entry, f'ys_{yearsession}', ys_map[yearsession])
                    else:
                        setattr(prof_entry, f'ys_{yearsession}', 0)

                bulk_objects.append(prof_entry)

        db.session.bulk_save_objects(bulk_objects)
        db.session.commit()


if __name__ == '__main__':
    main()