#!/usr/local/bin/python3

import re
import os
import sys
import shlex
import subprocess

buildAppCommand = shlex.split('./gradlew -Dorg.gradle.java.home=/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home assembleDebug')
permissionCommand = shlex.split('chmod +x gradlew')

class CallChainItem:
  def __init__(self, className, methodName):
    self.className = className
    self.methodName = methodName 

  def __str__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)

  def __repr__(self):
    return "class name: {0}, method name: {1}".format(self.className, self.methodName)

class ProblemInfo:
  def __init__(self):
    #debating if I should have a field to let me know what other fields are
    #defined. Leaving it out right now, but may add it back in
    self.methodName = None
    self.innerClassName = None
    self.outerClassName = None
    self.chainsInfo = None
    self.className = None

  def __str__(self):
    return 'method name: {0}, inner class name: {1}, outer class name: {2}, chains info: {3}, class name: {4}'.format(self.methodName, self.innerClassName, self.outerClassName, self.chainsInfo, self.className)

  def __rep__(self):
    return self.__str__()

  def __eq__(self, other):
    if other is self:
      return True
    elif type(other) is type(self):
        return self.__dict__ == other.__dict__
    else:
      return False

#class ProblemSetk:
  #def __init__(self):
    #pass

  def getFilenameWithProblem(self):
    if not self.outerClassName is None:
      return '{0}.java'.format(self.outerClassName)
    elif not self.className is None:
      return '{0}.java'.format(self.className)
    elif not self.chainsInfo is None:
      for chainItem in list(reversed(callChains[0]))[1:]:
        if not chainItem.className.startswith('android.app'):
          classToGetMethodFrom = chainItem.className
          classItems = classToGetMethodFrom.split('.')
          fileBaseName = classItems[-1]
          if '$' in fileBaseName:
            nameItems = fileBaseName.split('$')
            fileBaseName=nameItems[0]
          fileToGetMethodFrom = fileBaseName+".java"
          return fileToGetMethodFrom
    else:
      #really shouldn't throw an error for this case till I update the checker 
      #outputs; currently some checkers don't define problem files in the output
      #since knowledge of the problem file isn't needed to repair that issue
      return None

def checkForSootError(checkerResult):
  for line in checkerResult.stderr.decode('utf-8').splitlines():
    if line.startswith('[main] ERROR soot'):
      return True
    if 'ERROR soot' in line:
      print(line)
      input('stop to see the error line')
  print('did not find a soot error')
  return False


def getChainListFromLine(line):
  currentChain = []
  listSequenceMatch = re.match(r'.+List\((.+)\).*', line)
  if listSequenceMatch:
    #print('found list: {0}'.format(listSequenceMatch.group(1)))
    callitems = re.findall(r'<([^>]+)>',listSequenceMatch.group(1))
    for c in callitems:
      #print(c)
      itemsInCall = c.split(':')
      currentChain.append(CallChainItem(itemsInCall[0], itemsInCall[1]))
      #print('length of chain added: {0}'.format(len(currentChain)))
  return currentChain

def parseCallChains(testResultLines):
  savingLines = False
  chainsInfo = []
  currentChain = []
  print('starting to create call chains')
  #handle either the multiple line print out case or the single List print out
  #case
  for line in testResultLines:
    #print('line from output: {0}'.format(line))
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
      #print('length of chain added: {0}'.format(len(currentChain)))
      currentChain = []
      #print('length of new call chain: {0}'.format(len(currentChain)))
      savingLines = False
    elif savingLines:
      m = re.match(r"<(.+): (.+)> .*", line)
      if m:
        currentChain.append(CallChainItem(m.group(1), m.group(2)))
      else:
          print("call chain line did not match: {0}".format(line))
    elif line.startswith('@@@@@ Found a problem:'):
      #print('found problem line: {0}'.format(line))
        chainsInfo.append(getChainListFromLine(line))
        #sys.exit(0)
  #print('finished creating call chains')
  #print('final problem count: {0}'.format(currentProblems))
  return chainsInfo

#I can't decide if I should iterate through the checker output or just have it 
#work on a single line, trying to see if iterating over the full output is too 
#slow
def extractProblemCountFromCheckerOutput(checkerOutputLines):
  for line in checkerOutputLines:
    if line.startswith('total number of caught problems'):
      errorCount = int(line.split()[-1]) 
      return errorCount
  return None

