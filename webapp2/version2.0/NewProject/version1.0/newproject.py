#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from Tools import *
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

parser = argparse.ArgumentParser(description="Tool create new project from xml file v1.0")
parser.add_argument('-n', '--name', help="Project Struct's filename", required=True)
parser.add_argument('-p', '--path', help="Project's path")
args = parser.parse_args()

_name   = ''
_path   = ''

#Genera el path de donde se esta ejecutando este script
_path = os.path.abspath(__file__)
_path = os.path.dirname(_path) + '/'


#Obtiene el path de los args
if args.path:
    _path = args.path

#Obtiene el nombre del archivo
if args.name:
    _name = args.name
    
#obtiene la ruta absoulta del archivo
project     = _path + _name
#Lee del archivo name
textLines   = OpenFileInList(project, sep=': ')
#Filtra comentarios que empiecen con #
textLines   = [text for text in textLines if not text[0].startswith('#')]
#Elimina los saltos de linea '\n' de los valores
textLines   = [[text[0],text[1].rstrip('\n')] for text in textLines]

projectName = ''
pathProject = ''
inputs      = []
views       = []
controllers = []

#Valida si existe el formato llave-valor
if Columns(textLines, 2):
    #Recorre la lista de lineas validas que se pasaron
    for textLine in textLines:
        #Lee el nombre del proyecto a crear
        if textLine[0] == 'project' and not NotEmpty(projectName):
            projectName = textLine[1]
            projectName = OnlyName(projectName)
        #Lee el path del proyecto a crear
        if textLine[0] == 'path' and not NotEmpty(pathProject):
            pathProject = textLine[1]
            if not pathProject.endswith('/'):
                pathProject += '/'
        #Lee los inputs
        if textLine[0] == 'input':
            inputs.append(textLine[1])
        #Lee los views
        if textLine[0] == 'view':
            views.append(textLine[1])
        #Lee los controller
        if textLine[0] == 'controller':
            controllers.append(textLine[1])
    #se cre el arbol xml
    xmlProject = Element('project', name=projectName)
    #Se agregan los nodos
    #inputs
    if NotEmptyList(inputs):
        for _input in inputs:
            inputChild = SubElement(xmlProject, 'input')
            inputChild.text = _input
    #views
    if NotEmptyList(views):
        for _view in views:
            viewChild = SubElement(xmlProject, 'view')
            viewChild.text = _view
    #controllers
    if NotEmptyList(controllers):
        for _controller in controllers:
            controllerChild = SubElement(xmlProject, 'controller')
            controllerChild.text = _controller
    #Se genera el archivo de salida
    if NotNone(xmlProject):
        if not NotEmpty(pathProject):
            pathProject = _path
        output = pathProject + projectName +".xml"
        if (ExistFile(output)):
            print "The file "+projectName+".xml already has been created"
        else:
            SaveFile(output, FormatXml(xmlProject))
            print "Path: "+pathProject
            print "The file: "+projectName+".xml has been created"
else:
    print "The format is incorrect"
