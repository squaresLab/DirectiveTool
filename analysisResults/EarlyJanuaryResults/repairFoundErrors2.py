#!/usr/local/bin/python3

import subprocess
import shlex
import os
import shutil
import sys
import random
import timeout_decorator
import re


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import extractRepoInfo
import utilitiesForRepair

#TODO: I should probably move the functions that these two files share - doesn't make
#sense to keep them in the runInjectionTests file when both need them
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'injectFaultsDir'))
import runInjectionTests

#This file was copied from runInjectionTests - changing it so I can fix the found errors

getRepoFolderCommand =  shlex.split('git rev-parse --show-toplevel')
copyRepoLocation = '/Users/zack/git/DirectiveTool/analysisResults/EarlyJanuaryResults/tempRepoForRepair/'
#I may need to convert them to using gradlew instead of gradle wrapper
#buildAppCommand = shlex.split('gradle wrapper assembleDebug')
#testAppCommand = shlex.split('gradle wrapper test')
errorListLocation = '/Users/zack/git/DirectiveTool/analysisResults/EarlyJanuaryResults/optionsMenuCheckerResults.txt'
#errorListLocation = '/Users/zack/git/DirectiveTool/analysisResults/EarlyJanuaryResults/inflateCheckerResults.txt'
fDroidRepoDir = '/Users/zack/git/reposFromFDroid/'
attemptedAPKsFile = '/Users/zack/git/DirectiveTool/analysisResults/EarlyJanuaryResults/triedFixes.txt'

def extractErrorList(fileToExtractFrom):
  errorList = []
  with open(fileToExtractFrom,'r') as fin:
    for line in fin:
      print('read line: {0}'.format(line))
      if line.startswith('success!'):
        print('found success line!!!!')
        lineItems = line.split()
        apkName = lineItems[-1]
        checkerName = lineItems[5]
        errorList.append((checkerName, apkName))
  return errorList

def filterErrorList(checkersList, alreadyTestedAPKsDict, errorList):
  newErrorList = []
  for e in errorList:
    if len(checkersList) > 0 and ((checkersList[0] == 'all' or e[0] in checkersList)):
      if not e[1] in alreadyTestedAPKsDict:
        newErrorList.append(e)
  return newErrorList

