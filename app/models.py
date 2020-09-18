from app import db
import enum


class CampusEnum(enum.Enum):
    UBCV = 0
    UBCO = 1


class SessionEnum(enum.Enum):
    W = 0
    S = 1


class PAIRReportsGrade(db.Model):
    __tablename__ = "PAIRReportsGrade"
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
    educators = db.Column(db.String())
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
            "detail": self.detail,
            "section": self.section,
            "course_title": self.course_title,
            "educators": self.educators,
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
    __tablename__ = "TableauDashboardGrade"
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
    educators = db.Column(db.String())
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
            "detail": self.detail,
            "section": self.section,
            "course_title": self.course_title,
            "educators": self.educators,
            "enrolled": self.enrolled,
            "average": self.average,
            "stdev": self.stdev,
            "high": self.high,
            "low": self.low,
        }


class Course(db.Model):
    __tablename__ = "Course"
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    faculty_title = db.Column(db.String())
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    subject_title = db.Column(db.String())
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    course_title = db.Column(db.String())
    average = db.Column(db.Float())
    average_past_5_yrs = db.Column(db.Float())
    stdev = db.Column(db.Float())
    max_course_avg = db.Column(db.Integer())
    min_course_avg = db.Column(db.Integer())

    def __repr__(self):
        return f"<Course {self.campus.name}--{self.subject}-{self.course}{self.detail if self.detail != '' else ''}>"

    def to_dict(self):
        values = {
            "campus": self.campus.name,
            "faculty_title": self.faculty_title,
            "subject": self.subject,
            "subject_title": self.subject_title,
            "course": self.course,
            "detail": self.detail,
            "course_title": self.course_title,
            "average": self.average,
            "average_past_5_yrs": self.average_past_5_yrs,
            "stdev": self.stdev,
            "max_course_avg": self.max_course_avg,
            "min_course_avg": self.min_course_avg,
        }

        for key, val in values.items():
            if val is None:
                values[key] = ''

        return values


class CourseDistributions(db.Model):
    __tablename__ = 'CourseDistributions'
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    year = db.Column(db.String(4), primary_key=True)  # Ex: 2012
    session = db.Column(db.Enum(SessionEnum), primary_key=True)  # W or S
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    # We note these fields are nullable
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
            "subject": self.subject,
            "course": self.course,
            "detail": self.detail
        }


class Educator(db.Model):
    __tablename__ = 'Educator'
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    name = db.Column(db.String(), primary_key=True)
    ys_1996S = db.Column(db.Integer())
    ys_1996W = db.Column(db.Integer())
    ys_1997S = db.Column(db.Integer())
    ys_1997W = db.Column(db.Integer())
    ys_1998S = db.Column(db.Integer())
    ys_1998W = db.Column(db.Integer())
    ys_1999S = db.Column(db.Integer())
    ys_1999W = db.Column(db.Integer())
    ys_2000S = db.Column(db.Integer())
    ys_2000W = db.Column(db.Integer())
    ys_2001S = db.Column(db.Integer())
    ys_2001W = db.Column(db.Integer())
    ys_2002S = db.Column(db.Integer())
    ys_2002W = db.Column(db.Integer())
    ys_2003S = db.Column(db.Integer())
    ys_2003W = db.Column(db.Integer())
    ys_2004S = db.Column(db.Integer())
    ys_2004W = db.Column(db.Integer())
    ys_2005S = db.Column(db.Integer())
    ys_2005W = db.Column(db.Integer())
    ys_2006S = db.Column(db.Integer())
    ys_2006W = db.Column(db.Integer())
    ys_2007S = db.Column(db.Integer())
    ys_2007W = db.Column(db.Integer())
    ys_2008S = db.Column(db.Integer())
    ys_2008W = db.Column(db.Integer())
    ys_2009S = db.Column(db.Integer())
    ys_2009W = db.Column(db.Integer())
    ys_2010S = db.Column(db.Integer())
    ys_2010W = db.Column(db.Integer())
    ys_2011S = db.Column(db.Integer())
    ys_2011W = db.Column(db.Integer())
    ys_2012S = db.Column(db.Integer())
    ys_2012W = db.Column(db.Integer())
    ys_2013S = db.Column(db.Integer())
    ys_2013W = db.Column(db.Integer())
    ys_2014S = db.Column(db.Integer())
    ys_2014W = db.Column(db.Integer())
    ys_2015S = db.Column(db.Integer())
    ys_2015W = db.Column(db.Integer())
    ys_2016S = db.Column(db.Integer())
    ys_2016W = db.Column(db.Integer())
    ys_2017S = db.Column(db.Integer())
    ys_2017W = db.Column(db.Integer())
    ys_2018S = db.Column(db.Integer())
    ys_2018W = db.Column(db.Integer())
    ys_2019S = db.Column(db.Integer())
    ys_2019W = db.Column(db.Integer())
    ys_2020S = db.Column(db.Integer())

    def __repr__(self):
        return f"<Educator {self.campus}-{self.subject}-{self.course}{self.course.detail}>"

    def to_dict(self):
        data = {}
        yearsessions = {}
        for key, val in vars(self).items():
            if "ys_" in key:
                if val != 0:
                    yearsessions[key[3:]] = val
            else:
                data[key] = val

        data['yearsessions'] = yearsessions

        data['campus'] = self.campus.name
        data.pop('_sa_instance_state')

        return data


