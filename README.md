# 🎓 Timetable Optimization using Genetic Algorithm

This project generates optimized timetables based on number of classes per week, subjects, sections, breaks, faculty, etc using genetic algorithm. Genetic algorithm automatically creates conflict-free, optimized class schedules for schools, colleges, or universities.

---

## 📁 Project Structure

```bash
flash_card_generator/
│
├── static/
│   └── css/
│       └── styles.css
│
├── templates/
│   ├── base.html
│   ├── form.html
│   ├── index.html
│   └── timetable.html
│
├── .gitignore
├── generate_timetable.py
├── main.py
├── README.md
├── requirements.txt
└── time_table_form.py
```

---

## 🚀 How It Works

1. **Access the website**: Users can go to the website built using flask.
2. **Get Features**: Users enter their details in the form provided like number of classes per week, faculty, subjects, sections, etc.
3. **Processing**: `Genetic Algorithm` will work behind the scenes generating timetables for all the sections (eg, IT01, IT02, etc.).
4. **Show Timetables**: Formats the timetables and displays them in tabular format in the website, which they can take a screenshot of.

---

### 📦 Python Packages

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## 🖥️ How to Run

```bash
python main.py
```

## 🧬 How the Genetic Algorithm works

The project uses a Genetic Algorithm (GA) to evolve optimized, conflict-free timetables. Here's how the core GA process works:

-   **Chromosome Representation**: Each individual (chromosome) is a list representing all timetable slots for all sections. Subjects are placed based on their credit hours, and remaining slots are filled with `"Free"` periods.

-   **Initial Population Generation**: A population of random individuals is created by shuffling subject and free period assignments while maintaining required subject counts for each section.

-   **Fitness Function**: The fitness function evaluates each timetable based on:

    -   How closely the subject frequency matches the required credits.
    -   Whether any faculty is scheduled in multiple sections at the same time (conflict). The fewer the mismatches and conflicts, the better the fitness (penalties are minimized).

-   **Selection, Crossover, and Mutation**:

    -   _Selection_: Tournament selection picks the fittest individuals.
    -   _Crossover_: Two-point crossover recombines individuals to explore new solutions.
    -   _Mutation_: Shuffle mutation introduces randomness to avoid local optima.

-   **Evolution Loop**: Over 40 generations, the population is evolved by applying selection, crossover, and mutation, constantly refining the timetable quality.

-   **Best Solution Extraction**: After evolution, the best individual is decoded into human-readable timetables, assigning each subject to a period with its corresponding faculty and classroom.

## ✨ Future Improvements

-   Add more conflicts (like same subjects not multiple times in a single day)
-   Add download button to download the timetables
-   Optimized genetic algorithm implementation
-   Adapt to sudden subject changes and real life implementation
-   Add options for teachers to choose their own timings.

## 🧑‍💻 Author

Made with 💡 by Koustav Chatterjee, Suprabhat Ghosh and Ankita Hazra

---
