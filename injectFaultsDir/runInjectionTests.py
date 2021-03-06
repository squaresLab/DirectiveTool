#!/usr/local/bin/python3

import injectGetResourcesIssue 
import injectSetThemeIssue
import injectGetActivityIssue
import injectSetInitialSavedStateProblem
import injectSetPackageSetSelectorProblem
import injectInflateAndOptionsMenuIssues
import injectSetArgumentsProblem
import injectSetContentViewIssue
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
import utilitiesForRepair

getRepoFolderCommand =  shlex.split('git rev-parse --show-toplevel')
copyRepoLocation = '/Users/zack/git/DirectiveTool/injectFaultsDir/tempRepoForInjection/'
#I may need to convert them to using gradlew instead of gradle wrapper
#buildAppCommand = shlex.split('gradle wrapper assembleDebug')
#testAppCommand = shlex.split('gradle wrapper test')
testAppCommand = shlex.split('./gradlew -Dorg.gradle.java.home=/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home test')
runCheckerTemplate = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=56329:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar analysis.{0} {1}'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/reposWithSuccessfulTests.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/optionsMenuDefinitionRepos.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectSetSelectorSetPackageProblem.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectInvalidInflateCallMain.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectInvalidSetTheme.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectIncorrectGetActivityMain.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/singleGetActivityInjectionRepos.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectSetArgumentsMain.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/reposWithZeroErrors.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectIncorrectSetInitialSavedState.txt'
#workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectInvalidSetContentViewFindViewByIDOrdering.txt'
workingReposFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/successfulInjectionReposDetectMissingSetHasOptionsMenu.txt'
fDroidRepoDir = '/Users/zack/git/reposFromFDroid/'
attemptedFoldersFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/triedInjectionFolders.txt'
#reposWithZeroErrorsFile = '/Users/zack/git/DirectiveTool/injectFaultsDir/reposWithZeroErrors.txt'

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
#that mattered for the injection type. 
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
    injectedProblem = False
    for fullFilename in javaFiles:
      if injectIssueMethod(fullFilename):
        print('changed: {0}'.format(fullFilename))
        injectedProblem = True
        #input('stop for a change. Press enter to continue')
        break
    if not injectedProblem:
      print('never injected problem in repo: {0}'.format(repoDir))
      input('stopping to check lack of injection')
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


