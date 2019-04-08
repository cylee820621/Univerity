"""
@author: cylee820621
"""
import unittest
import hw09

class Hw9CleeTest(unittest.TestCase):
    def test_read_student(self):
        data = hw09.University("/Users/cylee820621/Desktop/SSW-810/hw9")
        keys = ['10103', '10115', '10172', '10175', '10183', '11399', '11461', '11658', '11714', '11788']
        self.assertEquals(data.students.__len__(), len(keys))

    def test_read_instructor(self):
        data = hw09.University("/Users/cylee820621/Desktop/SSW-810/hw9")
        keys = ['98765', '98764', '98763', '98762', '98761', '98760']
        self.assertEquals(data.instructors.__len__(), len(keys))

    def test_read_grade(self):
        data = hw09.University("/Users/cylee820621/Desktop/SSW-810/hw9")  
        self.assertEquals(data.students['10103'].cwid, '10103')
        self.assertEquals(data.students['10103'].name, 'Baldwin, C')
        self.assertEquals(data.students['10103'].dept, 'SFEN')
        self.assertEquals(data.students['10103'].course.__len__(), 4)
    
    def test_student_prettytable(self):
        data = hw09.University("/Users/cylee820621/Desktop/SSW-810/hw9")
        st_pt = ['10103', 'Baldwin, C', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']]
        self.assertEquals(data.students['10103'].prettytable(), st_pt)
    
    def test_instructor_prettytable(self):
        data = hw09.University("/Users/cylee820621/Desktop/SSW-810/hw9")
        it_pt = ('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4)
        self.assertEquals(next(data.instructors['98765'].prettytable()), it_pt)
       

if __name__== "__main__":
    unittest.main(exit=False, verbosity=2)