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
import runAllRepairs
import extractRepoInfo

getRepoFolderCommand =  shlex.split('git rev-parse --show-toplevel')
copyRepoLocation = '/Users/zack/git/DirectiveTool/injectFaultsDir/tempRepoForRepair/'
#I may need to convert them to using gradlew instead of gradle wrapper
buildAppCommand = shlex.split('gradle wrapper assembleDebug')
testAppCommand = shlex.split('gradle wrapper test')
runCheckerTemplate = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=56329:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar analysis.{0} {1}'
fDroidRepoDir = '/Users/zack/git/reposFromFDroid/'
fileWithErrorList = '/Users/zack/git/DirectiveTool/analysisResults/EarlyJanuaryResults/rerunFDroidCheckResults.txt'

finishedRepoSaveFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/finishedRepairRepos.txt'

#TODO: eventually combine many of the similar methods with runInjectionTest.py 
#since many of the methods were copied from there

class InjectionDispatch:
  def __init__(self, checkerName, getPossibleInjectionSites, injectIssue):
    self.checkerName = checkerName
    self._getPossibleInjectionSites = getPossibleInjectionSites
    self._injectIssue = injectIssue

  def getPossibleInjectionSites(self, dirName):
    return self._getPossibleInjectionSites(dirName)

  def injectIssue(self, dirName):
    return self._injectIssue(dirName)


def getTestResultsOfRepo(repoDir):
  originalDir = os.getcwd()
  os.chdir(repoDir)
  testResult = subprocess.run(testAppCommand, capture_output=True)
  testsSucceeded = False
  if testResult.returncode == 0:
    print('tests succeeeded!')
    for line in testResult.stdout.decode('utf-8').splitlines():
      print(line)
    testsSucceeded = True
  else:
    print('tests failed')
  #input('stopping to see test results')
  os.chdir(originalDir)
  return testsSucceeded

def buildApp(repoDir):
  os.chdir(repoDir)
  buildResult = subprocess.run(buildAppCommand, capture_output=True)
  for line in buildResult.stdout.decode('utf-8').splitlines():
    print(line)
  possibleBuildFiles = []
  buildFilesToCheck = []
  for root, dirs, files in os.walk(copyRepoLocation, topdown=False):
    for f in files:
      if f.endswith('.apk'):
        possibleBuildFiles.append(os.path.join(root,f))
  if len(possibleBuildFiles) < 1:
    print('error: no successful builds')
    #input('stopping to inspect the error')
  elif len(possibleBuildFiles) > 1:
    for b in possibleBuildFiles:
      if 'x86_64' in b:
        buildFilesToCheck.append(b)
    if len(buildFilesToCheck) < 1:
      for b in possibleBuildFiles:
        if 'universal' in b:
          buildFilesToCheck.append(b)
    if len(buildFilesToCheck) < 1:
      for b in possibleBuildFiles:
        if 'debug' in b:
          buildFilesToCheck.append(b)
    if len(buildFilesToCheck) < 1:
      print('error: unable to find a valid build')
      print('builds:')
      for b in possibleBuildFiles:
        print(b)
      input('stopping to check error')
  else:
    buildFilesToCheck.append(possibleBuildFiles[0])
  return buildFilesToCheck

def clearAPKS(dir):
  for root, dirs, files in os.walk(copyRepoLocation, topdown=False):
    for f in files:
      if f.endswith('.apk'):
        os.remove(os.path.join(root,f))



def filterRepoInitializer(containsFileOfInterestMethod):
  def findPossibleInjectionRepos(possibleRepoList):
    reposOfInterest = [r for r in possibleRepoList if containsFileOfInterestMethod(r)]
    return reposOfInterest 
  return findPossibleInjectionRepos
 
def injectInRepoInitializer(injectIssueMethod):
  def injectInRepo(repoDir):
    javaFiles = []
    for root, dirs, files in os.walk(repoDir, topdown=False):
      for f in files:
        if f.endswith('.java'):
          fullFilename = os.path.join(root,f)
          javaFiles.append(fullFilename)
    random.shuffle(javaFiles)
    for fullFilename in javaFiles:
      if injectIssueMethod(fullFilename):
        print('changed: {0}'.format(fullFilename))
        #input('stop for a change. Press enter to continue')
        break
  return injectInRepo

def injectInRepoWithDirectoriesInitializer(injectIssueMethod):
  def injectInRepoWithDirectories(repoDir):
    javaFiles = []
    for root, dirs, files in os.walk(repoDir, topdown=False):
      for f in files:
        if f.endswith('.java'):
          fullFilename = os.path.join(root,f)
          javaFiles.append(fullFilename)
    random.shuffle(javaFiles)
    for fullFilename in javaFiles:
      if injectIssueMethod(fullFilename):
        print('changed: {0}'.format(fullFilename))
        #input('stop for a change. Press enter to continue')
        break
  return injectInRepo

