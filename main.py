from datetime import timedelta

from flask import Flask, jsonify, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap5

from generate_timetable import WEEKDAYS, GenerateTimetable
from time_table_form import TimeTableForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloworld"
app.permanent_session_lifetime = timedelta(days=7)
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    session.permanent = True
    return render_template("index.html")


@app.route("/generate", methods=["GET", "POST"])
def generate():
    time_table_form = TimeTableForm()
    if time_table_form.validate_on_submit():
        details = {
            "days_per_week": time_table_form.days_per_week.data,
            "periods": time_table_form.periods.data,
            "duration": time_table_form.duration.data,
            "subjects_faculties": [
                {
                    "subject": sf.subject.data,
                    "credit": sf.credit.data,
                    "faculty": sf.faculty.data,
                }
                for sf in time_table_form.subjects_faculties
            ],
            "sections": [s.data for s in time_table_form.sections],
            "lunch_break": time_table_form.lunch_break.data,
            "lunch_break_time": time_table_form.lunch_break_time.data,
            "course": time_table_form.course.data,
            "classrooms": [c.data for c in time_table_form.classrooms],
        }

        if len(details["classrooms"]) < len(details["sections"]):
            return jsonify(
                response={"error": "classrooms cannot be lower than sections"}
            )

        tables = GenerateTimetable(details)
        best = tables.run_ga()

        session["best_timetable"] = best
        session["details"] = details

        return redirect(url_for("show_timetable"))
    else:
        return render_template("form.html", form=time_table_form)


@app.route("/timetable")
def show_timetable():
    timetable = session.get("best_timetable")
    details = session.get("details")
    return render_template(
        "timetable.html", timetable=timetable, details=details, WEEKDAYS=WEEKDAYS
    )


if __name__ == "__main__":
    app.run(debug=True)
