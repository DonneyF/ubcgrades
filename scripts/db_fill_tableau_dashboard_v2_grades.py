"""
Imports data from Tableau Dashboard v2 into the database. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import TableauDashboardV2Grade
import os
import json
import csv

from nameparser import HumanName
from nameparser.util import u

# Modified HumanName class
class HumanNameHashable(HumanName):
    def __hash__(self):
        return hash((u(self)).lower())

    def is_equal_except_middle(self, name):
        return self.first == name.first and self.last == name.last and self.title == name.title and \
               self.suffix == name.suffix and self.nickname == name.nickname and self.middle != name.middle


def main():
    app, db = create_app(Config)

    with app.app_context():
        db.create_all()

        path_to_csv_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'ubc-pair-grade-data',
                                         'tableau-dashboard-v2')

        # Build subject dict
        extra = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, 'ubc-pair-grade-data', 'extra')
        subjects = {}
        for file in ['UBCO_subjects.json', 'UBCV_subjects.json']:
            for subject in json.load(open(os.path.join(extra, file), 'r')):
                subjects.update({f'{file[0:4]}-{subject["code"]}': subject})

        for dirpath, subdirs, csv_files in os.walk(path_to_csv_files):
            for csv_file in csv_files:
                if not csv_file.endswith('csv'):
                    continue
                csv_reader = csv.DictReader(open(os.path.join(dirpath, csv_file)))
                # Convert to normal dictionaries
                grades_dict = [dict(ele) for ele in csv_reader]
                for row in grades_dict:
                    educators = combine_educator(row['Professor'])
                    subject_key = f'{row["Campus"]}-{row["Subject"]}'
                    section = str(row['Section']).zfill(3) if type(row['Section']) == int or row['Section'].isnumeric() else row['Section']
                    course = str(row['Course']).zfill(3) if type(row['Course']) == int or row['Course'].isnumeric() else row['Course']
                    entry = TableauDashboardV2Grade(campus=row['Campus'], year=row['Year'], session=row['Session'],
                                                  faculty_title=subjects[subject_key]['faculty_school'],
                                                  subject=row['Subject'],
                                                  subject_title=subjects[subject_key]['title'],
                                                  course=course, detail=row['Detail'],
                                                  section=section,
                                                  course_title=row['Title'], educators=educators,
                                                  reported=row['Reported'], average=row['Avg'],
                                                  percentile_25=row['Percentile (25)'], percentile_75=row['Percentile (75)'],
                                                  median=row['Median'], high=row['High'], low=row['Low'],
                                                  grade_lt50=row['<50'], grade_50_54=row['50-54'],
                                                  grade_55_59=row['55-59'], grade_60_63=row['60-63'],
                                                  grade_64_67=row['64-67'], grade_68_71=row['68-71'],
                                                  grade_72_75=row['72-75'], grade_76_79=row['76-79'],
                                                  grade_80_84=row['80-84'], grade_85_89=row['85-89'],
                                                  grade_90_100=row['90-100'])
                    db.session.add(entry)
        db.session.commit()

def combine_educator(educators: str):
    """Combines educators if they differ only by middle name. Keep the one with the middle name."""

    educators_set = {HumanNameHashable(educator) for educator in educators.split(';')}
    skip = set()
    for educator in set(educators_set):
        if educator in skip:
            continue
        # Check similarity of this educator against every other educator. This is O(n^2) maybe can be improved.
        educators_to_rm = set()
        for other_educator in educators_set:
            if educator.is_equal_except_middle(other_educator) and educator not in educators_to_rm:
                # Find which one has the longer middle name
                if len(educator.middle) > len(other_educator.middle):
                    # Keep the current educator
                    educators_to_rm.add(other_educator)
                else:
                    educators_to_rm.add(educator)

        for del_educator in educators_to_rm:
            educators_set.remove(del_educator)
            skip.add(del_educator)

    return ';'.join({str(educator) for educator in educators_set})


if __name__ == "__main__":
    main()
