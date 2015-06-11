#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from Tools import *
from xml.dom.minidom import parse
import xml.dom.minidom


def getYaml(project, controller):
    Yaml = "application: "+project+"\n"
    Yaml += "version: 1\n"
    Yaml += "runtime: python27\n"
    Yaml += "api_version: 1\n"
    Yaml += "threadsafe: true\n"
    Yaml += "\n"
    Yaml += "handlers:\n"
    if NotNone(controller):
        Yaml += getYamlController(controller)
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
    View += "      Hola Mundo Webapp2\n"
    View += "    </form>\n"
    View += "  </body>\n"
    View += "</html>\n"
    return View

def getModels():
    return "from google.appengine.ext import db\n\n"

def CreateProject(path, name, imprime=True):
    pathProject = path + name
    if not ExistDir(pathProject):
        os.mkdir(pathProject)
        print "The project "+name+" has been created"
    else:
        if imprime:
            print "Updating the project "+name+"..."
    pathProject += "/"
    return pathProject

def CreateMain(project):
    main = project + "main.py"
    if not ExistFile(main):
        dataMain = getMain()
        SaveFile(main, dataMain)
        print "The file main.py has been created"

def CreateModelsFile(project):
    models = project + "models.py"
    if not ExistFile(models):
        dataModels = getModels()
        SaveFile(models, dataModels)
        print "The file models.py has been created"

def CreateView(project, _view):
    view = project + _view+'.html'
    if not ExistFile(view):
        dataView = getView()
        SaveFile(view, dataView)
        print "The file "+_view+".html has been created"
        return True
    return False

def CreateController(project, _controller):
    controller = project + _controller + '.py'
    if not ExistFile(controller):
        dataController = getController(_controller)
        SaveFile(controller, dataController)
        print "The file "+_controller+".py has been created"
        return True
    return False

def CreateNewYaml(yaml, name, controller):
    dataYaml = getYaml(name, controller)
    SaveFile(yaml, dataYaml)
    print "The file app.yaml has been created"
    
def UpdateYaml(yaml, _controller):
    dataYaml = OpenFileInList(yaml)
    index = WhereDataList(dataYaml, '- url: .*')
    dataYaml = UpdateDataList(dataYaml, getYamlController(_controller)[:-1], index)
    dataYaml = ListToString(dataYaml)
    SaveFile(yaml, dataYaml)
    #print "The file app.yaml has been updated"
    
def UpdateModels(models, entity):
    codeEntity = ''
    if entity.hasAttribute('name'):
        codeEntity = ToClassModel(entity.getAttribute('name'))
    attributes = entity.getElementsByTagName('atribute')
    for attribute in attributes:
        typeData = ''
        if attribute.hasAttribute('type'):
            typeData = attribute.getAttribute('type')
        else:
            typeData = 'string'
        nameAttribute = attribute.childNodes[0].data
        codeEntity += CodeAttribute(nameAttribute, typeData)
    codeEntity += '\n'
    UpdateEndFile(models, codeEntity)
    
def ToClassModel(name):
    return 'class ' + name + '(db.Model):\n'

def CodeAttribute(nameAttribute, typeData):
    if typeData == 'string':
        typeData = 'db.StringProperty()'
    elif typeData == 'int':
        typeData = 'db.IntegerProperty()'
    return '  '+nameAttribute + ' = ' + typeData + "\n"
    
def OpenXmlProject(path, _file, projectTree, imprime=True):
    if projectTree.hasAttribute('name'):
        name = projectTree.getAttribute('name')
        newpath = projectTree.getElementsByTagName('path')
        if NotEmptyList(newpath):
            path = newpath[0].childNodes[0].data
        inputs = projectTree.getElementsByTagName('input')
        views = projectTree.getElementsByTagName('view')
        controllers = projectTree.getElementsByTagName('controller')
        CreateProjectCompleteFromFile(path, name, inputs, views, controllers, imprime)
    else:
        print "Error parsing "+_file
        
def OpenXmlModel(path, _model, modelTree, imprime=True):
    if modelTree.hasAttribute('name'):
        name = modelTree.getAttribute('name')
        newpath = modelTree.getElementsByTagName('path')
        if NotEmptyList(newpath):
            path = newpath[0].childNodes[0].data
        entitys = modelTree.getElementsByTagName('entity')
        CreateModelCompleteFromFile(path, name, entitys, imprime)
    else:
        print "Error parsing "+_model
        
def CreateModelCompleteFromFile(path, name, entitys = None, imprime=True):
    if NotNone(entitys):
        project = CreateProject(path, name, imprime)
        
        CreateModelsFile(project)
        
        for entity in entitys:
            UpdateModels(project+'models.py', entity)
            
    else:
        print "Not found entitys for the project"
        
