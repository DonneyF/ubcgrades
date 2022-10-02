"""
Preprocessor and data importer for historical course averages. Uses a combination of PAIR Reports and Tableau
Dashboard data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, TableauDashboardV2Grade as TDG2, Course, CourseAverageHistory, CampusEnum
from multiprocessing import Pool


CAMPUSES = [CampusEnum.UBCV, CampusEnum.UBCO]


def get_sections_separated(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections_TDG2 = [row for row in TDG2.query.filter_by(campus=course.campus, subject=course.subject,
                                                       course=course.course, detail=course.detail).all()]
    sections_TDG = [row for row in TDG.query.filter_by(campus=course.campus, subject=course.subject,
                                                                    course=course.course, detail=course.detail, section='OVERALL').all()]

    sections_PRG = [row for row in PRG.query.filter(PRG.section != "OVERALL").filter(PRG.year < '2014') \
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail)]

    return sections_TDG2, sections_TDG, sections_PRG


def compute_weighted_average(year_session_map, sections):
    sections_by_ys = {}
    for section in sections:
        yearsession = f'{section.year}{section.session.name}'
        try:
            sections_by_ys[yearsession].append(section)
        except KeyError:
            sections_by_ys[yearsession] = [section]

    for yearsession, section_list in sections_by_ys.items():
        # For each yearsession, compute the weighted average of the course average
        if section_list and hasattr(section_list[0], 'enrolled'):
            num_students = [section.enrolled - section.audit - section.other - section.withdrew for section in
                            section_list if section.average is not None]
        else:
            num_students = [section.reported for section in section_list if section.average is not None]
        averages = [section.average for section in section_list if section.average is not None]

        if len(averages) == 1:
            year_session_map[yearsession] = averages[0]
        elif len(averages) > 1:
            weighted_average = sum(weight * value for weight, value in zip(num_students, averages)) / sum(num_students)
            year_session_map[yearsession] = weighted_average


def main():
    app, db = create_app(Config)
    with app.app_context():
        db.create_all()
        bulk_objects = []
        # In the database, we have a sections -> educators. We wish to create course -> educators, yearsessions they are active
        # Get all the courses
        courses = [row for row in
                   Course.query.with_entities(Course.campus, Course.subject, Course.course, Course.detail).all()]

        # Get all the yearsessions
        year_sessions = set([row for row in TDG.query.with_entities(TDG.year, TDG.session).distinct()])
        year_sessions = year_sessions.union(
            set([row for row in PRG.query.with_entities(PRG.year, PRG.session).distinct()]))
        year_sessions = year_sessions.union(
            set([row for row in TDG2.query.with_entities(TDG2.year, TDG2.session).distinct()]))

        N = len(courses)
        for index, course in enumerate(courses):
            if index % 100 == 0:
                print(f'{index}/{N}')
            # Get all the sections
            sections_TDG2, sections_TDG, sections_PRG = get_sections_separated(course)
            # Dictionary that maps a yearsession to the average for that yearsession
            year_session_map = {f'{ele.year}{ele.session.name}': '' for ele in year_sessions}

            # TDG sections have OVERALL sections for each yearsession
            for section in sections_TDG:
                yearsession = f'{section.year}{section.session.name}'
                year_session_map[yearsession] = section.average

            # PRG and TDG2 sections do not have OVERALL sections. Manually compute for each yearsession
            # Sort the sections into a map of yearsession -> year
            compute_weighted_average(year_session_map, sections_PRG)
            compute_weighted_average(year_session_map, sections_TDG2)

            # Build our db object to add
            hist_entry = CourseAverageHistory(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail)

            for ys, avg in year_session_map.items():
                setattr(hist_entry, f'ys_{ys}', avg) if avg != '' else setattr(hist_entry, f'ys_{ys}', None)

            bulk_objects.append(hist_entry)

        db.session.bulk_save_objects(bulk_objects)
        db.session.commit()


if __name__ == '__main__':
    main()