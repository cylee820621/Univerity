"""
@author: cylee820621
"""
import os
from prettytable import PrettyTable
from collections import defaultdict

class Dept:
    def __init__(self, dept):
        self.dept = dept
        self.required = {'R':list()}
        self.electives = {'E':list()}

    def add_course(self,course,re_flag):
        if re_flag == 'R':
            self.required['R'].append(course)
        elif re_flag == 'E':
            self.electives['E'].append(course)
        
    def prettytable(self):
        return [self.dept ,sorted(self.required['R']), sorted(self.electives['E'])]

class Student:
    def __init__(self, cwid, name, dept):
        """
        Store student information.
        """
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.course = dict()
        self.completed_course = list()
        self.remaining_required = list()
        self.remaining_electives = None

    def add_course(self,course,grade):
        """
        add dictionary,course as key, grade as value.
        """
        self.course[course] = grade
        if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+','C']:
            self.completed_course.append(course)
    
    def add_remaining_required(self,course):
        """
        add sorted
        """
        self.remaining_required = sorted(course)
    
    def add_remaining_electives(self,course):
        if course == None:
            self.remaining_electives = 'None'
        else:
            self.remaining_electives = sorted(course)
        
    def prettytable(self):
        """
        Return data needed for prettytalbe.
        """
        return [self.cwid, self.name, self.dept, sorted(self.completed_course), self.remaining_required, self.remaining_electives]


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
        self.majors_file = os.path.join(path, 'majors.txt')
        self.students = dict()
        self.instructors = dict()
        self.majors = dict()
        self.read_student()
        self.read_instructor()
        self.read_grade()
        self.read_majors()
        self.add_required()
        self.add_electives()
        self.students_pt = self.student_prettytable()
        self.instructors_pt = self.instructor_prettytable()
        self.majors_pt = self.majors_prettytable()

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
        
    def read_majors(self):
        for dept, re_flag, course in self.file_reader(self.majors_file, fields = 3, sep = '\t', header = False):
            
            if not dept in self.majors:
                self.majors.update({dept:Dept(dept)}) 

            self.majors[dept].add_course(course,re_flag)
    
    def add_required(self):
        for cwid in self.students:

            if self.students[cwid].dept == 'SFEN':
                required_course = set(self.majors['SFEN'].required['R'])

            elif self.students[cwid].dept == 'SYEN':
                required_course = set(self.majors['SYEN'].required['R'])
        
            for course in required_course.copy():

                if course in self.students[cwid].completed_course:
                    required_course.remove(course)

            self.students[cwid].add_remaining_required(required_course)
            
        
    def add_electives(self):
        for cwid in self.students:

            if self.students[cwid].dept == 'SFEN':
                electives_course = set(self.majors['SFEN'].electives['E'])

            elif self.students[cwid].dept == 'SYEN':
                electives_course = set(self.majors['SYEN'].electives['E'])

            for course in electives_course.copy():

                if course in self.students[cwid].completed_course:
                    self.students[cwid].add_remaining_electives(None)
                    break

                else:
                    self.students[cwid].add_remaining_electives(electives_course)
                    
                    
            

    def majors_prettytable(self):
        pt = PrettyTable(field_names = ["Dept", "Required", "Electives"])

        for i in self.majors:
            pt.add_row(self.majors[i].prettytable())

        return pt    

    def student_prettytable(self):  
        """
        creat and print a prettytable for students
        """
        pt = PrettyTable(field_names = ["CWID", "Name","Major", "Completed Courses", "Remaining Required","Remaining Electives"])

        for i in self.students:
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
    print(data.majors_pt)
    print(data.students_pt)
    print(data.instructors_pt)
  
if __name__=="__main__":
    dir = "/Users/cylee820621/Desktop/SSW-810/hw9"
    main(dir)