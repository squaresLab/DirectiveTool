#!/usr/local/bin/python3

import sys
import os
import os.path
import shutil
import subprocess
import re
#checkerToRun = sys.argv[1]
#    originalSourceFolder = sys.argv[2]
#    apkLocation = sys.argv[3]
#    methodOfInterest1 = sys.argv[4]
#    if len(sys.argv > 5):
#      methodOfInterest2 = sys.argv[5]

#TODO: move the variables to the right locations in the methods
#later make it easier to switch between the different checkers
#checkerToRun='DetectIncorrectGetActivityMain'
#runFlowDroidCommand= '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=59095:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-cmd/target/scala-2.12/classes'
#originalSourceFolder = "/Users/zack/git/DirectiveTool/testFolder/" 
#Eventually, I may want to move these hard-coded paths to parameters
edittingFolder = "/Users/zack/git/DirectiveTool/temporaryTestOfChange"
checkerRootDir = "/Users/zack/git/DirectiveTool/FlowDroidTest"
#newAPKLocation = '/Users/zack/git/DirectiveTool/temporaryTestOfChange/app/build/outputs/apk/debug/app-debug.apk'
#newAPKLocation = '/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/build/outputs/apk/debug/Application-debug.apk'
#methodOfInterest1 = "getActivity"
#methodOfInterest2 = "findViewById"
#methodOfInterest2 = None
#the code must append the source code directory path to get this command to work
runGetMethodLocations = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=57377:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/ExtractMethodInfo/squareslab.zackc/production/ExtractMethodInfo:/Users/zack/.m2/repository/com/github/javaparser/javaparser-core/3.12.0/javaparser-core-3.12.0.jar main.java.ExtractMethodInfoMain'
printingDebugInfo = False

#TODO: consider combining the move back and forward methods

#currently not handling comments that contain the method; might need to fix
#that later
#def moveBackMethodBeforePreviousMethod(fileToTest, method1, method2, edittingFolder):
  #executeTestOfChangedApp(edittingFolder)
#  indentationCount = 0
#  method1LineNumber = None
#  method2LineNumber = None
#  foundChangeInFile = False
#  def checkIndentationCountAndResetForNewMethods():
#    if indentationCount < 2:
#      method1LineNumber = None
#      method2LineNumber = None
#  with open(fileToTest,'r') as fin:
#    linesInFile = fin.readlines()
#    for lineCount, line in enumerate(linesInFile):
#      for c in line:
#        if c == "{":
#          indentationCount = indentationCount + 1
#          checkIndentationCountAndResetForNewMethods()
#        elif c == "}":
#          indentationCount = indentationCount - 1
#          checkIndentationCountAndResetForNewMethods()
#      if method1 in line:
#        method1LineNumber = lineCount
#      elif method2 in line:
#        method2LineNumber = lineCount
#      if method1LineNumber is not None and method2LineNumber is not None:
#        if method1LineNumber < method2LineNumber:
#          previousMethodLine = method1LineNumber
#          lastMethodLine = method2LineNumber
#        else:
#          previousMethodLine = method2LineNumber
#          lastMethodLine = method1LineNumber
#        methodToMove = linesInFile[lastMethodLine]
#        del linesInFile[lastMethodLine]
#        linesInFile.insert(previousMethodLine, methodToMove)
#        foundChangeInFile = True
#        break
#  if foundChangeInFile:
#    with open(fileToTest, 'w') as fout:
#      for line in linesInFile:
#        print(line, end="", file=fout)
#  return foundChangeInFile
#  #for debugging
#  #for line in linesInFile:
  #  print(line)
  #sys.exit(0)

class MethodInfo:
  def __init__(self, className, methodName, lineNumber, columnNumber, fileName):
    self.className = className
    self.methodName = methodName
    self.lineNumber = lineNumber
    self.columnNumber = columnNumber
    self.fileName = fileName