def runTestOfApp(checkerName, app, debuggingResultList):
  debuggingResultList.append('testing application: {0}'.format(app))
  checkerCommand = shlex.split(runCheckerTemplate.format(checkerName, app))
  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  fileWithProblem = None
  isAppToFix = False
  for line in checkerResult.stdout.decode('utf-8').splitlines():
    print(line)
    line = line.strip()
    if line.startswith('total') and not line.startswith('total time'):
      errorCount = int(line.split()[-1])
      if errorCount > 0:
        if errorCount == 1:
          debuggingResultList.append(line)
          isAppToFix = True
        else:
          debuggingResultList.append('found too many errors in application')
          print('found too many errors - currently unable to repair multiple errors in an application')
          print(line)
          print('found {0} errors in app'.format(errorCount))
      else:
        debuggingResultList.append('found no errors in application')
        print('found no errors in the application')
    elif line.startswith('@@@@@'):
      #classWithProblemWithFullNamespace = 
      lineItems = line.split()
      classWithProblemWithFullNamespace = None
      print('found line with problem')
      print(line)
      #I think I can change previous logic to only checking the last word in the
      #line, but I'll leave it here in case I need to revert
      for l in lineItems:
        periodCount = 0
        for c in l:
          if c == '.':
            periodCount += 1
            if periodCount > 1:
              classWithProblemWithFullNamespace = l
              break
        if classWithProblemWithFullNamespace:
          break
      if classWithProblemWithFullNamespace: 
        fileWithProblem = '{0}.java'.format(classWithProblemWithFullNamespace.split('.')[-1])
  if not isAppToFix:
    debuggingResultList.append('never found problem to fix')
  #only print out the file problem if the problem was found because the 
  #case where they both occur is obvious and add unnecessary print statements
  else:
    if fileWithProblem is None:
      debuggingResultList.append('never found file with problem')
      #for line in checkerResult.stdout.decode('utf-8').splitlines():
      #  print(line)
      #input('stopping to see this case')
  return isAppToFix, fileWithProblem, debuggingResultList

def tryToRepairApps(checkerName, appBuilds, debuggingResultList):
  attemptedFixCount = 0
  successfulRepairCount = 0
  repairedApps = []
  for app in appBuilds:
    currentChecker = checkerName
    os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
    isAppToFix, fileWithProblem, debuggingResultList = runTestOfApp(checkerName, app, debuggingResultList)
    if isAppToFix:
      attemptedFixCount += 1
      try:
        repairResult = runAllRepairs.runRepairOptions(currentChecker, app, fileWithProblem, copyRepoLocation)
      except timeout_decorator.TimeoutError as t:
        repairResult = None
      if repairResult:
        getTestResultsOfRepo(runAllRepairs.testDir)
        print('!!!! Succeeded !!!!')
        successfulRepairCount += 1
        repairedApps.append(app)
    else:
      print('ran checker but did not find the right number of errors')
  return attemptedFixCount, successfulRepairCount, repairedApps, debuggingResultList

def extractErrorList(fileToExtractFrom):
  errorList = []
  with open(fileToExtractFrom,'r') as fin:
    for line in fin:
      if line.startswith('success!'):
        lineItems = line.split()
        apkName = lineItems[-1]
        checkerName = lineItems[5]
        errorList.append((checkerName, apkName))
  return errorList



