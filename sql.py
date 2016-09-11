import sqlparse
import sys
import itertools

def get_condition(cmd):
    conds = ""
    for i in range(len(cmd)):
        if cmd[i:i+5]=="where":
            conds = cmd[i+5:]
            break
    return conds.strip()

def get_attributes(cmd):
    temp = ""
    for i in range(len(cmd)):
        if cmd[i:i+6]=="select":
            temp = cmd[i+6:]
            break
    for i in range(len(temp)):
        if temp[i:i+4]=="from":
            temp = temp[:i]
            break
#    print isinstance(temp, basestring)
    attrs = temp.split('\n')
    for i in range(len(attrs)):
        attrs[i] = attrs[i].encode('ascii','ignore').strip(',').strip()
    attrs = filter(None, attrs)
    return attrs

def get_table(cmd):
    temp = ""
    for i in range(len(cmd)):
        if cmd[i:i+4]=="from":
            temp = cmd[i+5:]
            break
    temp=temp.strip()
    for i in range(len(temp)):
        if temp[i:i+5]=="where":
            temp = temp[:i]
            break
    tables = temp.split('\n')
    tables = [x.encode('ascii','ignore').strip(',').strip() for x in tables]
    tables = filter(None, tables)
    return str(tables).strip('[]').strip("'")

def print_result(a):
    maxlen = len(a)
    res = list(itertools.product(*a))
    final = []
    for i in res:
        print list(itertools.chain(*i))

######################Get all the columns and tables
database = []
text = [line.strip('\r\n') for line in open('metadata.txt')]
while True:
    try :
        index = text.index('<end_table>')
    except:
        break
    database.append(text[1:index])
    text = text[index+1:]
print database
######################
cmd = sys.argv[1]
table_data = []
print cmd
print "-"*20
print "Attributes:",get_attributes(cmd)
tables = get_table(cmd)
print "Tables:",tables
print "Conditions:",get_condition(cmd)
print '-'*20
tables = tables.split(',')
for i in tables:
    lines = [line.rstrip('\r\n') for line in open(i+".csv")]
    list1 = []
    for j in lines:
        temp = [int(x) for x in j.split(',')]
        list1.append(temp)
    table_data.append(list1)
print_result(table_data)