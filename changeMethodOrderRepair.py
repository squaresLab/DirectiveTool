#!/usr/local/bin/python3

import sys
import os
import os.path
import shutil
import subprocess
import re
import traceback


import levenshteinDistance
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
#- decided to leave them defined here, but edittingFolder is an optional paramater that can
#be overridden
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

  def __str__(self):
    return "class name: {0}, method name: {1}, line number: {2}, columnNumber: {3}, file name: {4}".format(self.className, self.methodName, self.lineNumber, self.columnNumber, self.fileName)

  def __repr__(self):
    return "class name: {0}, method name: {1}, line number: {2}, columnNumber: {3}, file name: {4}".format(self.className, self.methodName, self.lineNumber, self.columnNumber, self.fileName)



class CallChainItem:
  def __init__(self, className, methodName):
    self.className = className
    self.methodName = methodName 

  def __str__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)

  def __repr__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)


#I don't use this at the moment - I'm debating on refactoring the code so that 
#most of the method arguments are passed around in this object. However, I also
#need to figure out how to make the repair work on only one instance of the problem, 
#so maybe this is the way to do it.
class RunMethodOrderRepairItem:
  #This class stores the information required to run the method order repair
  #maybe it would make sense to break this information up, but I haven't figured
  #out the right way at the moment
  def __init__(self, checkerToRun, runFlowDroidCommand, originalSourceFolder, 
    apkLocation, methodOfInterest1, fileWithProblem = None, 
    methodOfInterest2 = None, 
    requiresObjectReferences = None, 
    #I think I have something like a line or method with problem; I need to look
    #into the best way to do it.
    lineWithProblem = None,
    methodWithProblem = None
     ):
    self.checkerToRun = checkerToRun
    self.runFlowDroidCommand = runFlowDroidCommand
    self.originalSourceFolder = originalSourceFolder
    self.apkLocation = apkLocation
    self.methodOfInterest1 = methodOfInterest1
    self.fileWithProblem = fileWithProblem
    self.methodOfInterest2 = methodOfInterest2
    self.requiresObjectReferences = requiresObjectReferences
    self.lineWithProblem = lineWithProblem
    self.methodWithProblem = methodWithProblem
    #if the testFolder is set, this will be the location where copies of the 
    #program is made and altered. If it is not set initially, it will get set to
    #edittingFolder at a later point in the code
    self.testFolder = None
    #I might eventually make this a parameter, but I'm currently leaving it to
    #get the value from the global variable
    self.checkerRootDir = checkerRootDir

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
  return foundChangeInFile

def extractProblemCountFromTestContents(testResultLines):
  #print(line)
  for line in testResultLines:
    if line.startswith('total number of caught problems:'):
      print(line)
      lineItems = line.split(' ')
      return int(lineItems[-1])
  return None

def buildAppWithGradle(repairItem):
  print("before build")
  currentDir = os.getcwd()
  os.chdir(repairItem.testFolder)
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
    #commandList = ['./gradlew','assembleDebug','--debug', '--stacktrace']
    #commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True)
    #print(commandOutput.stdout)
    os.chdir(currentDir)
    return False
  return True

def runCheckerAndGetOutput(repairItem):
  # I need to split by space but not on quoted parts of the string
  originalDir = os.getcwd()
  unquotedAndQuotedList = repairItem.runFlowDroidCommand.split('"')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  checkerToRun = 'analysis.{0}'.format(repairItem.checkerToRun)
  commandList.append(checkerToRun)
  if os.path.exists(repairItem.apkLocation):
    commandList.append(repairItem.apkLocation)
  else:
    repairItem.apkLocation = levenshteinDistance.findAPKInRepo(repairItem.testFolder, repairItem.apkLocation)
    commandList.append(repairItem.apkLocation)
  try: 
    print("current directory for command: {0}".format(os.getcwd()))
    print("running command: {0} {1} {2}".format("\"".join(unquotedAndQuotedList),checkerToRun, repairItem.apkLocation))
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
    testResultLines = []
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      testResultLines.append(line)
  except Exception as e: 
    print(e)
    testResultLines = []
  os.chdir(originalDir)
  return testResultLines

