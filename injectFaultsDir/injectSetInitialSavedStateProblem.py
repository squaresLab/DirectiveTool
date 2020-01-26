#!/usr/local/bin/python3




#!/usr/local/bin/python3
import os
import re
import random
import sys
import subprocess
import shlex
import string

#I'm not sure my initial approach makes the most sense because the Fragment instance
#may be different when you move it around

startingDir = '/Users/zack/git/reposFromFDroid/'
newInstanceDeclarationPattern = re.compile('public static .* newInstance(){')
#debating on converting the code to use the multiple statements below
injectImportStatement = 'import android.support.v4.app.Fragment;\n'
#injectImportStatements = ['import android.support.v4.app.Fragment;\n', 'import ']
injectProblemStringInActivity = "Fragment.SavedState savedState = getSupportFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
#injectProblemStringInFragment = "Fragment.SavedState savedState = getFragmentManager().saveFragmentInstanceState({0});\n{0}.setInitialSavedState(savedState);\n"
#injectProblemStringInFragmentList = """Fragment.SavedState savedState = null;\ntry {\nsavedState = Fragment.SavedState.class.getConstructor(Bundle.class).newInstance(new Bundle());\n}\ncatch(Exception e) { \n}\n{0}.setInitialSavedState(savedState);\n"""
#injectProblemStringInFragmentTemplate = string.Template("Fragment.SavedState savedState = null;\ntry {\nsavedState = Fragment.SavedState.class.getConstructor(Bundle.class).newInstance(new Bundle());\n}\ncatch(Exception e) { \n}\n$instance.setInitialSavedState(savedState);\n")
injectProblemStringInFragment = "Fragment.SavedState savedState = null;\ntry {\nsavedState = Fragment.SavedState.class.getConstructor(Bundle.class).newInstance(new Bundle());\n}\ncatch(Exception e) { \n}\nsetInitialSavedState(savedState);\n"

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
        #just focusing on the fragment case at the moment
        if len(linesOfInterest) > 0 and (isFragment):
          return True
  return False
        

def getPossibleInjectionLines(fullFilename):
  nestingCount = 0
  injectionLineList = []
  with open(fullFilename,'r',encoding='utf-8',errors="surrogateescape") as fin:
    for lineCount, line in enumerate(fin):
      # get lines inside of a class and method - This doesn't handle nested classes,
      # so I might need to add that functionality later
      if nestingCount == 2:
        injectionLineList.append(lineCount)
      for c in line: 
        if c == '{':
          nestingCount += 1
        if c == '}':
          nestingCount -= 1
  return injectionLineList




def injectSetInitialSavedStateProblem(fullFilename):
  #don't just inject into lines of interest like I was doing earlier; those
  #are the correct parts of the application
  fileContents, linesOfInterest, instanceList, isFragment, isActivity = determineChanges(fullFilename)
  if isFragment:
    injectionLineList = getPossibleInjectionLines(fullFilename)
    lineToChange = injectionLineList[random.randrange(len(injectionLineList))]
    #don't add the instances anymore
    #for instance, lineNumber in instanceList:
      #if lineNumber < lineToChange:
        #instanceToAdd = instance
      ##else:
        #break
    if isFragment:
      #print('instance to add: {0}'.format(instanceToAdd))
      fullString = injectProblemStringInFragment
      print('injection code: {0}'.format(fullString))
      print('line to change: {0}'.format(lineToChange))
      print('file contents length: {0}'.format(len(fileContents)))
      fileContents.insert(lineToChange, fullString)
      #fileContents.insert(lineToChange, injectProblemStringInFragment.format(instanceToAdd))
    elif isActivity:
      fileContents.insert(lineToChange, injectProblemStringInActivity.format(instanceToAdd))
    else:
      print('error: was not able to determine if the file was a Fragment or an Activity: {0}'.format(fullFilename))
      sys.exit(1)
    #first scan the import statements to see if the import statement needs to 
    #be added; if so go through them again to find the place to add the statement
    #may eventually be able to combine these iterations
    needsToAddImportStatment = True
    #-2 to remove the ;\n at the end
    baseClassToImport = injectImportStatement.split('.')[-1][:-2]
    for line in fileContents:
      if line.startswith('import'):
        importedClass = line.split(' ')[1]
        classBaseName = importedClass.split('.')[-1][:-2]
        if classBaseName == baseClassToImport:
          needsToAddImportStatment = False
          break
    if needsToAddImportStatment:
      for lineCount, line in enumerate(fileContents):
        if line.startswith('import'):
          fileContents.insert(lineCount, injectImportStatement)
          break
    with open(fullFilename,'w') as fout:
      for line in fileContents:
        print(line, file=fout, end="")
    print('done, check file: {0}, line number: {1}'.format(fullFilename, lineToChange))
    commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
    subprocess.run(commandList)
    input('stopping to check result. press enter to continue') 
    return True
  return False


if __name__ == "__main__":
  for root, dirs, files in os.walk(startingDir, topdown=False):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root,f)
        injectSetInitialSavedStateProblem(fullFilename)
