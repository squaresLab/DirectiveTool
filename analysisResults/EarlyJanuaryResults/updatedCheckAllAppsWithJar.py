#!/usr/bin/python3

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


def runChecker(fout, fullFilename, checkerCount):
  #jarLocation = '/Users/zfc/UnsyncedDocuments/CheckerJars/AndroidDirectiveChecker.jar'
  jarLocation = '/home/zack/runCheckerPackage/MultipleJarBuild/AndroidDirectiveChecker.jar'
  androidJarLocation = '/home/zack/runCheckerPackage/MultipleJarBuild/android.jar'
  runJarDir = '/home/zack/runCheckerPackage/' 
  #checkerCommand = ['java', '-jar', jarLocation]
  
  checkerCommandTemplate = 'java -jar {0} {1} {2} {3}'
  checkerNames = ['DetectInvalidInflateCallMain','DetectIncorrectGetActivityMain',
    'DetectMissingSetHasOptionsMenu', 'DetectSetArgumentsMain',
    'DetectInvalidSetContentViewFindViewByIDOrdering', 'DetectInvalidGetResources',
    'DetectIncorrectSetInitialSavedState', 'DetectInvalidSetTheme',
    'DetectSetSelectorSetPackageProblem']
  #currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
  #fullFilename = os.path.join(currentAppFolder, filename)
  #currentCheckerCommand.append('analysis.{0}'.format(checker))
  print('testing {0}:{1}'.format(checkerCount,fullFilename))
  for checker in checkerNames:
    #currentCheckerCommand.append(checker)
    #currentCheckerCommand.append(fullFilename)
    checkerCommand = shlex.split(checkerCommandTemplate.format(jarLocation,checker,fullFilename, androidJarLocation))
    originalDir = os.getcwd()
    os.chdir(runJarDir)
    #debuggingCommand = currentCheckerCommand.copy()
    #debuggingCommand[1] = '"{0}"'.format(debuggingCommand[1])
    #print(' '.join(debuggingCommand))
    print('running checker: {0}'.format(checker))
    try:
      checkerResult = subprocess.run(checkerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=3600)
    except:
      print('there was a timeout running {0} on {1}'.format(checker, fullFilename))
      fout.write("timeout: checker {0} on app {1}\n".format(checker, fullFilename))
      fout.flush()
      os.fsync(fout.fileno())
      continue
    #print('-------------------------')
    #print(checkerResult.stdout.decode('utf-8'))
    #print('return code: {0}'.format(checkerResult.returncode))
    #input('')
    #checkerResult = subprocess.check_output(checkerCommand)
    os.chdir(originalDir)
    callgraphErrorCount = 0
    if checkerResult.returncode == 0:
      #print('checker result: {0}'.format(checkerResult))
      checkerFoundAnError = False
      for line in checkerResult.stdout.decode('utf-8').splitlines():
        #print('line: {0}'.format(line))
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
            checkerFoundAnError = True
      if not checkerFoundAnError:
        print('checker did not find an error')
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
  outputFileName = '/home/zack/runCheckerPackage/rerunFDroidCheckResults.txt'
  finishedFileName = '/home/zack/runCheckerPackage/checkedApksForServerFailure.txt'
  apksLocation = '/home/zack/runCheckerPackage/appsFromFDroid/'
  skippedCount = 0


  #with open(outputFileName,'r') as fin:
  #  for line in fin:
  #    line = line.strip()
  #    if line.startswith('error;'):
  #      lineItems = line.split()
  #      checkerWithError =  lineItems[4]
  #      apkWithError = lineItems[-1]
  #      checkedErrorTuples.append((checkerWithError, apkWithError))
  print('starting')
  with open(outputFileName, 'a') as fout:
    with open(finishedFileName, 'a') as finishedFileHandle:
      checkerCount = 0
      for f in os.listdir(apksLocation):
        #for f in files:
        print(f)
        if f.endswith('.apk'):
          fullFilename = os.path.join(apksLocation,f)
          runChecker(fout, fullFilename, checkerCount)
          checkerCount += 1
          print(fullFilename,file=finishedFileHandle)
          finishedFileHandle.flush()
          os.fsync(finishedFileHandle.fileno())
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