def parseCallChains(testResultLines):
  savingLines = False
  chainsInfo = []
  currentChain = []
  print('starting to create call chains')
  #handle either the multiple line print out case or the single List print out
  #case
  for line in commandOutput.stdout.decode('utf-8').splitlines():
    print('line from output: {0}'.format(line))
    if line.startswith('total number of caught problems:'):
      lineItems = line.split(' ')
      currentProblems = int(lineItems[-1])
    elif line.startswith('start of call chain'):
      savingLines = True
      currentChain = []
    elif line.startswith('end of call chain'):
      currentChain.reverse()
      #if not currentChain in chainsInfo:
      chainsInfo.append(currentChain.copy())
      print('length of chain added: {0}'.format(len(currentChain)))
      currentChain = []
      print('length of new call chain: {0}'.format(len(currentChain)))
      savingLines = False
    elif savingLines:
      m = re.match(r"<(.+): (.+)> .*", line)
      if m:
        currentChain.append(CallChainItem(m.group(1), m.group(2)))
      else:
          print("call chain line did not match: {0}".format(line))
    elif line.startswith('@@@@@ Found a problem:'):
      print('found problem line: {0}'.format(line))
      listSequenceMatch = re.match(r'.+List\((.+)\).*', line)
      if listSequenceMatch:
        print('found list: {0}'.format(listSequenceMatch.group(1)))
        callitems = re.findall(r'<([^>]+)>',listSequenceMatch.group(1))
        for c in callitems:
          #print(c)
          itemsInCall = c.split(':')
          currentChain.append(CallChainItem(itemsInCall[0], itemsInCall[1]))
          print('|{0}|'.format(chainsInfo))
        #currentChain.reverse()
        #if not currentChain in chainsInfo:
        print('length of new call chain: {0}'.format(len(currentChain)))
        chainsInfo.append(currentChain.copy())
        print('length of chain added: {0}'.format(len(currentChain)))
        currentChain = []
        #sys.exit(0)
  print('finished creating call chains')
  print('final problem count: {0}'.format(currentProblems))
  return chainsInfo

#This can probably be combined with the method call executeTestOfChangedApp but
#I'm unsure how at the moment and eventually decided it wasn't worth thinking 
#about any more
def executeTestOfChangedAppAndGetCallChains(repairItem):
  #TODO: figure out a reasonable return value for the number of problems in 
  #this case
  print('in execute test and get call chains')
  failedExecuteProblemCount = -1
  buildSucceeded = buildAppWithGradle(repairItem)
  if not buildSucceeded:
    return failedExecuteProblemCount, []
  testResultLines = runCheckerAndGetOutput(repairItem)
    #input('press enter when looking at output')
    #print(commandOutput)
    #print(commandOutput.stderr)
    #for line in commandOutput.stderr.decode('utf-8').splitlines():
      #print(line)
  chainsInfo = parseCallChains(testResultLines)
  os.chdir(currentDir)
  #print("succeeded - change: {0}, method {1}".format(change, method))
  print(chainsInfo)
  print(len(chainsInfo))
  input('stopping to check the current chain items')
  return currentProblems, chainsInfo

def executeTestOfChangedApp(repairItem):
  buildSucceeded = buildAppWithGradle(repairItem)
  if not buildSucceeded:
    return False
  testResultLines = runCheckerAndGetOutput(repairItem)
  problemCount = extractProblemCountFromTestContents(testResultLines)
  #I'll need to change this so that it can determine a fix for problem
  #counts greater than 1
  if problemCount == 0:
    #The problem was fixed!!
    return True
  else:
    return False
 #add the change to the method call of the copied app
 #run the application and see if it still produces the problem
 #if the application does not produce the problem, then print the change
 #that fixed the issue and stop

