#!/usr/local/bin/python3

import os
import sys
import subprocess
import traceback
import re
import time

metadataDir = '/Users/zack/git/fdroiddata/metadata/'
appsDir = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
reposDir = '/Users/zack/git/reposFromFDroid/'

problematicFilesToSkip = {'pt.isec.tp.am.yml':True, 'tk.elevenk.dailybread.yml':True,
   'com.funambol.androidsync.txt':True, 'to.doc.android.ipv6config.yml': True, 
   'org.sixgun.ponyexpress.yml': True, 'remuco.client.android.yml': True,
   'org.wikimedia.commons.muzei.yml': True, 'ru.o2genum.coregame.yml': True,
   'org.scoutant.cc.yml': True, 'ru.glesik.nostrangersms.yml': True, 
   'org.androhid.txt': True, 'org.systemcall.scores.yml': True, 
   'com.agiro.scanner.android.txt': True}

def findRepoInfo(repoInfoList, repoUrl):
  for packageBaseName, repoName, commitHash in repoInfoList:
    if repoName == repoUrl:
      print('found with equals')
      return packageBaseName, repoName, commitHash
  #I'm hoping the first check will work but I'm adding the second check in 
  #case this doesn't. This method clearly isn't optimized, but I can do that 
  #later
  for packageBaseName, repoName, commitHash in repoInfoList:
    if repoName in repoUrl:
      print('found with contains')
      return packageBaseName, repoName, commitHash
  return None

repoInfoList = []
repoCount = 0
for file in os.listdir(metadataDir):
  foundCommit = False
  foundRepo = False
  foundSourceLoc = False
  foundCurrentVersion = False
  sourceLocation = None
  currentVersion = None
  print('{0}: extracting from - {1}'.format(repoCount, file))
  repoCount = repoCount + 1
  if file.endswith('.yml') or file.endswith('.txt'):
    fullFilename = os.path.join(metadataDir, file)
    with open(fullFilename) as fin:
      for line in fin:
        line = line.strip()
        if not foundRepo and line.startswith('Repo:'):
          repoName = line.split(' ')[-1]
          foundRepo = True
        elif not foundSourceLoc and (line.startswith('SourceCode:') or line.startswith('Source Code:')):
          foundSourceLoc = True
          sourceLocation = line.split(' ')[-1]
        if not foundCommit:
          if line.startswith('commit:'):
            foundCommit = True
            commitHash = line.split(' ')[-1]
          elif line.startswith('commit='):
            foundCommit = True
            commitHash = line.split('=')[-1]
        if not foundCurrentVersion:
          if line.startswith('Current Version:'):
            currentVersion = line.split(':')[-1]
            foundCurrentVersion = True
          elif line.startswith('CurrentVersion:'):
            currentVersion = line.split(':')[-1]
            foundCurrentVersion = True
        #if the repo is specifically labeled, try to get it from the source 
        #location label instead
        if foundCommit and foundRepo:
          break
      if not foundRepo:
        if sourceLocation:
          repoName = sourceLocation
          foundRepo = True
      if not foundCommit:
        if foundCurrentVersion:
          commitHash = currentVersion
          foundCommit = True
    if not file in problematicFilesToSkip:
      if not foundCommit or not foundRepo:
        print('there was an error with file {0}: unable to find repo or commit'.format(fullFilename))
        if not foundCommit: 
          print('commit was not found')
        if not foundRepo:
          print('repo was not found')
        commandList = ['open', '-a', "Sublime Text", fullFilename]
        subprocess.call(commandList)
        sys.exit(1)
      else:
        packageBaseName = file[:-4]
        if repoName.startswith('Repo:'):
          repoItems = repoName.split(':')
          repoName = ':'.join(repoItems[1:])
        if repoName.startswith('Code:'):
          repoItems = repoName.split(':')
          repoName = ':'.join(repoItems[1:])
        repoInfoList.append((packageBaseName,repoName, commitHash))
#first look into the packages in the app list and see how many repos match
#create hash of the packageBaseNames
packageDict = {}
for packageBaseName, repoName, commitHash in repoInfoList:
  packageDict[packageBaseName] = False
#check if appBaseName is in the hash
foundCount = 0
missedCount = 0
originalAppCount = 0
for file in os.listdir(appsDir):
  if not file.startswith('.'):
    originalAppCount = originalAppCount + 1
    appBaseName = file.split('_')[0]
    if appBaseName in packageDict:
      #do the real work here later
      packageDict[appBaseName] = True
      foundCount = foundCount + 1
      pass
    else:
      missedCount = missedCount + 1
      print('unable to find {0} in the list of packages'.format(appBaseName))
print('found: {0}'.format(foundCount))
print('missed: {0}'.format(missedCount))
originalDir = os.getcwd()
buildErrorCount = 0
buildSuccessCount = 0
buildExceptionCount = 0

