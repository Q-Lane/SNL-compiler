# -*- coding: utf-8 -*-
import pandas as pd
L = ''.join([chr(i) for i in range(97, 123)])
L += L.upper()  #字母
D = '0123456789'   #数字
DF0 = '=<+-*/();,[]'   #单分界符
ed = DF0 + '. \r\n\t:'
DF1 = []
for i in DF0:
    DF1.append(i)
DF = pd.Series(['EQ', 'LT', 'PLUS', 'MINUS', 'TIMES', 'OVER', 'LPAREN', 'RPAREN',
                'SEMI', 'COMMA', 'LMIDPAREN', 'RMIDPAREN'], index=DF1)
DF1 = pd.Series(['ASSIGN', 'UNDERANGE', 'DOT'], index=[':=', '..', '.'])
Type = ['ENDFILE', 'ERROR',  #
        'PROGRAM', 'PROCEDURE', 'TYPE', 'VAR', 'IF', 'THEN', 'ELSE', 'FI', 'WHILE',
        'DO', 'ENDWH', 'BEGIN', 'END', 'READ', 'WRITE', 'ARRAY', 'OF', 'RECORD',
        'RETURN',                           #保留字
        'INTEGER', 'CHAR',                 #类型
        'ID', 'INTC', 'CHARC',                #单词类型
        'ASSIGN', 'EQ', 'LT', 'PLUS', 'MINUS', 'TIMES','OVER', 'LPAREN', 'RPAREN',  
        'DOT', 'COLON', 'SEMI', 'COMMA', 'LMIDPAREN', 'RMIDPAREN', 'UNDERANGE']
Reserved = Type[2:23] #保留字
reserved = []
for i in Reserved:
    reserved.append(i.lower())
def GetWord(line, i, state):  #返回(word，word_type,i)
    while i < len(line):
        if state =='s0':
            if line[i] in L:        state = 's1' #第一个是字母/标识符
            elif line[i] in D:      state = 's2' #第一个是数字/常熟
            elif line[i] in DF0:     return line[i], DF[line[i]], i+1#单分界符
            elif line[i] == ':':    state = 's4' #(:=)双分界符
            elif line[i] == '{':    state = 's6' #注释
            elif line[i] == '.':    state = 's8' #结束或数组下标
            elif line[i] == '\'':    state = 's10'
            elif line[i] in ' \t\n': pass 
            else:   
                b = i
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
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
            if line[i] not in ed:
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
            else:
                word_type = 'INTC'       # INTC表示常数
                return int(line[b:i]),word_type,i
        elif state == 's4':          #':='双分界符
            if (i < len(line)) and line[i] == '=':
                return ':=','ASSIGN',i+1
            else: 
                b = i
                while(line[i] not in ed): i+=1
                return line[b:i], 'ERROR', i
        elif state == 's6' :                    #注释
            while (i<len(line)) and (line[i] != '}') :
                i+=1
            if i >= len(line) :
                return 0,'COMMENT',-1          #-1表示注释还没完，延续到下一行
            else: 
                i += 1
                state = 's0'
        elif state == 's8':                  
            if (i < len(line)) and line[i] == '.':          #数组下标
                return '..','UNDERANGE',i+1
            else :return '.','DOT',i   #程序结束标志
        elif state == 's10':   #字符
            b = i-1
            while (i<len(line)) and line[i] != '\'':  
                i+=1
            if i >= len(line):
                return line[b:i],'CHARC',-1    #-1同注释
            else :
                return line[b:i+1],'CCHARC',i+1    #返回该字符串
    return 0,0,0
def getword(line,i): #从文法文本中获取一个字符串
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
            wait = [[j0,i0[1]]]
            IS0.append([j0,i0[1]])
            i1 = i0[1]
            #衍生
            while (a != len(j0) - 1):#'*'非末尾
                #可以先计算其展望符集
                u=[]
                wait.remove(wait[0])
                d = 1
                if (j0[a + 1] in VT):
                    d = 0
                # *后面是VN
                elif (a != len(j0) - 2): #‘*’非倒数第二个字符
                    if(j0[a + 2] in VT):#后面是VT，u就那VT了
                        u = [j0[a + 2]]
                    else: 
                        k = a + 2
                        # k不是末尾，k在VN里，空在k的first集里
                        while(k<len(j0) and (j0[k] in VN) and ('KONG' in First[j0[k]])):
                            for j in First[j0[k]]:
                                if(j != 'KONG') and (j not in u):
                                    u.append(j)
                            k += 1
                        if(k == len(j0)): #到末尾了还要继承之前的
                            for j in i1:
                                if j not in u:
                                    u.append(j)
                        elif j0[k] not in VN:#到VT了，直接把k放进去
                            if j0[k] not in u:
                                u.append(j0[k])
                        else: #first集里没空了，把该first集放入
                            for j in First[j0[k]]:
                                if j not in u:
                                    u.append(j)
                else : #'*'是倒数第二个字符，直接继承
                    u = i1
                if(d):
                    for i in range(len(A)):
                        if j0[a+1] == A[i]:
                            IS0.append([P0[i],u])
                            wait.append([P0[i],u])
                if len(wait) == 0:
                    break
                j0 = wait[0][0]
                i1 = wait[0][1]
                a = j0.index('*')
    return IS0