def repairTestThenResetInitializer(testFunction):
  def repairTestThenReset(repairItem, fileToTest):
    foundAPossibleFix = testFunction(fileToTest, repairItem.methodOfInterest1, repairItem.methodOfInterest2)
    if foundAPossibleFix:
      print('testing: {0}'.format(fileToTest))
      isFixed = executeTestOfChangedApp(repairItem)
      if isFixed:
        #don't reset if it is fixed so we can save the successful repair
        return True
      else: 
        #print('testing file: {0} failed'.format(fileToTest))
        #sys.exit(0)
        print('failed to fix with move before')
        createNewCopyOfTestProgram(repairItem)
        return False
  return repairTestThenReset


def testFileWithProblemOrFilesInRepo(repairItem, testMethod):
  repairTestThenResetCall = repairTestThenResetInitializer(testMethod)
  if repairItem.fileWithProblem is None:
    testedFiles = {}
    for dirpath, dirnames, filenames in os.walk(repairItem.testFolder):
      for filename in [f for f in filenames if f.endswith(".java")]:
        fileToTest = os.path.join(dirpath, filename)  
        #print('found a file: {0}'.format(fileToTest))
        if not fileToTest in testedFiles:
          #print('file not in tested files: {0}'.format(fileToTest))
          testedFiles[fileToTest] = True
          isFixed = repairTestThenResetCall(repairItem, fileToTest)
          if isFixed:
            return True
            #print('ending early')
    #sys.exit(0)
    return False
  else:
    return repairTestThenResetCall(repairItem, repairItem.fileWithProblem)


def tryMoveBefore(repairItem): 
  print('in try move before')
  return testFileWithProblemOrFilesInRepo(repairItem, moveBackMethodBeforePreviousMethod)

def tryMoveAfter(repairItem): 
  print('in try move after')
  return testFileWithProblemOrFilesInRepo(repairItem, moveFrontMethodAfterBackMethod)
  
def tryDeleteSecondCall(repairItem): 
  testedFiles = {}
  print('in try to delete second call')
  everFoundAChange = False
  for dirpath, dirnames, filenames in os.walk(repairItem.testFolder):
    for filename in [f for f in filenames if f.endswith(".java")]:
      fileToTest = os.path.join(dirpath, filename)  
      if not fileToTest in testedFiles:
        testedFiles[fileToTest] = True
        foundChangeInFile = False
        method1LineNumber = None
        method2LineNumber = None
        inBlockComments = False
        indentationCount = 0
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
            if method1LineNumber is None and repairItem.methodOfInterest1 in nonCommentPartOfLine:
              method1LineNumber = lineCount
            elif method2LineNumber is None and repairItem.methodOfInterest2 in nonCommentPartOfLine:
              method2LineNumber = lineCount
            if method1LineNumber is not None and method2LineNumber is not None:
              if method1LineNumber > method2LineNumber:
                lineNumberToDelete = method1LineNumber
              else:
                lineNumberToDelete = method2LineNumber
              lineToDelete = linesInFile[lineNumberToDelete]
              del linesInFile[lineNumberToDelete]
              print('deleted line {0} at line number {1} '.format(lineToDelete, lineNumberToDelete))
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
          everFoundAChange = True


  if everFoundAChange:
    print('testing: {0}'.format(fileToTest))
    isFixed = executeTestOfChangedApp(repairItem)
    if isFixed:
      return True
    else:
      print('failed to fix with deleting second line')
      input('stopping to see why delete failed')
            #I think I recopy the test program twice now; I should go through
            #the logic and test again.
      createNewCopyOfTestProgram(repairItem)
  return False

def updateRepairItemForNewCopy(repairItem):
  repairItem.apkLocaiton = repairItem.apkLocation.replace(repairItem.originalSourceFolder, repairItem.testFolder)
  if not repairItem.fileWithProblem is None:
    repairItem.fileWithProblem = repairItem.fileWithProblem.replace(repairItem.originalSourceFolder, repairItem.testFolder)


