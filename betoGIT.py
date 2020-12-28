import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
import sys
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


reserved = {          #關鍵字的tokens
    'if' : 'IF',
    'then' :'THEN',
    'else' : 'ELSE',
    'for' : 'FOR',
    'ran' : 'RAN',
    'sig' :'SIG',
    'add' : 'ADD',
    'sub':'SUB',
    'div':'DIV',
    'mul':'MUL',
    'psd' : 'PSD',
}
tokens = [
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'EQUALS','POWER','ROOT',
    'LPAREN', 'RPAREN',
    'EQUAL', 'NOTEQ', 'LARGE', 'SMALL', 'LRGEQ', 'SMLEQ',
] + list(reserved.values())
t_PLUS    = r'\+' #符號的tokens
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MODULO  = r'%'
t_EQUALS  = r'='
t_POWER  = r'\^'
t_ROOT   = r'\$'
t_EQUAL   = r'\=\='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NOTEQ   = r'\!\='
t_LARGE   = r'\>'
t_SMALL   = r'\<'
t_LRGEQ   = r'\>\='
t_SMLEQ   = r'\<\='


#自定義變數
def t_NAME(t):

    r'[a-zA-Z_][a-zA-Z_0-9]*'

    t.type = reserved.get(t.value,'NAME')    

    return t

#數字
def t_NUMBER(t):
    r'\d+'  
    t.value = int(t.value)  
    return t

#無視空白

t_ignore = " \t"  

#換行
def t_newline(t):
    r'\n+'  
    t.lexer.lineno += t.value.count("\n")  


# error 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])  
    t.lexer.skip(1)  


#左、右運算
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),
)


#空字串
names = {}

#for迴圈
def p_statement_for(p):
    '''statement    : FOR NAME RAN NUMBER NUMBER ADD
                    | FOR NAME RAN NUMBER NUMBER SUB'''
                    # for 變數 範圍的 起始  結束 遞增或遞減
    sum=0
    for i in range(p[4],p[5]+1):
       if p[6]=='add':
          sum +=i 
       elif p[6]=='sub':
           sum-=i
    print(p[2]," = ",sum)
    names[p[2]] = sum

#if 變數比較 
def p_statement_if(p):
    '''statement    : IF NAME NUMBER EQUAL NUMBER THEN NUMBER ELSE NUMBER
                    | IF NAME NUMBER NOTEQ NUMBER THEN NUMBER ELSE NUMBER
                    | IF NAME NUMBER LARGE NUMBER THEN NUMBER ELSE NUMBER
                    | IF NAME NUMBER SMALL NUMBER THEN NUMBER ELSE NUMBER
                    | IF NAME NUMBER LRGEQ NUMBER THEN NUMBER ELSE NUMBER
                    | IF NAME NUMBER SMLEQ NUMBER THEN NUMBER ELSE NUMBER'''
                    # if   X  4      ==    4       Y     5     N      3
    if p[4] == '==':
        p[3] = p[3] == p[5]
    elif p[4] == '!=':
        p[3] = p[3] != p[5]
    elif p[2] == '>':
        p[0] = p[3] > p[5]
    elif p[2] == '>=':
        p[0] = p[3] >= p[5]
    elif p[2] == '<':
        p[0] = p[3] < p[5]
    elif p[2] == '<=':
        p[0] = p[3] <= p[5]

    if p[3]==True:
        names[p[3]] = p[6]
        print(" True X= ",p[6])
    else:
        names[p[3]]=p[9]
        print(" False X= ",p[9])
    

#sigma計算機
def p_statement_sig(p):
    '''statement      : SIG NAME ADD NUMBER NUMBER NUMBER NUMBER
                      | SIG NAME SUB NUMBER NUMBER NUMBER NUMBER
                      | SIG NAME MUL NUMBER NUMBER NUMBER NUMBER
                      | SIG NAME DIV NUMBER NUMBER NUMBER NUMBER''' 
                     # sig 變數  運算子 數字 起始值 結束值  冪方
                      #mul 乘法 div除法
    sum=0
    num=int(p[4])
    power=int(p[7])
    for i in range(p[5],p[6]+1):
        if p[3]=='add':
            sum+=(i+num) ** power
        elif p[3]=='sub':
            sum+=(i-num) ** power
        elif p[3]=='mul':
            sum+=(i*num) ** power
        elif p[3]=='div':
            sum+=(i/num) ** power
    names[p[2]]=sum
    print("Ars = ",sum)