class CallChainItem:
  def __init__(self, className, methodName):
    self.className = className
    self.methodName = methodName 

  def __str__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)

  def __repr__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)


def getNonComments(line, inBlockComments):
  #return the part of the string that is the not the comment
  #and if the code is currently in a block comment

  #first return a blank for a single line comment - this is done hueristically
  #and may not work in all cases
  if line.strip().startswith('//'):
    return ('', inBlockComments)
  if inBlockComments: 
    if '*/' in line:
      inBlockComments = False
      commentEnd = line.strip().find('*/')
      return (line[commentEnd+2:], inBlockComments)
    else:
      return ('', inBlockComments)
  else:
    if '/*' in line:
      inBlockComments = True
      commentStart = line.strip().find('/*')
      return (line[0:commentStart], inBlockComments)
    else:
      return (line, inBlockComments)



def moveBackMethodBeforePreviousMethod(fileToTest, method1, method2):
  def getFrontMoveLocations(method1LineNumber, method2LineNumber):
    if method1LineNumber < method2LineNumber:
      moveLocation = method1LineNumber
      lineToMove = method2LineNumber
    else:
      moveLocation = method2LineNumber
      lineToMove = method1LineNumber
    return (lineToMove, moveLocation)
  return moveMethodsInSingleMethod(fileToTest, method1, method2, getFrontMoveLocations)

def moveFrontMethodAfterBackMethod(fileToTest, method1, method2):
  def getFrontMoveLocations(method1LineNumber, method2LineNumber):
    if method1LineNumber > method2LineNumber:
      moveLocation = method1LineNumber
      lineToMove = method2LineNumber
    else:
      moveLocation = method2LineNumber
      lineToMove = method1LineNumber
    return (lineToMove, moveLocation)
  return moveMethodsInSingleMethod(fileToTest, method1, method2, getFrontMoveLocations)



#currently not handling comments that contain the method; might need to fix
#that later
def moveMethodsInSingleMethod(fileToTest, method1, method2, getMoveLocations):
  indentationCount = 0
  method1LineNumber = None
  method2LineNumber = None
  foundChangeInFile = False
  inBlockComments = False
  def checkIndentationCountAndResetForNewMethods():
    if indentationCount < 2:
      method1LineNumber = None
      method2LineNumber = None
  with open(fileToTest,'r') as fin:
    linesInFile = fin.readlines()
    for lineCount, line in enumerate(linesInFile):
      for c in line:
        (nonCommentPartOfLine, inBlockComments) = getNonComments(line, inBlockComments)
        if nonCommentPartOfLine is not '':
          if c == "{":
            indentationCount = indentationCount + 1
            checkIndentationCountAndResetForNewMethods()
          elif c == "}":
            indentationCount = indentationCount - 1
            checkIndentationCountAndResetForNewMethods()
      if method1LineNumber is None and method1 in nonCommentPartOfLine:
        method1LineNumber = lineCount
      elif method2LineNumber is None and method2 in nonCommentPartOfLine:
        method2LineNumber = lineCount
      if method1LineNumber is not None and method2LineNumber is not None:
        (lineToMove, moveLocation) = getMoveLocations(method1LineNumber, method2LineNumber)
        methodToMove = linesInFile[lineToMove]
        del linesInFile[lineToMove]
        linesInFile.insert(moveLocation, methodToMove)
        print('moved {0} to line {1} '.format(methodToMove, moveLocation))
        foundChangeInFile = True
        break
    #for debugging
  #for line in linesInFile:
    #print(line)
  #sys.exit(0)
  if foundChangeInFile:
    print('found change in file: {0}'.format(fileToTest))
    with open(fileToTest, 'w') as fout:
      for line in linesInFile:
        print(line, end="", file=fout)
    #input('press enter to continue')
  return foundChangeInFile

