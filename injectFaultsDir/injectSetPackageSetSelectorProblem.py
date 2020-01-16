#!/usr/local/bin/python3

import os
import random
import subprocess
import shlex

startingDir = '/Users/zack/git/reposFromFDroid/'
setSelectorTemplate = '{0}.setSelector(new Intent());\n'
setPackageTemplate = '{0}.setPackage("testPackage");\n'

def extractInstanceFromLine(line):
  line = line.strip()
  lineItems = line.split('.')
  instance = lineItems[0]
  return instance

def determineInjectionInfo(fullFilename):
  #print(fullFilename)
  newFileLines =  []
  with open(fullFilename, 'r',encoding="utf-8",errors="ignore") as fin:
    foundSetSelector = False
    foundSetPackage = False
    everFoundSetSelector = False
    everFoundSetPackage = False
    linesOfInterest = []
    instanceList = []
    for lineCount, line in enumerate(fin):
      newFileLines.append(line)
      if foundSetPackage or foundSetSelector:  
        if '}' in line:
          foundSetSelector = False
          foundSetPackage = False
        linesOfInterest.append(lineCount)
      elif 'setSelector(' in line:
        #input('stopping here because found setSelector')
        foundSetSelector = True
        everFoundSetSelector = True
        lineCountOfInterest = lineCount
        instanceList.append((extractInstanceFromLine(line),lineCount))
      elif 'setPackage(' in line:
        #input('stopping here because found setPackage')
        foundSetPackage = True
        everFoundSetPackage = True
        lineCountOfInterest = lineCount
        instanceList.append((extractInstanceFromLine(line),lineCount))
  return newFileLines, linesOfInterest, instanceList, everFoundSetPackage, everFoundSetSelector

def isPossibleInjectionRepo(repo):
  for root, dirs, files in os.walk(repo):
    for f in files:
      if f.endswith('.java'):
        newFileLines, linesOfInterest, instanceList, everFoundSetPackage, everFoundSetSelector = determineInjectionInfo(os.path.join(root,f))
        if len(linesOfInterest) > 0 and (everFoundSetSelector or everFoundSetPackage):
          return True
  return False
        
def injectSetPackageSetSelectorProblem(fullFilename):
  newFileLines, linesOfInterest, instanceList, everFoundSetPackage, everFoundSetSelector = determineInjectionInfo(fullFilename)
  if everFoundSetPackage or everFoundSetSelector:  
    if len(linesOfInterest) > 0:
      #if we can try to avoid adding the line at the end of the method - avoid 
      #adding the line after return statements
      if len(linesOfInterest) > 1:
        linesOfInterest = linesOfInterest[:-1]
      lineToChange = linesOfInterest[random.randrange(len(linesOfInterest))]
      instanceToUse = ""
      for instance, lineNumber in instanceList:
        if lineNumber < lineToChange:
          instanceToUse = instance
        else:
          break
      codeToAdd = ""
      if everFoundSetPackage:
        print('added setSelector')
        codeToAdd = setSelectorTemplate.format(instanceToUse)
      elif everFoundSetSelector:
        print('added setPackage')
        codeToAdd = setPackageTemplate.format(instanceToUse)
      newFileLines.insert(lineToChange, codeToAdd)
      print('added line {0}'.format(newFileLines[lineToChange]))
      with open(fullFilename, 'w') as fout:
        for line in newFileLines:
          print(line, file=fout, end="")
      print('file: {0}, line: {1}'.format(fullFilename, lineToChange))
      commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
      subprocess.run(commandList)
      input('stopping to check the injection')
      return True
  return False


if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetPackageSetSelectorProblem(fullFilename)
