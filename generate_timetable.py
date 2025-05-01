import random

import numpy as np
from deap import algorithms, base, creator, tools

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


class GenerateTimetable:
    def __init__(self, details: dict):
        self.days_per_week = details.get("days_per_week")
        self.periods = details.get("periods")
        self.duration = details.get("duration")
        self.subjects_faculties = details.get("subjects_faculties")
        self.classrooms = details.get("classrooms")
        self.sections = details.get("sections")
        self.course = details.get("course")

        self.total_slots_per_section = self.days_per_week * self.periods
        self.total_slots_all = self.days_per_week * self.periods * len(self.sections)

        self.subject_teacher_map = {}
        self.subject_credit_map = {}

        for sf in self.subjects_faculties:
            subject = sf["subject"]
            self.subject_credit_map[subject] = int(sf["credit"])
            self.subject_teacher_map[subject] = sf["faculty"]

        self.subjects = list(self.subject_teacher_map.keys())
        self.total_credits = sum(self.subject_credit_map.values())
        self.free_periods = self.total_slots_per_section - self.total_credits

    def fitness_function(self, individual):
        timetable = {
            f"Section_{i + 1}": np.array(
                individual[
                    i * self.total_slots_per_section : (i + 1)
                    * self.total_slots_per_section
                ]
            ).reshape((self.days_per_week, self.periods))
            for i in range(len(self.sections))
        }

        penalties = 0

        for sec in timetable:
            subject_counts = {subj: 0 for subj in self.subjects}
            for subj in timetable[sec].flatten():
                if subj != "Free" and subj in subject_counts:
                    subject_counts[subj] += 1
            for subj in self.subjects:
                expected = self.subject_credit_map[subj]
                actual = subject_counts[subj]
                penalties += abs(expected - actual)

        for day in range(self.days_per_week):
            for period in range(self.periods):
                teachers = set()
                for sec in timetable:
                    subj = timetable[sec][day][period]
                    if subj == "Free":
                        continue
                    teacher = self.subject_teacher_map[subj]
                    if teacher in teachers:
                        penalties += 1
                    teachers.add(teacher)

        return (-penalties,)

    def generate_individual(self):
        subjects_with_counts = []

        for subject, credit in self.subject_credit_map.items():
            subjects_with_counts.extend([subject] * credit)

        free_slots = self.total_slots_per_section - len(subjects_with_counts)
        subjects_with_counts.extend(["Free"] * free_slots)

        full_list = subjects_with_counts * len(self.sections)
        for _ in range(len(self.sections)):
            temp = subjects_with_counts.copy()
            random.shuffle(temp)
            full_list.extend(temp)
        return creator.Individual(full_list)

    def run_ga(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("individual", self.generate_individual)
        toolbox.register(
            "population", tools.initRepeat, list, toolbox.individual, n=100
        )
        toolbox.register("evaluate", self.fitness_function)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
        toolbox.register("select", tools.selTournament, tournsize=3)

        population = toolbox.population()
        NGEN = 40
        CXPB, MUTPB = 0.5, 0.2

        for gen in range(NGEN):
            offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
            fits = list(map(toolbox.evaluate, offspring))
            for ind, fit in zip(offspring, fits):
                ind.fitness.values = fit
            population = toolbox.select(offspring, len(population))

        best_ind = tools.selBest(population, k=1)[0]
        return self.generate_readable_timetables(best_ind)

    def generate_readable_timetables(self, individual):
        timetables = {
            f"{self.sections[i]['section']}": np.array(
                individual[
                    i * self.total_slots_per_section : (i + 1)
                    * self.total_slots_per_section
                ]
            ).reshape((self.days_per_week, self.periods))
            for i in range(len(self.sections))
        }

        output = {}
        for sec, matrix in timetables.items():
            sec_output = []
            for day in range(self.days_per_week):
                day_schedule = []
                for period in range(self.periods):
                    subj = matrix[day][period]
                    if subj == "Free":
                        entry = f"{WEEKDAYS[day]} Period {period + 1}: Free"
                        day_schedule.append(entry)
                        continue

                    teacher = self.subject_teacher_map[subj]
                    entry = f"{WEEKDAYS[day]} Period {period + 1}: {subj} -> {teacher} ({self.duration} min)"
                    day_schedule.append(entry)
                sec_output.append(day_schedule)
            output[sec] = sec_output

        formatted = {}

        for i, (section, days) in enumerate(output.items()):
            formatted[section] = {"classroom": self.classrooms[i]["classroom"]}
            for day in days:
                for period in day:
                    day_label = period.split(" Period")[0]

                    if day_label not in formatted[section]:
                        formatted[section][day_label] = []

                    if " -> " not in period:
                        formatted[section][day_label].append({"Free": ""})
                    else:
                        subject_faculty = period.split(": ")[-1].split(" -> ")
                        if len(subject_faculty) == 2:
                            subject = subject_faculty[0].strip()
                            faculty = subject_faculty[1].split(" (")[0].strip()
                            formatted[section][day_label].append({subject: faculty})
                        else:
                            formatted[section][day_label].append({"Unknown": "Unknown"})

        return formatted