def CreateProjectCompleteNotFile(path, name, _input='', _view='', _controller='', imprime=True):
    anynew = []
    
    project = CreateProject(path, name, imprime)
    
    CreateMain(project)
    
    yaml = project + "app.yaml"
    if not ExistFile(yaml):
        CreateNewYaml(yaml, name, None)

    if NotEmpty(_input):
        anynew.append(CreateController(_input))
        UpdateYaml(yaml, _input, imprime)
        anynew.append(CreateView(_input))
    
    if NotEmpty(_view):
        anynew.append(CreateView(project, _view))

    if NotEmpty(_controller):
        anynew.append(CreateController(project, _controller))
        UpdateYaml(yaml, _controller, imprime)
    
    anynew = [new for new in anynew if new is True]
    
    if IsEmptyList(anynew):
        print "The project "+name+" already on day"
    

def CreateProjectCompleteFromFile(path, name, inputs=None, views=None, controllers=None, imprime=True):
    project = CreateProject(path, name, imprime)
    
    CreateMain(project)
    
    yaml = project + "app.yaml"
    if not ExistFile(yaml):
        CreateNewYaml(yaml, name, None)
    
    if NotEmptyList(inputs) or NotNone(inputs):
        for _input in inputs:
            #input's name
            _controller=_input.childNodes[0].data
            
            CreateController(project, _controller=_controller)
            UpdateYaml(yaml, _controller, imprime)
            CreateView(project, _view=_controller)

    if NotEmptyList(views) or NotNone(views):
        for _view in views:
            CreateView(project, _view=_view.childNodes[0].data)
    
    if NotEmptyList(controllers) or NotNone(controllers):
        for _controller in controllers:
            CreateController(project, _controller=_controller.childNodes[0].data)
            UpdateYaml(yaml, _controller, imprime)
    
    print "All files has been created"
    
'''
        Tool Framework webapp2 
        Version:    2.0
        Autor:      Jarov
        Fecha:      27-05-2015

Esta herrmaienta pretende ofrecer una forma flexible
y rapida de generar plantillas para webapp2, utilizando MVC
Model, View, Control, a traves de un archivo xml con la
estructura del proyecto
'''

parser = argparse.ArgumentParser(description="Tool Framework webapp2 v2.0")
parser.add_argument('-n', dest='name', help="Project webapp2's name")
parser.add_argument('-p', dest='path', help="Project's path")
parser.add_argument('-i', dest='input', help="Input filename to create VC")
parser.add_argument('-v', dest='view', help="View filename")
parser.add_argument('-c', dest='controller', help="Control filename")
parser.add_argument('-m', dest='model', help="Xml file with database's configuration")
parser.add_argument('-x', dest='xml', help="Xml filename with project's configuration" )
args = parser.parse_args()

name        = ''
_input      = ''
_view       = ''
_controller = ''
_file       = ''
_model      = ''

#Genera el path de donde se esta ejecutando este script
path = os.path.abspath(__file__)
path = os.path.dirname(path) + '/'

notfile         = True
haveName        = False
haveInput       = False
haveView        = False
haveController  = False


#Obtiene el nombre del archivo xml para el project
if args.xml:
    _file = args.xml
    _file = HaveExtension(_file, "xml")
    notfile = False
#Obtiene el nombre del archivo xml para models
elif args.model:
    _model = args.model
    _model = HaveExtension(_model, "xml")
    notfile = False
else:
    #Obtiene el nombre del proyecto
    if args.name:
        name = args.name
        haveName = True
        
    #Obtiene el path de los args
    if args.path:
        path = args.path

    #Obtiene el nombre para archivos VC
    if args.input:
        _input = args.input
        _input = OnlyName(_input)
        haveInput = True
        
    #Obtiene el nombre para V
    if args.view:
        _view = args.view
        _view = OnlyName(_view)
        haveView = True
        
    #Obtiene el nombre para C
    if args.controller:
        _controller = args.controller
        _controller = OnlyName(_controller)
        haveController = True
    
if notfile:
    if haveName:
        if haveInput or haveView or haveController:
            CreateProjectCompleteNotFile(path, name, _input, _view, _controller)
        else:
            print "Argument [-i], [-v] or [-c] is required"
    else:
        print "Argument [-n] (project name) is required"
elif NotEmpty(_file):
    projectTree = OpenXmlTree(path + _file, "project")
    if NotNone(projectTree):
        OpenXmlProject(path, _file, projectTree, True)
    else:
        print "Not Found File: " + path + _file
elif NotEmpty(_model):
    modelTree = OpenXmlTree(path + _model, "project")
    if NotNone(modelTree):
        OpenXmlModel(path, _model, modelTree)
    else:
        print "Not Found File: " + path + _model