# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
L = ''.join([chr(i) for i in range(97,123)])
L += L.upper()  #字母
DF0 = '=<+-*/();,[]'   #单分界符
DF1 = []
for i in DF0:
    DF1.append(i)
DF = pd.Series(['EQ','LT','PLUS','MINUS','TIMES','OVER','LPAREN','RPAREN',
        'SEMI','COMMA','LMIDPAREN','RMIDPAREN'],index =DF1)
DF1 = pd.Series(['ASSIGN','UNDERANGE','DOT'],index = [':=','..','.'])
def getword(line,i):
    if(line[i] in L):
        a=line[i]
        i+=1
        while (i<len(line)) and (line[i] in L):
            a+=line[i]
            i+=1
        return a,i
    elif line[i] in ' \r\t\n':
        i+=1
        while (i<len(line)) and (line[i] in ' \r\t\n') :
            i+=1
        if i<len(line):
            a,i = getword(line,i)
            return a,i
        else :
            return 0,-1
    elif line[i:i+3] == '::=':
        i += 3
        a,i= getword(line,i)
        return a,i
    elif (line[i:i+2] == ':=') or (line[i:i+2] == '..'):
        return line[i:i+2],i+2
    else :
        return line[i],i+1
def Cfirst(VT,a,A,B,First,R):          
    if (a in R) or (len(First[a])!=0):
        return
    R.append(a)
    wait=[]
    for i in range( len(A) ):
        if (a == A[i]):
            if (B[i][0] in VT):       #若为终极符，则判断是否已有后加入
                if ( B[i][0] not in First[a]):
                    First[a].append(B[i][0])
            else:                    #若为非终极符，则将其First加入
                wait.append(i)
    for i in wait:        
        Cfirst(VT,B[i][0],A,B,First,R)
        for b in First[B[i][0]]:
            if (b not in First[a]):
                First[a].append(b)
        j = 0
        while ('KONG' in First[B[i][j]]) :  #若其First集存在空
            j += 1                         #则将其下一个的First加入
            if(j >= len(B[i])):
                break
            if (B[i][j] in VT):
                if (B[i][j] not in First[a]):
                    First[a].append(B[i][j])
                    break
            else :
                Cfirst(VT,B[i][j],A,B,First,R)
                for b in First[B[i][j]]:
                    if (b not in First[a]):
                        First[a].append(b)
    R.remove(a)
def Next(i0,First,VN,A,P0):
    if(1):
        a0 = i0[0].index('*') #找到*的下标
        if(1):
            j0 = i0[0][:]
            j0[a0],j0[a0 + 1] = j0[a0 + 1] , j0[a0]  #*后移一位
            a = a0 + 1
            u = []    #展望符集
            IS0=[]
            wait = []
            IS0.append([j0,i0[1]])
            i1 = i0[1]
            while (a != len(j0) - 1) and (j0[a + 1] in VN):
                for i in range(len(A)):
                    if j0[a+1] == A[i]:
                        if (a != len(j0) - 2):
                            if(j0[a + 2] in VT):
                                u = [j0[a + 2]]
                            else: 
                                k = a + 2
                                while(k<len(j0) and (j0[k] in VN) and ('KONG' in First[j0[k]])):
                                    for j in First[j0[k]]:
                                        if(j != 'KONG') and (j not in u):
                                            u.append(j)
                                    k += 1
                                if(k == len(j0)):
                                    for j in i1:
                                        if j not in u:
                                            u.append(j)
                                elif j0[k] not in VN:
                                    if j0[k] not in u:
                                        u.append(j0[k])
                                else:
                                    for j in First[j0[k]]:
                                        if j not in u:
                                            u.append(j)
                        else :
                            u = i1
                        IS0.append([P0[i],u])
                        wait.append([P0[i],u])
                if (len(wait) == 0):
                    break
                j0 = wait[0][0]
                i1 = wait[0][1]
                wait.remove(wait[0])
                a = j0.index('*')
    return IS0