def main():
  #repos that had a problem - first one never copies because of too many symbolic
  #links, second one is getting no file found error
  reposToSkip = ['/Users/zack/git/reposFromFDroid/sdl_android', '/Users/zack/git/reposFromFDroid/ingress-intel-total-conversion']
  errorList = extractErrorList(fileWithErrorList)
  #I could probably go back and refactor extractRepoInfo to only return
  #what I need in the format that I need, but I'm not going to worry about it 
  #right now
  apkSourceInfo = extractRepoInfo.extractRepoInfo()
  apkInfoDict = {}
  for a in apkSourceInfo:
    if 'mindustry' in a[0]:
      print(a[0])
    apkInfoDict[a[0]] = (a[1],a[2])

  #setContentView 
  debuggingResultList = []
  

  originalDir = os.getcwd()
  #for file in injectorInstance.getPossibleInjectionSites(fDroidRepoDir):
    #os.chdir(os.path.dirname(file))
    #result = subprocess.run(getRepoFolderCommand, capture_output=True)
    #print('@@@starting output of interest')
    #if result.returncode == 0:
      #repoDir = result.stdout.decode('utf-8').strip()
  repoCount = 0
  attemptedFixCount = 0
  successfulRepairCount = 0
  print('error list size: {0}'.format(len(errorList)))
  #eventually I might want to change this from finished repos to finished application
  #errors. The apk can not have a repo, and then the app test fails and is not recorded
  #because I don't have a repo to record
  finishedReposDict = {}
  if os.path.exists(finishedRepoSaveFile):
    with open(finishedRepoSaveFile, 'r') as fin:
      for line in fin:
        finishedReposDict[line.strip()] = True
  with open(finishedRepoSaveFile,'a') as fout:
    for foundErrorItem in errorList:
      checkerName = foundErrorItem[0]
      apkName = foundErrorItem[1]
      try:
        apkItems = os.path.basename(apkName).split('_')[:-1]
        reducedApkName = '_'.join(apkItems)
        #if '.' in reducedApkName:
        #  reducedApkName = reducedApkName.split('.')[-1]
        repoName,commitHash = apkInfoDict[reducedApkName]
      except KeyError as k:
        print(k)
        print('original apkName: {0}'.format(apkName))
        print('unable to find repo for app: {0}'.format(apkName))
        print('there is probably no source for the application')
        print(repoName, file=fout)
        repoCount +=1
        continue
      if repoName in finishedReposDict or not 'git' in repoName:
        print(repoName, file=fout)
        repoCount +=1
        print('either repo is already checked or it\'s not a git repo')
        continue
      #download the repo folder if required and move to the repo folder
      if os.path.basename(repoName) == '':
        folderNameItems = repoName.split(os.path.sep)
        itemsBack = 1
        folderName = ''
        while folderName == '':
          folderName = folderNameItems[-itemsBack]
          itemsBack += 1
      else:
        folderName = os.path.basename(repoName).split('.')[0]
      #the added git check 
      #if folderName == 'https://archive.softwareheritage.org/browse/origin/https://android-cmis-browser.googlecode.com/hg//directory/':
      #  continue
      #else:
      if folderName == '': 
        print('unable to get folder name from repo name: {0}'.format(repoName))
        sys.exit(1)
      repoDir = os.path.join(fDroidRepoDir, folderName) 
      if repoDir == fDroidRepoDir:
        print('invalid repo directory')
        print('original repo name: {0}'.fromat(repoName))
        sys.exit(1)
      if os.path.exists(repoDir):
        os.chdir(repoDir)
      else:
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
          sys.exit(1)
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
              break
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
            continue
          else:
            repoDir = os.path.join(fDroidRepoDir, folderName)
            os.chdir(repoDir)
      #stopping here to go eat
      debuggingResultList.append(repoDir)
      gitCommitChangeCommand = shlex.split('git reset --hard {0}'.format(commitHash))
      gitCommitChangeResult = subprocess.run(gitCommitChangeCommand)
      if gitCommitChangeResult.returncode == 1:
        print('commit hash: {0} failed for repo {1}'.format(commitHash, repoName))
        sys.exit(1)
      print('repoDir: {0}'.format(repoDir))
      if repoDir in reposToSkip:
        print('repo in repos to skip - skipping: {0}'.format(repoName))
        print(repoName, file=fout)
        repoCount +=1
        continue
      if os.path.exists(copyRepoLocation):
        shutil.rmtree(copyRepoLocation)
      try:
        shutil.copytree(repoDir, copyRepoLocation)
      except Exception as e:
        print('repo dir: {0}'.format(repoDir))
        print('copy repo location: {0}'.format(copyRepoLocation))
        print(e)
        print('error copying the repo - skipping this one')
        print(repoName, file=fout)
        repoCount +=1
        continue
      clearAPKS(copyRepoLocation)
      appBuilds = buildApp(copyRepoLocation)
      if len(appBuilds) < 1:
        print('there was a problem building the app. Aborting before injecting problem.')
        debuggingResultList.append("couldn't build the app")
        repoCount +=1
        print(repoName, file=fout)
        continue
      else: 
        #see if the application already has a problem - if so, we don't need to inject anything.
        newAttemptedFixCount, newSuccessfulRepairCount, repairedApps, debuggingResultList = tryToRepairApps(checkerName, appBuilds, debuggingResultList)
        if attemptedFixCount > 0:
          debuggingResultList.append('found a problem in the original app')
          if newSuccessfulRepairCount:
            debuggingResultList.append('was able to repair a problem in the original app')
        else:
          print('was unable to find an error to repair in any of the apps in the repo')
          print(repoName, file=fout)
          repoCount +=1
          continue
      if newAttemptedFixCount < 1:
        debuggingResultList.append('never tried to fix any of the apps - was unable to find the problem with the checker after injecting the problem')
      elif len(repairedApps) < 1:
        debuggingResultList.append('was never able to successfully repair an app')
      else:
        #I'm not sure if running the tests should be before or after running the checker
        #to see if the application contains an error - I don't think it matters, but I'll
        #have to test it and see

        #the tests are for the whole repo, so not app specific
        if getTestResultsOfRepo(copyRepoLocation):
          print('passed tests')
          debuggingResultList.append('the application was completely repaired!')
          input('stopping to see repair for application/s {0}'.format(repairedApps))
              #input('stopping to see checker result after injecting error')
                    #run the automated fix on this application

              #run checker on the new app
        else:
          debuggingResultList.append('the tests failed after trying to repair the app/apps')
          print('failed tests')
      attemptedFixCount += newAttemptedFixCount
      successfulRepairCount += newSuccessfulRepairCount
      repoCount +=1
      print('number of checked repos: {0}'.format(repoCount))
      print(repoName, file=fout)

      #input('checking result')
  for line in debuggingResultList:
    print(line)
  print('that was all the repos!')
  print('attempted to fix {0} apps'.format(attemptedFixCount))
  print('successful fix count: {0}'.format(successfulRepairCount))
  

if __name__ == "__main__":
  main()