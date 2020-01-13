#!/usr/local/bin/python3

import sys
import subprocess
import os


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


with open('serverRunResults.txt','r') as fin:
  with open('rerunOfSecondPassErrors.txt','a') as fout:
    for line in fin:
      line = line.strip()
      if line.startswith("error;"):
        #print(line)
        #checker = "DetectInvalidSetContentViewFindViewByIDOrdering" 
        checker = line.split(" ")[4]
        apkName = line.split(" ")[-1]
        print('rerunning {0} on {1}'.format(checker, apkName))
        runChecker(checker,apkName,fout)
