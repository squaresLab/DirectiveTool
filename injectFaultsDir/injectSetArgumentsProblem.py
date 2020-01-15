#!/usr/local/bin/python3

import os
import re
import shlex
import subprocess
import random

startingDir = '/Users/zack/git/reposFromFDroid/'
injectionStringInFragment = 'Bundle args = new Bundle();\nargs.putInt("index", 5);\nsetArguments(args);\n'
injectionStringForFragmentInstance = 'Bundle args = new Bundle();\nargs.putInt("index", index);\n{0}.setArguments(args);\n'
#fragmentInstancePattern = re.compile('.*Fragment ([^ ]+)[| ]=')
lookAtFileCommandTemplate = 'open -a "Sublime Text" {0}'
extendsFragmentPattern = re.compile('.*extends [^ ]+Fragment .*')

#I haven't figured out how to do this the smart way, so I'm doing it the easy dumb way for now
#meaning - I can randomly inject errors, but I don't think people will make these errors in 
#practice. I'm not sure how to do the ones they will make without better state understanding
#from the app

#I might need to eventually change this to the case that my checker can handle

#This can still inject code in the wrong spot in nested classes. But I'm not sure
#how to fix that without writing a parser


def isRepoOfInterest(repo):
  for root, dirs, files in os.walk(repo):
    for f in files:
      fullFilename = os.path.join(root, f)
      linesInFile = []
      linesOfInterest = []
      nestingCount = 0
      inFragmentFile = False
      with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
        for lineCount, line in enumerate(fin):
          linesInFile.append(line)
          #print(line)
          if inFragmentFile:
            if nestingCount > 1:
              linesOfInterest.append(lineCount)
              return True
          else:
            matchResult = extendsFragmentPattern.match(line)
            if matchResult:
              #print('fragment instance: {0}, line count: {1}'.format(matchResult.group(1), lineCount))
              inFragmentFile = True
          if '{' in line:
            nestingCount += 1 
          if '}' in line:
            nestingCount -= 1
      if len(linesOfInterest) > 0:
        return True
  return False
 

def injectSetArgumentsProblem(fullFilename):
  linesInFile = []
  nestingCount = 0
  inFragmentFile = False
  linesOfInterest = []
  with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
    for lineCount, line in enumerate(fin):
      linesInFile.append(line)
      #print(line)
      if inFragmentFile:
        if nestingCount > 1:
          linesOfInterest.append(lineCount)
      else:
        matchResult = extendsFragmentPattern.match(line)
        if matchResult:
          #print('fragment instance: {0}, line count: {1}'.format(matchResult.group(1), lineCount))
          inFragmentFile = True
      if '{' in line:
        nestingCount += 1 
      if '}' in line:
        nestingCount -= 1
  if len(linesOfInterest) > 0:
    insertionLine = linesOfInterest[random.randrange(len(linesOfInterest))]
    linesInFile.insert(insertionLine, injectionStringInFragment)
    with open(fullFilename, 'w') as fout:
      for line in linesInFile:
        print(line, file=fout, end="")
    lookAtFileCommand = shlex.split(lookAtFileCommandTemplate.format(fullFilename))
    subprocess.run(lookAtFileCommand)
    #input('change made. Check to see')
    return True
  return False



if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetArgumentsProblem(fullFilename)