def changeToRepoAndCommit(repoName, commitHash):
  #download the repo folder if required and move to the repo folder
  #returns the downloaded repo directory if the repository was successfully downloaded
  #and the git commit change worked. Returns None otherwise (on error)

  #first try to get the name of the folder and see if it is already downloaded
  originalDir = os.getcwd()
  if os.path.basename(repoName) == '':
    folderNameItems = repoName.split(os.path.sep)
    itemsBack = 1
    folderName = ''
    while folderName == '':
      folderName = folderNameItems[-itemsBack]
      itemsBack += 1
  else:
    folderName = os.path.basename(repoName).split('.')[0]
  if folderName == '': 
    print('unable to get folder name from repo name: {0}'.format(repoName))
    return None
  repoDir = os.path.join(fDroidRepoDir, folderName) 
  print("original source code folder: {0}".format(repoDir))
  if repoDir == fDroidRepoDir:
    print('invalid repo directory')
    print('original repo name: {0}'.fromat(repoName))
    return None
  if os.path.exists(repoDir):
    os.chdir(repoDir)
  else:
    #if the folder is not already downloaded, download it.
    os.chdir(fDroidRepoDir)
    if repoName.count('http') > 1:
      repoItems = repoName.split('http')
      for r in repoItems:
        if 'git' in r:
          repoName = 'http' + r
          break
    gitCloneCommand = shlex.split('git clone {0}'.format(repoName))
    cloneResult = subprocess.run(gitCloneCommand,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if cloneResult.returncode == 1:
      print('unable to clone {0}'.format(repoName))
      os.chdir(originalDir)
      return None
    else:
      folderName = None
      for line in cloneResult.stdout.decode('utf-8').splitlines():
        if line.startswith('fatal: destination path'):
          folderNameString = line.split(' ')[3]
          folderName = re.findall(r"'([^']*)'", folderNameString)[0]
          print('found folder name: {0}'.format(folderName))
        elif line.startswith('fatal:'):
          #handle the case when an error occurs in the middle of downloading
          #- just skip this one
          folderName = None
          print(line)
          return None
        if line.startswith('Cloning into'):
          folderNameString = line.split(' ')[2]
          folderName = re.findall(r"'([^']*)'", folderNameString)[0]
          print('found folder name: {0}'.format(folderName))
        print('line: {0}'.format(line))  
      if folderName is None:
        print(cloneResult.stdout.decode('utf-8').splitlines())
        print('unable to find folder name for repo: {0}'.format(repoName))
        print('already tried repo dir: {0}'.format(repoDir))
        print("repo doesn't exist, so I am skipping this one")
        repoCount +=1
        print(repoName, file=fout)
        return None
      else:
        repoDir = os.path.join(fDroidRepoDir, folderName)
  os.chdir(repoDir)
  resetCommitCommand = shlex.split('git reset --HARD {0}'.format(commitHash))
  commitResult = subprocess.run(resetCommitCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  os.chdir(originalDir)
  if commitResult.returncode == 1:
    for line in combyProcess.stdout.decode('utf-8').splitlines():
      print(line)
      return None
  else:
    print('commit reset succeeded')
    return repoDir

def copyRepo(repoDir, copyLocation, debuggingResultList):
  if os.path.exists(copyLocation):
    shutil.rmtree(copyLocation)
  try:
    shutil.copytree(repoDir, copyLocation)
    return True
  except:
    debuggingResultList.append('problem copying repo: {0} to {1}'.format(repoDir, copyLocation))
    print('problem copying repo: {0} to {1}'.format(repoDir, copyLocation))
    return False

def main():
  #get the errors from the error file
  #get the applications that I can find repos for
  #change the repos to the right commit
  #run the checker to confirm the error
  #try to fix the error
  #run the checker to make sure the error went away 

  #the checkers to run the repairs for; allows only running the repair on 
  #specific checkers; use 'all' if you want to run on all cases
  #checkersList = ['DetectMissingSetHasOptionsMenu']
  #checkersList = ['DetectIncorrectGetActivityMain','DetectInvalidInflateCallMain']
  checkersList = ['DetectMissingOptionsMenuDefinition']
  errorList = extractErrorList(errorListLocation)
  print('error list size: {0}'.format(len(errorList)))

  debuggingResultList = []
  originalDir = os.getcwd()
  errorCount = 0
  totalAttemptedFixCount = 0
  totalSuccessfulRepairCount = 0
  workingReposDict = {}
  reposInFileAreFullPaths = False
  successfullyFixedRepoSet = set()

  apkSourceInfo = extractRepoInfo.extractRepoInfo()
  apkInfoDict = {}
  skippedBecauseOfBuildCount = 0
  for a in apkSourceInfo:
    #convert a list of appBaseName, repoName, commitHash to a dict
    #with key appBaseName and value repoName, commitHash 
    apkInfoDict[a[0]] = (a[1], a[2])

  folderInfoDict = {}

  attemptedAPKsDict = {}
  if os.path.exists(attemptedAPKsFile):
    with open(attemptedAPKsFile,'r') as fin:
      for line in fin:
        line = line.strip()
        #allow commenting out of lines
        if not line.startswith('#'):
          attemptedAPKsDict[line.strip()] = True

  errorList = filterErrorList(checkersList, attemptedAPKsDict, errorList)
  utilitiesForRepair.setJavaEnvironmentVariable()

  with open(attemptedAPKsFile,'a') as fout:
    print('errors to check count: {0}'.format(len(errorList)))
    for checkerName, apkName in errorList:
      debuggingResultList.append((checkerName, apkName))
      print('{0} error Item: {1}'.format(errorCount, (checkerName, apkName)))
      apkBasename = extractRepoInfo.extractAPKBasename(apkName)
      try:
        repoName, commitHash = apkInfoDict[apkBasename]
      except KeyError as k:
        print(k)
        print('original apkName: {0}'.format(apkName))
        print('unable to find repo for basename: {0}'.format(apkBasename))
        print('length of apkInfoDict: {0}'.format(len(apkInfoDict)))
        print('there is probably no source for the application')
        print(apkName, file=fout)
        errorCount +=1
        debuggingResultList.append('unable to find in apkInfoDict - no source for apk')
        #input('stop to see this case')
        continue 
      repoDir = changeToRepoAndCommit(repoName, commitHash)
      if repoDir is None:
        print('had an error changing to the right repo and commit')
        errorCount += 1
        print(apkName, file=fout)
        #input('stop before moving to next repo')
        continue
      wasSuccessful = copyRepo(repoDir, copyRepoLocation, debuggingResultList)
      if not wasSuccessful:
        print('error copying repo')
        errorCount += 1
        print(apkName, file=fout)
        #input('stop before moving to next repo')
        continue
      utilitiesForRepair.clearAPKS(copyRepoLocation)
      appBuilds = utilitiesForRepair.buildApp(copyRepoLocation, apkBasename)
      if len(appBuilds) < 1:
        print('there was a problem building the app. Aborting before injecting problem.')
        debuggingResultList.append("couldn't build the app")
        #print(repoDir, file=fout)
        errorCount += 1
        skippedBecauseOfBuildCount += 1
        print("skipped because of build count: {0} ({1})".format(skippedBecauseOfBuildCount, (skippedBecauseOfBuildCount/errorCount)))
        print(apkName, file=fout)
        #input('stop before moving to next repo')
        continue
      else: 
        attemptedFixCount, successfulRepairCount, repairedApps, debuggingResultList = runInjectionTests.tryToRepairApps(checkerName, appBuilds, debuggingResultList, copyRepoLocation, repoDir)
        if attemptedFixCount < 1:
          print('never tried to fix any of the applications')
          debuggingResultList.append('never tried to fix any of the apps - was unable to find the problem with the checker or found too many problems after injecting the problem')
          #input('stopping to debug never attempted case')
        elif len(repairedApps) < 1:
          print('was never able to repair an app')
          debuggingResultList.append('was never able to successfully repair an app')
        else:
          input('stopping to see successful fix case for {0} with checker {1}'.format(apkName, checkerName))
          #I'm not sure if running the tests should be before or after running the checker
          #to see if the application contains an error - I don't think it matters, but I'll
          #have to test it and see

          #the tests are for the whole repo, so not app specific
          if runInjectionTests.getTestResultsOfRepo(copyRepoLocation):
            print('passed tests')
            debuggingResultList.append('the application was completely repaired!')
            print('fixed repo: {0}'.format(repoDir))
            successfullyFixedRepoSet.add(repoDir)
            input('stopping to see the successful fix!!')
                  #input('stopping to see checker result after injecting error')
                        #run the automated fix on this application

                  #run checker on the new app
          else:
            debuggingResultList.append('the tests failed after trying to repair the app/apps')
            print('failed tests')
        totalAttemptedFixCount += attemptedFixCount
        totalSuccessfulRepairCount += successfulRepairCount

      #input('stop before moving to next repo')
      errorCount +=1
      print('number of checked errors: {0}'.format(errorCount))
      print(apkName, file=fout)

    #input('checking result')
  for line in debuggingResultList:
    print(line)
  print('that was all the repos!')
  print('tested {0} repos'.format(errorCount))
  print('attempted to fix {0} apps'.format(totalAttemptedFixCount))
  print('successful fix count: {0}'.format(totalSuccessfulRepairCount))
  print('successfully fixed repos: {0}'.format(successfullyFixedRepoSet))
  

if __name__ == "__main__":
  main()