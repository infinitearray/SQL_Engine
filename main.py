import sqlparse
import sys
import os
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
    distinct_flag = 0
    if "distinct" in cmd:
        distinct_flag = 1
        for i in range(len(attributes)):
            attributes[i] = attributes[i][8:].strip("()")

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
    
    max_flag = 0
    min_flag = 0
    avg_flag = 0
    sum_flag = 0
    
    if ("max" in cmd or "min" in cmd or "avg" in cmd or "sum" in cmd):
        try:
            assert (len(attributes)==1)
            attributes[0] = attributes[0][3:].strip("()")
        except:
            sys.exit('Error : Cannot project multiple columns when using aggregate functions')
    if "max" in cmd:
        max_flag = 1
    elif "min" in cmd:
        min_flag = 1
    elif "avg" in cmd:
        avg_flag = 1
    elif "sum" in cmd:
        sum_flag = 1
    if(attributes[0]=="*"):
        for i in array:
            print i,"\t",
        print
#        print "-"*80
        temp_final = []
        for i in final:
            if distinct_flag and i not in temp_final:
                temp_final.append(i)
                for j in i:
                    print j,"\t\t",
                print
            else:
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
 #       print "-"*80
        if max_flag:
            max_elem = final[0][sel[0]]
            for i in final:
                if(i[sel[0]]>max_elem):
                    max_elem = i[sel[0]]
            print max_elem
        elif min_flag:
            min_elem = final[0][sel[0]]
            for i in final:
                if(i[sel[0]]<min_elem):
                    min_elem = i[sel[0]]
            print min_elem
        elif sum_flag:
            sum_elem = 0
            for i in final:
                sum_elem = sum_elem+i[sel[0]]
            print sum_elem
        elif avg_flag:
            avg_elem = 0
            for i in final:
                avg_elem = avg_elem +i[sel[0]]
            print float(avg_elem/len(final))
        else:
            temp_temp = []
            if distinct_flag:
                for i in final:
                    temp = []
                    for j in sel:
                        temp.append(i[j])
                    if temp not in temp_temp:
                        temp_temp.append(temp)
                for i in temp_temp:
                    for j in i:
                        print j,"\t\t",
                    print
            else:
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
cmd = ""
try:
    cmd = sys.argv[1].strip(';')
except:
    sys.exit("Error : No SQL query\nUsage : python main.py <sql-query>")
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
    try:
        lines = [line.rstrip('\r\n') for line in open(i+".csv")]
        list1 = []
        for j in lines:
            temp = [int(x) for x in j.split(',')]
            list1.append(temp)
        table_data.append(list1)
    except:
        sys.exit("Error : No table "+i+".csv")

temp = []
for i in conditions:
    temp.append(i.split("=")[0])
for i in attributes+temp:
    cnt = 0
    for j in tables:
        for k in database:
            if j==k[0] and i in k:
                cnt = cnt+1
    if cnt>1:
        sys.exit("Error : Use <table_name>.col for same column names in different tables")
for i in range(len(attributes)):
    var = 0
    for j in tables:
        if j in attributes[i]:
            var = 1
    if var==0:
        for j in tables:
            for k in database:
                if attributes[i] in k and j==k[0] and ("distinct" or "sum" or "avg" or "min" or "max" not in attributes[i]):
                    attributes[i]=j+"."+attributes[i] 
                elif attributes[i][4:-1] in k and j==k[0] and ("sum" or "avg" or "min" or "max" in attributes[i]):
                    attributes[i]=attributes[i][:4]+j+"."+attributes[i][4:]
                elif attributes[i][9:-1] in k and j==k[0] and ("distinct" in attributes[i]):# or "avg" or "min" or "max" in attributes[i]):
                    attributes[i]=attributes[i][:9]+j+"."+attributes[i][9:]

for i in range(len(conditions)):
    var = 0
    temp_cond = conditions[i].split("=")[0]
    for j in tables:
        if j in temp_cond:
            var = 1
    if var==0:
        for j in tables:
            for k in database:
                if temp_cond in k and j==k[0]:
                    conditions[i]=j+"."+conditions[i]

print_result(cmd,table_data,attributes,database,tables,conditions)
