"""
@author: cylee820621
"""
import unittest
import hw10

class Hw9CleeTest(unittest.TestCase):
    
    def test_read_student(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")
        keys = ['10103', '10115', '10172', '10175', '10183', '11399', '11461', '11658', '11714', '11788']
        self.assertEquals(data.students.__len__(), len(keys))

    def test_read_instructor(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")
        keys = ['98765', '98764', '98763', '98762', '98761', '98760']
        self.assertEquals(data.instructors.__len__(), len(keys))

    def test_read_grade(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")  
        self.assertEquals(data.students['10103'].cwid, '10103')
        self.assertEquals(data.students['10103'].name, 'Baldwin, C')
        self.assertEquals(data.students['10103'].dept, 'SFEN')
        self.assertEquals(data.students['10103'].course.__len__(), 4)
    
    def test_major_prettytable(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")
        mj1_pt = ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']]
        mj2_pt = ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]
        self.assertEquals(data.majors['SFEN'].prettytable(), mj1_pt)
        self.assertEquals(data.majors['SYEN'].prettytable(), mj2_pt)


    def test_student_prettytable(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")
        st1_pt = ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], 'None']
        st2_pt = ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], 'None']
        self.assertEquals(data.students['10103'].prettytable(), st1_pt)
        self.assertEquals(data.students['10115'].prettytable(), st2_pt)
    
    def test_instructor_prettytable(self):
        data = hw10.University("/Users/cylee820621/Desktop/SSW-810/hw10")
        it_pt = ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4)
        self.assertEquals(next(data.instructors['98765'].prettytable()), it_pt)
       

if __name__== "__main__":
    unittest.main(exit=False, verbosity=2)