#This can probably be combined with the method call executeTestOfChangedApp but
#I'm unsure how at the moment and eventually decided it wasn't worth thinking 
#about any more
def executeTestOfChangedAppAndGetCallChains(path, runFlowDroidCommand, checkerToRun, apkLocation):
  #TODO: figure out a reasonable return value for the number of problems in 
  #this case
  print('in execute test and get call chains')
  failedExecuteProblemCount = -1
  currentDir = os.getcwd()
  os.chdir(path)
  print("current directory: {0}".format(os.getcwd()))
  commandList = ['./gradlew','assembleDebug']
  currentProblems = 0
  try: 
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    #print(commandOutput.stdout)
    #print(commandOutput.stderr)
  except:
    #try out the next change
    print('command failed ({0}); run again in debug mode to get output'.format(commandList))
    print("debugging directory: {0}".format(os.getcwd()))
    #commandList = ['./gradlew','assembleDebug','--debug']
    #commandList = ['./gradlew','assembleDebug','--debug', '--stacktrace']
    #commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    #print(commandOutput.stdout)
    os.chdir(currentDir)
    return failedExecuteProblemCount, []
  # I need to split by space but not on quoted parts of the string
  unquotedAndQuotedList = runFlowDroidCommand.split('"')
  print('creating execute command')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  checkerToRun = 'analysis.{0}'.format(checkerToRun)
  commandList.append(checkerToRun)
  commandList.append(apkLocation)
  #print(commandList)
  try: 
    print("current directory for command: {0}".format(os.getcwd()))
    os.chdir(checkerRootDir)
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if printingDebugInfo:
      for line in commandOutput.stderr.decode('utf-8').splitlines():
        print(line)
    #input('press enter when looking at output')
    #print(commandOutput)
    #print(commandOutput.stderr)
    #for line in commandOutput.stderr.decode('utf-8').splitlines():
      #print(line)
    savingLines = False
    chainsInfo = []
    currentChain = []
    print('starting to create call chains')
    #handle either the multiple line print out case or the single List print out
    #case
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      print(line)
      if line.startswith('total number of caught problems:'):
        lineItems = line.split(' ')
        currentProblems = int(lineItems[-1])
      elif line.startswith('start of call chain'):
        savingLines = True
        currentChain = []
      elif line.startswith('end of call chain'):
        currentChain.reverse()
        chainsInfo.append(currentChain)
        savingLines = False
      elif savingLines:
        m = re.match(r"<(.+): (.+)> .*", line)
        if m:
          currentChain.append(CallChainItem(m.group(1), m.group(2)))
        else:
            print("call chain line did not match: {0}".format(line))
      elif line.startswith('@@@@ Found a problem:'):
        print('found problem line: {0}'.format(line))
        listSequenceMatch = re.match(r'.+List\((.+)\).*', line)
        if listSequenceMatch:
          print('found list: {0}'.format(listSequenceMatch.group(1)))
          callItems = re.findall(r'<([^>]+)>',listSequenceMatch.group(1))
          for c in callItems:
            print(c)
            itemsInCall = c.split(':')
            currentChain.append(CallChainItem(itemsInCall[0], itemsInCall[1]))
          currentChain.reverse()
          chainsInfo.append(currentChain)
          #sys.exit(0)
    print('finished creating call chains')
    print('final problem count: {0}'.format(currentProblems))
    #if int(currentProblems) == 0:
    #  input('check to see if this is what you want')
  except Exception as e: 
    print(e)
    pass
  #print(chainsInfo)
  os.chdir(currentDir)
  #print("succeeded - change: {0}, method {1}".format(change, method))
  return currentProblems, chainsInfo

