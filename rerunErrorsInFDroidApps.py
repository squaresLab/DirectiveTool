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

#timeoutTime=120
#userAgentString='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'


def runChecker(checker, filename, fout):
  firstPartOfCheckerCommand = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java'
  secondPartOfCheckerCommand = '-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=58721:/Applications/IntelliJ IDEA CE.app/Contents/bin'
  checkerCommand = '-Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes'.split(' ')
  checkerCommand.insert(0,secondPartOfCheckerCommand)
  checkerCommand.insert(0,firstPartOfCheckerCommand)
  #checkerNames = ['DetectInvalidInflateCallMain','DetectIncorrectGetActivityMain',
    #'DetectMissingSetHasOptionsMenu', 'DetectSetArgumentsMain',
    #'DetectInvalidSetContentViewFindViewByIDOrdering', 'DetectInvalidGetResources',
    #'DetectIncorrectSetInitialSavedState', 'DetectInvalidSetTheme',
    #'DetectSetSelectorSetPackageProblem']
  currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
  fullFilename = os.path.join(currentAppFolder, filename)
  currentCheckerCommand = checkerCommand.copy()
  currentCheckerCommand.append('analysis.{0}'.format(checker))
  currentCheckerCommand.append(fullFilename)
  originalDir = os.getcwd()
  os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
  #debuggingCommand = currentCheckerCommand.copy()
  #debuggingCommand[1] = '"{0}"'.format(debuggingCommand[1])
  #print(' '.join(debuggingCommand))
  #print('running checker: {0}'.format(checker))
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
          print("found an error with checker {0} in app {1}".format(checker, filename))
          fout.write("success! error found: with checker {0} in app {1}\n".format(checker, filename))
          fout.flush()
          os.fsync(fout.fileno())
          #input("stopping to let you investigate. Press enter to continue")
  else: 
    wasCallGraphError = False
    for line in checkerResult.stderr.decode('utf-8').splitlines():
      if line.strip() == "[main] ERROR soot.jimple.infoflow.android.SetupApplication - Could not construct callgraph":
        wasCallGraphError = True
        callgraphErrorCount = callgraphErrorCount + 1
        fout.write("callgraph error on app {0}\n".format(filename))
        print('callgraph error')
    if not wasCallGraphError:
      print('there was an error running {0} on {1}'.format(checker, filename))
      fout.write("error; couldn't run: checker {0} on app {1}\n".format(checker, filename))
      fout.flush()
      os.fsync(fout.fileno())
#input('stopping to let you check. Press enter to continue')

def main():
  errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrorsSecondPass.txt'
  callgraphErrorCount = 0
  analyzedApplicationCount = 0
  checkedRepos = []
  checkedErrorTuples = []
  errorTuples = []
  checkCount = 1
  currentCount = 0
  outputFileName = '/Users/zack/git/DirectiveTool/rerunFDroidResults.txt'
  skippedCount = 0
  with open(outputFileName,'r') as fin:
    for line in fin:
      line = line.strip()
      if line.startswith('error;'):
        lineItems = line.split()
        checkerWithError =  lineItems[4]
        apkWithError = lineItems[-1]
        checkedErrorTuples.append((checkerWithError, apkWithError))
  with open(errorFileName,'r') as fin:
    for line in fin:
      line = line.strip()
      if line.startswith('error;'):
        lineItems = line.split()
        checkerWithError =  lineItems[4]
        apkWithError = lineItems[-1]
        errorItem = (checkerWithError, apkWithError)
        if not errorItem in checkedErrorTuples:
          errorTuples.append((checkerWithError, apkWithError))
        else:
          skippedCount = skippedCount + 1
        #if checkCount == currentCount:
        #currentCount = currentCount + 1
  print('found {0} errors to check'.format(len(errorTuples)))
  with open(outputFileName, 'a') as fout:
    for eCount, e in enumerate(errorTuples):
      print('checking error {0}'.format(eCount + skippedCount))
      runChecker(e[0],e[1], fout)

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