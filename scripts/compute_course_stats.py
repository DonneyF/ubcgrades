"""
Computes the course stats for Pair Grades and Tableau Dashboard v1
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, Course
import math
import tqdm
import multiprocessing
from tools import composite_SD

PAST_5_YEARS = set(str(i) for i in range(2015, 2022))  # Update on each new Winter session release of grades


def get_sections_combined(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections = []
    for row in TDG.query.filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in PRG.query.filter(PRG.section != "OVERALL").filter(PRG.year < '2014') \
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    return sections



def compute_average_stdev(sections, averages):
    """
    :param sections: Type: [sqlalchemy.util._collections.result]
    :return: Cumulative weighted average and standard deviation
    """

    # Construct a list of pairs with the average and the number of students
    num_students = []
    stdevs = [section.stdev for section in sections if section.average is not None]
    for section in sections:
        if section.average is None:
            continue

        if section.__tablename__ == "PAIRReportsGrade":
            num_students.append(section.enrolled - section.audit - section.other - section.withdrew)
        else:
            num_students.append(section.enrolled)

    # Compute
    if len(averages) == 0:
        return None, None
    elif len(averages) == 1:
        return averages[0], stdevs[0]
    else:
        # Compute the weighted average
        N = sum(num_students)
        weighted_average = sum(weight * value for weight, value in zip(num_students, averages)) / N

        # Compute the standard deviation of combined samples.
        composite_stdev = composite_SD(averages, stdevs, num_students)

        if N == 0:
            print(None)
            exit()

        return weighted_average, composite_stdev


def compute_average_past_5_years(sections):
    averages = [section.average for section in sections if section.year in PAST_5_YEARS if section.average is not None]
    num_students = [section.enrolled for section in sections if section.year in PAST_5_YEARS if section.average is not None]

    if sum(num_students) > 0:
        weighted_average = sum(weight * value for weight, value in zip(num_students, averages)) / sum(num_students)
    else:
        weighted_average = None

    return weighted_average


def init_worker():
    global shared_app, shared_db
    shared_app, shared_db = create_app(Config)


def process_course(course):
    with shared_app.app_context():
        sections = get_sections_combined(course)
        averages = [section.average for section in sections if section.average is not None]

        # Compute the average and standard deviation
        avg, stdev = compute_average_stdev(sections, averages)
        avg_past_5_yrs = compute_average_past_5_years(sections)

        max_course_avg = max(averages) if averages else None
        min_course_avg = min(averages) if averages else None

        # Get newest metadata
        meta = TDG.query.with_entities(TDG.faculty_title, TDG.course_title, TDG.subject_title)\
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail).first()

        if meta is None:
            meta = PRG.query.with_entities(PRG.faculty_title, PRG.course_title, PRG.subject_title) \
                .filter_by(campus=course.campus, subject=course.subject, course=course.course,
                           detail=course.detail).first()

        entry = Course(campus=course.campus, faculty_title=meta.faculty_title, subject=course.subject,
                       subject_title=meta.subject_title, course=course.course, course_title=meta.course_title,
                       detail=course.detail, average=avg, average_past_5_yrs=avg_past_5_yrs, stdev=stdev,
                       max_course_avg=max_course_avg, min_course_avg=min_course_avg)

        return entry


def main():
    global shared_app, shared_db
    shared_app, shared_db = create_app(Config)

    # First get a set of all the courses
    courses = set()  # Set of sqlalchemy.util._collections.result
    with shared_app.app_context():
        shared_db.create_all()
        for row in TDG.query.with_entities(TDG.campus, TDG.subject, TDG.course, TDG.detail).distinct():
            courses.add(row)

        for row in PRG.query.with_entities(PRG.campus, PRG.subject, PRG.course, PRG.detail).filter(PRG.year < '2014').distinct():
            courses.add(row)

        num_processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=num_processes, initializer=init_worker)
        pool_results = list(tqdm.tqdm(pool.imap(process_course, courses), total=len(courses)))
        pool.close()
        pool.join()

        shared_db.session.bulk_save_objects(pool_results)
        shared_db.session.commit()


if __name__ == "__main__":
    main()
