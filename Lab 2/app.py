import sys
from jinja2 import Template
import csv
import matplotlib.pyplot as plt

l = sys.argv

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    file = list(reader)

record_file = file[1:]
resultdata = []
total = 0
count = 0
highest = 0
x = []


if l[1] == '-c':
    for i in record_file:
        if int(i[1]) == int(l[2]):
            total = total + int(i[2])
            x.append(i[2])
            count = count + 1
            if int(i[2]) > highest:
                highest = int(i[2])
    average = (total / count)

    plt.hist(x)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig('img.png', dpi=300)

    TEMPLATE_1 = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title> Course Data </title>
        <meta name="description" content="This page lists Jnanpith Awardees"/>
    </head>
    <body>
            <h1> Course Details </h1>
            
            <table border="1px">
                <thead>
                    <tr border="1px">
                      <th>Average Marks</th>
                      <th>Maximum Marks</th>
                  </tr>
                </thead>
                <tbody>
                
                    <tr>
                        <td>{{ average }}</td>
                        <td>{{ highest }}</td>
                    </tr>
                      
                </tbody>
            </table>
        <img src="img.png" width="400px">
    </body>
</html>"""

    def main():

        template = Template(TEMPLATE_1)
        print(template.render(average=average, highest=highest))
        content = template.render(average=average, highest=highest)
        my_html_file = open('output.html', 'w')
        my_html_file.write(content)
        my_html_file.close()

    if __name__ == "__main__":
        main()
    # execute only if run as a script

elif l[1] == '-s':
    for i in record_file:
        if i[0] == l[2]:
            resultdata.append(i)
            total = total + int(i[2])
    TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title> Student Data </title>
        <meta name="description" content="This page lists Jnanpith Awardees"/>
    </head>
    <body>
            <h1> Student Details </h1>
            
            <table border="1px">
                <thead>
                    <tr>
                      <th>Student id</th>
                      <th>Course id</th>
                      <th>Marks</th>
                  </tr>
                </thead>
                <tbody>
                {% for jnanpith in resultdata %}
                    <tr>
                        <td >{{ jnanpith[0] }}</td>
                        <td >{{ jnanpith[1] }}</td>
                        <td >{{ jnanpith[2] }}</td>
                    </tr>
                    {% endfor %}
                    <tr>
                        <td style="text-align:center" colspan="2">  Total Marks</td>
                        <td>{{ total }}</td>
                    </tr>
                </tbody>
            </table>
    </body>
</html>"""

    def main():

        template = Template(TEMPLATE)
        print(template.render(resultdata=resultdata, total=total))
        content = template.render(resultdata=resultdata, total=total)
        my_html_file = open('output.html', 'w')
        my_html_file.write(content)
        my_html_file.close()

    if __name__ == "__main__":
        main()
    # execute only if run as a script

else:
    TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8"/>
        <title> Something Went Wrong </title>
    </head>
    <body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
    </body>
</html>"""

    def main():

        template = Template(TEMPLATE)
        print(template.render())
        content = template.render()
        my_html_file = open('output.html', 'w')
        my_html_file.write(content)
        my_html_file.close()

    if __name__ == "__main__":
        main()
