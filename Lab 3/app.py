from pickle import NONE
from jinja2 import Template
from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from flask import url_for
from csv import DictReader
import csv
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    cols = []
    with open('data.csv', newline="") as f:
        reader = csv.reader(f)
        file = list(reader)
        for col in file:
            cols.append(col)
    rows = cols[1:]

    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        ID = request.form["ID"]
        value = request.form["id_value"]
        if value == "":
            return render_template('error.html')
        if ID == "student_id":
            name = []
            total1 = 0
            for i in rows:
                if int(i[0]) == int(value):
                    name.append(i)
                    total1 = total1 + int(i[2])

            if total1 == 0:
                return render_template("error.html")
            else:
                template = '''
                
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8" />
                    <title> Student Details </title>
                </head>
                
                <body>
                    <h1>Enter the Details</h1>
                    
                    <table border = "2" id = "student-details-table">
                        <thead>
                            <tr>
                                <th>Student Id</th>
                                <th>Course Id</th>
                                <th>Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for id in data %}
                            <tr>
                                <td>{{id[0]}}</td>
                                <td>{{id[1]}}</td>
                                <td>{{id[2]}}</td>
                            </tr>
                            {% endfor %}
                
                            <thead>
                                <tr>
                                    <th id="total" colspan="2">Total Marks</th>
                                    <td>{{total}}</td>
                                </tr>
                            </thead>
                        </tbody>
                    </table>
                
                    <br>
                    <a href="/">Go Back</a>
                </body>
                
                </html>'''
                result = Template(template)
                File = open("./templates/student.html", "w")
                output = File.write(result.render(data=name, total=total1))
                File.close()

                return render_template('student.html')
        elif ID == "course_id":
            if value == "":
                return render_template('error.html')
            avg = 0
            list_1 = []
            total = 0
            s = 0
            for i in rows:
                if int(i[1]) == int(value):
                    list_1.append(i)
                    total = total + int(i[2])
            if total == 0:
                return render_template("error.html")
            max_1 = []
            for i in list_1:
                max_1.append(i[2])
                if int(i[2]) > s:
                    s = int(i[2])

            avg = total/len(max_1)
            plt.hist(max_1)
            plt.xlabel("Marks")
            plt.ylabel("Frequency")

            url_for('static', filename='myplot.png')
            plt.savefig('static/myplot.png', dpi=100)

            template = '''
            
            <!DOCTYPE html>
			<html>
			<head>
				<meta charset="UTF-8"/>
				<title> Course Details </title>
			</head>
			<body>
			    <h1>Course Details</h1>
            	<table border = "2" id = "course-details-table">
                    <thead>
                        <tr>
                            <th>Average Marks</th>
                            <th>Maximum Marks</th>
				    	</tr>
                    </thead>
                    <tbody>
                            <tr>
                                <td>{{avg}}</td>
                                <td>{{max}}</td>
                            </tr>
                    </tbody>
                </table>
                <img src="/static/myplot.png"/>
                <br>
                <a href="/">Go Back</a>
	        </body>
			</html> 		
			'''

            result = Template(template)
            File = open("./templates/course.html", "w")
            output = File.write(result.render(avg=avg, max=s))
            File.close()

            return render_template('course.html')
        else:
            return render_template('error.html')

    else:
        error()


def error():
    print("error")
    return render_template('error.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