def createNewCopyOfTestProgram(repairItem, newTestFolder = None):
  #create a new directory if necessary
  #path is the location of the program to copy from

  #assume that if newTestFolder is defined, we want to make it the new
  #test folder in the future
  if not newTestFolder is None:
    repairItem.testFolder = newTestFolder
  if repairItem.testFolder is None:
    repairItem.testFolder = edittingFolder

  if os.path.exists(repairItem.testFolder):
    shutil.rmtree(repairItem.testFolder)
  #try: 
  #  os.makedirs(path)
  #except OSError as e:
  #  print("Creation of the directory {0} failed".format(path))
  #  print(e)
  #  sys.exit(1)
  #distutils.dir_util.copy_tree("/Users/zack/git/DirectiveTool/testFolder/",path)
  #copy the application to the new directory
  shutil.copytree(repairItem.originalSourceFolder, repairItem.testFolder)
  #make sure the repairItem's testFolder is in the right format
  resultFolder = repairItem.testFolder
  #make sure the return matches the style that originalSourceFolder was provided in
  if originalSourceFolder[-1] == os.path.sep and edittingFolder[-1] != os.path.sep:
    #add the path seperator
    resultFolder += os.path.sep
  elif originalSourceFolder[-1] != os.path.sep and edittingFolder[-1] == os.path.sep:
    #remove the path seperator
    resultFolder = resultFolder[:-1]
  repairItem.testFolder = resultFolder
  updateRepairItemForNewCopy(repairItem)



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





def performMethodOrderRepair(repairItem):
  #get code to edit
  #run directive check on it
  #either determine methods in the check or get them from a manual source
  #move the back method to before the originally first method
  #run the checker again
  #if that doesn't work, move the originally first method after the second method

  print('in method order repair')
  createNewCopyOfTestProgram(repairItem)
  print('trying move before')
  #try moving the back method before the original first method
  isFixed = tryMoveBefore(repairItem)
  if not isFixed:
    #if the application is not fixed, then revert and move the first method behind the 
    #original last method
    #testFolder = createNewCopyOfTestProgram(originalSourceFolder)
    #apkLocation = apkLocation.replace(originalSourceFolder,testFolder)
    print('trying move after')
    isFixed = tryMoveAfter(repairItem)
  if not isFixed:
    #testFolder = createNewCopyOfTestProgram(originalSourceFolder)
    #apkLocation = apkLocation.replace(originalSourceFolder,testFolder)
    print('trying to delete the second method call')
    isFixed = tryDeleteSecondCall(repairItem)
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
  #removing the first item from the call chain because it's often the failing method
  #and not the location of the failing method
  #the call chain seems reversed in getActivity. Maybe I need to make them ordered
  #the same way
  innerClassWithProblem = None
  for chainItem in list(reversed(callChains[0]))[1:]:
    if not chainItem.className.startswith('android.app'):
      classToGetMethodFrom = chainItem.className
      methodWithProblem = chainItem.methodName
      break
  print('editing method with problem')
  methodWithProblem = re.sub(r'^[^ ]+\.','',methodWithProblem)
  methodWithProblem = re.sub(r'\w[\w\.]+\.','',methodWithProblem)
  methodWithProblem = re.sub(r'\(.*','',methodWithProblem)
  methodWithProblem = methodWithProblem + '('
  print('method with problem after editing: {0}'.format(methodWithProblem))
  classItems = classToGetMethodFrom.split('.')
  fileBaseName = classItems[-1]
  if '$' in fileBaseName:
    nameItems = fileBaseName.split('$')
    fileBaseName=nameItems[0]
    innerClassWithProblem = nameItems[1]

  print('file base name: {0}'.format(fileBaseName))
  fileToGetMethodFrom = fileBaseName+".java"
  print(fileToGetMethodFrom)
  fullFileName = ''
  for dirpath, dirnames, filenames in os.walk(projectDir):
    for f in filenames:
      if f == fileToGetMethodFrom:
        fullFileName = os.path.join(dirpath, f)
        print('found full file name: {0}'.format(fullFileName))
        break
  if fullFileName == '':
    print('error finding the file name for file {0} in directory {1}'.format(fileToGetMethodFrom, projectDir))
    sys.exit(1)
  else:
    return fullFileName, methodWithProblem, innerClassWithProblem

