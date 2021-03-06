#!/usr/local/bin/python3

import injectGetResourcesIssue 
import injectSetThemeIssue
import injectGetActivityIssue
import injectSetInitialSavedStateProblem
import injectSetPackageSetSelectorProblem
import injectInflateAndOptionsMenuIssues
import injectSetArgumentsProblem
import injectSetContentViewIssue
import runInjectionTests
import subprocess
import shlex
import os
import shutil
import sys
import random
import timeout_decorator


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import runAllRepairs
import extractRepoInfo

copyRepoLocation = '/Users/zack/git/DirectiveTool/injectFaultsDir/tempRepoForInjection/'
#I may need to convert them to using gradlew instead of gradle wrapper
#buildAppCommand = shlex.split('gradle wrapper assembleDebug')
#testAppCommand = shlex.split('gradle wrapper test')
#permissionCommand = shlex.split('chmod +x gradlew')
#runCheckerTemplate = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=56329:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar analysis.{0} {1}'
workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/reposWithSuccessfulTests.txt'
#fDroidRepoDir = '/Users/zack/git/reposFromFDroid/'
#attemptedFoldersFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/triedInjectionFolders.txt'
successfulInjectionReposTemplate = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionRepos{0}.txt'

#reposThatCompileNames = [
#'muzei-commons',
#'Riksdagskollen',
#'TUI-ConsoleLauncher',
#'PostWriter',
#'VlcFreemote',
#'privacy-friendly-2048',
#'android-sms-gate',
#'YouTubeStream',
#'aRevelation',
#'webcom-reader',
#'giggity',
#'muzei-nationalgeographic',
#'rxdroid',
#'privacy-friendly-finance-manager',
#'Handy-News-Reader',
#'PrivacyHelper',
#'child-resus-calc',
#'bepo-android',
#'powerbutton',
#'hacs',
#'bird-monitor',
#'badge-magic-android'
#]

class InjectionDispatch:
  def __init__(self, checkerName, isPossibleInjectionRepo, injectIssue):
    self.checkerName = checkerName
    self._isPossibleInjectionRepo = isPossibleInjectionRepo
    self._injectIssue = injectIssue

  def isPossibleInjectionRepo(self, folderInfoDict, dirName):
    return self._isPossibleInjectionRepo(folderInfoDict, dirName)

  def injectIssue(self, dirName):
    return self._injectIssue(dirName)


def getTestResultsOfRepo(repoDir):
  originalDir = os.getcwd()
  os.chdir(repoDir)
  testResult = subprocess.run(runInjectionTests.testAppCommand, capture_output=True)
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
  originalDir = os.getcwd()
  os.chdir(repoDir)
  if not os.path.exists(os.path.join(repoDir, 'gradlew')):
    print('unable to find the gradle build file in directory: {0}'.format(repoDir))
    os.chdir(originalDir)
    return []
  try:
    buildResult = subprocess.run(runInjectionTests.buildAppCommand, capture_output=True)
  except PermissionError as p:
    subprocess.run(runInjectionTests.permissionCommand, capture_output=True)
    buildResult = subprocess.run(runInjectionTests.buildAppCommand, capture_output=True)
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
  os.chdir(originalDir)
  return buildFilesToCheck

def clearAPKS(dir):
  for root, dirs, files in os.walk(copyRepoLocation, topdown=False):
    for f in files:
      if f.endswith('.apk'):
        os.remove(os.path.join(root,f))

def downloadRepo(folderInfoDict, repoDir):
  downloadDir = os.path.dirname(repoDir)
  originalDir = os.getcwd()
  os.chdir(downloadDir)
  folderName = os.path.basename(repoDir)
  #print(folderInfoDict[folderName])
  gitCloneCommand = shlex.split('git clone {0}'.format(folderInfoDict[folderName][1]))
  try:
    cloneResult = subprocess.run(gitCloneCommand)
  except:
    os.chdir(orignalDir)
    return False
  os.chdir(originalDir)
  if cloneResult.returncode == 1:
    return False
  else:
    return True

#This method was originally used to filter down a list of repos to the ones
#that mattered for the injection type. Due to reordering, this is now dead code,
#but I'm leaving it here in case the logic is useful later
def filterRepoInitializer(containsFileOfInterestMethod):
  def findPossibleInjectionRepos(folderInfoDict, possibleRepoList):
    for r in possibleRepoList:
      if not os.path.exists(r):
        downloadRepo(folderInfoDict, r)
      if os.path.exists(r):
        if containsFileOfInterestMethod(r):
          yield r
    #reposOfInterest = [r for r in possibleRepoList if containsFileOfInterestMethod(r)]
    #return reposOfInterest 
  return findPossibleInjectionRepos

