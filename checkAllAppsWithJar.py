#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import time
import subprocess
import os
import sys
import shutil
import random
import math
import shlex

#timeoutTime=120
#userAgentString='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'


def runChecker(fullFilename):
  jarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/MultipleJarBuild/AndroidDirectiveChecker.jar'
  runJarDir = '/Users/zack/git/DirectiveTool/FlowDroidTest' 
  #checkerCommand = ['java', '-jar', jarLocation]
  checkerCommandTemplate = 'java -jar {0} analysis.{1} {2}'
  checkerNames = ['DetectInvalidInflateCallMain','DetectIncorrectGetActivityMain',
    'DetectMissingSetHasOptionsMenu', 'DetectSetArgumentsMain',
    'DetectInvalidSetContentViewFindViewByIDOrdering', 'DetectInvalidGetResources',
    'DetectIncorrectSetInitialSavedState', 'DetectInvalidSetTheme',
    'DetectSetSelectorSetPackageProblem']
  #currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
  #fullFilename = os.path.join(currentAppFolder, filename)
  #currentCheckerCommand.append('analysis.{0}'.format(checker))
  print('testing {0}'.format(fullFilename))
  for checker in checkerNames:
    #currentCheckerCommand.append(checker)
    #currentCheckerCommand.append(fullFilename)
    checkerCommand = shlex.split(checkerCommandTemplate.format(jarLocation,checker,fullFilename))
    originalDir = os.getcwd()
    os.chdir(runJarDir)
    #debuggingCommand = currentCheckerCommand.copy()
    #debuggingCommand[1] = '"{0}"'.format(debuggingCommand[1])
    #print(' '.join(debuggingCommand))
    print('running checker: {0}'.format(checker))
    checkerResult = subprocess.run(currentCheckerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #print('-------------------------')
    #print(checkerResult.stdout.decode('utf-8'))
    #print('return code: {0}'.format(checkerResult.returncode))
    #input('')
    #checkerResult = subprocess.check_output(checkerCommand)
    os.chdir(originalDir)
    callgraphErrorCount = 0
    if checkerResult.returncode == 0:
      #print('checker result: {0}'.format(checkerResult))
      for line in checkerResult.stdout.decode('utf-8').splitlines():
      #  print('line: {0}'.format(line))
      #for line in checkerResult.stderr.decode('utf-8').splitlines():
      #  print('line: {0}'.format(line))
      #  for some reason the first line returned is processed as an integer
    #     if isinstance(line, str):
        if line.startswith('total number'):
    #         print(line)
          lineItems = line.split(' ')
          if int(lineItems[-1]) != 0:
            print("found an error with checker {0} in app {1}".format(checker, fullFilename))
            fout.write("success! error found: with checker {0} in app {1}\n".format(checker, fullFilename))
            fout.flush()
            os.fsync(fout.fileno())
            #input("stopping to let you investigate. Press enter to continue")
    else: 
      wasCallGraphError = False
      for line in checkerResult.stderr.decode('utf-8').splitlines():
        print(line)
        if line.strip() == "[main] ERROR soot.jimple.infoflow.android.SetupApplication - Could not construct callgraph":
          wasCallGraphError = True
          callgraphErrorCount = callgraphErrorCount + 1
          fout.write("callgraph error on app {0}\n".format(fullFilename))
          print('callgraph error')
      if not wasCallGraphError:
        print('there was an error running {0} on {1}'.format(checker, fullFilename))
        fout.write("error; couldn't run: checker {0} on app {1}\n".format(checker, fullFilename))
        fout.flush()
        os.fsync(fout.fileno())
#input('stopping to let you check. Press enter to continue')

def main():
  #errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrorsSecondPass.txt'
  callgraphErrorCount = 0
  analyzedApplicationCount = 0
  checkedRepos = []
  checkedErrorTuples = []
  errorTuples = []
  checkCount = 1
  currentCount = 0
  outputFileName = '/Users/zack/git/DirectiveTool/rerunFDroidResultsTemporaryTest.txt'
  apksLocation = '/Users/zack/something better'
  skippedCount = 0


  #with open(outputFileName,'r') as fin:
  #  for line in fin:
  #    line = line.strip()
  #    if line.startswith('error;'):
  #      lineItems = line.split()
  #      checkerWithError =  lineItems[4]
  #      apkWithError = lineItems[-1]
  #      checkedErrorTuples.append((checkerWithError, apkWithError))
  with open(outputFileName, 'w') as fout:
    for  root, dirs, files in os.path.walk(apkLocation)
      for f in files:
        if f.endswith('.apk'):
          fullFilename = os.path.join(root,f)
          runChecker(fullFilename)

  #with open(outputFileName,'w') as ferrOut:
  #  for file in os.listdir(currentAppFolder):
  #    filename = os.fsdecode(file)
  #    if filename.endswith(".apk"):  
  #      fullFilename = os.path.join(currentAppFolder, filename)
  #      print('{0}: running analysis on {1}'.format(analyzedApplicationCount, fullFilename))
  #      analyzedApplicationCount = analyzedApplicationCount + 1
  #      for checker in checkerNames:
  #        currentCheckerCommand = checkerCommand.copy()
  #        currentCheckerCommand.append(checker)
  #        currentCheckerCommand.append(fullFilename)
  #        originalDir = os.getcwd()
  #        os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
  #        debuggingCommand = currentCheckerCommand.copy()
  #        debuggingCommand[1] = '"{0}"'.format(debuggingCommand[1])
  #        print(' '.join(debuggingCommand))
  #        print('running checker: {0}'.format(checker))
  #        checkerResult = subprocess.run(currentCheckerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  #        #print('-------------------------')
  #        #print(checkerResult.stdout.decode('utf-8'))
  #        #print('return code: {0}'.format(checkerResult.returncode))
  #        #input('')
#           #checkerResult = subprocess.check_output(checkerCommand)
#           os.chdir(originalDir)
#           if checkerResult.returncode == 0:
#             #print('checker result: {0}'.format(checkerResult))
#             for line in checkerResult.stdout.decode('utf-8').splitlines():
#               #print('line: {0}'.format(line))
#               #for some reason the first line returned is processed as an integer
#               if isinstance(line, str):
#                 if line.startswith('total number'):
#                   print(line)
#                   lineItems = line.split(' ')
#                   if int(lineItems[-1]) != 0:
#                     print("found an error with checker {0} in app {1}".format(checker, filename))
#                     ferrOut.write("success! error found: with checker {0} in app {1}\n".format(checker, filename))
#                     ferrOut.flush()
#                     os.fsync(ferrOut.fileno())
#                     #input("stopping to let you investigate. Press enter to continue")
#           else: 
#             wasCallGraphError = False
#             for line in checkerResult.stderr.decode('utf-8').splitlines():
#               if line.strip() == "[main] ERROR soot.jimple.infoflow.android.SetupApplication - Could not construct callgraph":
#                 wasCallGraphError = True
#                 callgraphErrorCount = callgraphErrorCount + 1
#                 ferrOut.write("callgraph error on app {0}\n".format(filename))
#                 print('callgraph error')
#                 break
#             if not wasCallGraphError:
#               print('there was an error running {0} on {1}'.format(checker, filename))
#               ferrOut.write("error; couldn't run: checker {0} on app {1}\n".format(checker, filename))
#               ferrOut.flush()
#               os.fsync(ferrOut.fileno())
# #input('stopping to let you check. Press enter to continue')

#   print('number of applications downloaded/analyzed: {0}'.format(analyzedApplicationCount))
#   print('number of call graph errors: {0}'.format(callgraphErrorCount))


if __name__ == "__main__":
  main()