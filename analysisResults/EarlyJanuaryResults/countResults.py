#!/usr/local/bin/python3

#This is the updated version of processFullResults.py

import sys
import os
import subprocess
import collections

#errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrorsSecondPass.txt'
jarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/MultipleJarBuild/AndroidDirectiveChecker.jar'
currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
#outputFileName = '/Users/zack/git/DirectiveTool/runResults.txt'
androidJarLocation = '/Users/zack/git/DirectiveTool/runCheckerPackage/android.jar'

successDict = {}
errorDict = {}
callgraphProblemDict = {}
timeoutDict = {}

def runChecker(checker, filename):
  checkerCommand = ['java', '-jar', jarLocation]
  fullFilename = os.path.join(currentAppFolder, filename)
  currentCheckerCommand = checkerCommand.copy()
  currentCheckerCommand.append(checker)
  currentCheckerCommand.append(fullFilename)
  currentCheckerCommand.append(androidJarLocation)
  checkerResult = subprocess.run(currentCheckerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  callgraphErrorCount = 0
  if checkerResult.returncode == 0:
    print('checker result: {0}'.format(checkerResult))
    for line in checkerResult.stdout.decode('utf-8').splitlines():
      print('line: {0}'.format(line))
    for line in checkerResult.stderr.decode('utf-8').splitlines():
      print('line: {0}'.format(line))
      if line.startswith('total number'):
        lineItems = line.split(' ')
        if int(lineItems[-1]) != 0:
          print("found an error with checker {0} in app {1}".format(checker, filename))
  else: 
    wasCallGraphError = False
    for line in checkerResult.stderr.decode('utf-8').splitlines():
      print(line)
      if line.strip() == "[main] ERROR soot.jimple.infoflow.android.SetupApplication - Could not construct callgraph":
        wasCallGraphError = True
        callgraphErrorCount = callgraphErrorCount + 1
        print('callgraph error')
    if not wasCallGraphError:
      print('there was an error running {0} on {1}'.format(checker, filename))



with open('rerunFDroidCheckResults.txt','r') as fin:
  for line in fin:
    line = line.strip()
    if line.startswith('success!'):
      lineItems = line.split(' ')
      checkerName = lineItems[5]
      appName = lineItems[-1]
      mergedName = appName + checkerName
      if not mergedName in successDict:
        successDict[mergedName] = True
    elif line.startswith('error'):
      lineItems = line.split(' ')
      checkerName = lineItems[4]
      appName = lineItems[-1]
      mergedName = appName + checkerName
      if not mergedName in errorDict:
        errorDict[mergedName] = True
    elif line.startswith('callgraph error'):
      lineItems = line.split(' ')
      appName = lineItems[-1]
      if appName in callgraphProblemDict:
        if callgraphProblemDict[appName] < 9:
          callgraphProblemDict[appName] = callgraphProblemDict[appName] + 1
      else:
        callgraphProblemDict[appName] = 1
    elif line.startswith('timeout:'):
      lineItems = line.split(' ')
      checkerName = lineItems[2]
      appName = lineItems[-1]
      mergedName = appName + checkerName
      if not mergedName in timeoutDict:
        timeoutDict[mergedName] = True
    else: 
      print('problem - missed line: {0}'.format(line))
      sys.exit(1)
print('number of successes: {0}'.format(len(successDict)))
print('number of errors: {0}'.format(len(errorDict)))
callgraphProblemCount = 0
for k in callgraphProblemDict:
  callgraphProblemCount = callgraphProblemCount + callgraphProblemDict[k]
print('number of call graph errors: {0}'.format(callgraphProblemCount))
print('number of apps with call graph errors: {0}'.format(len(callgraphProblemDict)))
print('number of timouts: {0}'.format(len(timeoutDict)))
countDict = collections.defaultdict(int)
for mergedName in successDict:
  periodLoc = mergedName.rindex('.')  
  apkName = mergedName[:periodLoc+4]
  checkerName = mergedName[periodLoc+4:]
  countDict[checkerName] += 1
for checker in countDict:
  print('{0}: {1}'.format(checker, countDict[checker]))
#for mergedName in successDict:
#  periodLoc = mergedName.rindex('.')  
#  apkName = mergedName[:periodLoc+4]
#  checkerName = mergedName[periodLoc+4:]
#  print(apkName)
#  print(checkerName)
#  #if checkerName != "DetectIncorrectGetActivityMain":
#  #  runChecker(checkerName, apkName)
#  #  print('app name: {0}, checker name: {1}'.format(apkName, checkerName))
#  #  input('press enter to continue')
#for mergedName in timeoutDict:
#  periodLoc = mergedName.rindex('.')  
#  apkName = mergedName[:periodLoc+4]
#  checkerName = mergedName[periodLoc+4:]
#  print(apkName)
#  print(checkerName)