def isRepoOfInterestInitializer(containsFileOfInterestMethod):
  def isRepoOfInterestWrapper(folderInfoDict, possibleRepo):
    if not os.path.exists(possibleRepo):
      downloadRepo(folderInfoDict, possibleRepo)
    if os.path.exists(possibleRepo):
      if containsFileOfInterestMethod(possibleRepo):
        return True
    #reposOfInterest = [r for r in possibleRepoList if containsFileOfInterestMethod(r)]
    #return reposOfInterest 
    return False
  return isRepoOfInterestWrapper




 
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

def runTestOfApp(injectorInstance, app, debuggingResultList):
  debuggingResultList.append('testing application: {0}'.format(app))
  checkerCommand = shlex.split(runInjectionTests.runCheckerTemplate.format(injectorInstance.checkerName, app))
  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
  fileWithProblem = None
  isAppToFix = False
  for line in checkerResult.stdout.decode('utf-8').splitlines():
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
        print('found no errors in the application')
        debuggingResultList.append('found 0 errors in application')
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

def tryToRepairApps(injectorInstance, appBuilds, debuggingResultList):
  attemptedFixCount = 0
  successfulRepairCount = 0
  repairedApps = []
  print('number of app builds: {0}'.format(len(appBuilds)))
  originalDir = os.getcwd()
  for app in appBuilds:
    currentChecker = injectorInstance.checkerName
    os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
    isAppToFix, fileWithProblem, debuggingResultList = runTestOfApp(injectorInstance, app, debuggingResultList)
    if isAppToFix and fileWithProblem:
      attemptedFixCount += 1
      try:
        repairResult = runAllRepairs.runRepairOptions(currentChecker, app, fileWithProblem, copyRepoLocation)
      except timeout_decorator.TimeoutError as t:
        repairResult = None
        debuggingResultList.append('repair attempted timed out')
      if repairResult:
        getTestResultsOfRepo(runAllRepairs.testDir)
        print('!!!! Succeeded !!!!')
        successfulRepairCount += 1
        repairedApps.append(app)
    else:
      print('ran checker but did not find the right number of errors')
  print('finished try to repair apps')
  os.chdir(originalDir)
  return attemptedFixCount, successfulRepairCount, repairedApps, debuggingResultList

def getFolderNameFromRepo(repoName):
  if os.path.basename(repoName) == '':
    folderNameItems = repoName.split(os.path.sep)
    #print(folderNameItems)
    itemsBack = 1
    folderName = ''
    while folderName == '':
      folderName = folderNameItems[-itemsBack]
      itemsBack += 1
  else:
    folderName = os.path.basename(repoName).split('.')[0]
  return folderName

