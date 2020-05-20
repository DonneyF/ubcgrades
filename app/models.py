from app import db
import enum


class CampusEnum(enum.Enum):
    UBCV = 0
    UBCO = 1


class SessionEnum(enum.Enum):
    W = 0
    S = 1


class PAIRReportsGrade(db.Model):
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    year = db.Column(db.String(4), primary_key=True)  # Ex: 2012
    session = db.Column(db.Enum(SessionEnum), primary_key=True)  # W or S
    faculty_title = db.Column(db.String())
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    subject_title = db.Column(db.String())
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    section = db.Column(db.String(7), primary_key=True)  # Ex: 001, 100, GIS, T1A, OVERALL
    course_title = db.Column(db.String())
    professor = db.Column(db.String())
    enrolled = db.Column(db.Integer())
    average = db.Column(db.Float(), nullable=True)
    stdev = db.Column(db.Float(), nullable=True)
    high = db.Column(db.Integer())
    low = db.Column(db.Integer())
    num_pass = db.Column(db.Integer())
    num_fail = db.Column(db.Integer())
    withdrew = db.Column(db.Integer())
    audit = db.Column(db.Integer())
    other = db.Column(db.Integer())
    grade_0_9 = db.Column(db.Integer())
    grade_10_19 = db.Column(db.Integer())
    grade_20_29 = db.Column(db.Integer())
    grade_30_39 = db.Column(db.Integer())
    grade_40_49 = db.Column(db.Integer())
    grade_lt50 = db.Column(db.Integer())  # Num less than 50
    grade_50_54 = db.Column(db.Integer())
    grade_55_59 = db.Column(db.Integer())
    grade_60_63 = db.Column(db.Integer())
    grade_64_67 = db.Column(db.Integer())
    grade_68_71 = db.Column(db.Integer())
    grade_72_75 = db.Column(db.Integer())
    grade_76_79 = db.Column(db.Integer())
    grade_80_84 = db.Column(db.Integer())
    grade_85_89 = db.Column(db.Integer())
    grade_90_100 = db.Column(db.Integer())

    def __repr__(self):
        return f"<PAIRReportsGrade {self.campus.name}-{self.year}{self.session.name}-{self.subject}-{self.course}" \
            f"{self.detail if self.detail != '' else ''}-{self.section}>"

    def to_dict(self):
        return {
            "grades": {
                "0-9%": self.grade_0_9,
                "10-19%": self.grade_10_19,
                "20-29%": self.grade_20_29,
                "30-39%": self.grade_30_39,
                "40-49%": self.grade_40_49,
                "<50%": self.grade_lt50,
                "50-54%": self.grade_50_54,
                "55-59%": self.grade_55_59,
                "60-63%": self.grade_60_63,
                "64-67%": self.grade_64_67,
                "68-71%": self.grade_68_71,
                "72-75%": self.grade_72_75,
                "76-79%": self.grade_76_79,
                "80-84%": self.grade_80_84,
                "85-89%": self.grade_85_89,
                "90-100%": self.grade_90_100
            },
            "campus": self.campus.name,
            "year": self.year,
            "session": self.session.name,
            "faculty_title": self.faculty_title,
            "subject": self.subject,
            "subject_title": self.subject_title,
            "course": self.course,
            "section": self.section,
            "course_title": self.course_title,
            "professor": self.professor,
            "enrolled": self.enrolled,
            "average": self.average if self.average is not None else '',
            "stdev": self.stdev if self.stdev is not None else '',
            "high": self.high,
            "low": self.low,
            "pass": self.num_pass,
            "fail": self.num_fail,
            "withdrew": self.withdrew,
            "audit": self.audit,
            "other": self.other
        }


class TableauDashboardGrade(db.Model):
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    year = db.Column(db.String(4), primary_key=True)  # Ex: 2012
    session = db.Column(db.Enum(SessionEnum), primary_key=True)  # W or S
    faculty_title = db.Column(db.String())
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    subject_title = db.Column(db.String())
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    section = db.Column(db.String(7), primary_key=True)  # Ex: 001, 100, GIS, T1A, OVERALL
    course_title = db.Column(db.String())
    professor = db.Column(db.String())
    enrolled = db.Column(db.Integer())
    average = db.Column(db.Float())
    stdev = db.Column(db.Float())
    high = db.Column(db.Integer())
    low = db.Column(db.Integer())
    # We note these fields are nullable
    grade_lt50 = db.Column(db.Integer())  # Num less than 50
    grade_50_54 = db.Column(db.Integer())
    grade_55_59 = db.Column(db.Integer())
    grade_60_63 = db.Column(db.Integer())
    grade_64_67 = db.Column(db.Integer())
    grade_68_71 = db.Column(db.Integer())
    grade_72_75 = db.Column(db.Integer())
    grade_76_79 = db.Column(db.Integer())
    grade_80_84 = db.Column(db.Integer())
    grade_85_89 = db.Column(db.Integer())
    grade_90_100 = db.Column(db.Integer())

    def __repr__(self):
        return f"<TableauDashboardGrade {self.campus.name}-{self.year}{self.session.name}-{self.subject}-{self.course}" \
            f"{self.detail if self.detail != '' else ''}-{self.section}>"

    def to_dict(self):
        return {
            "grades": {
                "<50%": self.grade_lt50,
                "50-54%": self.grade_50_54,
                "55-59%": self.grade_55_59,
                "60-63%": self.grade_60_63,
                "64-67%": self.grade_64_67,
                "68-71%": self.grade_68_71,
                "72-75%": self.grade_72_75,
                "76-79%": self.grade_76_79,
                "80-84%": self.grade_80_84,
                "85-89%": self.grade_85_89,
                "90-100%": self.grade_90_100
            },
            "campus": self.campus.name,
            "year": self.year,
            "session": self.session.name,
            "faculty_title": self.faculty_title,
            "subject": self.subject,
            "subject_title": self.subject_title,
            "course": self.course,
            "section": self.section,
            "course_title": self.course_title,
            "professor": self.professor,
            "enrolled": self.enrolled,
            "average": self.average,
            "stdev": self.stdev,
            "high": self.high,
            "low": self.low,
        }
