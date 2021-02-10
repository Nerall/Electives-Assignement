# Electives assignment

## Introduction

The goal of this project is to have an automated way to solving the assignment problem, given a list of students, a list of electives, and additional restrictions, based on Hungarian/Munkres algorithm.
This code was used to assign fairly groups to projects.

The file 'students.txt' contains the list of students and their preference, for example, 'Gabriel 4 1 5 2 7 3 8 6', indicates that Gabriel's favorite projects are the number 4 and the number 1.

The file 'courses.txt' contains the list of courses and the different possible number of students assigned to this course. For example, 'ETIX 3 4' means that the course ETIX needs to be assigned exactly to 3 or 4 students.

The output is a set of each project that a student can choose to still have an optimal repartition. In our example, Gabriel was assigned to course ETIX, his second choice.

The score minimization is done so that we tend to minimize last choices rather than maximizing first choices.

## Run

To run the program, use the following command:

* `python3 electives_assigment.py courses.txt students.txt`

## Authors

* tertre_m