def executeTestOfChangedApp(path, checkerToRun, apkLocation):
  print("before build")
  currentDir = os.getcwd()
  os.chdir(path)
  print("current directory: {0}".format(os.getcwd()))

  commandList = ['./gradlew','assembleDebug']
  commandSucceeded = False
  try: 
    print('trying command: {0}'.format(commandList))
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    #print(commandOutput.stdout)
    #print(commandOutput.stderr)
  except:
    #try out the next change
    print('command failed ({0}); run again in debug mode to get output'.format(commandList))
    print("debugging directory: {0}".format(os.getcwd()))
    #commandList = ['./gradlew','assembleDebug','--debug']
    commandList = ['./gradlew','assembleDebug','--debug', '--stacktrace']
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    #print(commandOutput.stdout)
    os.chdir(currentDir)
    return False
  # I need to split by space but not on quoted parts of the string
  unquotedAndQuotedList = runFlowDroidCommand.split('"')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  checkerToRun = 'analysis.{0}'.format(checkerToRun)
  commandList.append(checkerToRun)
  commandList.append(apkLocation)
  try: 
    print("current directory for command: {0}".format(os.getcwd()))
    print("running command: {0} {1} {2}".format("\"".join(unquotedAndQuotedList),checkerToRun, apkLocation))
    os.chdir(checkerRootDir)
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if printingDebugInfo:
      for line in commandOutput.stderr.decode('utf-8').splitlines():
        print(line)
    #input('press enter when looking at output')

    #print(commandOutput)
    #print(commandOutput.stderr)
    #for line in commandOutput.stderr.decode('utf-8').splitlines():
      #print(line)
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      #print(line)
      if line.startswith('total number of caught problems:'):
        print(line)
        lineItems = line.split(' ')
        if int(lineItems[-1]) == 0:
          commandSucceeded = True
  except: 
    pass
  os.chdir(currentDir)
  #print("succeeded - change: {0}, method {1}".format(change, method))
  return commandSucceeded
 #add the change to the method call of the copied app
 #run the application and see if it still produces the problem
 #if the application does not produce the problem, then print the change
 #that fixed the issue and stop


def tryMoveBefore(projectDir, originalSourceFolder, method1, method2, testedFiles, checkerToRun, apkLocation): 
  print('in try move before')
  for dirpath, dirnames, filenames in os.walk(projectDir):
    for filename in [f for f in filenames if f.endswith(".java")]:
      fileToTest = os.path.join(dirpath, filename)  
      #print('found a file: {0}'.format(fileToTest))
      if not fileToTest in testedFiles:
        #print('file not in tested files: {0}'.format(fileToTest))
        testedFiles[fileToTest] = True
        foundAPossibleFix = moveBackMethodBeforePreviousMethod(fileToTest, method1, method2)
        if foundAPossibleFix:
          print('testing: {0}'.format(fileToTest))
          isFixed = executeTestOfChangedApp(edittingFolder, checkerToRun, apkLocation)
          if isFixed:
            return True
          else: 
            #print('testing file: {0} failed'.format(fileToTest))
            #sys.exit(0)
            print('failed to fix with move before')
            createNewCopyOfTestProgram(originalSourceFolder)
  #print('ending early')
  #sys.exit(0)
  return False

def tryMoveAfter(projectDir, originalSourceFolder, method1, method2, testedFiles, checkerToRun, apkLocation): 
  print('in try move after')
  for dirpath, dirnames, filenames in os.walk(projectDir):
    for filename in [f for f in filenames if f.endswith(".java")]:
      fileToTest = os.path.join(dirpath, filename)  
      if not fileToTest in testedFiles:
        testedFiles[fileToTest] = True
        foundAPossibleFix = moveFrontMethodAfterBackMethod(fileToTest, method1, method2)
        if foundAPossibleFix:
          print('testing: {0}'.format(fileToTest))
          isFixed = executeTestOfChangedApp(edittingFolder, checkerToRun, apkLocation)
          if isFixed:
            return True
          else:
            print('failed to fix with move after')
            createNewCopyOfTestProgram(originalSourceFolder)
  return False


