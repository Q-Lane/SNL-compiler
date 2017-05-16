# -*- coding: utf-8 -*-
#计算a的First集
L = ''.join([chr(i) for i in range(97,123)])
L += L.upper()  #字母
def getword(line,i):
    if(line[i] in L):
        a=line[i]
        i+=1
        while (i<len(line)) and (line[i] in L):
            a+=line[i]
            i+=1
        return a,i
    elif line[i] in ' \t\n':
        i+=1
        while (i<len(line)) and (line[i] in ' \t\n') :
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
#计算b的Follow集    
def Cfollow(VT,b,A,B,First,Follow,R):       
    if ((b in R) or (len(Follow[b]) != 0 and Follow[b] != '#')):
        return
    R.append(b)
    wait=[]
    for i in range(len(B)):
        if (b in B[i]):                #在->右边找到b
            J = []
            for j in range(len(B[i])):
                if(B[i][j] == b):
                    J.append(j)
            for m in range(len(J)):
                if(J[m] == ( len( B[i] ) - 1) ):   #若在末尾
                    wait.append(A[i])
                else :
                    k = J[m] + 1 
                    if(B[i][k] in VT):             #若下一位为终止符，则放入follow
                        if(B[i][k] not in Follow[b]):
                            Follow[b].append(B[i][k])
                    else :
                        for c in First[B[i][k]]: #非终止符则将其fisrt集放入
                            if((c not in Follow[b]) and (c != 'KONG')):
                                Follow[b].append(c)
                        while('KONG' in First[B[i][k]]): 
                            k += 1
                            if(k == len(B[i])):
                                wait.append(A[i])
                                break
                            if(B[i][k] in VT):
                                if(B[i][k] not in Follow[b]):
                                    Follow[b].append(B[i][k])
                                break
                            else :
                                for c in First[B[i][k]]:
                                    if((c not in Follow[b]) and (c != 'KONG')):
                                        Follow[b].append(c)
    for i in wait:
        Cfollow(VT,i,A,B,First,Follow,R)
        for a in Follow[i]:
            if(a not in Follow[b]):
                Follow[b].append(a)
    R.remove(b)
#计算Pridect集
def Cpredict(VT,A,B,First,Follow,P):
    for i in range(len(A)):
        if (B[i][0] == 'KONG'):
            P[i] = Follow[A[i]]
        elif (B[i][0] in VT):
            P[i].append(B[i][0])
        else :
            if('KONG' not in First[B[i][0]]):
                for c in First[B[i][0]]:
                    P[i].append(c)
            else :
                for a in First[B[i][0]]:
                    if (a != 'KONG'):
                        P[i].append(a)
                j = 0
                while('KONG' in First[B[i][j]]):
                    j += 1
                    if (j == len(B[i])):
                        for a in Follow[A[i]]:
                            if (a not in P[i]):
                                P[i].append(a)
                        break
                    if (B[i][j] in VT):
                        if (B[i][j] not in P[i]):
                            P[i].append(B[i][j])
                        break
                    for a in First[B[i][j]]:
                        if ((a != 'KONG') and (a not in P[i])):
                            P[i].append(a)

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
First = {}
Follow = {}
Predict = []
for i in VN:         #计算所有VN的First集
    First[i] = []
for i in VN:
    if(len(First[i]) == 0):
        R=[]
        Cfirst(VT,i,A,B,First,R)
for i in VN:         #计算所有VN的Follow集
    Follow[i] = []
Follow[S] = '#'
for i in VN:
    if((i == S) or (len(Follow[i]) == 0)):
        R=[]
        Cfollow(VT,i,A,B,First,Follow,R)
for i in A:
    Predict.append([])
Cpredict(VT,A,B,First,Follow,Predict)
for i in VN:
    pp=[]
    for j in range(len(A)):
        if i == A[j]:
            for k in Predict[j]:
                if k in pp:
                    print "WRONG"
                    break
                pp.append(k)