#this method tries to extract the lines in the file needed to make the lineToMove
#compile in a new method, but does so heuristically, so it's not perfect
def getLineToMoveDependencies(fullFileName, lineToMove):
  #get the variables in the line
  paramString = lineToMove.split('(')[-1].split(')')[0]
  if paramString == '':
    #didn't find any dependencies so just return the original line
    return [lineToMove]
  else:
    paramItems = paramString.split(',')
    totalDependencyLines = []
    totalTryLines = []
    for p in paramItems:
      p = p.strip()
      dependencyLineTuples = []
      nestingCount = 0
      tryTuples = []
      nestingToRecord = []
      try:
        with open(fullFileName, 'r') as fin:
          for lineCount,line in enumerate(fin):
            if p in line:
              dependencyLineTuples.append((line, lineCount))
            testLine = line.strip()
            if testLine.startswith('try'):
              tryTuples.append(('try',lineCount,nestingCount, line))
              nestingToRecord.append(nestingCount)
            elif testLine.startswith('catch'):
              tryTuples.append(('catch',lineCount,nestingCount, line))
              nestingToRecord.append(nestingCount)
            for c in line:
              if c == '{':
                nestingCount += 1
              if c == '}':
                nestingCount -= 1
            if nestingCount in nestingToRecord:
              nestingToRecord.remove(nestingCount)
              tryTuples.append(('end',lineCount, nestingCount, line))
      except Exception:
        #This try except probably isn't needed anymore. I had a misnamed variable
        #issue that I couldn't figure out, so I added this. I think everything is
        #fixed now, but leaving it just in case
        print(e)
        traceback.print_exc()
        input('stop to check the exception')
      #now that I have the try catch blocks, try to determine the ones I need
      #to copy over  
      tryLinesToAdd = []
      endCountSavedInTry = 0
      #savingTry = False
      nestCountToSave = None
      #print(dependencyLineTuples)
      #print(tryTuples)
      for t in tryTuples:
        if t[0] == 'try':
          #if the try statement is right before a line to add, add the try end, and catch
          #to the lines to add
          if t[1]+1 in [lineCountToAdd for line, lineCountToAdd in dependencyLineTuples]:
            tryLinesToAdd.append(t)
            nestCountToSave = t[2]
        elif nestCountToSave != None:
          if t[2] == nestCountToSave:
            tryLinesToAdd.append(t)
            if t[0] == 'end':
              endCountSavedInTry += 1
              #currently only gets one catch statement
              if endCountSavedInTry == 2:
                nestCountToSave = None
      totalTryLines.extend(tryLinesToAdd)
      totalDependencyLines.extend(dependencyLineTuples)
    #combine the full lists in sorted order, also this should remove duplicates
    #in the lists
    fullLinesToAddDict = {} 
    for t in totalTryLines:
      fullLinesToAddDict[t[1]] = t[3]
    for d in totalDependencyLines:
      fullLinesToAddDict[d[1]] = d[0]
    finalLineList = []
    for k in sorted(fullLinesToAddDict.keys()):
      finalLineList.append(fullLinesToAddDict[k])
    print(finalLineList)
    return finalLineList

#the method with problem string is really messed up for methods in nested classes
#for example the onCreate method in MyPreferenceFragment is
#lambda$onCreate$0$SettingsActivity$MyPreferenceFragment
#just extract the onCreate part and the inner class name
def cleanMethodWithProblem(methodWithProblem):
  if '$' in methodWithProblem:
    methodItems = methodWithProblem.split('$')
    #the inner class name, then the method
    return methodItems[-1] + '$' + methodItems[1]
  else:
    return methodWithProblem

  


