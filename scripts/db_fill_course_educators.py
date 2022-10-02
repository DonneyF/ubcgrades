"""
Preprocessor and data importer for educators and their courses. Uses a combination of PAIR Reports and Tableau
Dashboard data.
"""

from app import create_app
from config import Config
from app.models import PAIRReportsGrade as PRG, TableauDashboardGrade as TDG, TableauDashboardV2Grade as TDG2, CourseV2, Educator, CampusEnum
from multiprocessing import Pool
from nameparser import HumanName
from nameparser.util import u


CAMPUSES = [CampusEnum.UBCV, CampusEnum.UBCO]


# Modified HumanName class
class HumanNameHashable(HumanName):
    def __hash__(self):
        return hash((u(self)).lower())

    def is_equal_except_middle(self, name):
        return self.first == name.first and self.last == name.last and self.title == name.title and \
               self.suffix == name.suffix and self.nickname == name.nickname and self.middle != name.middle


def get_sections_separated(course):
    """
    :param course: Type: sqlalchemy.util._collections.result
    :return: A list of sqlalchemy.util._collections.result with sections under the course for that campus, ignoring OVERALL sections
    """
    sections_TDG2 = [row for row in TDG2.query.filter(TDG2.year > '2021').with_entities(TDG2.year, TDG2.session, TDG2.educators, TDG2.section)\
        .filter(TDG2.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject,  course=course.course, detail=course.detail)]

    sections_TDG = [row for row in TDG.query.with_entities(TDG.year, TDG.session, TDG.educators, TDG.section)\
        .filter(TDG.section != "OVERALL").filter_by(campus=course.campus, subject=course.subject,  course=course.course, detail=course.detail)]

    sections_PRG = [row for row in PRG.query.with_entities(PRG.year, PRG.session, PRG.educators, PRG.section).filter(PRG.section != "OVERALL").filter(PRG.year < '2014') \
            .filter_by(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail)]

    return sections_TDG2, sections_TDG, sections_PRG


def main():
    app, db = create_app(Config)
    with app.app_context():
        db.create_all()
        bulk_objects = []
        # In the database, we have a sections -> educators. We wish to create course -> educators, yearsessions they are active
        # Get all the courses
        courses = [row for row in
                   CourseV2.query.with_entities(CourseV2.campus, CourseV2.subject, CourseV2.course, CourseV2.detail).all()]

        # Get all the yearsessions
        year_sessions = set([row for row in TDG.query.with_entities(TDG.year, TDG.session).distinct()])
        year_sessions = year_sessions.union(
            set([row for row in TDG2.query.with_entities(TDG2.year, TDG2.session).distinct()]))
        year_sessions = year_sessions.union(
            set([row for row in PRG.query.with_entities(PRG.year, PRG.session).distinct()]))

        N = len(courses)
        for index, course in enumerate(courses):
            if index % 100 == 0:
                print(f'{index}/{N}')
            # Get all the sections
            sections_TDG2, sections_TDG, sections_PRG = get_sections_separated(course)
            # Dictionary that maps a educators to a dictionary that maps a yearsession to the number of sections the
            # educators was active in that yearsession
            educator_map = {}

            # Sections have Educator fields that contain a list of names. Sections from PRG can have names that
            # are in all-caps. We check equality between names using nameparser
            for section in sections_TDG + sections_PRG + sections_TDG2:
                section_ys = f'{section.year}{section.session.name}'
                educator_str = section.educators
                for educator in educator_str.split(";"):
                    educator_name = HumanNameHashable(educator)
                    if educator_name not in educator_map:
                        educator_map[educator_name] = {}

                    try:
                        educator_map[educator_name][section_ys] += 1
                    except KeyError:
                        educator_map[educator_name][section_ys] = 1

            # Sections from TDG also include the middle name where possible. Iterate through all the keys and check similarity of the keys
            # Keep only the HumanName with the middle name, add sections to the HumanName with the middle name that have year < 2014, and
            # discard the HumanName without the middle name
            educators = set(educator_map.keys())  # This will change size during iteration
            skip = set()
            for educator in set(educator_map.keys()):
                if educator in skip:
                    continue
                # Check similarity of this educator against every other educator. This is O(n^2) maybe can be improved.
                educators_to_rm = set()
                for other_educator in educators:
                    if educator.is_equal_except_middle(other_educator) and educator not in educators_to_rm:
                        # Find which one has the longer middle name
                        if len(educator.middle) > len(other_educator.middle):
                            # Keep the current educator
                            keep_educator = educator
                            del_educator = other_educator
                        else:
                            keep_educator = other_educator
                            del_educator = educator

                        ys_maps = educator_map.pop(del_educator)
                        for ys, num_appearances in ys_maps.items():
                            # Merge the appearances
                            if ys not in educator_map[keep_educator]:
                                educator_map[keep_educator][ys] = num_appearances

                        educators_to_rm.add(del_educator)

                for del_educator in educators_to_rm:
                    educators.remove(del_educator)
                    skip.add(del_educator)



            for educator, ys_map in educator_map.items():
                educator_entry = Educator(campus=course.campus, subject=course.subject, course=course.course, detail=course.detail,
                                          name=str(educator))

                for yearsession_result in year_sessions:
                    yearsession = f'{yearsession_result.year}{yearsession_result.session.name}'
                    if yearsession in ys_map:
                        setattr(educator_entry, f'ys_{yearsession}', ys_map[yearsession])
                    else:
                        setattr(educator_entry, f'ys_{yearsession}', 0)

                bulk_objects.append(educator_entry)

        db.session.bulk_save_objects(bulk_objects)
        db.session.commit()


if __name__ == '__main__':
    main()