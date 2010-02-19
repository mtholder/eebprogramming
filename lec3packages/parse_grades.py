import sys

def parse_file(inp):
    """Will parse a space separated grade file.
    Returns three objects:
        - a list of grade items (from the header of the file),
        - a dict mapping student id to a list of grades
        - a dict mapping student id to a the student's name

    Students with incomplete grades will be disregarded.
    """
    sg = {}
    sn = {}
    for n, line in enumerate(inp):
        aw = line.split()
        if n == 0:
            lgi = aw[3:]
            #print lgi
        else:
            sid = aw[2]
            assert sid not in sg
            assert sid not in sn
            gr_strings = aw[3:]
            if len(gr_strings) != len(lgi):
                sys.stderr.write("Skipping student " + sid +" because they don't have enough grades\n")
            else:
                gf = []
                for i in gr_strings:
                    gf.append(float(i))
                sg[sid] = gf
                sn[sid] = aw[1] + " " + aw[0]
    return lgi, sg, sn



def calc_mean_for_grade_item(sg, ind):
    sum = 0.0
    number = 0
    for grade_list in sg.itervalues():
        sum = sum + grade_list[ind]
        number += 1
    return sum/number


filename = sys.argv[1]
file_obj = open(filename, 'rU')
blob = parse_file(file_obj)
grade_items, student_grades, student_names = blob


#print "grade_items =", grade_items
#print "student_grades =", student_grades
#print "student_names =", student_names

mean_for_item = sys.argv[2]


if mean_for_item in grade_items:
    sys.stderr.write("Calculating mean for the grade item" + str(mean_for_item) + "\n")
    ind = grade_items.index(mean_for_item)
    print calc_mean_for_grade_item(student_grades, ind)
elif mean_for_item in student_grades:
    sys.stderr.write("Calculating mean for student " + str(mean_for_item) + "\n")
    grades = student_grades[mean_for_item]
    mean = sum(grades)/len(grades)
    print mean
else:
    sys.exit("I don't know what " + mean_for_item + " is!")