#currently I am getting the file and method with problem every iteration and
#they don't change between each iteration, need to refactor the code
#to remove this unnessary calculation later

#I also need to change the code to move any variable initializations that it
#depends on with it; doing that now
def moveLineToNewMethod(projectDir, methodToMove, moveLocationObj, callChains):
  print('in move line to new method')
  print('current project dir: {0}'.format(projectDir))
  fullFileName, methodWithProblem, innerClassWithProblem = getFileAndMethodWithProblem(callChains, projectDir)
  print('before clean method to watch')
  #I think I should move this functionality to getFileAndMethod
  #methodWithProblem = cleanMethodWithProblem(methodWithProblem)
  #if '$' in methodWithProblem:
  #  methodItems = methodWithProblem.split('$')
  #  methodWithProblem = methodItems[1]
  #  innerClassWithProblem = methodItems[0]
  #else:
  #  innerClassWithProblem = None
  print('after setting clean method stuff')
  #print(fullFileName)
  #currently heuristically assuming that the next method call of the method of 
  #interest after seeing the method declaration is the wrong call
  foundMethodWithProblem = False
  foundInnerClassWithProblem = False
  fileWithoutLineToMove = []
  lineToMove = None
  print('trying to open: {0}'.format(fullFileName))
  print('innerClassWithProblem: {0}'.format(innerClassWithProblem))
  input('stopping here to watch')
  with open(fullFileName,'r') as fin:
    for lineCount, line in enumerate(fin):
      print(line)
      if foundMethodWithProblem and (innerClassWithProblem is None or foundInnerClassWithProblem):
        if methodToMove in line:
          print('found method to move ({0}) in line: {1}'.format(methodToMove, lineCount))
          lineToMove = line
        else:
          fileWithoutLineToMove.append(line)
      else:
        fileWithoutLineToMove.append(line)
        #this check currently only works if the method with problem returns a void,
        #takes no arguments, and is only on a single line
        if methodWithProblem in line:
          #using next check (the statement ender) to differentiate statement 
          #ends and method declarations since I only want the method declaration
          if ';' not in line:
            foundMethodWithProblem = True
        if (not innerClassWithProblem is None) and innerClassWithProblem in line:
          foundInnerClassWithProblem = True
  if lineToMove is None:
    print('error: never found method to move {0} in file {1}'.format(methodToMove, fullFileName))
    input('stop to check this error')
  else:
    print('calling line to move with dependencies')
    lineToMoveWithDependencies = getLineToMoveDependencies(fullFileName, lineToMove)
  #remove the faulty code line from the file to test
  with open(fullFileName,'w') as fout:
    for line in fileWithoutLineToMove:
      fout.write(line)
  #get the contents of the file to move the method to
  contentsOfFileWithAddedLine = []
  with open(moveLocationObj.fileName,'r') as fin:
    for line in fin:
      contentsOfFileWithAddedLine.append(line)
  #TODO SOON: this next line isn't working for some reason; or the file is 
  #not being correctly overwritten
  #contentsOfFileWithAddedLine.insert(int(moveLocationObj.lineNumber) + 1, lineToMove)
  #making it two to give room for longer function declarations - might eventually want
  #to count how long the function declaration is and adjust later
  insertLocation = int(moveLocationObj.lineNumber) + 2
  contentsOfFileWithAddedLine[insertLocation: insertLocation] = lineToMoveWithDependencies
  with open(moveLocationObj.fileName, 'w') as fout:
    for line in contentsOfFileWithAddedLine:
      fout.write(line)
  print('rewrote {0}'.format(moveLocationObj.fileName))
  input('stop to check the rewrite')





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
  #first check if the fix can be moved to a method in the current file
  with open(fullFileName, 'r') as fin:
    for lineCount, line in enumerate(fin):
      if instantiationString in line:
        lineItems = line.split(' ')
        varName = lineItems[lineItems.index('=') - 1]
        yield lineCount,fullFileName, varName
  #otherwise, see if the method can moved to a method in the other java files
  for root, dirnames, filenames in os.walk(projectDir):
    for filename in [os.path.join(root,f) for f in filenames if f.endswith(".java")]:
      if filename != fullFileName:
        with open(filename, 'r') as fin:
          for lineCount, line in enumerate(fin):
            if instantiationString in line:
              lineItems = line.split(' ')
              varName = lineItems[lineItems.index('=') - 1]
              yield lineCount, filename, varName 

 

