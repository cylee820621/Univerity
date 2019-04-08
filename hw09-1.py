"""
@author: cylee820621
"""
import os
from prettytable import PrettyTable
from collections import defaultdict

class Student:
    def __init__(self, cwid, name, dept):
        """
        Store student information.
        """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(str)

    def add_course(self,cwid,grade):
        """
        add dictionary,course as key, grade as value.
        """
        self.course[cwid] = grade
    
    def prettytable(self):
        """
        Return data needed for prettytalbe.
        """
        return [self.cwid, self.name, sorted(list(self.course.keys()))]
        

class Instructor:
    def __init__(self, cwid, name, dept):
        """
        Store instrictor information.
        """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = defaultdict(int)

    def add_course(self,course):
        """
        add dictionary,course as key, numbers ofstudents as value.
        """
        self.course[course] += 1

    def prettytable(self):
        """
        Return data needed for prettytalbe.
        """
        for course, students in self.course.items():
            yield (self.cwid,self.name,self.dept,course,students)
    

class University:
    def __init__(self,path):
        """
        Store file paths
        Store each students in dictionary
        Store each instructors in dictionary
        """
        self.student_file = os.path.join(path, 'students.txt')
        self.instructors_file = os.path.join(path, 'instructors.txt')
        self.grade_file = os.path.join(path, 'grades.txt')
        self.students = dict()
        self.instructors = dict()
        self.read_student()
        self.read_instructor()
        self.read_grade()
        self.students_pt = self.student_prettytable()
        self.instructors_pt = self.instructor_prettytable()

    def file_reader(self, path, fields, sep, header = False):
        """
        if file can be open, yield each line in the file.
        """
        try:
            fp = open(path,'r')
        except FileNotFoundError:
            raise FileNotFoundError(f'{path} cannot be found')
        else:
            with fp:

                if header == True:
                    next(fp)

                for index, line in enumerate(fp):
                    new_text = line.strip().split(sep)
                    output = tuple(new_text)

                    if len(output) != fields:
                        raise ValueError(f"{path} has {len(output)} fields on line {index} but expected {fields}")
                    
                    yield output    

    def read_student(self):
        """
        Store each students cwid into dictionay as key, and store other information as value.
        """
        for cwid, name, major in self.file_reader(self.student_file, fields = 3, sep = '\t', header = False):
            self.students.update({cwid : Student(cwid, name, major)})
    
    def read_instructor(self):
        """
        Store each instructors cwid into dictionay as key, and  store other information as value.
        """
        for in_cwid, name, dept in self.file_reader(self.instructors_file, fields = 3, sep = '\t', header = False):
            self.instructors.update({in_cwid : Instructor(in_cwid, name, dept)})
    
    def read_grade(self):
        """
        Store a defauldictionary, course as key and grade as value, into Student Class.
        Store a defauldictionary, course as key and student as value, into Instructor Class.
        """
        for cwid, course, lettergrade, in_cwid in self.file_reader(self.grade_file, fields = 4, sep = '\t', header = False):    
            
            for i in self.students:
                if cwid == i:
                    self.students[i].add_course(course,lettergrade)

            for j in self.instructors:
                if in_cwid == j:
                    self.instructors[j].add_course(course)
        
    def student_prettytable(self):  
        """
        creat and print a prettytable for students
        """
        pt = PrettyTable(field_names = ["cwid", "name", "course"])
        for i in self.students:

            if len(self.students[i].course) == 0:
                continue

            pt.add_row(self.students[i].prettytable())

        return pt

    def instructor_prettytable(self):
        """
        creat and print a prettytable for instructors
        """  
        pt = PrettyTable(field_names = ["cwid", "name", "department", "course", "student"])
        for i in self.instructors:

            for a,b,c,d,e in self.instructors[i].prettytable():
                pt.add_row([a,b,c,d,e])

        return pt


def main(path):
    data = University(path)
    print(data.students_pt)
    print(data.instructors_pt)
    
if __name__=="__main__":
    dir = "/Users/cylee820621/Desktop/SSW-810/hw9"
    main(dir)

    

    