def extractProblemInfoFromEndOfLine(line):
  pi = ProblemInfo()
  lineItems = line.split(' ') 
  className = lineItems[-1]
  pi.clasName = className
  return pi

#This tries to extract whatever information can be found from the different
#problem reports
#Also, I'm not sure if it's better to prevent repeats from being added to
#the problemSet or not. If the checker lines include the stderr output with 
#the stdout output, then every problem may be reported twice, however, the
#problem information here may not be granular enough to determine each error
#individually and throwing out repeats may suppress an error state I need to 
#handle. Decided to currently throw out repeats.
def extractProblemInfoFromCheckerOutput(checkerOutputLines):
  chainsInfo = None
  problemList = list()
  for line in checkerOutputLines:
    if line.startswith('@@@@@ Found a problem: calling getResources'):
      pi = ProblemInfo()
      lineItems = line.split(' ')
      #s"@@@@@ Found a problem: calling getResources on a background fragment in ${m.getName()} of ${cl.getName()} with outer Fragment class ${cl.getOuterClass.getName}" 
      pi.methodName = lineItems[-8]
      pi.innerClassName = lineItems[-6]
      pi.outerClassName = lineItems[-1]
      if not pi in problemList:
        problemList.append(pi)
    elif line.startswith('@@@@@ Found a problem:'):
      chainsInfo = getChainListFromLine(line)
      if chainsInfo == []:
        chainsInfo = None
      else:
        pi = ProblemInfo()
        pi.chainsInfo = chainsInfo
        if not pi in problemList:
          problemList.append(pi)
      if chainsInfo is None:
        pi = extractProblemInfoFromEndOfLine(line)
        if not pi in problemList:
          problemList.append(pi)
    elif line.startswith('@@@@@ problem:'):
      pi = extractProblemInfoFromEndOfLine(line)
      if not pi in problemList:
        problemList.append(pi)
 
  #check that at least one source of information was found
  #if methodName is None and innerClassName is None and outerClassName is None \
  #  and chainsInfo is None and className is None:
  #This case can happen if there are no problems found by the checker
  #if len(problemList) < 1:
    #print('error: no information extracted from checker output')
    #outputFile = os.path.join(os.getcwd(),'checkerOutputWithoutProblemInfo.txt')
    #with open(outputFile, 'w') as fout:
      #for line in checkerOutputLines:
        #print(line, file=fout,end='')
    #print('saved checker output to file: {0}'.format(outputFile))
    #sys.exit(1)
  return problemList

#eventually, I should figure out how to keep this up to date with the important
#lines extracted in other functions, when created this is manually up to date with
#extractProblemInfo and extractProblemCount

#This is an optimization method designed to remove the important lines from the
#checker output, so other methods that look for information in the checker output
#don't have to scan every line every time
def extractImportantCheckerLines(checkerOutputLines):
  importantLines = []
  for line in checkerOutputLines:
    if line.startswith('@@@@@ Found a problem:'):
      importantLines.append(line)
    elif line.startswith('total number of caught problems'):
      importantLines.append(line)
    elif line.startswith('@@@@@ problem:'):
      importantLines.append(line)
  return importantLines


#If you are getting an error, you might need to 
def buildApp(repoDir):
  originalDir = os.getcwd()
  os.chdir(repoDir)
  if not os.path.exists('./gradlew'):
    print('unable to find the gradle build file in directory: {0}'.format(repoDir))
    os.chdir(originalDir)
    return []
  try:
    buildResult = subprocess.run(buildAppCommand, capture_output=True)
    print('built app')
  except PermissionError as p:
    subprocess.run(permissionCommand, capture_output=True)
    buildResult = subprocess.run(buildAppCommand, capture_output=True)
  #for line in buildResult.stdout.decode('utf-8').splitlines():
    #print(line)
  possibleBuildFiles = []
  buildFilesToCheck = []
  print('finding apks in : {0}'.format(os.getcwd()))
  for root, dirs, files in os.walk('.', topdown=False):
    for f in files:
      if f.endswith('.apk'):
        possibleBuildFiles.append(os.path.join(os.getcwd(), root,f))
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