def moveMethodToObjectInstantiation(repairItem, callChains):
  createNewCopyOfTestProgram(repairItem)
  
  #might eventually save these returns into the repairItem
  fullFileName, methodWithProblem, innerClassWithProblem = getFileAndMethodWithProblem(callChains, repairItem.testDir)
  className = fullFileName.split(os.path.sep)[-1].split('.')[-2]
  instantiationString = "new {0}(".format(className)
  fileLines = []
  lineToMove = None
  for (changeLine, changeFile, varName) in getInstantiationLines(fullFileName, repairItem.testDir, instantiationString):
    with open(changeFile, 'r') as fin:
      for line in fin:
        if repairItem.methodOfInterest1 in line:
          lineToMove = line
        else:
          fileLines.append(line)
    if lineToMove is None:
      print('unable to find method to move {0} in {1}'.format(methodToMove, changeFile))
      input('stopping to check if this is an error or not')
      return False
    lineToMove=lineToMove.lstrip()
    lineToMoveWithDependencies = getLineToMoveDependencies(changeFile, lineToMove)
    for lCount, l in enumerate(lineToMoveWithDependencies):
      if methodToMove in l:
        lineToMoveWithDependencies[lCount] = '{0}.{1}'.format(varName, l)
    insertLocation = changeLine + 1
    fileLines[insertLocation:insertLocation] = lineToMoveWithDependencies
    with open(changeFile, 'w') as fout:
      for line in fileLines:
        fout.write(line)
    #test the newly created file and break with a success if the test succeeds
    print('changed file: {0}'.format(changeFile))
    input('stop to check file changed with object instance added')
    appWasFixed = executeTestOfChangedApp(repairItem)
    print('app was fixed: {0}'.format(appWasFixed))
    #sys.exit(0)
    if appWasFixed:
      return True
  return False

#I might eventually move callChains into the repairItem object. So I'll need
#to refactor this method at that time if I do 
def testMethodObj(repairItem, m, callChains):
  createNewCopyOfTestProgram(repairItem)
  moveLineToNewMethod(repairItem.testFolder, repairItem.methodOfInterest1, m, callChains)
  #alteredCallChains is not used; but I have to catch the return value
  currentProblemCount, alteredCallChains = executeTestOfChangedAppAndGetCallChains(repairItem)
  return currentProblemCount, alteredCallChains
 