filename = 'wenfa.txt'  #文法所在文件
fp = open(filename,'r')  
VN=[]    #存非终极符
VT=[]   #存终极符
P=[]    #存全部文法，P[0]表示文法左部
for line in fp.readlines(): #从文法文件中读取到 P 中
    p=[]
    i=0
    while(i<len(line)):
        a,i = getword(line,i) #返回获取的一个字符和下一个读取位置
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
S = P[0][0]   #初始符
A=[]    #AB将P分为左右两部分
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
df0 = pd.DataFrame(t,columns = a)
df = pd.DataFrame(t,columns = a)
ix = 0  #dangqian
im = 0 #zuida
while(ix <= im):
    ISk = IS[ix]
    Temp=[]#暂存下一个方块数据
    for i0 in ISk:
        a0 = i0[0].index('*')
        if(a0 == len(i0[0]) - 1): #‘*’在末尾，可规约
            j0 = i0[0][:]
            j0.remove('*')  #找到该文法在P中的位置
            k0 = P.index(j0)
            for c in i0[1]: 
                if k0 == 0 and c == '#':   #成功
                    df[c][ix] = 'V'
                else:#规约
                    df[c][ix] = 'R' + str(k0)
        else:
            m = i0[0][a0+1] #m存放输入的字符
            if m == 'KONG':#空可规约
                k0 = P0.index(i0[0])
                for c in i0[1]:
                    df[c][ix] = 'R' + str(k0)
                continue
            IS0 = Next(i0,First,VN,A,P0) #i0根据m得到的方块
            k=1
            for i in range(len(Temp)): #在Temp中有同样通过m得到的方块则合并
                if m == Temp[i][0]:
                    k = 0
                    for j in IS0:
                        if j not in Temp[i][1]:
                            Temp[i][1].append(j)
                    break
            if(k):#若无m则加上去
                Temp.append([m,IS0])
    for i in range(len(Temp)):
        k = 1
        if(Temp[i][1] in IS):
            j = IS.index(Temp[i][1])
            df[Temp[i][0]][ix] = 'S' +str(j)
        else:
            IS.append(Temp[i][1])
            im += 1
            df = df.append(df0, ignore_index=True)
            df[Temp[i][0]][ix] = 'S' + str(im)
    ix = ix + 1   

filename = 'c1.txt'   #你要测试的snl程序代码文件
fp = open(filename,'r')
ch = ''
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
                state = 's10'
                ch += word
            else :
                state = 's8'
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

state =[0]   #状态栈
ch = []     #符号栈
Input = []  #输入栈
for i in Translated:
    Input.append(i[1])
i = Input.pop()
if i != 'DOT':
    Input.append(i)
Input.append('#')
if 'ERROR' in Input:
    print "词法分析错误"
    k = Input.index('ERROR')
    print '第',Translated[k][0],'行：\'',Translated[k][2],'\'出错'
    cifa = 0
i = 0 #状态栈指针
j = -1 #符号栈指针
k = 0 #输入栈指针
while(cifa):
    t = df[Input[k]][state[i]]
    if(t[0] == 'S'):
        g = int(t[1:])
        state.append(g)  #状态栈 +1
        i += 1
        ch.append(Input[k]) #符号栈 +1
        j += 1
        k += 1 #输入栈 +1
    elif(t[0] == 'R'): #规约
        g = int(t[1:])
        if('KONG' not in P[g]):     
            l = len(P[g]) - 1
            i0 = 0
            while(i0 < l):
                i0 += 1
                state.pop()  #状态栈出栈
                i -= 1
                ch.pop()    #符号栈出栈
                j -= 1
        ch.append(P[g][0]) #符号栈进一个
        j += 1
        t0 = df[ch[j]][state[i]]
        g0 = int(t0[1:])
        state.append(g0)
        i += 1
    elif(t == 'V'):
        print '成功'
        break
    else:
        print '语法分析错误'
        print '第',Translated[k][0],'行：\'',Translated[k][2],'\'错误'
        break
