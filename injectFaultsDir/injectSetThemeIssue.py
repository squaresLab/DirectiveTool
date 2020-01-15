#!/usr/local/bin/python3 

import os
import subprocess
import shlex
import random
import sys


startingDir = '/Users/zack/git/reposFromFDroid/'
setThemeInjectionString = 'setTheme(android.R.style.Theme_Translucent_NoTitleBar);\n'

def containsFileOfInterest(repo):
  for root, dirs, files in os.walk(repo, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fileContents = []
        fullFilename = os.path.join(root, f)
        with open(fullFilename,'r',encoding="utf-8",errors="surrogateescape") as fin:
          foundSetTheme = False
          recordingImportantLines = False
          importantLines = []
          onCreateDeclaration = 'protected void onCreate(Bundle savedInstanceState) {'
          inOnCreate = False
          for lineCount, line in enumerate(fin):
            fileContents.append(line)
            if inOnCreate and '}' in line:
              if recordingImportantLines:
                importantLines.append(lineCount)
              inOnCreate = False
              recordingImportantLines = False
            elif onCreateDeclaration in line:
              inOnCreate = True
            elif 'setContentView(' in line and inOnCreate:
              #print('found setContentView in line: {0}'.format(lineCount))
              foundSetTheme = True
              recordingImportantLines = True
            elif recordingImportantLines:
              importantLines.append(lineCount)
        if foundSetTheme:
          return True
  return False


def findPossibleInjectionRepos(possibleRepos):
  #print(os.listdir(startingDirectory))
  #print(os.path.isdir(os.listdir(startingDirectory)[0]))
  reposOfInterest = [d for d in possibleRepos if containsFileOfInterest(d)]
  #print(possibleRepos)
  #if True:
  #print(len(possibleRepoList))
  #reposOfInterest = [r for r in possibleRepoList if containsFileOfInterest(r)]
  return reposOfInterest
  
  
def injectSetThemeIssue(fullFilename):
  fileContents = []
  with open(fullFilename,'r') as fin:
    foundSetTheme = False
    recordingImportantLines = False
    importantLines = []
    onCreateDeclaration = 'protected void onCreate(Bundle savedInstanceState) {'
    inOnCreate = False
    for lineCount, line in enumerate(fin):
      fileContents.append(line)
      if inOnCreate and '}' in line:
        if recordingImportantLines:
          importantLines.append(lineCount)
        inOnCreate = False
        recordingImportantLines = False
      elif onCreateDeclaration in line:
        inOnCreate = True
      elif 'setContentView(' in line and inOnCreate:
        print('found setContentView in line: {0}'.format(lineCount))
        foundSetTheme = True
        recordingImportantLines = True
      elif recordingImportantLines:
        importantLines.append(lineCount)
  if foundSetTheme:
    lineToChange = importantLines[random.randrange(len(importantLines))]
    fileContents.insert(lineToChange, setThemeInjectionString)
    with open(fullFilename, 'w') as fout:
      for line in fileContents:
        print(line, end='', file=fout)
    return True
  else:
    return False
    #commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
    #subprocess.run(commandList)
    #input('inserted line of interest in file: {0}\nPress enter to continue'.format(fullFilename))

def injectInRepo(repoDir):
  javaFiles = []
  for root, dirs, files in os.walk(repoDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        javaFiles.append(fullFilename)
  random.shuffle(javaFiles)
  for fullFilename in javaFiles:
    if injectSetThemeIssue(fullFilename):
      print('changed: {0}'.format(fullFilename))
      #input('stop for a change. Press enter to continue')
      break


if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetThemeIssue(fullFilename)