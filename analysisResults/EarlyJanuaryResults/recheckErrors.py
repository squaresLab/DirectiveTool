#!/usr/local/bin/python3

#This is the updated version of processFullResults.py

import sys
import os
import subprocess
import collections
import shlex
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import extractRepoInfo

fullCheckerCommand = '/Library/Java/JavaVirtualMachines/jdk0.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=59432:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar'# analysis.DetectInvalidInflateCallMain'
#errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrorsSecondPass.txt'
jarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2/AndroidDirectiveChecker.jar'
currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
#outputFileName = '/Users/zack/git/DirectiveTool/runResults.txt'
#androidJarLocation = '/Users/zack/git/DirectiveTool/runCheckerPackage/android.jar'
androidJarLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2/android.jar'
runCheckerLocation = '/Users/zack/git/DirectiveTool/FlowDroidTest'

successDict = {}
errorDict = {}
callgraphProblemDict = {}
timeoutDict = {}

firstClassInSequencePattern = re.compile('[^<]<+([^;]+);.+')
openFileTemplate = 'open -a "Sublime Text" {0}'

#may want to eventually expand this to read all the items in the sequence list
def getFistClassFromSequenceList(line):
  firstSequenceMatch = firstClassInSequencePattern.match(line)
  if firstSequenceMatch:
    return firstSequenceMatch.group(1)
  else:
    return None

def openFileInRepo(repoName, classToLookFor):
  if '$' in classToLookFor:
    classToLookFor = classToLookFor.split('$')[0]
  for root, dirs, files in os.path.walk(repoName):
    for f in files:
      if classToLookFor in f:
        openFileCommand = shlex.split(openFileTemplate.format(f))





def runChecker(checker, filename):
  originalDir = os.getcwd()
  os.chdir(runCheckerLocation) 
  fullFilename = os.path.join(currentAppFolder, filename)
  checkerCommand = ['java', '-jar', jarLocation, checker, fullFilename, androidJarLocation]
  print('command: {0}'.format(' '.join(checkerCommand)))
  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
      elif 'call sequence List(' in line:
        openFileInRepo(repoName, getFistClassFromSequenceList(line))
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


apkSourceInfo = extractRepoInfo.extractRepoInfo()
apkInfoDict = {}
skippedBecauseOfBuildCount = 0
for a in apkSourceInfo:
  #convert a list of appBaseName, repoName, commitHash to a dict
  #with key appBaseName and value repoName, commitHash 
  apkInfoDict[a[0]] = (a[1], a[2])

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
for mergedName in successDict:
  periodLoc = mergedName.rindex('.')  
  apkName = mergedName[:periodLoc+4]
  checkerName = mergedName[periodLoc+4:]
  if os.path.sep in apkName:
    apkName = os.path.basename(apkName) 
  print(apkName)
  print(checkerName)
  if checkerName == "DetectInvalidGetResources":
    runChecker(checkerName, apkName)
    print('app name: {0}, checker name: {1}'.format(apkName, checkerName))
    apkBasename = extractRepoInfo.extractAPKBasename(apkName)
    try:
      repoName, commitHash = apkInfoDict[apkBasename]
      print('repo name: {0}'.format(repoName))
    except KeyError as k:
      pass
    input('press enter to continue')
#for mergedName in timeoutDict:
#  periodLoc = mergedName.rindex('.')  
#  apkName = mergedName[:periodLoc+4]
#  checkerName = mergedName[periodLoc+4:]
#  print(apkName)
#  print(checkerName)