"""
Preprocessor and data importer from Pair Reports data. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, TableauDashboardV2Grade as TDG2, CourseV2
import math
import re
import json
import csv
from sqlalchemy.exc import StatementError

PAST_5_YEARS = set(str(i) for i in range(2015, 2022))  # Update on each new Winter session release of grades

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

def compute_average_past_5_years(sections):
    averages = [section.average for section in sections if section.year in PAST_5_YEARS if section.average is not None]
    num_students = [section.enrolled for section in sections if section.year in PAST_5_YEARS if section.average is not None]

    if sum(num_students) > 0:
        weighted_average = sum(weight * value for weight, value in zip(num_students, averages)) / sum(num_students)
    else:
        weighted_average = None

    return weighted_average


def compute_average(sections, averages):
    """
    :param sections: Type: [sqlalchemy.util._collections.result]
    :return: Cumulative weighted average
    """

    # Construct a list of pairs with the average and the number of students
    num_students = []
    for section in sections:
        if section.average is None:
            continue

        if section.__tablename__ == "PAIRReportsGrade":
            num_students.append(section.enrolled - section.audit - section.other - section.withdrew)
        elif section.__tablename__ == 'TableauDashboardGrade':
            num_students.append(section.enrolled)
        else:
            num_students.append(section.reported)

    # Compute
    if len(averages) == 0:
        return None
    elif len(averages) == 1:
        return averages[0]
    else:
        # Compute the weighted average
        N = sum(num_students)
        weighted_average = sum(weight * value for weight, value in zip(num_students, averages)) / N

        if N == 0:
            print(None)
            exit()

        return weighted_average

def main():
    app, db = create_app(Config)
    with app.app_context():
        bulk_objects = []
        db.create_all()

        # First get a set of all the courses
        courses = set()  # Set of sqlalchemy.util._collections.result
        for row in TDG2.query.with_entities(TDG2.campus, TDG2.subject, TDG2.course, TDG2.detail).filter(TDG2.year > '2021').distinct():
            courses.add(row)

        for row in TDG.query.with_entities(TDG.campus, TDG.subject, TDG.course, TDG.detail).distinct():
            courses.add(row)

        for row in PRG.query.with_entities(PRG.campus, PRG.subject, PRG.course, PRG.detail).filter(PRG.year < '2014').distinct():
            courses.add(row)

        N = len(courses)
        for index, course in enumerate(courses):
            if index % 100 == 0:
                print(f'{index}/{N}')
            sections = get_sections_combined(course)
            averages = [section.average for section in sections if section.average is not None]

            # Compute the average
            avg = compute_average(sections, averages)
            avg_past_5_yrs = compute_average_past_5_years(sections)

            max_course_avg = max(averages) if averages else None
            min_course_avg = min(averages) if averages else None

            # Get newest metadata
            meta = TDG2.query.with_entities(TDG2.faculty_title, TDG2.course_title, TDG2.subject_title)\
                .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail).first()

            if meta is None:
                meta = TDG.query.with_entities(TDG.faculty_title, TDG.course_title, TDG.subject_title)\
                    .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail).first()

            if meta is None:
                meta = PRG.query.with_entities(PRG.faculty_title, PRG.course_title, PRG.subject_title) \
                    .filter_by(campus=course.campus, subject=course.subject, course=course.course,
                               detail=course.detail).first()

            new_entry = CourseV2(campus=course.campus, faculty_title=meta.faculty_title, subject=course.subject,
                               subject_title=meta.subject_title, course=course.course, course_title=meta.course_title,
                               detail=course.detail, average=avg, average_past_5_yrs=avg_past_5_yrs,
                               max_course_avg=max_course_avg, min_course_avg=min_course_avg)

            bulk_objects.append(new_entry)

        db.session.bulk_save_objects(bulk_objects)
        db.session.commit()


if __name__ == "__main__":
    main()
