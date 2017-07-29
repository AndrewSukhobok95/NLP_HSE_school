import pandas as pd
import re

table = pd.read_csv('sentiframes_df.csv')

def find_regexp(s):
    regexp = re.compile('\(.*?\)', flags = re.U | re.DOTALL)
    lst = regexp.findall(s)
    if len(lst)==0:
        return None
    return lst

def find_regexp_2(s):
    regexp = re.compile('\(.*?\)', flags = re.U | re.DOTALL)
    lst = regexp.findall(s)
    return lst

def update(A, A1, A2, A3, A4, lst1, lemma_child1):
    lst = A
    for i in range(5):
        if A1 != None and i < len(A1):
            s = A1[i][1:len(A1[i])-1].split()
            if len(set(s)&set(lst1)) > 1:
                lst[0] = lemma_child1
                 
        if A2 != None and i < len(A2):
            s = A2[i][1:len(A2[i])-1].split()
            if len(set(s)&set(lst1)) > 1:
                lst[1] = lemma_child1

        if A3 != None and i < len(A3):
            s = A3[i][1:len(A3[i])-1].split()
            if len(set(s)&set(lst1)) > 1:
                lst[2] = lemma_child1

        if A4 != None and i < len(A4):
            s = A4[i][1:len(A4[i])-1].split()
            if len(set(s)&set(lst1)) > 1:
                lst[3] = lemma_child1
    return lst

def find_polar(parent, child1, child2):
    lst1 = [child1[3]]
    lst1 += child1[4].split('|')
    lst2 = [child2[3]]
    lst2 += child2[4].split('|')
    lemma_parent = parent[len(parent)-1]
    lemma_child1= child1[len(child1)-1]
    lemma_child2= child2[len(child2)-1]

    A=[0, 0, 0, 0]    #граммемы актантов глагола - из русентифреймс
    
    notindict = table[table.lemma==lemma_parent]
    A1 = find_regexp(str(notindict.A1))   #признаки первого актанта глагола
    A2 = find_regexp(str(notindict.A2))
    A3 = find_regexp(str(notindict.A3))    
    A4 = find_regexp(str(notindict.A4))
    
    A = update(A, A1, A2, A3, A4, lst1, lemma_child1)
    A = update(A, A1, A2, A3, A4, lst2, lemma_child2)

    st = set()
    for i in range(len(A)):
        if A[i] != 0:
            st.add('A'+str(i+1))
    if len(table[table.lemma==lemma_parent])==0: return None
    line_num = int(table[table.lemma==lemma_parent].index.values)
    try:
      row = find_regexp_2(table.get_value(line_num, 'Polarity'))
    except:
      return None
    my_set=set()
    for i in st:
        for j in st:
            if i != j:
                my_set.add(i+', '+j)    #сет всех возможных комбинаций пар
    result=list()    
    for actants in row:
        for combo in my_set:
            if actants.find(combo) != -1:
                polarity = actants.split(',')[2]
                polarity = polarity[1:len(polarity)]
                if polarity == 'pos' :
                   polarity=1
                else: polarity=-1
                first = actants.split(',')[0]
                first = first[1:len(first)]
                second = actants.split(',')[1]
                second = second[1:len(second)]
                frs = A[int(first[1])-1]
                scd = A[int(second[1])-1]
                result.append((frs, scd, polarity))
                #!!! вывожу результат на экран. правьте и делайте так, как вам удобно !!!
                #если делать return frs, scd, polarity, то выводятся не все данные.
    return result

lst = [['31', '42', 'бось', 'VERB', 'Aspect=Imperf|VerbForm=Inf|fPOS=VERB++', '2', 'nsubj', 'бояться'],       
       ['78', '83', 'Сирии', 'NOUN', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Sing|fPOS=NOUN++', '10', 'dobj', 'сирия'],
       ['107', '115', 'Румийлан', 'NOUN', 'Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing|fPOS=NOUN++', '15', 'appos', 'румийлан']]
parent = lst[0][len(lst[0])-1]  #лемма родителя

l = table[table.lemma==u'атака'].empty #false есть в словаре = not l, true нет в словаре

find_polar(lst[0], lst[1], lst[2])
