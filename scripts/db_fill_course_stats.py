"""
Preprocessor and data importer from Pair Reports data. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, Course
import math
import re
import json
import csv
from sqlalchemy.exc import StatementError


def get_sections_combined(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections = []
    for row in TDG.query.filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    for row in PRG.query.filter(PRG.section != "OVERALL").filter(PRG.year < '2014')\
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail):
        sections.append(row)

    return sections


def composite_SD(means, SDs, ncounts):
    '''Calculate combined standard deviation via ANOVA (ANalysis Of VAriance)
       See:  http://www.burtonsys.com/climate/composite_standard_deviations.html
       Inputs are:
         means, the array of group means
         SDs, the array of group standard deviations
         ncounts, number of samples in each group (can be scalar
                  if all groups have same number of samples)
       Result is the overall standard deviation.
    '''
    G = len(means)  # number of groups
    if G != len(SDs):
        raise Exception('inconsistent list lengths')
    if not hasattr(ncounts, '__contains__'):
        ncounts = [ncounts] * G  # convert scalar ncounts to array
    elif G != len(ncounts):
        raise Exception('wrong ncounts list length')

    # calculate total number of samples, N, and grand mean, GM
    N = sum(ncounts)  # total number of samples
    if N <= 1:
        raise Exception("Warning: only " + str(N) + " samples, SD is incalculable")
    GM = 0.0
    for i in range(G):
        GM += means[i] * ncounts[i]
    GM /= N  # grand mean

    # calculate Error Sum of Squares
    ESS = 0.0
    for i in range(G):
        ESS += ((SDs[i])**2) * (ncounts[i] - 1)

    # calculate Total Group Sum of Squares
    TGSS = 0.0
    for i in range(G):
        TGSS += ((means[i]-GM)**2) * ncounts[i]

    # calculate standard deviation as square root of grand variance
    result = math.sqrt((ESS+TGSS)/(N-1))
    return result


def compute_average_stdev(sections):
    """
    :param sections: Type: [sqlalchemy.util._collections.result]
    :return: Cumulative weighted average and standard deviation
    """

    # Construct a list of pairs with the average and the number of students
    averages = [section.average for section in sections]
    num_students = []
    stdevs = [section.stdev for section in sections]
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

        return weighted_average, composite_stdev


def main():
    app, db = create_app(Config)
    with app.app_context():
        db.create_all()

        # First get a set of all the courses
        courses = set()  # Set of sqlalchemy.util._collections.result
        for row in TDG.query.with_entities(TDG.campus, TDG.faculty_title, TDG.subject, TDG.subject_title,
                                           TDG.course, TDG.course_title, TDG.detail).distinct():
            courses.add(row)

        for row in PRG.query.with_entities(PRG.campus, PRG.faculty_title, PRG.subject, PRG.subject_title,
                                           PRG.course, PRG.course_title, PRG.detail).filter(PRG.year < '2014').distinct():
            courses.add(row)

        for course in courses:
            sections = get_sections_combined(course)

            # Compute the average and standard deviation
            avg, stdev = compute_average_stdev(sections)

            averages = [section.average for section in sections if section.average is not None]
            max_course_avg = max(averages) if averages else None
            min_course_avg = min(averages) if averages else None

            new_entry = Course(campus=course.campus, faculty_title=course.faculty_title, subject=course.subject,
                               subject_title=course.subject_title, course=course.course, course_title=course.course_title,
                               detail=course.detail, average=avg, stdev=stdev, max_course_avg=max_course_avg,
                               min_course_avg=min_course_avg)

            db.session.add(new_entry)

        db.session.commit()


if __name__ == "__main__":
    main()
