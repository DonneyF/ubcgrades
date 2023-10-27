"""
Preprocessor and data importer from course distributions by yearsessions. Uses a combination of PAIR Reports and Tableau
Dashboard data. This depends on having complete distributions available
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, TableauDashboardV2Grade as TDG2, CourseV2, CourseDistributions, CampusEnum
import multiprocessing
import tqdm
from functools import partial

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
    for row in TDG2.query.filter(TDG2.year >= '2022').filter(TDG2.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in TDG.query.filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in PRG.query.filter(PRG.section != "OVERALL").filter(PRG.year < '2014')\
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    return sections


def init_worker():
    global shared_app, shared_db
    shared_app, shared_db = create_app(Config)


def process_course(year_sessions, course):
    with shared_app.app_context():
        results = []
        # Get all the sections
        sections = get_sections_combined(course)

        # Sum all the grades for the year and campus
        for campus in CAMPUSES:
            for year, session in year_sessions:
                # Get the relevant sections
                sections_to_compute = [section for section in sections if
                                       section.year == year and section.session == session
                                       and section.campus == campus]

                if not sections_to_compute:
                    continue
                subject = sections_to_compute[0].subject
                if year >= '2014':
                    # TDG and TDG2 grades do not have any entries for sub-50%
                    grades = {key: '' for key in GRADES_V2}
                    for section in sections_to_compute:
                        for item, val in section.to_dict()['grades'].items():
                            if grades[item] == '' and val is not None:
                                grades[item] = val
                            elif grades[item] != '' and val is not None:
                                grades[item] += val
                    entry = CourseDistributions(campus=campus, subject=subject,
                                                year=year, session=session,
                                                course=course.course, detail=course.detail,
                                                grade_0_9=None,
                                                grade_10_19=None,
                                                grade_20_29=None,
                                                grade_30_39=None,
                                                grade_40_49=None,
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
                    results.append(entry)
                else:
                    # Use PRG
                    grades = {key: 0 for key in GRADES_V1}
                    for section in sections_to_compute:
                        for item, val in section.to_dict()['grades'].items():
                            grades[item] += val
                    entry = CourseDistributions(campus=campus, subject=subject,
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

                    results.append(entry)
        return results


def main():
    global shared_app, shared_db
    shared_app, shared_db = create_app(Config)
    with shared_app.app_context():
        shared_db.create_all()

        # Get all the courses
        courses = [row for row in CourseV2.query.with_entities(CourseV2.campus, CourseV2.subject, CourseV2.course, CourseV2.detail).all()]

        # Get all the yearsessions
        year_sessions = set([row for row in TDG.query.with_entities(TDG.year, TDG.session).distinct()])
        year_sessions = year_sessions.union(
            set([row for row in TDG2.query.with_entities(TDG2.year, TDG2.session).distinct()]))
        year_sessions = year_sessions.union(
            set([row for row in PRG.query.with_entities(PRG.year, PRG.session).distinct()]))

        num_processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_processes, initializer=init_worker)
        pool_results = []

        for result_set in tqdm.tqdm(pool.imap(partial(process_course, year_sessions), courses), total=len(courses)):
            pool_results.extend(result_set)

        pool.close()
        pool.join()

        shared_db.session.bulk_save_objects(pool_results)
        shared_db.session.commit()


if __name__ == '__main__':
    main()