filename = 'wenfa.txt'
fp = open(filename,'r')
VN=[]
VT=[]
P=[]
for line in fp.readlines():
    p=[]
    i=0
    while(i<len(line)):
        a,i = getword(line,i)
        if i == -1:
            break
        elif a=='|':
            P.append(p)
            b=p[0]
            p=[]
            p.append(b)
        else:
            p.append(a)
    P.append(p)
fp.close()
S = P[0][0]
A=[]
B=[]
for i in range(len(P)):
    if P[i][0] not in VN:
        VN.append(P[i][0])
    A.append(P[i][0])
    B.append(P[i][1:len(P[i])])
for i in range(len(P)):
    for j in range(1,len(P[i])):
        if (P[i][j] not in VN) and (P[i][j] not in VT):
            VT.append(P[i][j])   
for i in range(len(VT)):
    if VT[i] in DF :
        VT[i] = DF[VT[i]]
    elif VT[i] in DF1:
        VT[i] = DF1[VT[i]]
for i in range(len(B)):
    for j in range(len(B[i])):
        if B[i][j] in DF:
            B[i][j] = DF[B[i][j]]
        elif B[i][j] in DF1:
            B[i][j] = DF1[B[i][j]]
P=[]
for i in range(len(A)):
    P.append([A[i]]+B[i])
First = {}
for i in VN:         #计算所有VN的First集
    First[i] = []
for i in VN:
    if(len(First[i]) == 0):
        R=[]
        Cfirst(VT,i,A,B,First,R)
IS = []
P0=[]
for i in P:
    P1=i[:]
    P1.insert(1,'*')
    P0.append(P1)
IS0 = []
u=[]
wait=[]
IS0.append([P0[0],['#']])
a = P0[0].index('*')
if (a != len(P0[0]) - 1) and (P0[0][a + 1] in VN):
    for i in range(len(A)):
        if P0[0][a+1] == A[i]:
            if (a != len(P0[0]) - 2):
                if(P0[0][a + 2] in VT):
                    u = [P0[0][a + 2]]
                elif ('KONG' in First[P0[0][a + 2]]):
                    u = IS0[0][1][:]
                    for j in First[P0[0][a + 2]]:
                        if(j != 'KONG') and (j not in u):
                            u.append(j)
                else:
                    u = First[P0[0][a + 2]]
            else:
                u = IS0[0][1]
            IS0.append([P0[i],u])
    IS.append(IS0)
    wait.append(0)
a = len(VN) + len(VT) + 1
t = ['error'] * a
t = [t]
a=VT+['#']+VN
ix = ['n']
df0 = pd.DataFrame(t,index =ix ,columns = a)
df = pd.DataFrame(t,columns = a)
ix = 0  #dangqian
im = 0 #zuida
while(ix <= im):
    ISk = IS[ix]
    Temp=[]
    for i0 in ISk:
        a0 = i0[0].index('*')
        if(a0 == len(i0[0]) - 1):
            j0 = i0[0][:]
            j0.remove('*')
            k0 = P.index(j0)
            for c in i0[1]:
                df[c][ix] = 'R' + str(k0)
        else:
            m = i0[0][a0+1]
            IS0 = Next(i0,First,VN,A,P0)
            k=1
            for i in range(len(Temp)):
                if m == Temp[i][0]:
                    k = 0
                    for j in IS0:
                        if j not in Temp[i][1]:
                            Temp[i][1].append(j)
                    break
            if(k):
                Temp.append([m,IS0])
    for i in range(len(Temp)):
        k = 1
        for j in range(len(IS)):
            if(Temp[i][1] == IS[j]):
                k = 0
                df[Temp[i][0]][ix] = 'S' + str(j)
        if(k):
            IS.append(Temp[i][1])
            im += 1
            df = pd.concat([df,df0])
            df = df.reindex(range(im))
            df[Temp[i][0]][ix] = 'S' + str(im)
    ix = ix + 1            



















