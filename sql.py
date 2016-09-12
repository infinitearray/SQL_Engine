import sqlparse
import sys
import itertools

def get_condition(cmd,string):
    conds = ""
    for i in range(len(cmd)):
        if cmd[i:i+5]=="where":
            conds = cmd[i+5:]
            break
    conds=conds.strip('\n').strip()
    conds = conds.split(string)
    conds = [x.encode('ascii','ignore').strip(',').strip() for x in conds]
    conds = filter(None, conds)
    return conds

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
    attrs = temp.split(',')
    attrs = [x.encode('ascii','ignore').strip(',').strip() for x in attrs]
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

def print_result(cmd,a,attributes,database,tables,conditions):
    maxlen = len(a)
    res = list(itertools.product(*a))
    array = []
    for i in database:
        for j in tables:
            if i[0]==j:
                for x in range(1,len(i)):
                    array.append(i[0]+"."+i[x])
    final = []
    for i in res:
        final.append(list(itertools.chain(*i)))
    #####   For conditions
    if('and' in cmd or ('and' not in cmd and 'or' not in cmd)):
        for i in conditions:
            var = i.split("=")
            ans = []
            for i in final:
                flag = 0
                for j in database:
                    if j[0] in var[1]:
                        flag = 1
                        break
                if(flag==0):
                    for j in range(len(array)):
                        if(array[j]==var[0] and i[j]==int(var[1])):
                           ans.append(i)
                else:
                    for j in range(len(array)):
                        for k in range(len(array)):
                            if(array[j]==var[0] and array[k]==var[1] and i[j]==i[k]):
                                ans.append(i)
            final = ans
    else:
        conditions = get_condition(cmd,"or")
        ans =[]
        for i in conditions:
            var = i.split("=")
            for i in final:
                flag = 0
                for j in database:
                    if j[0] in var[1]:
                        flag = 1
                        break
                if(flag==0):
                    for j in range(len(array)):
                        if(array[j]==var[0] and i[j]==int(var[1]) and i not in ans):
                           ans.append(i)
                else:
                    for j in range(len(array)):
                        for k in range(len(array)):
                            if(array[j]==var[0] and array[k]==var[1] and i[j]==i[k] and i not in ans):
                                ans.append(i)
        final = ans

    if(attributes[0]=="*"):
        for i in array:
            print i,"\t",
        print
        print "-"*80
        for i in final:
            for j in i:
                print j,"\t\t",
            print
    else:
        sel = []
        cnt = 0
        directory = {}
        for i in tables:
            for j in database:
                if i==j[0]:
                    directory[i]=len(j)-1
        for i in tables:
            for j in database:
                if i==j[0]:
                  for k in attributes:
                      if i in k:
                          sel.append(cnt+j.index(k.replace(i+".",""))-1)
            cnt=cnt+directory[i]
        for i in attributes:
            print i,"\t",
        print
        print "-"*80
        for i in final:
            for j in sel:
                print i[j],"\t\t",
            print

######################  Get all the columns and tables
database = []
text = [line.strip('\r\n') for line in open('metadata.txt')]
while True:
    try :
        index = text.index('<end_table>')
    except:
        break
    database.append(text[1:index])
    text = text[index+1:]
#print database
######################
cmd = sys.argv[1]
table_data = []
attributes = get_attributes(cmd)
tables = get_table(cmd)
conditions = get_condition(cmd,"and")
"""print cmd
print "-"*20
attributes = get_attributes(cmd)
print "Attributes:",attributes
tables = get_table(cmd)
print "Tables:",tables
conditions = get_condition(cmd,"and")
print "Conditions:",conditions
print '-'*20"""
tables = tables.split(',')
for i in tables:
    lines = [line.rstrip('\r\n') for line in open(i+".csv")]
    list1 = []
    for j in lines:
        temp = [int(x) for x in j.split(',')]
        list1.append(temp)
    table_data.append(list1)
print_result(cmd,table_data,attributes,database,tables,conditions)