def createNewCopyOfTestProgram(originalSourceFolder):
  #create a new directory if necessary
  #path is the location of the program to copy from
  if os.path.exists(edittingFolder):
    shutil.rmtree(edittingFolder)
  #try: 
  #  os.makedirs(path)
  #except OSError as e:
  #  print("Creation of the directory {0} failed".format(path))
  #  print(e)
  #  sys.exit(1)
  #distutils.dir_util.copy_tree("/Users/zack/git/DirectiveTool/testFolder/",path)
  #copy the application to the new directory
  shutil.copytree(originalSourceFolder, edittingFolder)
  return edittingFolder


def extractMethodInformation(sourceFile):
  with open(sourceFile,'r') as fin:
    #handles nested classes
    classNestingList = []
    currentNestingCount = 0
    currentClass = ''
    wasOneMoreThanClassNesting = False
    isOneMoreThanClassNesting = False
    for line in fin:
      lineItems = line.split(' ')
      foundClass = False
      foundClassInLine = False
      for i in lineItems:
        if foundClass:
          foundClass = False
          currentClass = i
        if i is 'class':
          foundClass = True
          foundClassInLine = True
      if foundClass:
        print('error: found class should not be true at this point')
      for c in line:
        if c == '{':
          currentNestingCount = currentNestingCount + 1
        elif c == '}':
          currentNestingCount = currentNestingCount - 1
          if currentNestingCount == nestingCountList[len(nestingCountList) - 1]:
            nestingCountList.pop()
      if foundClassInLine:
        nestCountList.append(currentNestingCount)
      if currentNestingCount == nestingCountList[0] + 1:
        isOneMoreThanClassNesting = True
      if isOneMoreThanClassNesting and not wasOneMoreThanClassNesting:
        pass





def performMethodOrderRepair(checkerName, checkerCommand, originalSourceFolder, apkLocation, methodOfInterest1, methodOfInterest2):
  #get code to edit
  #run directive check on it
  #either determine methods in the check or get them from a manual source
  #move the back method to before the originally first method
  #run the checker again
  #if that doesn't work, move the originally first method after the second method
  testFolder = createNewCopyOfTestProgram(originalSourceFolder)
  testedFiles = {}
  print('trying move before')
  isFixed = tryMoveBefore(testFolder, originalSourceFolder, methodOfInterest1, methodOfInterest2, testedFiles, checkerName, apkLocation)
  #try moving the back method before the original first method
  #check isFaulty again
  if not isFixed:
    testFolder = createNewCopyOfTestProgram(originalSourceFolder)
    testedFiles = {}
    print('trying move after')
    tryMoveAfter(testFolder, originalSourceFolder, methodOfInterest1, methodOfInterest2, testedFiles, checkerName, apkLocation)
    isFixed = executeTestOfChangedApp(edittingFolder, checkerName, apkLocation)
  #if isFaulty is true, then revert and move the first method behind the 
  #original last method
  if isFixed:
    print('Successfully fixed the problem')
    return True
  else:
    print('the problem was not fixed but the repair ended')
    return False

#def testMoveMethod():
#    moveBackMethodBeforePreviousMethod(fin.readlines(), methodOfInterest1, methodOfInterest2)
#    moveFrontMethodAfterBackMethod(fin.readlines(), methodOfInterest1, methodOfInterest2)

def getFileAndMethodWithProblem(callChains, projectDir):
  for chainItem in callChains[0]:
    if not chainItem.className.startswith('android.app'):
      classToGetMethodFrom = chainItem.className
      methodWithProblem = chainItem.methodName
      break
  methodWithProblem = re.sub(r'^[^ ]+\.','',methodWithProblem)
  methodWithProblem = re.sub(r'\w[\w\.]+\.','',methodWithProblem)
  methodWithProblem = re.sub(r'\(.*','',methodWithProblem)
  methodWithProblem = methodWithProblem + '('
  classItems = classToGetMethodFrom.split('.')
  fileBaseName = classItems[-1]
  if '$' in fileBaseName:
    fileBaseName=fileBaseName[:fileBaseName.index('$')]
  fileToGetMethodFrom = fileBaseName+".java"
  print(fileToGetMethodFrom)
  fullFileName = ''
  for dirpath, dirnames, filenames in os.walk(projectDir):
    for f in filenames:
      if f == fileToGetMethodFrom:
        fullFileName = os.path.join(dirpath, f)
        break
  if fullFileName == '':
    print('error finding the file name for file {0} in directory {1}'.format(fileToGetMethodFrom, projectDir))
    sys.exit(1)
  else:
    return fullFileName, methodWithProblem


