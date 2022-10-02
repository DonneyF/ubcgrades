"""
Preprocessor and data importer from course distributions by yearsessions. Uses a combination of PAIR Reports and Tableau
Dashboard data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, TableauDashboardV2Grade as TDG2, CourseV2, CourseDistributions, CampusEnum
from multiprocessing import Pool

GRADES_V1 = ["0-9%", "10-19%", "20-29%", "30-39%", "40-49%", "<50%", "50-54%", "55-59%", "60-63%", "64-67%", "68-71%",
             "72-75%", "76-79%", "80-84%", "85-89%", "90-100%"]
GRADES_V2 = ["<50%", "50-54%", "55-59%", "60-63%", "64-67%", "68-71%", "72-75%", "76-79%", "80-84%", "85-89%",
             "90-100%"]
CAMPUSES = [CampusEnum.UBCV, CampusEnum.UBCO]


def get_sections_combined(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections = []
    for row in TDG2.query.filter(TDG2.year >= '2022').filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in TDG.query.filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in PRG.query.filter(PRG.section != "OVERALL").filter(PRG.year < '2014')\
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    return sections


def main():
    app, db = create_app(Config)
    with app.app_context():
        db.create_all()

        # Get all the courses
        courses = [row for row in CourseV2.query.with_entities(CourseV2.campus, CourseV2.subject, CourseV2.course, CourseV2.detail).all()]

        # Get all the yearsessions
        year_sessions = set([row for row in TDG.query.with_entities(TDG.year, TDG.session).distinct()])
        year_sessions = year_sessions.union(
            set([row for row in TDG2.query.with_entities(TDG2.year, TDG2.session).distinct()]))
        year_sessions = year_sessions.union(
            set([row for row in PRG.query.with_entities(PRG.year, PRG.session).distinct()]))

        for course in courses:  # (actually course + detail)
            # Get all the sections
            sections = get_sections_combined(course)

            # Sum all the grades for the year and campus
            for campus in CAMPUSES:
                for year, session in year_sessions:
                    # Get the relevant sections
                    sections_to_compute = [section for section in sections if
                                           section.year == year and section.session == session
                                           and section.campus == campus]
                    if len(sections_to_compute) == 1:
                        section = sections_to_compute[0]
                        if year >= '2014':
                            new_entry = CourseDistributions(campus=campus, subject=section.subject,
                                                            year=year, session=session,
                                                            course=course.course, detail=course.detail,
                                                            grade_0_9='', grade_10_19='', grade_20_29='',
                                                            grade_30_39='', grade_40_49='',
                                                            grade_lt50=section.grade_lt50,
                                                            grade_50_54=section.grade_50_54,
                                                            grade_55_59=section.grade_55_59,
                                                            grade_60_63=section.grade_60_63,
                                                            grade_64_67=section.grade_64_67,
                                                            grade_68_71=section.grade_68_71,
                                                            grade_72_75=section.grade_72_75,
                                                            grade_76_79=section.grade_76_79,
                                                            grade_80_84=section.grade_80_84,
                                                            grade_85_89=section.grade_85_89,
                                                            grade_90_100=section.grade_90_100)
                        else:
                            new_entry = CourseDistributions(campus=campus, subject=section.subject,
                                                            year=year, session=session,
                                                            course=course.course, detail=course.detail,
                                                            grade_0_9=section.grade_0_9,
                                                            grade_10_19=section.grade_10_19,
                                                            grade_20_29=section.grade_20_29,
                                                            grade_30_39=section.grade_30_39,
                                                            grade_40_49=section.grade_40_49,
                                                            grade_lt50=section.grade_lt50,
                                                            grade_50_54=section.grade_50_54,
                                                            grade_55_59=section.grade_55_59,
                                                            grade_60_63=section.grade_60_63,
                                                            grade_64_67=section.grade_64_67,
                                                            grade_68_71=section.grade_68_71,
                                                            grade_72_75=section.grade_72_75,
                                                            grade_76_79=section.grade_76_79,
                                                            grade_80_84=section.grade_80_84,
                                                            grade_85_89=section.grade_85_89,
                                                            grade_90_100=section.grade_90_100)
                        db.session.add(new_entry)

                    elif len(sections_to_compute) > 1:
                        grades = {key: '' for key in GRADES_V1}
                        section = sections_to_compute[0]
                        for section in sections_to_compute:
                            for item, val in section.to_dict()['grades'].items():
                                if grades[item] == '' and val != '':
                                    grades[item] = val
                                elif grades[item] != '' and val != '':
                                    grades[item] += val

                        new_entry = CourseDistributions(campus=campus, subject=section.subject,
                                                        year=year, session=session,
                                                        course=course.course, detail=course.detail,
                                                        grade_0_9=grades['0-9%'],
                                                        grade_10_19=grades['10-19%'],
                                                        grade_20_29=grades['20-29%'],
                                                        grade_30_39=grades['30-39%'],
                                                        grade_40_49=grades['40-49%'],
                                                        grade_lt50=grades['<50%'],
                                                        grade_50_54=grades['50-54%'],
                                                        grade_55_59=grades['55-59%'],
                                                        grade_60_63=grades['60-63%'],
                                                        grade_64_67=grades['64-67%'],
                                                        grade_68_71=grades['68-71%'],
                                                        grade_72_75=grades['72-75%'],
                                                        grade_76_79=grades['76-79%'],
                                                        grade_80_84=grades['80-84%'],
                                                        grade_85_89=grades['85-89%'],
                                                        grade_90_100=grades['90-100%'])

                        db.session.add(new_entry)

        db.session.commit()


if __name__ == '__main__':
    main()
