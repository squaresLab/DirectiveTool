#!/usr/local/bin/python3

#This is the updated version of processFullResults.py

import sys
import os
import subprocess
import collections
import shlex
import re

#I should later move the method called here to a different file
import repairFoundErrors2

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import extractRepoInfo
import utilitiesForRepair

#fullCheckerCommand = '/Library/Java/JavaVirtualMachines/jdk0.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=59432:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar'# analysis.DetectInvalidInflateCallMain'
#errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrorsSecondPass.txt'
jarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2/AndroidDirectiveChecker.jar'
currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
#outputFileName = '/Users/zack/git/DirectiveTool/runResults.txt'
#androidJarLocation = '/Users/zack/git/DirectiveTool/runCheckerPackage/android.jar'
androidJarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2/android.jar'
runCheckerLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest'
repoLocation = '/Users/zack/git/reposFromFDroid'

successDict = {}
errorDict = {}
callgraphProblemDict = {}
timeoutDict = {}

firstClassInSequencePattern = re.compile('<([^:]+)')
openFileTemplate = 'open -a "Sublime Text" {0}'

#may want to eventually expand this to read all the items in the sequence list
def getFistClassFromSequenceList(line):
  firstSequenceMatch = re.findall(firstClassInSequencePattern,line)
  if firstSequenceMatch and len(firstSequenceMatch) > 0:
    return firstSequenceMatch[0]
  else:
    return None

def openFileInRepo(repoName, classToLookFor):
  print('class to look for: {0}'.format(classToLookFor))
  if '$' in classToLookFor:
    classToLookFor = classToLookFor.split('$')[0]
  if not classToLookFor.endswith('.java') and '.' in classToLookFor:
    classToLookFor = classToLookFor.split('.')[-1]
  if repoName.endswith('.git'):
    repoName = repoName[-4]
  repoBasename = repoName.split(os.path.sep)[-1]
  repoDir = os.path.join(repoLocation, repoBasename)
  for root, dirs, files in os.walk(repoDir):
    for f in files:
      if classToLookFor in f:
        openFileCommand = shlex.split(openFileTemplate.format(os.path.join(root,f)))
        subprocess.run(openFileCommand)
        return





def runChecker(checker, filename, repoName):
  originalDir = os.getcwd()
  os.chdir(runCheckerLocation) 
  fullFilename = os.path.join(currentAppFolder, filename)
  checkerCommand = ['java', '-jar', jarLocation, checker, fullFilename, androidJarLocation]
  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  callgraphErrorCount = 0
  problemCount = None
  if checkerResult.returncode == 0:
    checkerOutputLines = []
    for line in checkerResult.stdout.decode('utf-8').splitlines():
      line = line.strip()
      checkerOutputLines.append(line)
      print(line)
      #if line.startswith('total') and not line.startswith('total time'):
    importantCheckerLines = utilitiesForRepair.extractImportantCheckerLines(checkerOutputLines)
    problemList = utilitiesForRepair.extractProblemInfoFromCheckerOutput(importantCheckerLines)  
    problemCount = utilitiesForRepair.extractProblemCountFromCheckerOutput(importantCheckerLines)
    for i in importantCheckerLines:
      print(i)
    print('problem count at end of extract checker output: {0}'.format(problemCount))
    if not problemCount is None and problemCount != len(problemList):
      print('error: problem count does not match the problem list size')
      print('problem count: {0}, problem list: {1}'.format(problemCount, problemList))
      sys.exit(1)
    if problemCount != 0 and not problemCount is None:
      print("found an error with checker {0} in app {1}".format(checker, filename))
      repoDir = repairFoundErrors2.changeToRepoAndCommit(repoName, commitHash)
      print('repo dir: {0}'.format(repoDir))
      openFileInRepo(repoDir, problemList[0].getFilenameWithProblem())
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
  os.chdir(originalDir)
  print('problem count at end of run checker: {0}'.format(problemCount))
  return problemCount


apkSourceInfo = extractRepoInfo.extractRepoInfo()
apkInfoDict = {}
skippedBecauseOfBuildCount = 0
for a in apkSourceInfo:
  #convert a list of appBaseName, repoName, commitHash to a dict
  #with key appBaseName and value repoName, commitHash 
  apkInfoDict[a[0]] = (a[1], a[2])

#with open('rerunFDroidCheckResults.txt','r') as fin:
newAppsWithErrorCount = 0
usingApkList = True
if usingApkList:
  with open('secondSetArgumentsCheck.txt', 'r') as fin:
    for line in fin:
      line = line.strip()
      checkerName = line
      mergedName = line + 'DetectSetArgumentsMain'
      if not mergedName in successDict:
        successDict[mergedName] = True
else:
  with open('setArgumentsCheckerResults.txt','r') as fin:
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
print('number of timeouts: {0}'.format(len(timeoutDict)))
countDict = collections.defaultdict(int)
for mergedName in successDict:
  periodLoc = mergedName.rindex('.')  
  apkName = mergedName[:periodLoc+4]
  checkerName = mergedName[periodLoc+4:]
  countDict[checkerName] += 1
for checker in countDict:
  print('{0}: {1}'.format(checker, countDict[checker]))
for mergedName in successDict:
  periodLoc = mergedName.rindex('.')  
  apkName = mergedName[:periodLoc+4]
  checkerName = mergedName[periodLoc+4:]
  if os.path.sep in apkName:
    apkName = os.path.basename(apkName) 
  print(apkName)
  if checkerName == "DetectSetArgumentsMain":
    repName = None
    apkBasename = extractRepoInfo.extractAPKBasename(apkName)
    try:
      repoName, commitHash = apkInfoDict[apkBasename]
    except KeyError as k:
      pass
    problemCount = runChecker(checkerName, apkName, repoName)
    print('app name: {0}, checker name: {1}'.format(apkName, checkerName))
    if not repoName is None:
      print('repo name: {0}'.format(repoName))
    if (not problemCount is None) and problemCount != 0:
      input('press enter to continue')
      print('\n')
      newAppsWithErrorCount += 1
      #with open('secondSetArgumentsCheck.txt','a') as fout:
      #  print(apkName, file=fout)
    else:
      print('skipped stopping with problem count: {0}'.format(problemCount))
print('found {0} errors now'.format(newAppsWithErrorCount))
#for mergedName in timeoutDict:
#  periodLoc = mergedName.rindex('.')  
#  apkName = mergedName[:periodLoc+4]
#  checkerName = mergedName[periodLoc+4:]
#  print(apkName)
#  print(checkerName)