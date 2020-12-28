# 2020System

```diff
- 欲執行PLY請輸入：python mylex.py 
```

# 語法：
* 冪次運算： base  ^  n
```diff
calc > 2^3 
8
```
* 根號運算： num  **  n
```diff
calc > 4**2 
2.0
```
* for-loop： for 起始值 to 結束 ("欲執行的指令運算")
```diff
calc > i=0
calc > for 1 to 3 (i=i+2)
calc > i
6
``` 
* if-else： if ("條件判斷") "expression" else "expression" 
```diff
calc > i=0
calc > if (i<0) i=1 else i=2
calc > i
2
``` 
* 若輸入四則運算，則會依序列出：(1)lex輸出 (2)執行結果 (3)Three-Address Code
```diff
calc > 2*3-6/2^2
LexToken(NUMBER,2,1,0)
LexToken(TIMES,'*',1,1)
LexToken(NUMBER,3,1,2)
LexToken(MINUS,'-',1,3)
LexToken(NUMBER,6,1,4)
LexToken(DIVIDE,'/',1,5)
LexToken(NUMBER,2,1,6)
LexToken(POWER,'^',1,7)
LexToken(NUMBER,2,1,8)
4.5
[['op', 'arg1', 'arg2', 'result'], ['^', '2', '2', 't1'], ['/', '6', 't1', 't2'], ['*', '2', '3', 't3'], ['-', 't3', 't2', 't4'], ['=', 't4', ' ', 'a']]
``` 
* 最後資料夾內會產生一份.png檔，為依據上述所建立的一棵 (4)Parsing Tree  
  (若Node中出現相同Label則以"L_"及"R_"加以辨別)
![image](https://github.com/huikaiwang/SP_2020/blob/main/img/nx_test.png)