#currently I am getting the file and method with problem every iteration and
#they don't change between each iteration, need to refactor the code
#to remove this unnessary calculation later
def moveLineToNewMethod(projectDir, methodToMove, moveLocationObj, callChains):
  print('in move line to new method')
  print('current project dir: {0}'.format(projectDir))
  fullFileName, methodWithProblem = getFileAndMethodWithProblem(callChains, projectDir)
  #print(fullFileName)
  #currently heuristically assuming that the next method call of the method of 
  #interest after seeing the method declaration is the wrong call
  foundMethodWithProblem = False
  fileWithoutLineToMove = []
  with open(fullFileName,'r') as fin:
    for line in fin:
      if foundMethodWithProblem:
        if methodToMove in line:
          lineToMove = line
        else:
          fileWithoutLineToMove.append(line)
      else:
        fileWithoutLineToMove.append(line)
        if 'onCreateView' in line:
          print('line: {0}, methodWithProblem: {1}, is in line: {2}'.format(line, methodWithProblem, methodWithProblem in line))
        #this check currently only works if the method with problem returns a void,
        #takes no arguments, and is only on a single line
        if methodWithProblem in line:
          #using next check (the statement ender) to differentiate statement 
          #ends and method declarations since I only want the method declaration
          if ';' not in line:
            foundMethodWithProblem = True
  #remove the faulty code line from the file to test
  with open(fullFileName,'w') as fout:
    for line in fileWithoutLineToMove:
      fout.write(line)
  #get the contents of the file to move the method to
  contentsOfFileWithAddedLine = []
  with open(moveLocationObj.fileName,'r') as fin:
    for line in fin:
      contentsOfFileWithAddedLine.append(line)
  print('moving |{0}| to line number {1} (method: {2}) in file: {3}'.format(lineToMove, int(moveLocationObj.lineNumber) + 1, moveLocationObj.methodName, moveLocationObj.fileName))
  #TODO SOON: this next line isn't working for some reason; or the file is 
  #not being correctly overwritten
  contentsOfFileWithAddedLine.insert(int(moveLocationObj.lineNumber) + 1, lineToMove)
  with open(moveLocationObj.fileName, 'w') as fout:
    for line in contentsOfFileWithAddedLine:
      fout.write(line)





  #for dirpath, dirnames, filenames in os.walk(projectDir):
  #  for filename in [f for f in filenames if f.endswith(".java")]:
  #    print('call chains: {0}'.format(callChains))
  #    print(callChains[0][0])
  #    print(callChains[0][0].className)
  #    print(callChains[0][0].methodName)
  #    if filename == callChains[0][0].className:
  #      print(filename)
      #fileToTest = os.path.join(dirpath, filename)
      #with open(fileToTest,'r') as fin:
        #for line in fin:
          #TODO: finish this once you have an idea for how to get the surrounding 
          #method of the failing call
          #pass
          #
def getInstantiationLines(fullFileName, projectDir, instantiationString):
  with open(fullFileName, 'r') as fin:
    for lineCount, line in enumerate(fin):
      if instantiationString in line:
        lineItems = line.split(' ')
        varName = lineItems[lineItems.index('=') - 1]
        yield lineCount,fullFileName, varName
  for dirpath, dirnames, filenames in os.walk(projectDir):
    for filename in [f for f in filenames if f.endswith(".java")]:
      if filename != fullFileName:
        with open(filename, 'r') as fin:
          for lineCount, line in enumerate(fin):
            if instantiationString in line:
              lineItems = line.split(' ')
              varName = lineItems[lineItems.index('=') - 1]
              yield lineCount, filename, varName 

 

