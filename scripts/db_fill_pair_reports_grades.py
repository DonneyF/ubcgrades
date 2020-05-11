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


def fix_professors(path_to_corrections_file, sections):
    # There is an edge-case wherein two rows differ by an instructor, but one entry has an empty instructor

    professor_corrections = json.load(open(path_to_corrections_file, 'r'))
    # Begin by constructing a dictionary that maps the unqiue ID to a list of instructors for that ID
    id_professors = {}
    for entry in sections:
        yearsession = "{}{}".format(entry['Year'], entry['Session'])
        # Guarantee uniqueness of rows by constructing an ID based on key elements
        id = "{}-{}-{}{}-{}".format(yearsession, entry['Subject'].strip(), entry['Course'], entry['Detail'].strip(),
                                    entry['Section'].strip())
        try:
            id_professors[id].append(entry['Professor'])
        except KeyError:
            id_professors[id] = [entry['Professor']]

    # Loop through the values of the dicionary, and ensure there is at most 2 entries for every ID
    # Build a dictionary that maps an ID to a single instructor
    id_professor = {}
    id_instructor_duplicates = []
    for id, professors in id_professors.items():
        # Remove all duplicate instructors
        professors = list(set(professors))
        # Remove all the entries in the array that are ""
        professors = [instructor for instructor in professors if instructor != '']
        if len(professors) == 0:
            # All entries are just ""
            id_professor[id] = ""
        elif len(professors) == 1:
            id_professor[id] = professors[0]
        else:
            # There are multiple instructor-strings for a single ID.
            # Solution: Look up the section on UBC pair and manually override the correct instructor
            try:
                # Prefix UBC campus as that's the only available data source
                id_professor[id] = professor_corrections["UBC-" + id]
            except KeyError:
                print("{} has {} non-empty entries:\n".format(id, len(professors)) + "".join(professors))
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
            entry['Professor'] = id_professor[id]
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
    sections = fix_professors(path_to_correction_file, sections)

    app, db = create_app(Config)

    with app.app_context():
        db.create_all()

        for section in sections:
            campus = CampusEnum.UBCV
            session = SessionEnum.W if section['Session'] == "W" else SessionEnum.S
            average = None if section['Avg'] == '' else section['Avg']
            stdev = None if section['Std dev'] == '' else section['Std dev']
            entry = PAIRReportsGrade(campus=campus, year=section['Year'], session=session,
                                     subject=section['Subject'], course=section['Course'],
                                     detail=section['Detail'].strip(),
                                     section=section['Section'], title=section['Title'], professor=section['Professor'],
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
