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

def OpenXmlTree(_file, root):
    from xml.dom.minidom import parse
    import xml.dom.minidom
    try:
        DOMTree = xml.dom.minidom.parse(_file)
    except IOError as _except:
        print _except
        return None
    return DOMTree.documentElement

def HaveExtension(_file, extension):
    if IsNameFile(_file):
        index = getIndex(_file, '.')
        __file = _file[:index]
        _extension = _file[index:]
        if extension == _extension:
            return _file
        else:
            return __file + ".xml"
    
def SaveFile(_file, data):
    f = open(_file, 'w')
    f.writelines(data)
    
def FormatXml(dataXml):
    from xml.etree import ElementTree
    from xml.dom import minidom
    
    rough_string = ElementTree.tostring(dataXml, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

def UpdateEndFile(_file, data):
    f = open(_file, 'a')
    f.writelines(data)

def ExistFile(_file):
    import os.path as path
    return path.isfile(_file)

def ExistDir(_dir):
    import os.path as path
    return path.exists(_dir)

def NotEmpytAndNone(text):
    #return NotEmpty(text) and NotNone(text)
    return not IsEmptyAndIsNone(text)

def IsEmptyAndIsNone(text):
    return IsEmpty(text) and IsNone(text)

def NotEmpytOrNone(text):
    #return NotEmpty(text) or NotNone(text)
    return not IsEmptyOrIsNone(text)

def IsEmptyOrIsNone(text):
    return IsEmpty(text) or IsNone(text)
    
def NotEmpty(text):
    #return text is not ''
    return not IsEmpty(text)

def IsEmpty(text):
    return text is ''

def NotEmptyList(_list):
    #return len(_list) != 0
    return not IsEmptyList(_list)

def IsEmptyList(_list):
    return len(_list) == 0

def NotNone(text):
    return not IsNone(text)

def IsNone(text):
    return text is None

def OnlyName(_file):
    if IsNameFile(_file):
        return _file[:_file.index('.')]
    return _file

def getIndex(string, char):
    if char in string:
        return string.index(char)
    return -1

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

def HaveColumns(_list, columns):
    valid = True
    for _listIn in _list:
        if len(_listIn) != columns:
            valid = False
            break
    return valid

def SeparateInList(_list, separator):
    return [element[0].split(separator) for element in _list ]