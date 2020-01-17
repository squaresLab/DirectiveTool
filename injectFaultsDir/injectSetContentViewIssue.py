#!/usr/local/bin/python3




import os
import re
import random
import sys
import subprocess
import shlex

#I'm not sure my initial approach makes the most sense because the Fragment instance
#may be different when you move it around

startingDir = '/Users/zack/git/reposFromFDroid/'
#newInstanceDeclarationPattern = re.compile('public static .* newInstance(){')
#injectProblemStringInActivity = "Fragment.SavedState savedState = getSupportFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
#injectProblemStringInFragment = "Fragment.SavedState savedState = getFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
injectFindViewByIdTemplate = 'View viewItem = findViewById(R.id.{0});\n'
androidIdPattern = re.compile('.*android:id="([^"]+)".*')

def extractIDs(fullLayoutFilename):
  print('extracting ids from: {0}'.format(fullLayoutFilename))
  ids = []
  with open(fullLayoutFilename,'r', encoding='utf-8', errors='surrogateescape') as fin:
    for line in fin:
      if 'android:id' in line:
        androidIdMatch = androidIdPattern.match(line)
        if androidIdMatch:
          ids.append(androidIdMatch.group(1).split('/')[-1])
  #if len(ids) > 0:
    #lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullLayoutFilename))
    #subprocess.run(lookAtFileCommand)
    #input('stop here because I can\'t see it')
  return ids




#This method just finds the layout file from a given basename. The purpose of 
#this method is to get an id that will compile when the injected call is moved
#to the right place.
#extractIDs parses the file to get the
#ids out
def getValidLayoutFile(fullFilename, layoutFile):
  currentFilePath = fullFilename
  #I'm not sure if using startingDir here will cause issues in other situations
  #I'll have to figure it out later
  startingBasePath = os.getcwd()
  if startingBasePath[-1] == '/' and len(startingBasePath) > 1:
    startingBasePath = startingBasePath[:-1]
  #try to get the repo folder so it can be searched for valid ids
  while currentFilePath != '/' and currentFilePath != '' and \
  (not os.path.isdir(currentFilePath) or not '.git' in os.listdir(currentFilePath)):
    currentFilePath = os.path.dirname(currentFilePath)
  print('file path: {0} for inputs {1},{2}'.format(currentFilePath, fullFilename, layoutFile))
  #while dirname != startingBasePath and dirname is not '' and dirname is not '/':
  #  currentFilePath = dirname
  #  dirname = os.path.dirname(dirname)
  for root, dirs, files in os.walk(currentFilePath, topdown=False):
    for f in files:
      if f.endswith('.xml') and layoutFile in f:
          #print('{0}, {1}'.format(f, os.path.join(root,f)))
          return os.path.join(root,f)
  return None

def addViewImport(fullFilename):
  importViewLine = 'import android.view.View;'
  foundViewImportLine = False
  fileContents = []
  lastImportLineCount = -1
  with open(fullFilename, 'r') as fin:
    for lineCount, line in enumerate(fin):
      fileContents.append(line)
      line = line.strip()
      if line == importViewLine:
        foundViewImportLine = True
      if line.startswith('import '):
        lastImportLineCount = lineCount
  #if the view import line isn't in there, add the import line to the file
  if not foundViewImportLine and lastImportLineCount > 0:
    fileContents.insert(lastImportLineCount, importViewLine)
  with open(fullFilename, 'w') as fout:
    for line in fileContents:
      print(line, file=fout, end="")







  #add the line import android.view.View


def isPossibleInjectionFile(fullFilename):
  #I don't remember why I have this check here. Maybe delete it?
  #if 'transistor' in fullFilename:
  #  return False 
  #lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
  foundSetContentView = False
  ids = []
  linesOfInterest = []
  inSectionOfInterest = False
  with open(fullFilename, 'r', encoding='utf-8', errors='surrogateescape') as fin:
    for lineCount, line in enumerate(fin):
      line = line.strip()
      if inSectionOfInterest:
        linesOfInterest.append(lineCount)
        if '}' in line:
          inSectionOfInterest = False
      if line.startswith('setContentView('):
        inSectionOfInterest = False
        layoutFileFullName = line[line.index('(')+1:line.index(')')]
        layoutFile = layoutFileFullName.split('.')[-1]
        foundSetContentView = True
        #subprocess.run(lookAtFileCommand)
        #input('stopping to look at file {0}'.format(fullFilename))
        fileResult = getValidLayoutFile(fullFilename, layoutFile)
        if fileResult:
          ids = extractIDs(fileResult)
          if len(ids) > 0:
            print('found {0} ids in file {1}'.format(len(ids), fileResult))
        break
      elif 'onCreate(' in line:
        inSectionOfInterest = True
  if len(ids) > 0:
    return True
  return False

def isPossibleInjectionRepo(repo):
  for root, dirs, files in os.walk(repo):
    for f in files:
      if f.endswith('.java'):
        if isPossibleInjectionFile(os.path.join(root,f)):
          return True
  return False


def injectSetContentViewIssue(fullFilename):
  #lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
  foundSetContentView = False
  ids = []
  fileContents = []
  linesOfInterest = []
  inSectionOfInterest = False
  with open(fullFilename, 'r', encoding='utf-8', errors='surrogateescape') as fin:
    for lineCount, line in enumerate(fin):
      fileContents.append(line)
      line = line.strip()
      if inSectionOfInterest:
        linesOfInterest.append(lineCount)
        if '}' in line:
          inSectionOfInterest = False
      if ids == []:
        if line.startswith('setContentView('):
          print('found set content view')
          inSectionOfInterest = False
          layoutFileFullName = line[line.index('(')+1:line.index(')')]
          layoutFile = layoutFileFullName.split('.')[-1]
          print('looking for {0} in injection process'.format(layoutFile))
          foundSetContentView = True
          #subprocess.run(lookAtFileCommand)
          #input('stopping to look at file {0}'.format(fullFilename))
          fileResult = getValidLayoutFile(fullFilename, layoutFile)
          if fileResult:
            ids = extractIDs(fileResult)
            #print('length of ids: {0}'.format(len(ids)))
        elif 'onCreate(' in line:
          #print('found onCreate')
          inSectionOfInterest = True
  if len(ids) > 0:
    idToUse = ids[random.randrange(len(ids))]
    injectLine = injectFindViewByIdTemplate.format(idToUse)
    print(injectLine)
    #print(linesOfInterest)
    fileContents.insert(linesOfInterest[random.randrange(len(linesOfInterest))], injectLine)
    with open(fullFilename, 'w') as fout:
      for line in fileContents:
        print(line, file=fout, end="")
    addViewImport(fullFilename)
    print('injected set content view issue into {0}'.format(fullFilename))
    return True
  return False
    #subprocess.run(lookAtFileCommand)
    #input('stopping here to check')


if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetContentViewIssue(fullFilename)