def moveMethodToObjectInstantiation(projectDir, orignalSouceFolder, methodToMove, moveLocationObjList, callChains, checkerName, apkLocation):
  createNewCopyOfTestProgram(originalSourceFolder)
  fullFileName, methodWithProblem = getFileAndMethodWithProblem(callChains, projectDir)
  className = fullFileName.split(os.path.sep)[-1].split('.')[-2]
  instantiationString = "new {0}(".format(className)
  fileLines = []
  for (changeLine, changeFile, varName) in getInstantiationLines(fullFileName, projectDir, instantiationString):
    with open(changeFile, 'r') as fin:
      for line in fin:
        if methodToMove in line:
          lineToMove = line
        else:
          fileLines.append(line)
    lineToMove=lineToMove.lstrip()
    lineToMove = '{0}.{1}'.format(varName, lineToMove)
    print('line to move: {0}'.format(lineToMove))
    fileLines.insert(changeLine + 1, lineToMove)
    with open(changeFile, 'w') as fout:
      for line in fileLines:
        fout.write(line)
    #test the newly created file and break with a success if the test succeeds
    print('changed file: {0}'.format(changeFile))
    appWasFixed = executeTestOfChangedApp(projectDir, checkerName, apkLocation)
    print('app was fixed: {0}'.format(appWasFixed))
    #sys.exit(0)
    if appWasFixed:
      return True
  return False

  


