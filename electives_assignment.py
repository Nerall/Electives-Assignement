import numpy as np
import random
from sys import argv
from scipy.optimize import linear_sum_assignment

class Course:
    def __init__(self, line):
        tokens = line.rstrip().split(' ')
        self.name = tokens[0]
        self.values = tuple(int(token) for token in tokens[1:])

class Courses:
    def __init__(self, courses):
        self.courses = courses
        self.configurations = []
        self.generate_configurations(np.empty([8], dtype=int))

    def generate_configurations(self, line, i = 0, n = 27):
        if i < len(self.courses):
            for value in self.courses[i].values:
                if n >= value:
                    line = line.copy()
                    line[i] = value
                    self.generate_configurations(line, i + 1, n - value)
        elif n == 0:
            self.configurations.append(line)

class Student:
    def __init__(self, line):
        tokens = line.rstrip().split(' ')
        self.name = tokens[0]
        self.preferences = tuple(int(token) - 1 for token in tokens[1:])
        self.costs = self.preferences_to_costs()
        
    def preferences_to_costs(self):
        nb_courses = len(self.preferences)
        size = nb_courses - 1
        costs = np.empty([nb_courses], dtype=int)
        for i, preference in enumerate(self.preferences):
            # h is the percentaged position of the choice among other choices
            # for example, 2nd choice over 8 is 1/7 = 0.14
            # see https://www.reddit.com/r/fireemblem/comments/
            #     4jpw4f/true_hit_formula_2rn_system/ for more details
            h = i / size * 100
            if h <= 50:
                cost = h * (2 * h + 1) / 100
            else:
                cost = (-2 * h**2 + 399 * h - 9900) / 100
            costs[preference] = cost
        return costs

def assignment(courses, students):
    assignments = {}

    min_sum = np.inf
    nb_students = len(students)
    nb_courses = len(courses.courses)
    for k in range(len(students)):
        # Repeat to ensure each student will be once first
        students_2 = random.sample(students, k=len(students))
        for configurations in courses.configurations:
            subjects = np.empty([nb_students], dtype=int)
            count = 0
            for i, nb_places in enumerate(configurations):
                subjects[count:count+nb_places] = i
                count += nb_places

            # Build cost matrix
            cost = np.empty([nb_students, nb_students], dtype=int)
            for i, student in enumerate(students_2):
                count = 0
                for j, nb_places in enumerate(configurations):
                    cost[i, count:count+nb_places] = student.costs[j]
                    count += nb_places
        
            # Apply linear sum algorithm
            row_ind, col_ind = linear_sum_assignment(cost)
            if cost[row_ind, col_ind].sum() < min_sum:
                # Empty dict
                for student in students_2:
                    assignments[student.name] = set()
                min_sum = cost[row_ind, col_ind].sum()
            elif cost[row_ind, col_ind].sum() == min_sum:
                # Add to dict
                for i, student in enumerate(students_2):
                    assignments[student.name].add(\
                               courses.courses[subjects[col_ind[i]]].name)
        print(k)

    for name, el in assignments.items():
        print(f"{name}: {el}")

def main(courses_path, students_path):
    # Initialization
    with open('courses.txt') as f:
        try:
            # Courses represent the capacity and index of each course
            courses = Courses(tuple(Course(line) for line in f.readlines()))
        except Exception:
            raise(ValueError('File "courses.txt" has invalid format'))

    with open('students.txt', encoding='utf-8') as f:
        try:
            # Students represent the position of each course for each student
            students = tuple(Student(line) for line in f.readlines())
        except Exception:
            raise(ValueError('File "students.txt" has invalid format'))
    assignment(courses, students)

if __name__ == '__main__':
    if len(argv) < 2:
        print("Missing arguments, run with {courses_path} and {students_path}")
    else:
        main(argv[0], argv[1])