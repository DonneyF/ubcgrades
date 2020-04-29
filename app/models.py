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
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    section = db.Column(db.String(7), primary_key=True)  # Ex: 001, 100, GIS, T1A, OVERALL
    title = db.Column(db.String())
    professor = db.Column(db.String())
    enrolled = db.Column(db.Integer())
    average = db.Column(db.Float())
    stdev = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
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


class TableauDashboardGrade(db.Model):
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    year = db.Column(db.String(4), primary_key=True)  # Ex: 2012
    session = db.Column(db.Enum(SessionEnum), primary_key=True)  # W or S
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    section = db.Column(db.String(7), primary_key=True)  # Ex: 001, 100, GIS, T1A, OVERALL
    title = db.Column(db.String())
    professor = db.Column(db.String())
    enrolled = db.Column(db.Integer())
    average = db.Column(db.Float())
    stdev = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
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
