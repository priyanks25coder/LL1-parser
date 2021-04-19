#Epsilon represented by @
#Starting Variable must be in the left hand side of first production
#Production Rules should be in the following format only
# A -> R/G/...

import numpy as np
from prettytable import PrettyTable

def first(seq,gra,nonterm):
    first_=set()
    for i in seq:
        flag=0
        if i in nonterm:
            for j in gra[i]:
                first_= first_ | first(j,gra,nonterm)
                if '@' in first(j,gra,nonterm):
                    flag=1
            if flag==0:
                break
        else:
            first_=first_|{i}
            break
    return first_


def follow(var_nt,gra,nonterm):
    follow_=set()
    start_var=(list(gra.keys())[0])  
    if var_nt==start_var:
        follow_=follow_|{'$'}
    for left_v in gra:
        for prod in gra[left_v]:
            if prod!='@':
                for i in range(len(prod)):
                    if prod[i]==var_nt:
                        if i!=(len(prod)-1):
                            next_str=prod[(i+1):]
                            first_str=first(next_str,gra,nonterm)
                            if '@' in first_str:
                                follow_= follow_ | (first_str-{'@'})
                                if(left_v!=var_nt):
                                    follow_=follow_  | follow(left_v,gra,nonterm)
                            else:
                                follow_= follow_ | first_str
                        else:
                            if(left_v!=var_nt):
                                follow_=follow_  | follow(left_v,gra,nonterm)
    return follow_

def ll1_parser(gra,nonterm,term):
    mat=np.array([["0"]*(len(term)+2)]*(len(nonterm)+1))
    mat=mat.astype('<U100')
    term.append('$')
    for i in range((len(nonterm)+1)):
        for j in range((len(term)+1)):
            if i==0 and j>=1:
                mat[i,j]=term[j-1]
            elif i>=1 and j==0:
                mat[i,j]=nonterm[i-1]

    isll1=True

    for left_v in gra:
        row_n=nonterm.index(left_v)+1
        for prod in gra[left_v]:
            first_rule=first(prod,gra,nonterm)
            if '@' in first_rule:
                first_rule=first_rule-{'@'}
                first_rule=first_rule | follow_set[left_v]
            for i in first_rule:
                col_n=term.index(i)+1
                if mat[row_n,col_n]=='0':
                    mat[row_n,col_n]=left_v+'->'+prod
                else:
                    mat[row_n,col_n]=mat[row_n,col_n]+'\n'+left_v+'->'+prod
                    isll1=False
    x=PrettyTable()
    x.field_names=mat[0]
    for i in range(len(mat)):
        if i>0:
            x.add_row(mat[i])
    print(x)
    if isll1:
        print("This grammar can be used for LL1 Parser")
    else:
        print("This grammar cannot be used for LL1 Parser")

def read_gra(fname):
    f=open(fname,"r")
    raw_gra=f.read()
    lines=raw_gra.split('\n')
    gra=dict({})
    for i in lines:
        words=i.split()
        prod=words[2].split('/')
        gra[words[0]]=prod
    return gra


follow_set=dict({})
first_set=dict({})

nonterm=[]
term=[]

n_nonterm=int(input("Enter number of non terminals: "))
print("Enter the non terminals:")
for i in range(n_nonterm):
    c=input()
    nonterm.append(c)

n_term=int(input("Enter number of terminals: "))
print("Enter the terminals:")
for i in range(n_term):
    c=input()
    term.append(c)

gra=read_gra("grammar.txt")

for i in gra:
    first_set[i]=first(i,gra,nonterm)

for i in gra:
    follow_set[i]=follow(i,gra,nonterm)

print("First of Variables of Grammar: ",end='')
print(first_set)
print("Follow of Variables of Grammar: ",end='')
print(follow_set)
ll1_parser(gra,nonterm,term)
