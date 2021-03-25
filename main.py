# Import Dependencies
from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)

# Get courses from JSON
# Courses is a list of dictionaries. 
# Uncomment to view the print out on your command line tool. 
with open('student_courses.json') as d:
    course_data = json.load(d)
students = course_data['students']
courses = course_data['courses']
#print('Courses loaded from file: ', students)
#print('Courses loaded from file: ', courses)

# Initialize "course buckets" array
courseBuckets = dict()
coursesList = []

# Create "course buckets" for courses: index 0 represents course 1, index 1 represents course 2...
for course in courses:
	# Index 0 of the people array is always the professor.
	courseBuckets[course['name']] = [course['professor']]

# For each student, check what courses they are enrolled in and put them in "course buckets" accordingly
for student in students:
	for courseId in student['courses']:
		courseName = courses[courseId-1]['name']
		courseBuckets[courseName].append(student['name'])

# Print out students in each course
for courseName, students in courseBuckets.items():
	# Append all courses to list in hashmap form (FOR PART 2 USE)
	coursesList.append({courseName: students})
	print(courseName, ":",  ", ".join(students))

# for course in coursesList:
# 	print("ajsdnoiuasd")
# 	print(course.get())
# Render using "courses.html"
# Note: "courses.html" can be found in the "templates" folder
# CSS file in static/css adds formating to the template as well
# Provide courses as an argument to the html
@app.route('/')
def home_page():
	return render_template('home_page.html', coursesList = coursesList, coursesJSON = courses)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
	coursesList = []
	course = str(request.args.get("title"))
	print(course)

	# If all course courses is option, then include all courses
	if course == "All Courses":
		for courseName, students in courseBuckets.items():
			coursesList.append({courseName: students})
	# Otherwise, only include selected course
	else:
		coursesList.append({course: courseBuckets[course]})

	return render_template('home_page.html', coursesList = coursesList, coursesJSON = courses)



if __name__ == '__main__':
	app.debug = True
	app.run(host = 'localhost', port = 5000)