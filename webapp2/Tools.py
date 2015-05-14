#!/usr/bin/python
# -*- coding: utf-8 -*-

def OpenFileInList(_file, sep='\n'):
    return [(l).split(sep) for l in (open(_file).readlines())]

def OpenRead(_file):
    return open(_file, "rb")

def OpenWrite(_file):
    return open(_file, "wb")

def OpenFile(_file):
    return OpenRead(_file)

def SaveFile(_file, data):
    f = open(_file, 'wb')
    f.writelines(data)

def Save():
    pass

def ExistFile(_file):
    import os.path as path
    return path.isfile(_file)

def ExistDir(_dir):
    import os.path as path
    return path.exists(_dir)

def NotEmpytAndNone(text):
    return NotEmpty(text) and NotNone(text)

def NotEmpytOrNone(text):
    return NotEmpty(text) or NotNone(text)
    
def NotEmpty(text):
    return text is not ''

def NotNone(text):
    return text is not None

def OnlyName(_file):
    if IsNameFile(_file):
        return _file[:_file.index('.')]
    return _file

def IsNameFile(_file):
    if '.' in _file:
        return True
    return False

def WhereDataList(data, string):
    idnex = 0
    for index, data1 in enumerate(data):
        if string == data1[0]:
            break
    return index

def UpdateDataList(data, newdata, index):
    data.insert(index, [newdata])
    return data

def ListToString(_list):
    string = ''
    for listIn in _list:
        string += str(listIn[0]) + '\n'
    return string