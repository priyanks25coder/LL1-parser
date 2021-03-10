# @ -> epsilon
# all treminal var must be of length 1 only and variables must be from A-Z
# starting variable must be in the LHS of the first  production rule

import numpy as np
from collections import deque

class Ll1parser:
    start_var=""
    gra={}
    first_gra={}
    follow_gra={}
    gra_vars=set([])
    ter=set([])
    mat=[]
    prev_follow=''

    def def_gram(self):
        gra={}
        contd="y"
        while contd=="y":
            print("Enter the left hand side of the grammer: ")
            lhs=input()

            if self.start_var=="":
                self.start_var=lhs

            rhs=[]
            c="y"
            while c=="y":
                print("Enter the right hand side of the grammer: ")
                rhs.append(input())
                c=input("If you want to enter rule for same LHS else type n: ")

            gra[lhs]=rhs
            self.first_gra[lhs]=set([])
            self.follow_gra[lhs]=set([])
            contd=input("If you want to enter more rules enter y else type n: ")
        self.gra=gra
        self.follow_gra[self.start_var].add('$')
        for i in self.gra:
            for j in self.gra[i]:
                for k in j:
                    if ord(k)>=65 and ord(k)<=90:
                        self.gra_vars.add(""+k)
                    elif k!='@':
                        self.ter.add(""+k)
        self.ter.add("$")
        self.gra_vars.add(""+self.start_var)
        print("The Grammer:")
        print(self.gra)

    def first_var(self,gvar):
        for i in self.gra:
            if i==gvar:
                for j in self.gra[i]:
                    count=0
                    for k in j:
                        if ord(k)>=65 and ord(k)<=90:
                            self.first_var(k)
                            flag=0
                            for i in self.first_gra[k]:
                                if i=='@':
                                    flag+=1
                                else:
                                    self.first_gra[gvar].add(i)
                                    
                            if flag!=1:
                                break
                            else:
                                if count==len(j)-1:
                                    self.first_gra[gvar].add('@')
                        else:
                            self.first_gra[gvar].add(k)
                            break
    
    def follow_var(self,gvar):
        for i in self.gra:
            for j in self.gra[i]:
                c=1
                for k in range(len(j)):
                    if j[k]==gvar and k==len(j)-1:
                        if i!=gvar:
                            if self.prev_follow=='':
                                self.prev_follow=gvar
                                self.follow_var(i)
                                for m in self.follow_gra[i]:
                                    self.follow_gra[gvar].add(m)
                            else:
                                if self.prev_follow!=i:
                                    self.prev_follow=i
                                    self.follow_var(i)
                                    for m in self.follow_gra[i]:
                                        self.follow_gra[gvar].add(m)
                                else:
                                    for m in self.follow_gra[i]:
                                        self.follow_gra[gvar].add(m)
                        else:
                            continue
                    elif j[k]==gvar and k!=len(j)-1:
                        if ord(j[c])>=65 and ord(j[c])<=90:
                            hasNull=False
                            while True:
                                for m in self.first_gra[j[c]]:
                                    if m!='@':
                                        self.follow_gra[gvar].add(m)
                                    else:
                                        hasNull=True
                                if hasNull==False:
                                    break
                                else:
                                    if c+1<len(j)-1:
                                        c+=1
                                        if (not(ord(j[c])>=65 and ord(j[c])<=90)):
                                            self.follow_gra[gvar].add(j[c])
                                            break
                                    else:
                                        c=len(j)-1
                                        if (not(ord(j[c])>=65 and ord(j[c])<=90)):
                                            self.follow_gra[gvar].add(j[c])
                                            break
                                        else:
                                            if i!=gvar:
                                                self.follow_var(i)
                                                for m in self.follow_gra[i]:
                                                    self.follow_gra[gvar].add(m)
                                                break
                                            else:
                                                break
                        else:
                            self.follow_gra[gvar].add(j[c])
                            break    
                    c+=1

    def first(self):
        for i in self.gra:
            self.first_var(i)
        self.disp_first()
        return 

    def follow(self):
        for i in self.gra:
            self.follow_var(i)
        self.disp_follow()
        return

    def disp_first(self):
        print(self.first_gra)
    
    def disp_follow(self):
        print(self.follow_gra)

    def disp_parsingTable(self):
        print(self.mat)

    def makeTable(self):
        isll1parser=True
        print("First for the Grammer: ")
        self.first()
        print("Follow for the Grammer: ")
        self.follow()
        gra_vars=[]
        ter=[]
        for i in self.gra_vars:
            gra_vars.append(i)
        for i in self.ter:
            ter.append(i)
        
        mat=np.array([["0"]*(len(self.ter)+1)]*(len(self.gra_vars)+1))
        mat=mat.reshape((len(self.gra_vars)+1),(len(self.ter)+1))
        mat=mat.astype('<U6')

        for i in range((len(self.gra_vars)+1)):
            for j in range((len(self.ter)+1)):
                if i==0 and j>=1:
                    mat[i,j]=ter[j-1]
                elif i>=1 and j==0:
                    mat[i,j]=gra_vars[i-1]

        for i in self.gra:
            r=gra_vars.index(i)
            r+=1
            for j in self.gra[i]:
                for k in j:
                    rule=j
                    if ((ord(k)>=65 and ord(k)<=90)):
                        hasnull=0
                        temp=self.first_gra[k]
                        for m in temp:
                            if m!='@':
                                c=ter.index(m)
                                c+=1
                                if mat[r,c]=="0":
                                    mat[r,c]=""+rule
                                else:
                                    mat[r,c]=""+mat[r,c]+","+rule
                                    isll1parser=False
                            else:
                                hasnull=1
                        
                        if hasnull==1:
                            for m in self.follow_gra[i]:
                                c=ter.index(m)
                                c+=1
                                if mat[r,c]=="0":
                                    mat[r,c]=""+rule
                                else:
                                    mat[r,c]=""+mat[r,c]+","+rule
                                    isll1parser=False
                        else:
                            break
                    else:
                        if k!='@':
                            c=ter.index(k)
                            c+=1
                            if mat[r,c]=="0":
                                mat[r,c]=""+rule
                            else:
                                mat[r,c]=""+mat[r,c]+","+rule
                                isll1parser=False
                            break
                        else:
                            for m in self.follow_gra[i]:
                                c=ter.index(m)
                                c+=1
                                if mat[r,c]=="0":
                                    mat[r,c]=""+rule
                                else:
                                    mat[r,c]=""+mat[r,c]+","+rule
                                    isll1parser=False
        self.mat=mat
        print("Parsing Table for the Grammer: ")
        self.disp_parsingTable()
        print("Note: '0' indicates empty cell....")
        if isll1parser==False:
            print("Not a LL1 Parser!!")
        else:
            print("It is a LL1 Parser")
        return isll1parser

    def parse_string(self,par_str,stk=[]):
        if len(stk)==0:
            stk.append('$')
            stk.append(self.start_var)
        
        gra_vars=[]
        ter=[]
        mat=self.mat
        print(stk,par_str)
        
        for i in self.gra_vars:
            gra_vars.append(i)
        for i in self.ter:
            ter.append(i)
        top=stk[len(stk)-1]
        
        if ((ord(top)>=65 and ord(top)<=90)):
            r=gra_vars.index(top)
            r+=1
            c=ter.index(par_str[0])
            c+=1
            rule=mat[r,c]
            stk.pop()
            for i in reversed(range(len(rule))):
                stk.append(rule[i])
            self.parse_string(par_str,stk)
        
        elif top=='@':
            stk.pop()
            self.parse_string(par_str,stk)

        elif top!='$' and par_str!='$':
            stk.pop()
            par_str=par_str[1:]
            self.parse_string(par_str,stk)
        
        elif top=='$' and par_str=="$":
            print("String Passed")
            return 
        
        elif ((top=='$' and par_str!='$') or (top!='$' and par_str=='$') or (top!='$' and par_str!='$')):
            print("String Does not Belong to this grammar")
            return

print("\nEnter the production Rules using terminal!!\n")
print("Rules\n@ means epsilon \nAll treminal variables must be of length 1 only and variables must be from A-Z \nStarting variable must be in the LHS of the first  production rule\n")
ll1_par=Ll1parser()
ll1_par.def_gram()
if ll1_par.makeTable():
    print("Parsing string to the Grammer...")
    in_str=input("Enter String which you want to check in the parser with $ at last  ")
    ll1_par.parse_string(in_str)