#標準差計算機(process standard deviation
def p_statement_psd(p):
    '''statement      : PSD NAME NUMBER NUMBER NUMBER 
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER
                      | PSD NAME NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER NUMBER 
    '''
                    #  psd 變數 幾筆資料 資料.....資料 範圍是2~11筆
    avg=0
    sd=0
    for i in range(4,4+p[3]):
        avg+=p[i]/p[3]
    for i in range(4,4+p[3]):
        sd+=(((p[i]-avg)**2)*(1/p[3]))
    sd=sd**0.5
    names[p[2]]=sd
    print("這",p[3],"筆資料的標準差為 ： ",sd)
    
#將輸入放入字串中
def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]  


#顯示expression的值
def p_statement_expr(p):
    'statement : expression'
    print(p[1])
    

def p_statement_comp(p):
    'statement : comparison'
    print(p[1])


#比較符號
def p_comparison_binop(p):
    '''comparison : expression EQUAL expression
                          | expression NOTEQ expression
                          | expression LARGE expression
                          | expression SMALL expression
                          | expression LRGEQ expression
                          | expression SMLEQ expression'''
    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]

#定義運算子
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression MODULO expression
                  | expression ROOT expression   '''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]
    elif p[2] == '$':
        p[0] = p[1] ** (1/p[3])
    

#數值
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

#偵測語法錯誤
def p_error(p):
    print("Syntax error at '%s'" % p.value)


#變數名稱
def p_expression_name(p):
    'expression : NAME'
    # attempt to lookup variable in current dictionary, throw error if not found
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


#負數處理
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

#抓括號內的
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


# build parser
yacc.yacc()

while True:
    try:
        s = input('input : ')
        lexer = lex.lex()
        lexer.input(s)
        while True:
            tok = lexer.token()
            if not tok:
                break
             
        if s=='exit':
            break
            sys.exit()
        ip_lst = list(map(str,s))    
    except EOFError:
        break
    yacc.parse(s)  
    
    
    
    #Three-Address Code 
    prio_dict = {'-':1,'+':2,'*':3,'/':4,'$':5,'^':6} #優先順序
    op_lst = []
    op_lst.append(['op','arg1','arg2','result'])
    def find_top_prio(lst):
        top_prio = 1
        count_ops = 0
        for ops in lst:
            if ops in prio_dict:
                count_ops += 1
                if prio_dict[ops] > 1:
                    top_prio = prio_dict[ops]
        return top_prio, count_ops
    top_prio, count_ops = find_top_prio(ip_lst)
    ip = ip_lst
    i=0
    res=0
    while i in range(len(ip)):
        if ip[i] in prio_dict:
            op=ip[i]
            if(prio_dict[op]==1)and(prio_dict[op+1]==2):
                res+=1
                op_lst.append([ip[-1],ip[i],' ','t'+str(res)])
                ip[i]='t'+str(res)
                ip.pop(i)
                ip.pop(i+1)
                i=0
                top_prio,count_ops=find_top_prio(ip)
                
                
            elif(prio_dict[op]==5):
                res+=1
                op_lst.append([ip[-1],ip[i],' ','t'+str(res)])
                ip[i]='t'+str(res)
                ip.pop(i-1)
                ip.pop(i)
                i=0
                top_prio,count_ops=find_top_prio(ip)
                
                
            elif(prio_dict[op]>=top_prio)and (ip[i+1] in prio_dict):
                res +=1
                op_lst.append([ip[i+1],ip[i+2],' ','t'+str(res)])
                ip[i+1]='t'+str(res)
                ip.pop(i+2)
                i=0
                top_prio,count_ops=find_top_prio(ip)
                
                
            elif prio_dict[op]>=top_prio:
                    
                res +=1
                op_lst.append([op,ip[i-1],ip[i+1],'t'+str(res)])
                ip[i]='t'+str(res)
                    
                ip.pop(i-1)
                ip.pop(i)
                i=0
                top_prio,count_ops=find_top_prio(ip)
                
            
                    
        if len(ip) ==1:
            op_lst.append(['=',ip[i],' ','a'])
            print("{}".format(op_lst),sep=".")
                
        #parsing tree
            G = nx.DiGraph() 
            G.clear()
            data = op_lst
            for i in range(1,len(data)-1):
                if(data[i][1]==data[i][2]):
                    data[i][1] = "L_" + data[i][1]
                    data[i][2] = "R_" + data[i][2]

                G.add_node("%s" %(data[i][1]))
                G.add_node("%s" %(data[i][2]))
                G.add_node("%s" %(data[i][3]))
                G.add_edge("%s" %(data[i][3]), "%s" %(data[i][1]))
                G.add_edge("%s" %(data[i][3]), "%s" %(data[i][2]))

            nx.nx_agraph.write_dot(G,'test.dot')
            plt.title('draw_networkx')
            pos = graphviz_layout(G, prog='dot')
            nx.draw(G, pos, with_labels=True, arrows=False, node_size=500)

            plt.savefig('nx_test.png')
            plt.clf()
        i=i+1
        
