#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from Tools import *

def getYaml(project, controllers=None):
    Yaml = "application: "+project+"\n"
    Yaml += "version: 1\n"
    Yaml += "runtime: python27\n"
    Yaml += "api_version: 1\n"
    Yaml += "threadsafe: true\n"
    Yaml += "\n"
    Yaml += "handlers:\n"
    if NotNone(controllers):
        Yaml += getYamlControllers(controllers)
    Yaml += "- url: .*\n"
    Yaml += "  script: main.application\n"
    Yaml += "\n"
    Yaml += "libraries:\n"
    Yaml += "- name: webapp2\n"
    Yaml += '  version: "2.5.1"\n'
    Yaml += "- name: jinja2\n"
    Yaml += '  version: latest\n'
    return Yaml

def getYamlControllers(controllers):
    yamlcontrollers = ""
    for controller in controllers:
        yamlcontrollers += getYamlController(controller)
    return yamlcontrollers

def getYamlController(controller):
    yamlcontroller  = "- url: /"+controller+"\n"
    yamlcontroller += "  script: "+controller+".application\n"
    return yamlcontroller


def getMain():
    Main  = getImports()
    Main += getTemplate()
    Main += getClass("main")+"\n"
    Main += getInterClass('main')
    Main += getApplication('main') + '\n'
    return Main
    
def getImports():
    Imports  = "import jinja2\n"
    Imports += "import webapp2\n"
    Imports += "\n"
    return Imports

def getTemplate():
    Template  = "template_env = jinja2.Environment(\n"
    Template += "  loader = jinja2.FileSystemLoader(os.getcwd()))\n"
    Template += "\n"
    return Template

def getInterClass(_class):
    Inter  = "  "+getGet()+"\n"
    Inter += "    template = template_env.get_template('"+_class+".html')\n"
    Inter += "    self.response.out.write(template.render())\n"
    Inter += "\n"
    return Inter

def getApplication(_class):
    App  = "application = webapp2.WSGIApplication(["
    App += "('"+getPathFile(_class)+"', "+getNameClass(_class)+")"
    App += "],\n"
    App += "  debug=True)\n"
    return App
    
    
def getClass(name):
    return "class "+getNameClass(name)+"(webapp2.RequestHandler):"

def getNameClass(name):
    name = name[0].upper() + name[1:]
    return name+"Page"

def getPathFile(filename):
    main = ["main", "Main"]
    return ('/'+filename, '/')[filename in main]

def getGet():
    return "def get(self): "

def getPost():
    return "def post(self): "
  
def getController(filename):
    Controller  = getImports()
    Controller += getTemplate()
    Controller += getClass(filename)+"\n"
    Controller += getInterClass(filename)
    Controller += getApplication(filename)
    return Controller

def getView():
    View  = "<html>\n"
    View += "  <head>\n"
    View += "    <meta charset='utf-8'>\n"
    View += "    <meta http-equiv='Expires' content='0'>\n"
    View += "    <title>Create with Framework Webapp2</title>\n"
    View += "  </head>\n"
    View += "  <body>\n"
    View += "    <form action='/controller' method='post'>\n"
    View += "    </form>\n"
    View += "  </body>\n"
    View += "</html>\n"
    return View

'''
        Tool Framework webapp2 
        Version:    1.0
        Autor:      Jarov
        Fecha:      13-05-2015

Esta herrmaienta pretende ofrecer una forma flexible
y rapida de generar plantillas para webapp2, utilizando MVC
Model, View, Control
'''

parser = argparse.ArgumentParser(description="Tool Framework webapp2 v1.0")
parser.add_argument('-n', '--name', help="Name of project webapp2", required=True)
parser.add_argument('-i', '--input', help="Input filename to create VC")
parser.add_argument('-p', '--path', help="Path of output files MVC without project name")
parser.add_argument('-v', '--view', help="Filename to create view")
parser.add_argument('-c', '--controller', help="Filename to create controller")
args = parser.parse_args()

name        = ''
_file       = ''
_input      = ''
_view       = ''
_controller = ''

#Genera el path de donde se esta ejecutando este script
path = os.path.abspath(__file__)
path = os.path.dirname(path) + '/'

model       = ''
fine        = False

#Obtiene el path de los args
if args.path:
    path = args.path

#Obtiene el nombre del proyecto
if args.name:
    name = args.name

if args.input:
    _input = args.input
    _input = OnlyName(_input)
    fine = True
#Obtiene el nombre para V
if args.view:
    _view = args.view
    _view = OnlyName(_view)
    fine = True
#Obtiene el nombre para C
if args.controller:
    _controller = args.controller
    _controller = OnlyName(_controller)
    fine = True
    
if fine:
    controllers = None
    project = path + name
    print "path: "+ project
    if not ExistDir(project):
        os.mkdir(project)
        print "The project "+name+" has been created"
    else:
        print "Updating the project "+name+"..."
    project += "/"
    
    main = project + "main.py"
    if not ExistFile(main):
        dataMain = getMain()
        SaveFile(main, dataMain)
        print "The file main.py has been created"
    
    if NotEmpty(_input):
        files = project + _input
        controller = files +".py"
        if not ExistFile(controller):
            dataController = getController(_input)
            SaveFile(controller, dataController)
            print "The file "+_input+".py has been created"
        controllers = [_input]
        view = files + ".html"
        if not ExistFile(view):
            dataView = getView()
            SaveFile(view, dataView)
            print "The file "+_input+".html has been created"
    
    if NotEmpty(_view):
        view = project + _view+'.html'
        if not ExistFile(view):
            dataView = getView()
            SaveFile(view, dataView)
            print "The file "+_view+".html has been created"

    newController = False
    if NotEmpty(_controller):
        controller = project + _controller + '.py'
        if not ExistFile(controller):
            dataController = getController(_controller)
            SaveFile(controller, dataController)
            newcontroller = True
            print "The file "+_controller+".py has been created"
    
    yaml = project + "app.yaml"
    if not ExistFile(yaml):
        dataYaml = getYaml(name, controllers)
        SaveFile(yaml, dataYaml)
        print "The file app.yaml has been created"
    else:
        if NotEmpty(_controller):
            if newController:
                dataYaml = OpenFileInList(yaml)
                index = WhereDataList(dataYaml, '- url: .*')
                dataYaml = UpdateDataList(dataYaml, getYamlController(_controller)[:-1], index)
                dataYaml = ListToString(dataYaml)
                SaveFile(yaml, dataYaml)
                print "The file app.yaml has been updated"
            else:
                print "The controller "+_controller+" has already been created"
            
else:
    print "Argument [-i], [-v] or [-c] is required"