packageRepos = os.listdir(reposDir)
successCount = 0
failedCount = 0
totalCount = 0
skippedCount = 0
foundCount = 0
foundList = []
for repo in packageRepos:
  dirForTests = os.path.join(reposDir, repo)
  if os.path.isdir(dirForTests):
    os.chdir(dirForTests)
    #test checkout
    getRepoNameCommand = ['git', 'config', '--get', 'remote.origin.url']
    repoCommandResult = subprocess.run(getRepoNameCommand,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    if repoCommandResult:
      for line in repoCommandResult.stdout.decode('utf-8').splitlines():
        line = line.strip()
        repoUrl = line
      repoInfo = findRepoInfo(repoInfoList, repoUrl)
      changeCommitCommand = ['git', 'reset', '--hard', repoInfo[2]]
      commitChangeResult = subprocess.run(changeCommitCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
      for line in commitChangeResult.stdout.decode('utf-8').splitlines():
        line = line.strip()
        print(line)
      gradleCommandList = ['gradle', 'wrapper','assembleDebug']
      checkerResult = subprocess.run(gradleCommandList, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
      print('gradle return result: {0}'.format(checkerResult.returncode))
      if checkerResult.returncode == 0:
        buildSuccessCount = buildSuccessCount + 1
        didBuildSucceed = True
      else:
        buildErrorCount = buildErrorCount + 1
        didBuildSucceed = False
      if didBuildSucceed:
        testCommand = ['gradle', 'wrapper', 'test']
        testResult = subprocess.run(testCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        for line in testResult.stdout.decode('utf-8').splitlines():
          line = line.strip()
          if line.startswith("BUILD SUCCESSFUL"):
            successCount = successCount + 1
            #print('had to skip {0} to find one that works'.format(skippedCount))
            #input('found success with {0} - press enter to continue'.format(dirForTests))
            foundCount += 1
            foundList.append(repo)
          elif line.startswith("BUILD FAILED"):
            failedCount = failedCount + 1
        print(line)
      skippedCount += 1
    else:
      print('failed to find {0} in the repo list, with url {1}'.format(repo, repoUrl))
print('successful repos:')
for r in foundList:
  print(r)
print('successes found: {0}'.format(foundCount))
print('repos skipped: {0}'.format(skippedCount))

    #test out gradle test
    #testCommand = ['gradle', 'wrapper', 'test']
    #testResult = subprocess.run(testCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    #for line in testResult.stdout.decode('utf-8').splitlines():
    #  line = line.strip()
    #  if line.startswith("BUILD SUCCESSFUL"):
    #    successCount = successCount + 1
    #    input('found success with {0} - press enter to continue'.format(dirForTests))
    #  elif line.startswith("BUILD FAILED"):
    #    failedCount = failedCount + 1
    #  print(line)
    #totalCount = totalCount + 1
    #print('|{0}|'.format(repo))
    #print('success count: {0}'.format(successCount))
    #print('failed count: {0}'.format(failedCount))
    #print('total count: {0}'.format(totalCount))
    #print('results for: {0}'.format(dirForTests))
    #input('press enter to continue')
    #time.sleep(0.5)


  #os.chdir(repo)
#for packageBaseName, repoName, commitHash in repoInfoList:

  #try:
  #  if packageDict[packageBaseName]:
  #    os.chdir(reposDir)
  #    downloadCommandList = ['git','clone',repoName]
  #    print('executing: {0}'.format(' '.join(downloadCommandList)))
  #    checkerResult = subprocess.run(downloadCommandList, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  #    folderName = None
  #    for line in checkerResult.stdout.decode('utf-8').splitlines():
  #      if line.startswith('fatal: destination path'):
  #        folderNameString = line.split(' ')[3]
  #        folderName = re.findall(r"'([^']*)'", folderNameString)[0]
  #        print('found folder name: {0}'.format(folderName))
  #      if line.startswith('Cloning into'):
  #        folderNameString = line.split(' ')[2]
  #        folderName = re.findall(r"'([^']*)'", folderNameString)[0]
  #        print('found folder name: {0}'.format(folderName))
  #      print('line: {0}'.format(line)) 
  #    if folderName:
  #      os.chdir(folderName)
  #      gradleCommandList = ['gradle', 'wrapper','assembleDebug']
  #      checkerResult = subprocess.run(gradleCommandList, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  #      print('gradle return result: {0}'.format(checkerResult.returncode))
  #      if checkerResult.returncode == 0:
  #        buildSuccessCount = buildSuccessCount + 1
  #      else:
  #        buildErrorCount = buildErrorCount + 1
  #      print('current build success count: {0}'.format(buildSuccessCount))
  #      print('current build error count: {0}'.format(buildErrorCount))
  #      print('current build exception count: {0}'.format(buildExceptionCount))
  #      print('current total: {0}'.format(buildSuccessCount + buildErrorCount + buildExceptionCount))
  ##for line in checkerResult.stdout.decode('utf-8').splitlines():
  #      #  print(line)
  #      os.chdir(reposDir) 
  #except BaseException as e:
  #    print('error: {0}'.format(str(e)))
  #    traceback.print_exc()
  #    buildExceptionCount = buildExceptionCount + 1
  #    #result = input('press enter to try the next repo or q to quit')
  #    #if result == 'q':
      #  sys.exit(0)
#print('final build success count: {0}'.format(buildSuccessCount))
#print('final build error count: {0}'.format(buildErrorCount))

    #input('')

  #try to go to git and download the repos
  #change to the commit hash


