#!/usr/local/bin/python3

import os
import re
import shlex
import subprocess
import random
import sys

startingDir = '/Users/zack/git/reposFromFDroid/'
lookAtFileCommandTemplate = 'open -a "Sublime Text" {0}'
extendsFragmentPattern = re.compile('.*extends [^ ]+Fragment .*')
extendsAsyncTaskPattern = re.compile('.*extends AsyncTask .*')
inlineAsyncTaskPattern = re.compile('.* new [^ ]*AsyncTask[^ ]* .*{.*')
getResourcesCall = 'getResources();\n'

#this call inject code after a return statement - which doesn't do anything. 
#Might want to fix that later but I'm not sure if it is important. Making a
#note so I can figure out later

#consider pulling out the common parts of these two methods into another method
def containsFileOfInterest(repo):
  for root, dirs, files in os.walk(repo, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        linesInFile = []
        linesOfInterest = []
        foundExtendsFragment = False
        foundExtendsAsyncTask = False
        inImportantSection = False
        nestingCount = 0
        with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
          for lineCount, line in enumerate(fin):
            linesInFile.append(line)
            if inImportantSection:
              if '{' in line:
                nestingCount += 1
              elif nestingCount > 1 and line.strip() != '@Override':
                linesOfInterest.append(lineCount)
              #This needs to be evaluated as a separate if, otherwise it is never true
              if '}' in line:
                nestingCount -= 1
                if nestingCount < 1:
                  inImportantSection = False
            else: 
              fragmentMatchResult = extendsFragmentPattern.match(line)
              if fragmentMatchResult:
                #print('{0} matches Fragment pattern'.format(line))
                foundExtendsFragment = True
                #This check could easily get sections of code that are not useful - 
                #doesn't really calculate scope, but it should work in most cases
                if foundExtendsAsyncTask and not inImportantSection:
                  inImportantSection = True
                  nestingCount = 1
                #print('fragment instance: {0}, line count: {1}'.format(matchResult.group(1), lineCount))
              else:
                asyncMatchPattern = inlineAsyncTaskPattern.match(line) 
                #if asyncMatchPattern:
                if asyncMatchPattern:
                  print('{0} matches AsyncTask pattern'.format(line))
                  foundExtendsAsyncTask = True
                  #This check could easily get sections of code that are not useful - 
                  #doesn't really calculate scope, but it should work in most cases
                  if not inImportantSection and foundExtendsFragment:
                    inImportantSection = True
                    nestingCount = 1
        if len(linesOfInterest) > 0:
          yield fullFilename
          return
        
def findPossibleInjectionRepos(possibleRepoList):
  reposOfInterest = [r for r in possibleRepoList if containsFileOfInterest(r)]
  return reposOfInterest
 


def injectGetResourcesIssue(fullFilename):
  linesInFile = []
  linesOfInterest = []
  foundExtendsFragment = False
  foundExtendsAsyncTask = False
  inImportantSection = False
  nestingCount = 0
  with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
    for lineCount, line in enumerate(fin):
      linesInFile.append(line)
      if inImportantSection:
        if '{' in line:
          nestingCount += 1
        elif nestingCount > 1 and line.strip() != '@Override':
          linesOfInterest.append(lineCount)
        #This needs to be evaluated as a separate if, otherwise it is never true
        if '}' in line:
          nestingCount -= 1
          if nestingCount < 1:
            inImportantSection = False
      else: 
        fragmentMatchResult = extendsFragmentPattern.match(line)
        if fragmentMatchResult:
          #print('{0} matches Fragment pattern'.format(line))
          foundExtendsFragment = True
          #This check could easily get sections of code that are not useful - 
          #doesn't really calculate scope, but it should work in most cases
          if foundExtendsAsyncTask and not inImportantSection:
            inImportantSection = True
            nestingCount = 1
          #print('fragment instance: {0}, line count: {1}'.format(matchResult.group(1), lineCount))
        else:
          asyncMatchPattern = inlineAsyncTaskPattern.match(line) 
          #if asyncMatchPattern:
          if asyncMatchPattern:
            print('{0} matches AsyncTask pattern'.format(line))
            foundExtendsAsyncTask = True
            #This check could easily get sections of code that are not useful - 
            #doesn't really calculate scope, but it should work in most cases
            if not inImportantSection and foundExtendsFragment:
              inImportantSection = True
              nestingCount = 1
  if len(linesOfInterest) > 0:
    injectionLocation = linesOfInterest[random.randrange(len(linesOfInterest))]  
    linesInFile.insert(injectionLocation, getResourcesCall)
    with open(fullFilename,'w') as fout:
      for line in linesInFile:
        print(line, file=fout, end='')
    showFileCommand = shlex.split(lookAtFileCommandTemplate.format(fullFilename))
    subprocess.run(showFileCommand)
    return True 
  else:
    return False
    #lookAtFileCommand = shlex.split(lookAtFileCommandTemplate.format(fullFilename))
    #subprocess.run(lookAtFileCommand)
    #input('problem injected a line {0} of file {1}. Check to see'.format(injectionLocation, fullFilename))


def injectInRepo(repoDir):
  javaFiles = []
  for root, dirs, files in os.walk(repoDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        javaFiles.append(fullFilename)
  random.shuffle(javaFiles)
  for fullFilename in javaFiles:
    if injectGetResourcesIssue(fullFilename):
      print('changed: {0}'.format(fullFilename))
      #nput('stop for a change. Press enter to continue')
      break

if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectGetResourcesIssue(fullFilename)