def runTestOfApp(checkerName, app, debuggingResultList, repoDir):
  originalDir = os.getcwd()
  os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
  debuggingResultList.append('testing application: {0}'.format(app))
  checkerCommand = shlex.split(runCheckerTemplate.format(checkerName, app))
  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  isAppToFix = False
  errorCount = None
  foundLineOfInterest = False
  checkerOutputLines = []
  for line in checkerResult.stdout.decode('utf-8').splitlines():
    line = line.strip()
    checkerOutputLines.append(line)
    #print(line)
    #if line.startswith('total') and not line.startswith('total time'):
  importantCheckerLines = utilitiesForRepair.extractImportantCheckerLines(checkerOutputLines)
  problemList = utilitiesForRepair.extractProblemInfoFromCheckerOutput(importantCheckerLines)  
  print("problem list in runTestOfApp: {0}".format(problemList))
  for p in problemList:
    print(p)
  errorCount = utilitiesForRepair.extractProblemCountFromCheckerOutput(importantCheckerLines)
  if len(problemList) != errorCount and len(problemList) != 0 and not errorCount is None:
    if utilitiesForRepair.checkForSootError(checkerResult):
      problemList = []
      errorCount = 0
      print('soot had an error')
    else:
      outputFile = os.path.join(os.getcwd(), 'debuggingCheckerOutputFile.txt')
      with open(outputFile, 'w') as fout:
        for line in checkerOutputLines:
          print(line, file=fout)
        print('-------end of full output; starting important lines ------', file=fout)
        for line in importantCheckerLines:
          print(line, file=fout)
        print('#######checker error lines########', file=fout)
        for line in checkerResult.stderr.decode('utf-8').splitlines():
          print(line, file=fout, end='')
        print('******command to run checker*****', file=fout)
        print(' '.join(checkerCommand), file=fout)

      print('saved checker output to {0} for debugging'.format(outputFile))
      print('error: problem count is not equal to error count')
      print('app with error: {0}'.format(app))
      print('problem list: {0}'.format(problemList))
      print('error count: {0}'.format(errorCount))
      sys.exit(1)
  if not errorCount is None and errorCount > 0:
    print('greater than 0')
    if errorCount == 1:
      print('error count equals 1')
      debuggingResultList.append(line)
      #print('skipping when error count equals 1 for now - remove the skip later')
      isAppToFix = True
    else:
      isAppToFix = True
      print('found {0} errors in application {1}'.format(errorCount, app))
      #input('stopping to see the multiple error case for repo: {0}'.format(repoDir))
      debuggingResultList.append('found {0} errors in application {1}'.format(errorCount, app))
      #print('found too many errors - currently unable to repair multiple errors in an application')
      #print(line)
      #print('found {0} errors in app'.format(errorCount))
  else:
    print('found no errors in the application {0}'.format(app))
    debuggingResultList.append('found no errors in application')
    #I need to get the file to fix from the first item in the problem list
        #removing because the setArguments injection doesn't always inject a 
        #problem; it just injects into a guessed location
        #input('stopping to debug this case')
        #with open(reposWithZeroErrorsFile,'a') as fout:
        #  print(repoDir, file=fout)
    #commenting out this way of getting the class name to try a new one. Leaving
    #it commented out to 
    #elif line.startswith('@@@@@'):
      #foundLineOfInterest = True
      #lineItems = line.split()
      #classWithProblemWithFullNamespace = None
      #print('found line with problem')
      #print(line)
      ##I think I can change previous logic to only checking the last word in the
      #line, but I'll leave it here in case I need to revert
      #for l in lineItems:
        #periodCount = 0
        #for c in l:
          #if c == '.':
            #periodCount += 1
            #if periodCount > 1:
              #classWithProblemWithFullNamespace = l
              #break
        #if classWithProblemWithFullNamespace:
          #break
  
  #if foundLineOfInterest: 
    #input('stopping to allow check of line of interest')
  if not isAppToFix:
    debuggingResultList.append('never found problem to fix')
  #only print out the file problem if the problem was found because the 
  #case where they both occur is obvious and add unnecessary print statements
      #for line in checkerResult.stdout.decode('utf-8').splitlines():
      #  print(line)
      #input('stopping to see this case')
  os.chdir(originalDir)
  return isAppToFix, problemList, debuggingResultList

