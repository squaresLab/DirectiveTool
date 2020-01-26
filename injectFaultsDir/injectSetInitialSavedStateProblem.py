#!/usr/local/bin/python3




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
newInstanceDeclarationPattern = re.compile('public static .* newInstance(){')
injectImportStatement = 'import android.support.v4.app.Fragment;\n'
injectProblemStringInActivity = "Fragment.SavedState savedState = getSupportFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
#injectProblemStringInFragment = "Fragment.SavedState savedState = getFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
injectProblemStringInFragment = "Fragment.SavedState savedState = getFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
'Fragment.SavedState savedState = null;\ntry {\nsavedState = Fragment.SavedState.class.getConstructor(Bundle.class).newInstance(new Bundle());\n}\ncatch(Exception e) { \n}\n{0}.setInitialSavedState(savedState);\n'

def determineChanges(fullFilename):
  with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
    instanceList = []
    linesOfInterest = []
    lineStartsWithAFragment = False
    isActivity = False
    isFragment = False
    isNewInstance = False
    fileContents = []
    foundInstance = False
    for lineCount, line in enumerate(fin):
      fileContents.append(line)
      line = line.strip()
      if foundInstance:
        if '}' in line:
          foundInstance = False
        else:
          linesOfInterest.append(lineCount)
      if isNewInstance and '}' in line:
        isNewInstance = False
      elif not isFragment and not isActivity and line.startswith('public class'):
        if 'Fragment' in line:
          isFragment = True
        elif 'Activity' in line:
          isActivity = True
      elif newInstanceDeclarationPattern.match(line):
        #print('found new instance!!!')
        #print(line)
        inNewInstance = True
      else:
        lineItems = line.split(' ')
        if lineItems[0].endswith('Fragment') and '=' in line and not isNewInstance:
          #if isActivity:
            #print('is activity')
          #if isFragment:
            #print('is fragment')
          #print(line)
          #linesOfInterest.append(lineCount)
          lineStartsWithAFragment = True
          equalsIndex = None
          try:
            equalsIndex = lineItems.index('=')
          except ValueError as v:
            print('unable to find = in: {0}'.format(line))
            #input('stopping to check error')
          if equalsIndex:
            instanceList.append((lineItems[equalsIndex - 1], lineCount))
            foundInstance = True
  return fileContents, linesOfInterest, instanceList, isFragment, isActivity
    #if lineStartsWithAFragment:
      #print('file: {0} contains FragmentManager in line: {1}'.format(fullFilename, lineCount))
      #print('file of interest: {0}, lines of interest: {1}'.format(fullFilename, linesOfInterest))
      #input('stopping here to check file. Press enter when finished to move to next one')
  

def isPossibleInjectionRepo(repo):
  for root, dirs, files in os.walk(repo):
    for f in files:
      if f.endswith('.java'):
        fileContents, linesOfInterest, instanceList, isFragment, isActivity = determineChanges(os.path.join(root,f))
        if len(linesOfInterest) > 0 and (isFragment or isActivity):
          return True
  return False
        

 



def injectSetInitialSavedStateProblem(fullFilename):
  fileContents, linesOfInterest, instanceList, isFragment, isActivity = determineChanges(fullFilename)
  if len(linesOfInterest) > 0:
    lineToChange = linesOfInterest[random.randrange(len(linesOfInterest))]
    for instance, lineNumber in instanceList:
      if lineNumber < lineToChange:
        instanceToAdd = instance
      else:
        break
    if isFragment:
      fileContents.insert(lineToChange, injectProblemStringInFragment.format(instanceToAdd))
    elif isActivity:
      fileContents.insert(lineToChange, injectProblemStringInActivity.format(instanceToAdd))
    else:
      print('error: was not able to determine if the file was a Fragment or an Activity: {0}'.format(fullFilename))
      sys.exit(1)
    for lineCount, line in enumerate(fileContents):
      if line.startswith('import'):
        fileContents.insert(lineCount, injectImportStatement)
        break
    with open(fullFilename,'w') as fout:
      for line in fileContents:
        print(line, file=fout, end="")
    print('done, check file: {0}, line number: {1}'.format(fullFilename, lineToChange))
    input('stopping to check result. press enter to continue') 
    commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
    subprocess.run(commandList)
    return True
  return False


if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetInitialSavedStateProblem(fullFilename)