def main():
  #figure out where the problem can be injected but don't do it.
  #copy the files over to a new folder
  #inject the problem in the copy
  #compile the code with the problem
  #run the checker to catch the problem
  #try to fix the problem
  #repeat a certain number of times

  #I seem to be missing an injectInstance - look into it tomorrow

  #getResource injection and setArguments is not caught by my checker - it also might inject twice instead of once
  injectorInstanceList = []
  #need to update the 3 commented out injection options so that they support two parameters
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidGetResources', isRepoOfInterestInitializer(injectGetResourcesIssue.containsFileOfInterest), injectGetResourcesIssue.injectInRepo))
  #injectorInstanceList.append(InjectionDispatch('DetectSetArgumentsMain', isRepoOfInterestInitializer(injectSetArgumentsProblem.isRepoOfInterest), injectInRepoInitializer(injectSetArgumentsProblem.injectSetArgumentsProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidSetTheme', isRepoOfInterestInitializer(injectSetThemeIssue.containsFileOfInterest), injectSetThemeIssue.injectInRepo))
  #injectorInstanceList.append(InjectionDispatch('DetectIncorrectGetActivityMain', isRepoOfInterestInitializer(injectGetActivityIssue.isPossibleInjectionRepo), injectGetActivityIssue.injectInRepo))
  #injectorInstance = InjectionDispatch('DetectInvalidGetResources', injectGetResourcesIssue.findPossibleInjectionRepos, injectGetResourcesIssue.injectInRepo)
  #injectorInstance = InjectionDispatch('DetectSetArgumentsMain', filterRepoInitializer(injectSetArgumentsProblem.isRepoOfInterest), injectInRepoInitializer(injectSetArgumentsProblem.injectSetArgumentsProblem))
  #injectorInstance = InjectionDispatch('DetectInvalidSetTheme', injectSetThemeIssue.findPossibleInjectionRepos, injectSetThemeIssue.injectInRepo)
  #injectorInstance = InjectionDispatch('DetectIncorrectGetActivityMain', injectGetActivityIssue.findPossibleInjectionRepos, injectGetActivityIssue.injectInRepo)

  #using a new method starting here - need to fix the ones above here to adapt to the new approach
  #skipping come back to later - it doesn't compile when injected - getSupportFragment doesn't work
  #injectorInstance = InjectionDispatch('DetectIncorrectSetInitialSavedState', filterRepoInitializer(injectSetInitialSavedStateProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetInitialSavedStateProblem.injectSetInitialSavedStateProblem))
  #doesn't have enough instances - only two contain either, 1 compiles but doesn't parse in Flowdroid, the other one has the section commented out
  #tries to fix 0 apps
  #injectorInstanceList.append(InjectionDispatch('DetectIncorrectSetInitialSavedState', isRepoOfInterestInitializer(injectSetInitialSavedStateProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetInitialSavedStateProblem.injectSetInitialSavedStateProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectSetArgumentsMain', filterRepoInitializer(injectSetArgumentsProblem.isRepoOfInterest), injectInRepoInitializer(injectSetArgumentsProblem.injectSetArgumentsProblem)))
  #can fix at least 3
  #injectorInstanceList.append(InjectionDispatch('DetectSetSelectorSetPackageProblem', isRepoOfInterestInitializer(injectSetPackageSetSelectorProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetPackageSetSelectorProblem.injectSetPackageSetSelectorProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectMissingSetHasOptionsMenu', isRepoOfInterestInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem)))
  injectorInstanceList.append(InjectionDispatch('DetectInvalidInflateCallMain', isRepoOfInterestInitializer(injectInflateAndOptionsMenuIssues.determineInjectionInfoForInflateRepo), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.injectInflateProblemWithoutComby)))
  #Can fix
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidSetContentViewFindViewByIDOrdering', isRepoOfInterestInitializer(injectSetContentViewIssue.isPossibleInjectionRepo), injectInRepoInitializer(injectSetContentViewIssue.injectSetContentViewIssue)))
  #Can fix
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidSetTheme', filterRepoInitializer(injectSetThemeIssue.containsFileOfInterest), injectSetThemeIssue.injectInRepo))
  #injectorInstance = InjectionDispatch('DetectSetSelectorSetPackageProblem', filterRepoInitializer(injectSetPackageSetSelectorProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetPackageSetSelectorProblem.injectSetPackageSetSelectorProblem))
  #njectorInstance = InjectionDispatch('DetectInvalidInflateCallMain', filterRepoInitializer(injectInflateAndOptionsMenuIssues.determineInjectionInfoForInflateRepo), injectInflateAndOptionsMenuIssues.injectInflateProblem)
  #injectorInstance = InjectionDispatch('DetectMissingSetHasOptionsMenu', filterRepoInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem))
  #njectorInstance = InjectionDispatch('DetectMissingSetHasOptionsMenu', filterRepoInitializer(injectSetContentViewIssue.isPossibleInjectionRepo), injectInRepoInitializer(injectSetContentViewIssue.injectSetContentViewIssue))

  #ones left to hook up
  #setContentView 
  debuggingResultList = []


  startingDir = '/Users/zack/git/reposFromFDroid/'
  originalDir = os.getcwd()
  #posThatCompile = [os.path.join(startingDir,r) for r in reposThatCompileNames]
  #for file in injectorInstance.getPossibleInjectionSites(startingDir):
    #os.chdir(os.path.dirname(file))
    #result = subprocess.run(getRepoFolderCommand, capture_output=True)
    #print('@@@starting output of interest')
    #if result.returncode == 0:
      #repoDir = result.stdout.decode('utf-8').strip()
  repoCount = 0
  attemptedFixCount = 0
  successfulRepairCount = 0
  workingReposDict = {}
  printedCount = 0
  with open(workingReposFile, 'r') as fin:
    for line in fin:  
      workingReposDict[line.strip()] = True
  print('number of working repos: {0}'.format(workingReposDict))
  apkSourceInfo = extractRepoInfo.extractRepoInfo()
  #apkInfoDict = {}
  folderInfoDict = {}
  for a in apkSourceInfo:
    if a[1] != '':
      folderName = getFolderNameFromRepo(a[1])
      #apkInfoDict[a[0]] = (a[0],a[1],a[2])
      #print(folderName)
      if folderName in workingReposDict:
        #print('in working repos')
        folderInfoDict[folderName] = a
  print('folder info dict size: {0}'.format(len(folderInfoDict)))
  reposToCheck = [os.path.join(runInjectionTests.fDroidRepoDir, f) for f in folderInfoDict]
  #print('original repos to check count: {0}'.format(len(reposToCheck)))
  attemptedFoldersDict = {}
  #I assume this script will be short enough that I won't need this. I can 
  #add it back later if I end up needing it later
  #if os.path.exists(attemptedFoldersFile):
    #with open(attemptedFoldersFile,'r') as fin:
      #for line in fin:
        #attemptedFoldersDict[line.strip()] = True
  #if len(attemptedFoldersDict) > 0:
    #reposToCheck = [r for r in reposToCheck if not r in attemptedFoldersDict]

  #currently trying to figure out how to convert this to work for the list of 
  #possible repos that have test cases
  successfulRepoFile = successfulInjectionReposTemplate.format(injectorInstanceList[0].checkerName)
  with open(successfulRepoFile,'a') as fout:
    print('repo to check count: {0}'.format(len(reposToCheck)))
    for repoDir in reposToCheck:
      for injectorInstance in injectorInstanceList:
        print(injectorInstance.checkerName)
        if injectorInstance.isPossibleInjectionRepo(folderInfoDict, repoDir):
          print('is a possible injection repo')
          debuggingResultList.append('{0} repo: {1}'.format(repoCount, repoDir))
          print('repoDir: {0}'.format(repoDir))
          if os.path.exists(copyRepoLocation):
            shutil.rmtree(copyRepoLocation)
          try:
            shutil.copytree(repoDir, copyRepoLocation)
          except:
            print('problem copying repo')
            continue
          clearAPKS(copyRepoLocation)
          appBuilds = buildApp(copyRepoLocation)
          if len(appBuilds) < 1:
            print('there was a problem building the app. Aborting before injecting problem.')
            debuggingResultList.append("couldn't build the app")
            #print(repoDir, file=fout)
            continue
          else: 
            if getTestResultsOfRepo(copyRepoLocation):
              print(repoDir, file=fout)
              fout.flush()
              os.fsync(fout.fileno())
              print('found a repo to inject later')
              printedCount += 1

            #see if the application already has a problem - if so, we don't need to inject anything.
            #newAttemptedFixCount, newSuccessfulRepairCount, repairedApps, debuggingResultList = tryToRepairApps(injectorInstance, appBuilds, debuggingResultList)
            #if attemptedFixCount > 0:
              #debuggingResultList.append('found a problem in the original app')
              #if newSuccessfulRepairCount:
                #debuggingResultList.append('was able to repair a problem in the original app')
            #else:
              #print('injecting problem')
              #injectorInstance.injectIssue(copyRepoLocation)
              #clearAPKS(copyRepoLocation)
              #appBuilds = buildApp(copyRepoLocation)
              #if len(appBuilds) < 1:
                #print('there was a problem building the app. Aborting before checking for injected problem.')
                #debuggingResultList.append('there was a problem building the app with the injected problem')
                ##input('stopping to check the build error')
                ##sys.exit(0)
              #newAttemptedFixCount, newSuccessfulRepairCount, repairedApps, debuggingResultList = tryToRepairApps(injectorInstance, appBuilds, debuggingResultList)
          ##if newAttemptedFixCount < 1:
            #debuggingResultList.append('never tried to fix any of the apps - was unable to find the problem with the checker after injecting the problem')
          #elif len(repairedApps) < 1:
            #debuggingResultList.append('was never able to successfully repair an app')
          #else:
            ##I'm not sure if running the tests should be before or after running the checker
            ##to see if the application contains an error - I don't think it matters, but I'll
            ##have to test it and see
#
            ##the tests are for the whole repo, so not app specific
            #if getTestResultsOfRepo(copyRepoLocation):
              #print('passed tests')
              #debuggingResultList.append('the application was completely repaired!')
              #input('stopping to see the successful fix!!')
                  ##input('stopping to see checker result after injecting error')
                        ##run the automated fix on this application
#
                  ##run checker on the new app
            #else:
              #debuggingResultList.append('the tests failed after trying to repair the app/apps')
              #print('failed tests')
          #attemptedFixCount += newAttemptedFixCount
          #successfulRepairCount += newSuccessfulRepairCount
      repoCount +=1
      print('number of checked repos: {0}'.format(repoCount))
      #print(repoDir, file=fout)

    #input('checking result')
  for line in debuggingResultList:
    print(line)
  print('that was all the repos!')
  print('tested {0} repos'.format(repoCount))
  print('attempted to fix {0} apps'.format(attemptedFixCount))
  print('successful fix count: {0}'.format(successfulRepairCount))
  print('saved {0} repos to file'.format(printedCount))


if __name__ == "__main__":
  main()