def tryToRepairApps(currentChecker, appBuilds, debuggingResultList, currentTestRepo, repoDir):
  attemptedFixCount = 0
  successfulRepairCount = 0
  repairedApps = []
  print('number of app builds: {0}'.format(len(appBuilds)))
  originalDir = os.getcwd()
  for app in appBuilds:
    isAppToFix, problemList, debuggingResultList = runTestOfApp(currentChecker, app, debuggingResultList, repoDir)
    #if isAppToFix and fileWithProblem:
    if isAppToFix:
      attemptedFixCount += 1
      try:
        repairResult = runAllRepairs.runRepairOptions(currentChecker, app, problemList, currentTestRepo)
      except timeout_decorator.TimeoutError as t:
        repairResult = None
        debuggingResultList.append('repair attempted timed out')
        print('repair attempt timed out')
      if repairResult:
        if getTestResultsOfRepo(runAllRepairs.testDir):
          print('!!!! Succeeded !!!!')
          successfulRepairCount += 1
          repairedApps.append(app)
        else:
          print('repo tests failed after repair')
          debuggingResultList.append('repo tests failed after repair')
      else:
        print('fix attempt of application returned false')
    else:
      print('ran checker but did not find the right number of errors')
  print('finished trying to repair apps')
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
  #this works
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidSetTheme', isRepoOfInterestInitializer(injectSetThemeIssue.containsFileOfInterest), injectSetThemeIssue.injectInRepo))
  #can't get this one working - either has too many errors in the applications, or individual apps have
  ##issues - first one can only inject into a nested class (whose repair isn't supported) and
  #second one only injects into methods that aren't called directly (I could make those errors, but 
  #that would probably open up even more false positives)
  #injectorInstanceList.append(InjectionDispatch('DetectIncorrectGetActivityMain', isRepoOfInterestInitializer(injectGetActivityIssue.isPossibleInjectionRepo), injectGetActivityIssue.injectInRepo))
  #injectorInstance = InjectionDispatch('DetectInvalidGetResources', injectGetResourcesIssue.findPossibleInjectionRepos, injectGetResourcesIssue.injectInRepo)
  #injectorInstance = InjectionDispatch('DetectSetArgumentsMain', filterRepoInitializer(injectSetArgumentsProblem.isRepoOfInterest), injectInRepoInitializer(injectSetArgumentsProblem.injectSetArgumentsProblem))
  #injectorInstance = InjectionDispatch('DetectInvalidSetTheme', injectSetThemeIssue.findPossibleInjectionRepos, injectSetThemeIssue.injectInRepo)
  #injectorInstance = InjectionDispatch('DetectIncorrectGetActivityMain', injectGetActivityIssue.findPossibleInjectionRepos, injectGetActivityIssue.injectInRepo)

  #using a new method starting here - need to fix the ones above here to adapt to the new approach
  #skipping come back to later - it doesn't compile when injected - getSupportFragment doesn't work
  #injectorInstanceList.append(InjectionDispatch('DetectSetArgumentsMain', isRepoOfInterestInitializer(injectSetArgumentsProblem.isRepoOfInterest), injectInRepoInitializer(injectSetArgumentsProblem.injectSetArgumentsProblem)))
  #injectorInstance = InjectionDispatch('DetectIncorrectSetInitialSavedState', filterRepoInitializer(injectSetInitialSavedStateProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetInitialSavedStateProblem.injectSetInitialSavedStateProblem))
  #doesn't have enough instances - only two contain either, 1 compiles but doesn't parse in Flowdroid, the other one has the section commented out
  #tries to fix 0 apps
  #injectorInstanceList.append(InjectionDispatch('DetectIncorrectSetInitialSavedState', isRepoOfInterestInitializer(injectSetInitialSavedStateProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetInitialSavedStateProblem.injectSetInitialSavedStateProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectSetSelectorSetPackageProblem', isRepoOfInterestInitializer(injectSetPackageSetSelectorProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetPackageSetSelectorProblem.injectSetPackageSetSelectorProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidInflateCallMain', isRepoOfInterestInitializer(injectInflateAndOptionsMenuIssues.determineInjectionInfoForInflateRepo), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.injectInflateProblemWithoutComby)))
  #set options menu works now for 
  #injectorInstanceList.append(InjectionDispatch('DetectMissingOptionsMenuDefinition', isRepoOfInterestInitializer(injectInflateAndOptionsMenuIssues.canInjectOnCreateOptionsMenuProblem), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.injectOnCreateOptionsMenuProblem)))
  injectorInstanceList.append(InjectionDispatch('DetectMissingSetHasOptionsMenu', isRepoOfInterestInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.injectSetHasOptionsMenuProblem)))
  #injectorInstanceList.append(InjectionDispatch('DetectInvalidSetContentViewFindViewByIDOrdering', isRepoOfInterestInitializer(injectSetContentViewIssue.isPossibleInjectionRepo), injectInRepoInitializer(injectSetContentViewIssue.injectSetContentViewIssue)))
  #injectorInstance = InjectionDispatch('DetectSetSelectorSetPackageProblem', filterRepoInitializer(injectSetPackageSetSelectorProblem.isPossibleInjectionRepo), injectInRepoInitializer(injectSetPackageSetSelectorProblem.injectSetPackageSetSelectorProblem))
  #injectorInstance = InjectionDispatch('DetectInvalidInflateCallMain', filterRepoInitializer(injectInflateAndOptionsMenuIssues.determineInjectionInfoForInflateRepo), injectInflateAndOptionsMenuIssues.injectInflateProblem)
  #injectorInstance = InjectionDispatch('DetectMissingSetHasOptionsMenu', filterRepoInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem), injectInRepoInitializer(injectInflateAndOptionsMenuIssues.canInjectSetHasOptionsMenuProblem))
  #njectorInstance = InjectionDispatch('DetectMissingSetHasOptionsMenu', filterRepoInitializer(injectSetContentViewIssue.isPossibleInjectionRepo), injectInRepoInitializer(injectSetContentViewIssue.injectSetContentViewIssue))

  #ones left to hook up
  #setContentView 
  debuggingResultList = []


  startingDir = '/Users/zack/git/reposFromFDroid/'
  originalDir = os.getcwd()
  #reposThatCompile = [os.path.join(startingDir,r) for r in reposThatCompileNames]
  #for file in injectorInstance.getPossibleInjectionSites(startingDir):
    #os.chdir(os.path.dirname(file))
    #result = subprocess.run(getRepoFolderCommand, capture_output=True)
    #print('@@@starting output of interest')
    #if result.returncode == 0:
      #repoDir = result.stdout.decode('utf-8').strip()
  repoCount = 0
  totalAttemptedFixCount = 0
  totalSuccessfulRepairCount = 0
  workingReposDict = {}
  reposInFileAreFullPaths = False
  successfullyFixedRepoSet = set()
  with open(workingReposFile, 'r') as fin:
    checkedFullPaths = False
    for lineCount, line in enumerate(fin):  
      line = line.strip()
      #allow lines in the file to commented out
      if not line.startswith('#'):
        workingReposDict[line] = True
        if not checkedFullPaths and line[0] == '/':
          reposInFileAreFullPaths = True
          checkedFullPaths = True
  apkSourceInfo = extractRepoInfo.extractRepoInfo()
  #apkInfoDict = {}
  folderInfoDict = {}

  if reposInFileAreFullPaths:
    #assume that all folders exists, so folderInfoDict isn't needed
    #this assumption is based on the fact that the full file list points
    #to already downloaded repos on the machine and not just general repo names
    reposToCheck = [r for r in workingReposDict]
  else:
    #otherwise collect the folder names and get the folderInfoDict so the
    #repository can be downloaded
    for a in apkSourceInfo:
      if a[1] != '':
        folderName = getFolderNameFromRepo(a[1])
        #apkInfoDict[a[0]] = (a[0],a[1],a[2])
        #print(folderName)
        if folderName in workingReposDict:
          #print('in working repos')
          folderInfoDict[folderName] = a
    reposToCheck = [os.path.join(fDroidRepoDir, f) for f in folderInfoDict]
  #print('original repos to check count: {0}'.format(len(reposToCheck)))
  attemptedFoldersDict = {}
  if os.path.exists(attemptedFoldersFile):
    with open(attemptedFoldersFile,'r') as fin:
      for line in fin:
        line = line.strip()
        #allow commenting out of lines
        if not line.startswith('#'):
          attemptedFoldersDict[line.strip()] = True
  if len(attemptedFoldersDict) > 0:
    reposToCheck = [r for r in reposToCheck if not r in attemptedFoldersDict]

  #currently trying to figure out how to convert this to work for the list of 
  #possible repos that have test cases
  with open(attemptedFoldersFile,'a') as fout:
    print('repo to check count: {0}'.format(len(reposToCheck)))
    for repoDir in reposToCheck:
      print('checking repo: {0}'.format(repoDir))
      for injectorInstance in injectorInstanceList:
        print('injector instance: {0}'.format(injectorInstance))
        print(injectorInstance.checkerName)
        if injectorInstance.isPossibleInjectionRepo(folderInfoDict, repoDir):
          print('is a possible injection repo')
          debuggingResultList.append(repoDir)
          print('{0} repoDir: {1}'.format(repoCount, repoDir))
          if os.path.exists(copyRepoLocation):
            shutil.rmtree(copyRepoLocation)
          try:
            shutil.copytree(repoDir, copyRepoLocation)
          except:
            debuggingResultList.append('problem copying repo')
            print('problem copying repo')
            continue
          utilitiesForRepair.clearAPKS(copyRepoLocation)
          appBuilds = utilitiesForRepair.buildApp(copyRepoLocation)
          if len(appBuilds) < 1:
            print('there was a problem building the app. Aborting before injecting problem.')
            debuggingResultList.append("couldn't build the app")
            #print(repoDir, file=fout)
            continue
          else: 
            #see if the application already has a problem - if so, we don't need to inject anything.
            #commenting out for debugging - I should add this back later
            if injectorInstance.checkerName == 'DetectIncorrectGetActivityMain':
              attemptedFixCount, newSuccessfulRepairCount, repairedApps, debuggingResultList = tryToRepairApps(injectorInstance.checkerName, appBuilds, debuggingResultList, copyRepoLocation, repoDir)
              #added next line for a different test; remove later
              continue
            else:
              attemptedFixCount = 0
            if attemptedFixCount > 0:
              debuggingResultList.append('found a problem in the original app')
              if newSuccessfulRepairCount:
                debuggingResultList.append('was able to repair a problem in the original app on first try')
            else:
              print('injecting problem')
              injectorInstance.injectIssue(copyRepoLocation)
              utilitiesForRepair.clearAPKS(copyRepoLocation)
              appBuilds = utilitiesForRepair.buildApp(copyRepoLocation)
              if len(appBuilds) < 1:
                print('there was a problem building the app. Aborting before checking for injected problem.')
                debuggingResultList.append('there was a problem building the app with the injected problem')
                #input('stopping to check the build error')
                #sys.exit(0)
              newAttemptedFixCount, newSuccessfulRepairCount, repairedApps, debuggingResultList = tryToRepairApps(injectorInstance.checkerName, appBuilds, debuggingResultList, copyRepoLocation, repoDir )
          if newAttemptedFixCount < 1:
            debuggingResultList.append('never tried to fix any of the apps - was unable to find the problem with the checker or found too many problems after injecting the problem')
            #input('stopping to debug the failed injection case')
            print('never attempted to repair')
          elif len(repairedApps) < 1:
            debuggingResultList.append('was never able to successfully repair an app')
            input('general stop after trying to fix app')
          else:
            #I'm not sure if running the tests should be before or after running the checker
            #to see if the application contains an error - I don't think it matters, but I'll
            #have to test it and see

            #the tests are for the whole repo, so not app specific
            if getTestResultsOfRepo(copyRepoLocation):
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
              input('general stop after trying to fix app')
          totalAttemptedFixCount += newAttemptedFixCount
          totalSuccessfulRepairCount += newSuccessfulRepairCount
        else:
          debuggingResultList.append('{0} was determined not to be a possible repo for injection'.format(debuggingResultList))
          print('failed the test that it is an injection repo')
        #input('stopping after each injection to see what happened')
      repoCount +=1
      print('number of checked repos: {0}'.format(repoCount))
      print(repoDir, file=fout)
  for line in debuggingResultList:
    print(line)
  print('that was all the repos!')
  print('tested {0} repos'.format(repoCount))
  print('attempted to fix {0} apps'.format(totalAttemptedFixCount))
  print('successful fix count: {0}'.format(totalSuccessfulRepairCount))
  print('successfully fixed repos: {0}'.format(successfullyFixedRepoSet))
  

if __name__ == "__main__":
  main()