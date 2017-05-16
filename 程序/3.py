# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
L = ''.join([chr(i) for i in range(97, 123)])
L += L.upper()  #字母
D = '0123456789'   #数字
DF0 = '=<+-*/();,[]'   #单分界符
DF1 = []
for i in DF0:
    DF1.append(i)
DF = pd.Series(['EQ','LT','PLUS','MINUS','TIMES','OVER','LPAREN','RPAREN',
        'SEMI','COMMA','LMIDPAREN','RMIDPAREN'],index =DF1)
ALL = L+D+DF+':{}.\''
DF1 = pd.Series(['ASSIGN','UNDERANGE','DOT'],index = [':=','..','.'])
Type = ['ENDFILE','ERROR',
        'PROGRAM','PROCEDURE','TYPE','VAR','IF','THEN','ELSE','FI','WHILE',
        'DO','ENDWH','BEGIN','END','READ','WRITE','ARRAY','OF','RECORD',
        'RETURN',                           #保留字
        'INTEGER','CHAR',                 #类型
        'ID','INTC','CHARC',                #单词类型
        'ASSIGN','EQ','LT','PLUS','MINUS','TIMES','OVER','LPAREN','RPAREN',
        'DOT','COLON','SEMI','COMMA','LMIDPAREN','RMIDPAREN','UNDERANGE']
Reserved = Type [2:23]
reserved=[]
for i in Reserved:
    reserved.append(i.lower())
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
def GetWord(line,i,state):  #返回(word，word_type,i)
    while (i < len(line)):
        if state =='s0':
            if line[i] in L :        state = 's1' #第一个是字母/标识符
            elif line[i] in D :      state = 's2' #第一个是数字/常熟
            elif line[i] in DF0 :     return line[i],DF[line[i]],i+1#单分界符
            elif line[i] == ':' :    state = 's4' #(:=)双分界符
            elif line[i] == '{' :    state = 's6' #注释
            elif line[i] == '.' :    state = 's7' #结束或数组下标
            elif line[i] == '\'':    state = 's8'
            elif line[i] in ' \r\t\n': pass 
            else :   return 'error','ERROR',i+1
            i += 1
        if state == 's1' :                      #标识符或保留字
            b = i - 1
            while (i < len(line))and((line[i] in L) or (line[i] in D)):
                i += 1
            word_type = 'ID'          #'ID'表示标识符
            word = line[b:i]
            if word in reserved:     # 说明是保留字，由各自大写字母表示
                return word,word.upper(),i
            return word,word_type,i
        elif state == 's2' :                      #数字
            b = i - 1
            while (i < len(line))and(line[i] in D):
                i += 1
            word_type = 'INTC'       # INTC表示常数
            return int(line[b:i]),word_type,i
        elif state == 's4':          #':='双分界符
            if (i < len(line)) and line[i] == '=':
                return ':=','ASSIGN',i+1
            else: return 'error','ERROR',i
        elif state == 's6' :                    #注释
            while (i<len(line)) and (line[i] != '}') :
                i+=1
            if i >= len(line) :
                return 0,'COMMENT',-1          #-1表示注释还没完，延续到下一行
            else: 
                i += 1
                state = 's0'
        elif state == 's7':                  
            if (i < len(line)) and line[i] == '.':          #数组下标
                return '..','UNDERANGE',i+1
            else :return '.','DOT',i   #程序结束标志
        elif state == 's8':   #字符
            b = i-1
            while (i<len(line)) and line[i] != '\'':  
                i+=1
            if i >= len(line):
                return line[b:i],'CHARC',-1    #-1同注释
            else :
                return line[b:i+1],'CCHARC',i+1    #返回该字符串
    return 0,0,0
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
            if a in DF:
                a = DF[a]
            elif a in DF1:
                a = DF1[a]
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
#filename = raw_input("Please input the file's name:")
filename = 'scan.txt'
fp = open(filename,'r')
state0 = []
ch = ''
for i in range(13):
    state0.append('s' + str(i))
Translated = []
state ='s0'
k=0
for line in fp.readlines():
    k += 1
    i = 0
    #if line[len(line)-1] == '\n':
        #line = line[:len(line)-1]
    while(i<len(line)):
        word,word_type,i = GetWord(line,i,state)
        if(i==-1):   #注释或字符串还没完
            if(word_type == 'CHARC'):
                state = 's8'
                ch += word
            else :
                state = 's7'
            i = len(line)
        elif(i == 0 ):
            state = 's0'
            i = len(line)
        else :
            if (word_type == 'CHARC'):
                ch += word
                Translated.append([k,word_type,ch])
                ch = ''
            else :
                Translated.append([k,word_type,word])
            state = 's0'
fp.close()
cifa = 1
if state !='s0' :
    print "词法分析错误"
    cifa = 0
    
Input = []
for i in Translated:
    Input.append(i[1])
Input.append('#')
Input.reverse()
if 'ERROR' in Input:
    print "词法分析错误"
    cifa = 0
    
a=len(VN)
b=len(VT)
row = pd.Series(range(a),index = VN)
col = pd.Series(range(b),index = VT)
i = np.zeros(a*b).reshape(a,b)
j = np.ones(a*b).reshape(a,b)
Table = (i-j).astype(int)
for i in range(len(Predict)):
    c = A[i]
    for d in Predict[i]:
        Table[row[c]][col[d]] = i
df = pd.DataFrame(Table,index = VN,columns = VT)
Analysis = []
Analysis.append('#')
Analysis.append('DOT')
Analysis.append(S)
i = 2
j = len(Input) - 1
while (cifa):
    if (i == 0 or j == 0):
        if (i == 0 and j == 0):
            print "成功"
            break
        else :
            print "语法分析错误"
            break
    if (Analysis[i] in VT):
        if (Analysis[i] == Input[j]):
            Analysis.pop()
            Input.pop()
            i -= 1
            j -= 1
        else:
            print "语法分析错误"
            break
    else :
        c = Analysis.pop()
        i -= 1
        d = Input[j]
        if(df[d][c] == -1):
            print "语法分析错误"
            break
        else:
            k = df[d][c]
            B0 = B[k][:]
            B0.reverse()
            for m in B0:
                if m != 'KONG':
                    Analysis.append(m)
                    i += 1
