# SNL-compiler
SNL编译原理（词法，语法分析器）

语法分析器判断正误，不生成语法树

如果错误，只会报第一个错误

本程序使用python语言

1.py:词法分析程序，Token序列存在Translated中

2.py:根据所给文法计算其First，Follow，Predict集

3.py:一个完整的LL(1)语法分析程序（报错尚未实现）

4.py:根据所给文法生成LR(1)分析表

5.py:一个完整的LR(1)语法分析程序