def performMoveCallRepair(repairItem):
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
  createNewCopyOfTestProgram(repairItem)
  unquotedAndQuotedList = runGetMethodLocations.split('"')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  commandList.append(repairItem.testFolder)
  try: 
    #print(' '.join(commandList ))
    commandOutput = subprocess.run(commandList, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      if line.strip() is not '':
        m = re.match(r"(.+), (.+), \(line (\d+),col (\d+)\), (.+)", line)
        if m:
          #print('{0}, {1}, {2}, {3}'.format(m.group(1), m.group(2), m.group(3), m.group(4)))
          methodObjList.append(MethodInfo(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
          print('saving item to method obj list')
        else:
          print('line did not match: {0}'.format(line))
  except:
    pass
  print('calling execute and get call chains')
  #later, implement a way to handle multiple caught problems at the same time
  currentProblemCount, callChains = executeTestOfChangedAppAndGetCallChains(repairItem)
  #I could probably later change this to use the method of interest to get the class with problem
  #if I wanted
  if callChains == []:
    print('no call chain')
    return False
  #callChains start with the failing method and the class that method was defined in; then the next item holds the
  #class that incorrectly called the method
  #
  #for c in callChains[0]:
  #  print("call chain class: {0}, method {1}".format(c.className, c.methodName))
  #sys.exit(0)
  try:
    #the first call is always the exact failing method, but I want the location
    #where the failing method occurred. Also, the list is assumed to be ordered 
    #where the failing method call is at the end.
    classWithProblem=callChains[0][-2].className.split('.')[-1]
    #try to handle nested classes - although I'm not sure what I'm doing at the 
    #moment will fully support them or if this will just die later
    innerClassWithProblem = None
    if '$' in classWithProblem:
      classItems = classWithProblem.split('$')
      classWithProblem = classItems[0]
      innerClassWithProblem = classItems[1]
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
    #print('number of method objs: {0}'.format(l))
    #print('length of call chains: {0}'.format(len(callChains)))
    #print(requiresAddingReference)
    #input('stopping to see this value')
    if repairItem.requiresObjectReferences:
      print('method of interest1 before call: {0}'.format(repairItem.methodOfInterest1))
      result = moveMethodToObjectInstantiation(repairItem, callChains)
      if result:
        currentProblemCount = 0
    else:
      methodsInFileWithProblem = [ m for m in methodObjList if m.className == classWithProblem]
      if innerClassWithProblem is not None:
        methodsInInnerClass = [m for m in methodObjList if m.className == innerClassWithProblem]
        methodsInFileWithProblem.extend(methodsInInnerClass)
      if len(methodsInFileWithProblem) < 1:
        print('error: unable to find methods in problematic file: {0}'.format(classWithProblem))
        input('stopping to check error')
      for m in methodsInFileWithProblem:
        currentProblemCount, alteredCallChains = testMethodObj(repairItem, m, callChains)
        if currentProblemCount == 0:
          break
      if currentProblemCount != 0:
        methodsInFileWithOutProblem = [ m for m in methodObjList if m.className != classWithProblem]
        for m in methodsInFileWithOutProblem:
          currentProblemCount, alteredCallChains = testMethodObj(repairItem, m, callChains)
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

#eventually need to expand this with an arg parser to add the possible options for
#running the repair
if __name__ == "__main__":
  print('number of arguments: {0}'.format(len(sys.argv)))
  if len(sys.argv) < 5:
    print("Error: arguments must be (checkerToRun) (originalSourceFolder) (apkLocation) (methodOfInterest1) (optional: methodOfInterest2) (optional: edittingFolder)")
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
      if methodOfInterest2 == 'None':
        methodOfInterest2 = None
    else:
      methodOfInterest2 = None
    if len(sys.argv) > 7:
      #This section is already global, so I don't need to declare edittingFolder
      #as global
      edittingFolder = sys.argv[7]
  if methodOfInterest2 is not None:
    print('last argument: {0}'.format(methodOfInterest2))
    if methodOfInterest2 == 'REQUIRES_ADDING_OBJ_REF':
      #reference constructor for the repair items
      #self, checkerToRun, runFlowDroidCommand, originalSourceFolder, 
    #apkLocation, methodOfInterest1, fileWithProblem, 
    #methodOfInterest2 = None, 
    #requiresObjectReferences = None, 
    #lineWithProblem = None,
    #methodWithProblem = None
      repairItem = RunMethodOrderRepairItem(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, requiresObjectReferences = True)
      result = performMoveCallRepair(repairItem)
    else:
      repairItem = RunMethodOrderRepairItem(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, methodOfInterest2= methodOfInterest2)
      result = performMethodOrderRepair(repairItem)
  else:
    repairItem = RunMethodOrderRepairItem(checkerToRun, runFlowDroidCommand, originalSourceFolder, apkLocation, methodOfInterest1, requiresObjectReferences = False)
    result = performMoveCallRepair(repairItem)
  if result:
    print('repair ended with application fixed')
    sys.exit(0)
  else:
    print('repair ended with application not fixed')
    sys.exit(1)
  #testMoveMethod()