class CourseAverageHistory(db.Model):
    __tablename__ = 'CourseAverageHistory'
    campus = db.Column(db.Enum(CampusEnum), primary_key=True)  # UBCV or UBCO
    subject = db.Column(db.String(4), primary_key=True)  # Ex: BA, KIN, MATH
    course = db.Column(db.String(3), primary_key=True)  # Ex: 001, 200
    detail = db.Column(db.String(3), primary_key=True)  # Ex: A, B, C
    ys_1996S = db.Column(db.Integer())
    ys_1996W = db.Column(db.Integer())
    ys_1997S = db.Column(db.Integer())
    ys_1997W = db.Column(db.Integer())
    ys_1998S = db.Column(db.Integer())
    ys_1998W = db.Column(db.Integer())
    ys_1999S = db.Column(db.Integer())
    ys_1999W = db.Column(db.Integer())
    ys_2000S = db.Column(db.Integer())
    ys_2000W = db.Column(db.Integer())
    ys_2001S = db.Column(db.Integer())
    ys_2001W = db.Column(db.Integer())
    ys_2002S = db.Column(db.Integer())
    ys_2002W = db.Column(db.Integer())
    ys_2003S = db.Column(db.Integer())
    ys_2003W = db.Column(db.Integer())
    ys_2004S = db.Column(db.Integer())
    ys_2004W = db.Column(db.Integer())
    ys_2005S = db.Column(db.Integer())
    ys_2005W = db.Column(db.Integer())
    ys_2006S = db.Column(db.Integer())
    ys_2006W = db.Column(db.Integer())
    ys_2007S = db.Column(db.Integer())
    ys_2007W = db.Column(db.Integer())
    ys_2008S = db.Column(db.Integer())
    ys_2008W = db.Column(db.Integer())
    ys_2009S = db.Column(db.Integer())
    ys_2009W = db.Column(db.Integer())
    ys_2010S = db.Column(db.Integer())
    ys_2010W = db.Column(db.Integer())
    ys_2011S = db.Column(db.Integer())
    ys_2011W = db.Column(db.Integer())
    ys_2012S = db.Column(db.Integer())
    ys_2012W = db.Column(db.Integer())
    ys_2013S = db.Column(db.Integer())
    ys_2013W = db.Column(db.Integer())
    ys_2014S = db.Column(db.Integer())
    ys_2014W = db.Column(db.Integer())
    ys_2015S = db.Column(db.Integer())
    ys_2015W = db.Column(db.Integer())
    ys_2016S = db.Column(db.Integer())
    ys_2016W = db.Column(db.Integer())
    ys_2017S = db.Column(db.Integer())
    ys_2017W = db.Column(db.Integer())
    ys_2018S = db.Column(db.Integer())
    ys_2018W = db.Column(db.Integer())
    ys_2019S = db.Column(db.Integer())
    ys_2019W = db.Column(db.Integer())
    ys_2020S = db.Column(db.Integer())

    def __repr__(self):
        return f"<CourseAverageHistory {self.campus}-{self.subject}-{self.course}{self.course.detail}>"

    def to_dict(self):
        data = {}
        yearsessions = {}
        for key, val in vars(self).items():
            if "ys_" in key:
                if val != 0:
                    yearsessions[key[3:]] = val
            else:
                data[key] = val

        data['yearsessions'] = yearsessions

        data['campus'] = self.campus.name
        data.pop('_sa_instance_state')

        return data
