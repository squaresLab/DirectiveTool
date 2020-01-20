#!/usr/local/bin/python3

import sys
import os
import random
import subprocess
import shlex

injectionTemplateDir = '/Users/zack/git/DirectiveTool/injectFaultsDir/injectionTemplateDir'
lineToAdd = 'Toast.makeText(getActivity(), "Activity Title:"+getActivity().getTitle(), Toast.LENGTH_SHORT).show();'

def isPossibleInjectionRepo(dirToCheck):
  for root, dirs, files in os.walk(dirToCheck):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        #print('opening: {0}'.format(fullFilename))
        fileOfInterest = False
        randomLineToChange = None
        with open(fullFilename,'r',encoding="utf-8",errors="surrogateescape") as fin:
          foundExtendInPreviousLine = False
          for line in fin:
            if 'extends' in line or foundExtendInPreviousLine:
              #this is a simple heuristic. I should probably do something better later
              #print(line)
              lineItems = line.split()
              extendedIndex = None
              if foundExtendInPreviousLine:
                extendedIndex = 0
                foundExtendInPreviousLine = False
              else:
                for itemCount, item in enumerate(lineItems):
                  if item == 'extends':
                    extendedIndex = itemCount + 1
                    break
              if extendedIndex:
                if extendedIndex > len(lineItems) - 1:
                  foundExtendInPreviousLine = True
                else:
                  extendedClass = lineItems[extendedIndex]
                  if 'Fragment' in extendedClass and extendedClass != 'FragmentActivity':
                    fileOfInterest = True
                    #print(extendedClass)
                    break
        if fileOfInterest:
          methodBounds = []
          nestCount = 0
          with open(fullFilename, 'r') as fin:
            #print(fullFilename)
            for lineCount, line in enumerate(fin):
              if '{' in line:
                methodBounds.append(('start',lineCount+1, nestCount))
                nestCount += 1
              if '}' in line:
                nestCount -= 1
                methodBounds.append(('end',lineCount+1, nestCount))
          methodStartLocation = 0
          methodLineSum = 0
          for p, c, n in methodBounds:
            #print("{0}: {1}, {2}".format(p,c, n))
            if n == 2:
              if p == 'start':
                #adding a plus one because it doesn't make sense to add
                #a new line in the method call declaration. only makes sense 
                #after 
                methodStartLocation = c + 1
              elif p == 'end':
                methodLineSum += c - methodStartLocation + 1
          #print('chose the random line')
          if methodLineSum > 0:
            randomLineToChange = random.randrange(methodLineSum) + 1
            if randomLineToChange is not None:
              return True 
  return False

def findPossibleInjectionRepos(dirListToCheck):
  return [d for d in dirListToCheck if isPossibleInjectionRepo(d)]


def addToastImport(fullFilename):
  importToastLine = 'import android.widget.Toast;\n'
  foundToastImportLine = False
  fileContents = []
  lastImportLineCount = -1
  with open(fullFilename, 'r') as fin:
    for lineCount, line in enumerate(fin):
      fileContents.append(line)
      line = line.strip()
      if line == importToastLine:
        foundToastImportLine = True
      if line.startswith('import '):
        lastImportLineCount = lineCount
  #if the view import line isn't in there, add the import line to the file
  if not foundToastImportLine and lastImportLineCount > 0:
    fileContents.insert(lastImportLineCount, importToastLine)
  with open(fullFilename, 'w') as fout:
    for line in fileContents:
      print(line, file=fout, end="")


