#!/usr/bin/python env
#coding:utf-8

import re

def multiplication(array_str,array_eq):
    '''
    处理带有乘法的等式
    :param array_str: ['-']
    :param array_eq: ['-40 ',' / 5', '5*3']
    :return: 返回处理后的结果['-40/5', '5*3']
    '''
    for index,v in enumerate(array_eq):
        v = v.strip()
        if v.endswith('*') or v.endswith('/'):
            array_eq[index] = array_eq[index] + array_str[index] + array_eq[index+1]    #拼接 2*3
            del array_eq[index+1]
            del array_str[index]
        return array_str,array_eq

def calculate_multiplication(option):
    '''
    计算乘法
    :param option:传入 5*3
    :return: 返回计算的结果
    '''
    opt_str = re.findall('[*/]',option)
    opt_calc = re.split('[*/]',option)
    res = None
    for k,v in enumerate(opt_calc):
        try:
            if res:
                if opt_str[k-1] == '*':
                    res *= float(v)
                elif opt_str[k-1] == '/':
                    res /= float(v)
            else:
                res = float(v)
        except ValueError:
            pass
    return res

def  calculate_addition(symbol,equation):
    '''
    计算加减法
    :param option: 传入5+3
    :return: 返回计算的结果
    '''
    res = None
    tag = False
    for k,v in enumerate(equation):
        try:
            if tag:
                if symbol[k-1] == '+':
                    res += float(v)
                elif symbol[k-1] == '-':
                    res -= float(v)
            else:
                res = float(v)
                tag = True  #即使第一个数字为0,也要继续执行
        except ValueError:
            pass
    return res

def core(array):
    '''
    2、分析括号中的等式
    :param array: 传入带括号的等式 (-40/5)
    :return:    返回计算的结果
    '''
    array = array.strip('()')
    symbol = re.findall('[+-]',array)
    equation = re.split('[+-]',array)

    if equation[0] == '':   #此时括号中的第一个数字肯定为负
        equation[1] = symbol[0] + equation[1]
        del symbol[0]
        del equation[0]
    symbol,equation = multiplication(symbol,equation)
    for k,v in enumerate(equation):
        if re.search('[*/]',v): #如果此时还有乘法
            sub_res = calculate_multiplication(v)   #调用计算乘法
            equation[k] = sub_res
    #计算加法和减法
    res = calculate_addition(symbol,equation)
    return res

def serch_brackets(array):
    '''
    1、函数用于解析括号,如果没有括号直接调用计算函数.如果有括号循环执行解析
    :param array: 传入等式序列
    :return:    返回最终的计算结果
    '''
    count = True
    while count:
        res_parser = re.search(r'\([^()]+\)',array)    #拿到第一次解析等式的最内层的括号
        if res_parser:  #查到了括号
            parser_res = core(res_parser.group())   #res.group是将搜索到的括号传入给core函数进行处理
            array = array.replace(res_parser.group(),str(parser_res))
            print(array)
        else:
            #如果没有找到,证明等式里面没有括号,直接进行计算即可
            print('\n\n\033[41;1m最终结果:%s\033[2m' %(core(array)))
            break

if __name__ == '__main__':
    while True:
        choise = input('>>: ').strip()
        if not choise:
            continue
        serch_brackets(choise)
