# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:47:20 2024

@author: Bingchen
"""

def stringCheck(inputStr):
    bracketStack = []
    result = ''

    for i, char in enumerate(inputStr):
        #左括号序号入栈
        if char == '(':
            bracketStack.append(i)
            result += 'x'
         #左括号序号出栈，或标记右括号
        elif char == ')':
            if bracketStack:
                j = bracketStack.pop()
                result = result[:j] + ' ' + result[j+1:] +' '
            else:
                result += '?'
        else:
            result += ' '
    return result

    
if __name__=="__main__":
    input0 = input("请输入字符串：")
    resultStr = stringCheck(input0)
    print(input0)
    print(resultStr)
    