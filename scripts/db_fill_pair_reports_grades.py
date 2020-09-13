"""
Preprocessor and data importer from Pair Reports data. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade, CampusEnum, SessionEnum
import os
import re
import json
import csv
from sqlalchemy.exc import StatementError


def load_data(path_to_csv_files):
    # Load all the CSVs into an array
    sections = []
    for dirpath, subdirs, csv_files in os.walk(path_to_csv_files):
        for csv_file in csv_files:
            csv_reader = csv.DictReader(open(os.path.join(dirpath, csv_file)))
            # Convert to normal dictionaries
            input_file = [dict(ele) for ele in csv_reader]
            # Remove dictionaries that are key:value identical.
            input_file = [i for n, i in enumerate(input_file) if i not in input_file[n + 1:]]
            for row in input_file:
                sections.append(row)

    return sections


def fix_educators(path_to_corrections_file, sections):
    # There is an edge-case wherein two rows differ by an instructor, but one entry has an empty instructor

    educator_corrections = json.load(open(path_to_corrections_file, 'r'))
    # Begin by constructing a dictionary that maps the unqiue ID to a list of instructors for that ID
    id_educators = {}
    for entry in sections:
        yearsession = "{}{}".format(entry['Year'], entry['Session'])
        # Guarantee uniqueness of rows by constructing an ID based on key elements
        id = "{}-{}-{}{}-{}".format(yearsession, entry['Subject'].strip(), entry['Course'], entry['Detail'].strip(),
                                    entry['Section'].strip())
        try:
            id_educators[id].append(entry['Educator'])
        except KeyError:
            id_educators[id] = [entry['Educator']]

    # Loop through the values of the dicionary, and ensure there is at most 2 entries for every ID
    # Build a dictionary that maps an ID to a single instructor
    id_educator = {}
    id_instructor_duplicates = []
    for id, educators in id_educators.items():
        # Remove all duplicate instructors
        educators = list(set(educators))
        # Remove all the entries in the array that are ""
        educators = [educator for educator in educators if educator != '']
        if len(educators) == 0:
            # All entries are just ""
            id_educator[id] = ""
        elif len(educators) == 1:
            id_educator[id] = educators[0]
        else:
            # There are multiple instructor-strings for a single ID.
            # Solution: Look up the section on UBC pair and manually override the correct instructor
            try:
                # Prefix UBC campus as that's the only available data source
                id_educator[id] = educator_corrections["UBC-" + id]
            except KeyError:
                print("{} has {} non-empty entries:\n".format(id, len(educators)) + "".join(educators))
                exit()

    # Now loop through the original section array and remove the entries th
    ids = {}
    temp_sections = []
    for entry in sections:
        yearsession = "{}{}".format(entry['Year'], entry['Session'])
        # Guarantee uniqueness of rows by constructing an ID based on key elements
        id = "{}-{}-{}{}-{}".format(yearsession, entry['Subject'].strip(), entry['Course'], entry['Detail'].strip(),
                                    entry['Section'].strip())

        # Loop through our original array of sections and build a new array that overrides the instructor
        # and is now unique on the ID
        if id not in ids:
            ids[id] = 0
            entry['Educator'] = id_educator[id]
            temp_sections.append(entry)

    return temp_sections


def remove_overall_sections(sections):
    # The original CSVs do not generate OVERALL sections for courses with details, only for the entire course.
    # It generally does not make sense to consider an OVERALL Section for a course with detail, as each detail
    # may have entirely different focus and course content. Even with a course having one regular section and
    # one OVERALL section, there are discrepancies. Therefore it would be incorrect to say regular == OVERALL
    # in this case. The decision here is to remove OVERALL sections.

    return [section for section in sections if section['Section'] != 'OVERALL']


def main():
    path_to_csv_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'ubc-pair-grade-data',
                                     'pair-reports', 'UBC')
    path_to_correction_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'ubc-pair-grade-data',
                                           'pair-reports', 'UBC-instructor-corrections.json')
    sections = load_data(path_to_csv_files)
    sections = remove_overall_sections(sections)
    sections = fix_educators(path_to_correction_file, sections)

    app, db = create_app(Config)

    missing = set()

    with app.app_context():
        db.create_all()

        # Build subject dict
        extra = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'ubc-pair-grade-data', 'extra')
        subjects = {}
        for file in ['UBCV_subjects.json']:
            for subject in json.load(open(os.path.join(extra, file), 'r')):
                subjects.update({f'{file[0:3]}-{subject["code"]}': subject})

        for section in sections:
            campus = CampusEnum.UBCV
            session = SessionEnum.W if section['Session'] == "W" else SessionEnum.S
            average = None if section['Avg'] == '' else section['Avg']
            stdev = None if section['Std dev'] == '' else section['Std dev']
            subject_key = f'{section["Campus"]}-{section["Subject"].strip()}'
            entry = PAIRReportsGrade(campus=campus, year=section['Year'], session=session,
                                                  faculty_title=subjects[subject_key]['faculty_school'],
                                                  subject=section['Subject'].strip(),
                                                  subject_title=subjects[subject_key]['title'],
                                                  course=section['Course'], detail=section['Detail'].strip(),
                                                  section=section['Section'],
                                                  course_title=section['Title'], educators=section['Educator'],
                                     enrolled=section['Enrolled'], average=average,
                                     stdev=stdev, high=section['High'], low=section['Low'],
                                     num_pass=section['Pass'], num_fail=section['Fail'],
                                     withdrew=section['Withdrew'], audit=section['Audit'], other=section['Other'],
                                     grade_0_9=section['0-9'],
                                     grade_10_19=section['10-19'], grade_20_29=section['20-29'],
                                     grade_30_39=section['30-39'],
                                     grade_40_49=section['40-49'], grade_lt50=section['<50'],
                                     grade_50_54=section['50-54'],
                                     grade_55_59=section['55-59'],
                                     grade_60_63=section['60-63'], grade_64_67=section['64-67'],
                                     grade_68_71=section['68-71'], grade_72_75=section['72-75'],
                                     grade_76_79=section['76-79'], grade_80_84=section['80-84'],
                                     grade_85_89=section['85-89'], grade_90_100=section['90-100'])
            db.session.add(entry)
        db.session.commit()



if __name__ == "__main__":
    main()
