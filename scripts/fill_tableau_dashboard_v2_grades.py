"""
Imports data from Tableau Dashboard v2 into the database. This assumes the database has been created with the proper
models and the data exist in the project directory in /ubc-pair-grade-data.
"""

from app import create_app
from config import Config
from app.models import TableauDashboardV2Grade
import json
import pandas as pd
import tqdm
from pathlib import Path
from tools import combine_educator
import numpy as np


def main():
    app, db = create_app(Config)

    with app.app_context():
        db.create_all()

        path_to_csv_files = Path(__file__).parent.parent / Path('ubc-pair-grade-data/tableau-dashboard-v2')

        # Build subject dict
        extra = Path(__file__).parent.parent / Path('ubc-pair-grade-data/extra')
        subjects = {}
        for file in ['UBCO_subjects.json', 'UBCV_subjects.json']:
            for subject in json.load(open(str(extra / Path(file)), 'r')):
                subjects.update({f'{file[0:4]}-{subject["code"]}': subject})

        li = []
        for csvfile in path_to_csv_files.rglob('*.csv'):
            li.append(pd.read_csv(csvfile, index_col=None, header=0))

        df = pd.concat(li, axis=0, ignore_index=True)
        df['Professor'] = df['Professor'].fillna(value='')
        df['Detail'] = df['Detail'].fillna(value='')
        df.fillna(0)

        entries = []
        for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
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
            entries.append(entry)

        # Generate OVERALL sections
        overall = df[df['Year'] >= 2022]

        def weighted_average(group):
            return np.average(group['Avg'], weights=group['Reported'])

        group = overall.groupby(['Campus', 'Year', 'Session', 'Subject', 'Course', 'Detail'])
        A = group.agg({
            'Reported': 'sum',
            'Low': 'min',
            'High': 'max',
            '<50': 'sum',
            '50-54': 'sum',
            '55-59': 'sum',
            '60-63': 'sum',
            '64-67': 'sum',
            '68-71': 'sum',
            '72-75': 'sum',
            '76-79': 'sum',
            '80-84': 'sum',
            '85-89': 'sum',
            '90-100': 'sum',
            'Title': 'last'
        })
        B = group.apply(weighted_average)
        overall = pd.concat([A, B.rename('Avg')], axis=1)
        overall = overall.reset_index()

        for index, row in tqdm.tqdm(overall.iterrows(), total=overall.shape[0]):
            subject_key = f'{row["Campus"]}-{row["Subject"]}'
            course = str(row['Course']).zfill(3) if type(row['Course']) == int or row['Course'].isnumeric() else row['Course']
            entry = TableauDashboardV2Grade(campus=row['Campus'], year=row['Year'], session=row['Session'],
                                          faculty_title=subjects[subject_key]['faculty_school'],
                                          subject=row['Subject'],
                                          subject_title=subjects[subject_key]['title'],
                                          course=course, detail=row['Detail'],
                                          section='OVERALL',
                                          course_title=row['Title'], educators=None,
                                          reported=row['Reported'], average=row['Avg'],
                                          percentile_25=None, percentile_75=None,
                                          median=None, high=row['High'], low=row['Low'],
                                          grade_lt50=row['<50'], grade_50_54=row['50-54'],
                                          grade_55_59=row['55-59'], grade_60_63=row['60-63'],
                                          grade_64_67=row['64-67'], grade_68_71=row['68-71'],
                                          grade_72_75=row['72-75'], grade_76_79=row['76-79'],
                                          grade_80_84=row['80-84'], grade_85_89=row['85-89'],
                                          grade_90_100=row['90-100'])
            entries.append(entry)

        db.session.bulk_save_objects(entries)
        db.session.commit()


if __name__ == "__main__":
    main()