#the current approach could break multi line if-else statements with out {}'s. 
#Decide if it is worth it to correct this or determine another way around it'
def parseFileForInjection(fullFilename):
  #print('opening: {0}'.format(fullFilename))
  fileOfInterest = False
  randomLineToChange = None
  with open(fullFilename, 'r') as fin:
    for line in fin:
      if 'extends' in line:
        #this is a simple heuristic. I should probably do something better later
        #print(line)
        lineItems = line.split()
        extendedIndex = None
        for itemCount, item in enumerate(lineItems):
          if item == 'extends':
            extendedIndex = itemCount + 1
            break
        extendedClass = lineItems[extendedIndex]
        if 'Fragment' in extendedClass and extendedClass != 'FragmentActivity':
          fileOfInterest = True
          #print(extendedClass)
          break
  if fileOfInterest:
    methodBounds = []
    nestCount = 0
    with open(fullFilename, 'r') as fin:
      #print(fullFilename)
      for lineCount, line in enumerate(fin):
        if '{' in line:
          methodBounds.append(('start',lineCount+1, nestCount))
          nestCount += 1
        if '}' in line:
          nestCount -= 1
          methodBounds.append(('end',lineCount+1, nestCount))
    methodStartLocation = 0
    methodLineSum = 0
    for p, c, n in methodBounds:
      #print("{0}: {1}, {2}".format(p,c, n))
      #counting from 0, so 0 is the class and 1 is the class methods
      #might want to exclude the lines where n equals 2 later
      if n == 1:
        if p == 'start':
          #adding a plus one because it doesn't make sense to add
          #a new line in the method call declaration. only makes sense 
          #after 
          methodStartLocation = c + 1
        elif p == 'end':
          methodLineSum += c - methodStartLocation + 1
    #print('chose the random line')
    if methodLineSum > 0:
      print('possible number of lines to inject into: {0}'.format(methodLineSum))
      randomLineToChange = random.randrange(methodLineSum) + 1
    else:
      print(methodBounds)
      print(methodLineSum)
      print(fullFilename)
      print('error: unable to find any possible methods to inject getActivity in the file')
      sys.exit(1)
  if randomLineToChange is not None:
    tempLineToChange = randomLineToChange
    for p, c, n in methodBounds:
      #print("{0}: {1}, {2}".format(p,c, n))
      if n == 1:
        if p == 'start':
          methodStartLocation = c
        elif p == 'end':
          if tempLineToChange < c - methodStartLocation + 1:
            lineToChange = methodStartLocation + tempLineToChange + 1
          else:
            tempLineToChange -= c - methodStartLocation + 1
    newFileContents  = []
    with open(fullFilename, 'r') as fin:
      for lineCount, line in enumerate(fin):
        line = line.rstrip()
        if lineCount == lineToChange:
          newFileContents.append(lineToAdd)
        newFileContents.append(line)
    with open(fullFilename, 'w') as fout:
      for l in newFileContents:
        print(l, file=fout)
    addToastImport(fullFilename)
    print('changed line {0} of {1}'.format(lineToChange, fullFilename))
    #input('stopping to check change')
    lookAtFileCommand = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
    subprocess.run(lookAtFileCommand)
    input('stopping to look at file {0}'.format(fullFilename))
    return True
  return False
#
    #surroundingLines = []
    #linesToInclude = 3
    #with open(fullFilename, 'r') as fin:
    #  for lineCount, line in enumerate(fin):
    #    if lineCount > lineToChange - linesToInclude and lineCount < lineToChange + linesToInclude: 
    #      surroundingLines.append(line.rstrip())
    #print('changing line: {0}'.format(lineToChange))
    ##print(len(surroundingLines)) 
    #if randomLineToChange < linesToInclude:
    #  linesToSkip =  randomLineToChange
    #else:
    #  linesToSkip = linesToInclude
    #matchFile = os.path.join(injectionTemplateDir, 'match')
    #rewriteFile = os.path.join(injectionTemplateDir, 'rewrite')
    #with open(matchFile, 'w') as fout:
    #  for line in surroundingLines:
    #    print(line, file=fout)
    #with open(rewriteFile, 'w') as fout:
    #  for lineCount, line in enumerate(surroundingLines):
    #    if lineCount == linesToSkip:
    #      print(lineToAdd, file=fout)
    #    print(line, file=fout)
    #for l in surroundingLines:
    #  print(l)
    #for line in s
    #countCommandString = 'comby -match-only -count -f {0} -dir {1} -templates {2}'.format(f, root, injectionTemplateDir)
    #print(countCommandString)
    #combyCountCommand =  shlex.split(countCommandString)
    #combyCountResult = subprocess.run(combyCountCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in combyCountResult.stdout.decode('utf-8').splitlines():
    #  print(line)
    #input('stopping here for debugging')


def injectInDirectory(directory):
  for root, dirs, files in os.walk(dirToCheck):
    for f in files:
      if f.endswith('.java'):
        parseFileForInjection(os.path.join(root,f))


def injectInRepo(repoDir):
  javaFiles = []
  for root, dirs, files in os.walk(repoDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        javaFiles.append(fullFilename)
  random.shuffle(javaFiles)
  for fullFilename in javaFiles:
    if parseFileForInjection(fullFilename):
      print('changed: {0}'.format(fullFilename))
      #input('stop for a change. Press enter to continue')
      break


  

if __name__ == "__main__":
  if len(sys.argv) > 1:
    print(sys.argv[1])
    injectInDirectory(sys.argv[1])
  else:
    injectInDirectory('/Users/zack/git/reposFromFDroid/Riksdagskollen')