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
injectFindViewByIdTemplate = 'View viewItem = findViewById(R.id.{0})\n'
androidIdPattern = re.compile('.*android:id="([^"]+)".*')

def extractIDs(fullLayoutFilename):
  ids = []
  with open(fullLayoutFilename,'r', encoding='utf-8', errors='surrogateescape') as fin:
    for line in fin:
      if 'android:id' in line:
        androidIdMatch = androidIdPattern.match(line)
        if androidIdMatch:
          ids.append(androidIdMatch.group(1).split('/')[-1])
  if len(ids) > 0:
    lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullLayoutFilename))
    subprocess.run(lookAtFileCommand)
    #input('stop here because I can\'t see it')
  return ids




#This method just finds the layout file. extractIDs parses the file to get the
#ids out
def getValidLayoutFile(fullFilename, layoutFile):
  dirname = fullFilename
  print('starting valid ids from layout files')
  #I'm not sure if using startingDir here will cause issues in other situations
  #I'll have to figure it out later
  startingBasePath = startingDir
  if startingBasePath[-1] == '/' and len(startingBasePath) > 1:
    startingBasePath = startingBasePath[:-1]
  print('startingBase')
  while dirname != startingBasePath and dirname is not '' and dirname is not '/':
    currentFilePath = dirname
    dirname = os.path.dirname(dirname)
    #print(currentFilePath)
  for root, dirs, files in os.walk(currentFilePath, topdown=False):
    for f in files:
      #if f.endswith('.xml'):
      # print(f)
      if layoutFile in f:
        print('{0}, {1}'.format(f, os.path.join(root,f)))
        return os.path.join(root,f)
  return None


def isPossibleInjectionFile(fullFilename):
  if 'transistor' in fullFilename:
    return 
  lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
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
      if line.startswith('setContentView('):
        inSectionOfInterest = False
        layoutFileFullName = line[line.index('(')+1:line.index(')')]
        layoutFile = layoutFileFullName.split('.')[-1]
        print(layoutFile)
        foundSetContentView = True
        #subprocess.run(lookAtFileCommand)
        #input('stopping to look at file {0}'.format(fullFilename))
        fileResult = getValidLayoutFile(fullFilename, layoutFile)
        if fileResult:
          ids = extractIDs(fileResult)
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
        isPossibleInjectionFile(os.path.join(root,f))


def injectSetContentViewIssue(fullFilename):
  #a skip added for testing; remove later
  if 'transistor' in fullFilename:
    return 
  lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
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
      if line.startswith('setContentView('):
        inSectionOfInterest = False
        layoutFileFullName = line[line.index('(')+1:line.index(')')]
        layoutFile = layoutFileFullName.split('.')[-1]
        print(layoutFile)
        foundSetContentView = True
        #subprocess.run(lookAtFileCommand)
        #input('stopping to look at file {0}'.format(fullFilename))
        fileResult = getValidLayoutFile(fullFilename, layoutFile)
        if fileResult:
          ids = extractIDs(fileResult)
        break
      elif 'onCreate(' in line:
        inSectionOfInterest = True
  if len(ids) > 0:
    idToUse = ids[random.randrange(len(ids))]
    injectLine = injectFindViewByIdTemplate.format(idToUse)
    print(injectLine)
    print(linesOfInterest)
    fileContents.insert(linesOfInterest[random.randrange(len(linesOfInterest))], injectLine)
    with open(fullFilename, 'w') as fout:
      for line in fileContents:
        print(line, file=fout, end="")
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
