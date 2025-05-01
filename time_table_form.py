from flask_wtf import FlaskForm
from wtforms import (
    FieldList,
    FormField,
    IntegerField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, NumberRange


class SubjectFacultyForm(FlaskForm):
    subject = StringField(label="Subject", validators=[DataRequired()])
    credit = IntegerField(
        label="Credit Points", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    faculty = StringField(label="Faculty", validators=[DataRequired()])


class SectionForm(FlaskForm):
    section = StringField(label="Section", validators=[DataRequired()])


class ClassroomForm(FlaskForm):
    classroom = StringField(label="Classroom", validators=[DataRequired()])


class TimeTableForm(FlaskForm):
    days_per_week = IntegerField(
        label="Number of days per week(e.g., Monday-Friday will be 5)",
        validators=[DataRequired(), NumberRange(min=1, max=7)],
    )
    periods = IntegerField(
        label="Number of periods per day(e.g., 6, 7, or 8)", validators=[DataRequired()]
    )
    duration = IntegerField(label="Duration of each period(e.g., 45 mins or 60 mins)")
    subjects_faculties = FieldList(FormField(SubjectFacultyForm), min_entries=8)
    classrooms = FieldList(FormField(ClassroomForm), min_entries=2)
    sections = FieldList(FormField(SectionForm), min_entries=2)
    lunch_break = IntegerField(
        label="Lunch Break after how many classes?",
        validators=[DataRequired(), NumberRange(min=1)],
    )
    lunch_break_time = IntegerField(
        label="Duration of lunch break(e.g., 45 mins or 60 mins)",
        validators=[DataRequired()],
    )
    course = StringField(label="Course", validators=[DataRequired()])
    generate_btn = SubmitField(label="Generate Timetable")
