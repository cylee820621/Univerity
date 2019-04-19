"""
@author: cylee820621
"""
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return "Heloo world!"

@app.route('/Goodbye')
def see_ya():
    return "see you later"

@app.route('/instructor_courses')
def instructor_courses():
    """
    another page for needed instructor table
    """    
    DB_file = "/Users/cylee820621/Desktop/SSW-810/hw11/810_startup.db"

    query = """select HW11_instructors.CWID,
                    HW11_instructors.Name,
                    HW11_instructors.Dept,
                    HW11_grades.Course,
                    COUNT(HW11_grades.Student_CWID) as cnt
                    from HW11_instructors
                    left join HW11_grades
                    on HW11_instructors.CWID =HW11_grades.instructor_CWID
                    GROUP BY Course order by Cwid"""

    db = sqlite3.connect(DB_file)
    results = db.execute(query)

    data = [{'cwid':cwid,'name': name,'dept':dept,'course':course,'studnet':student}
            for cwid,name,dept,course,student in results]
        
    db.close()
    
    return render_template('instructor_courses.html',
                            title="Stevens Repository",
                            my_header="Stevens Repository",
                            my_param="Number of students by course and instructor",
                            instructors = data)

app.run(debug=True)