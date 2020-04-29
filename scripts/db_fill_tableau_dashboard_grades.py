"""
Imports data from Tableau Dashboard into the database. This assumes the database has been created with the proper
models and the data exist in the project directory in /data.
"""

from app import db
from app.models import TableauDashboardGrade
import os
import re
import csv


def main():
    path_to_csv_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')
    csv_files = [f for f in os.listdir(path_to_csv_files) if re.match(r'.+.csv', f)]
    for csv_file in csv_files:
        csv_reader = csv.DictReader(open(os.path.join(path_to_csv_files, csv_file)))
        # Convert to normal dictionaries
        grades_dict = [dict(ele) for ele in csv_reader]
        for row in grades_dict:
            entry = TableauDashboardGrade(campus=row['Campus'], year=row['Year'], session=row['Session'],
                    subject=row['Subject'], course=row['Course'], detail=row['Detail'], section=row['Section'],
                    title=row['Title'], professor=row['Professor'], enrolled=row['Enrolled'], average=row['Avg'],
                    stdev=row['Std dev'], high=row['High'], low=row['Low'], grade_lt50=row['<50'], grade_50_54=row['50-54'],
                    grade_55_59=row['55-59'], grade_60_63=row['60-63'], grade_64_67=row['64-67'], grade_68_71=row['68-71'],
                    grade_72_75=row['72-75'], grade_76_79=row['76-79'], grade_80_84=row['80-84'], grade_85_89=row['85-89'],
                    grade_90_100=row['90-100'])
            db.session.add(entry)
        db.session.commit()


if __name__ == "__main__":
    main()