def performMoveCallRepair(checkerName, checkerCommand, originalSourceFolder, apkLocation, methodOfInterest1, requiresAddingReference):
  #first I need to decide how much information the method repair has - should I 
  #implement a random method test? Or should I try to use information about the 
  #lifecycle. I also need to decide if I am only moving the method or the 
  #surrounding method call, but currently I'm deciding to move the surrounding
  #method call because certain calls, like getActivity, occur because the encompassing
  #method call is in the wrong place. Not getActivity specifically.

  #for getActivity, I want to move the call into a Fragment method; #for setArguments
  #I want to move the method call to a place where the Fragment has not been instantiated
  #yet

  #maybe first try moving the method call to right after the object is instantiated;
  #then try the method call in each of the methods in the that object.
  
  #see if method call of interest is called on an object. If so, get the type of the 
  #object, otherwise assume it is the type of the encapsulating class. Try to move
  #the method call to the first place the class is instantiated (maybe check for 
  #other places). After that, try to move the method to all the methods for the
  #class of the object.
  
  methodObjList = []
  testFolder = createNewCopyOfTestProgram(originalSourceFolder)
  unquotedAndQuotedList = runGetMethodLocations.split('"')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  commandList.append(testFolder)
  try: 
    #print(' '.join(commandList ))
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in commandOutput.stderr.decode('utf-8').splitlines():
      print(line)
    print('start of method information')
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      print(line)
      if line.strip() is not '':
        m = re.match(r"(.+), (.+), \(line (\d+),col (\d+)\), (.+)", line)
        if m:
          #print('{0}, {1}, {2}, {3}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
          methodObjList.append(MethodInfo(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
          print('saving item to method obj list')
        else:
          print('line did not match: {0}'.format(line))
    print('finished saving all the method information')
    print('found {0} method objs'.format(len(methodObjList)))
  except:
    pass
  print('calling execute and get call chains')
  #later, implement a way to handle multiple caught problems at the same time
  currentProblemCount, callChains = executeTestOfChangedAppAndGetCallChains(testFolder, checkerCommand, checkerName, apkLocation)
  #callChains start with the failing method and the class that method was defined in; then the next item holds the
  #class that incorrectly called the method
  #
  #for c in callChains[0]:
  #  print("call chain class: {0}, method {1}".format(c.className, c.methodName))
  #sys.exit(0)
  try:
    classWithProblem=callChains[0][-2].className.split('.')[-1]
  except IndexError:
    #print(callChains)
    #input('stopping to check call chain error')
    #I think I can just return a False here, because this problem should
    #only happen when running the wrong repair types for a detected issue
    print('unable to get class with problem from call chain item: {0}'.format(callChains))
    return False
  if currentProblemCount == -1:
    print('error: the changed app did not successfully execute')
  elif callChains == []:
    print('error: the call chains were not created')
  else: 
    l = len(methodObjList)
    print('number of method objs: {0}'.format(l))
    print('length of call chains: {0}'.format(len(callChains)))
    if requiresAddingReference:
      result = moveMethodToObjectInstantiation(testFolder, originalSourceFolder, methodOfInterest1, methodObjList, callChains, checkerName, apkLocation)
      if result:
        currentProblemCount = 0
    else:
      def testMethodObj(m):
        createNewCopyOfTestProgram(originalSourceFolder)
        print('calling move line to new method')
        moveLineToNewMethod(testFolder, methodOfInterest1, m, callChains)
        #alteredCallChains is not used; but I have to catch the return value
        currentProblemCount, alteredCallChains = executeTestOfChangedAppAndGetCallChains(testFolder, checkerCommand, checkerName, apkLocation)
        return currentProblemCount, alteredCallChains
      methodsInFileWithProblem = [ m for m in methodObjList if m.className == classWithProblem]
      print("methods in problematic file: {0}".format(len(methodsInFileWithProblem)))
      for m in methodsInFileWithProblem:
        print('*** moving to {0} in {1}'.format(m.methodName, m.className))
        currentProblemCount, alteredCallChains = testMethodObj(m)
        if currentProblemCount == 0:
          break
      if currentProblemCount != 0:
        methodsInFileWithOutProblem = [ m for m in methodObjList if m.className != classWithProblem]
        for m in methodsInFileWithOutProblem:
          currentProblemCount, alteredCallChains = testMethodObj(m)
          if currentProblemCount == 0:
            break
    if currentProblemCount == 0:
      print('successfully finished the repair!')
      return True
    else:
      return False
 
#for dirpath, dirnames, filenames in os.walk(projectDir):
#   for filename in [f for f in filenames if f.endswith(".java")]:
#
#     fileToTest = os.path.join(dirpath, filename)  
#     with open(fileToTest,'r') as fin:
#       for line in fin:
#          how to do I figure out if the call is valid or not, since these methods
#          might be used multiple times. I wonder if I can get the information from the 
#          checker; also, the checker already has lifecycle information, so it 
#          wouldn't be unreasonable to use the lifecycle information in the repair
#         if methodOfInterest1 in line:


if __name__ == "__main__":
  print('number of arguments: {0}'.format(len(sys.argv)))
  if len(sys.argv) < 5:
    print("Error: arguments must be (checkerToRun) (originalSourceFolder) (apkLocation) (methodOfInterest1) (optional: methodOfInterest2)")
  else:
    runFlowDroidCommand = sys.argv[1]
    #print(runFlowDroidCommand)
    #sys.exit(0)
    checkerToRun = sys.argv[2]
    originalSourceFolder = sys.argv[3]
    apkLocation = sys.argv[4]
    methodOfInterest1 = sys.argv[5]
    if len(sys.argv) > 6:
      methodOfInterest2 = sys.argv[6]
    else:
      methodOfInterest2 = None
  if methodOfInterest2 is not None:
    print('last argument: {0}'.format(methodOfInterest2))
    if methodOfInterest2 == 'REQUIRES_ADDING_OBJ_REF':
      result = performMoveCallRepair(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, True)
    else:
      result = performMethodOrderRepair(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, methodOfInterest2)
  else:
    result = performMoveCallRepair(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, False)
  if result:
    print('repair ended with application fixed')
    sys.exit(0)
  else:
    print('repair ended with application not fixed')
    sys.exit(1)
  #testMoveMethod()
