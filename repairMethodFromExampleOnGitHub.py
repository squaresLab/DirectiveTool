#!/usr/local/bin/python3

import sys
from bs4 import BeautifulSoup
import requests
import time
import subprocess
import json
#import urllib.request
import urllib
import os
import os.path
import itertools
#import distutils.dir_util
import shutil
import determineMethodDifferences
import operator
import traceback
import levenshteinDistance
import shlex
import utilitiesForRepair

#GitHub seems to require me to log in now to search the repos
#def loginToGitHub(session):

  #url = 'https://github.com/session' 
  #session.get(url)
  #response = BeautifulSoup(session.get(url).content,'html.parser')
  #hidden = response.find("input", {'name': 'utf8'})['value']
  #print(token)
  #login_data = dict(login_field='ZackC', password='cde3XSW@zaq1', authenticity_token=token, utf8=hidden)
  #with session.post(url, data=login_data) as r:
  #  print(r)
  #  print(r.cookies)
    #print(session.cookies)
  #next four lines are repeated here for testing - delete later
  #time.sleep(1)
  #urlToSearch='https://github.com/search?l=Java&q=onCreate+&type=Code'
  #print(r.cookies)
  #print(session.cookies)
  #session.cookies['logged_in'] = 'yes'
  #print(session.cookies)
  #response = session.get(urlToSearch).content.decode('utf-8')
  #for line in response.splitlines():
  #  print(line)

#with requests.Session() as session:
#loginToGitHub(session)

#Might need to add support for default variable types in the type list
#and add more support for nested methods in other methods

printingSearchUpdates = True

debugCounter = 0
printingDebugInfo = False
#containsFalse = False

#checkerToRun='DetectMissingSetHasOptionsMenu'
#checkerToRun='DetectInvalidInflateCallMain'
#runFlowDroidCommand= '/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=59095:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-cmd/target/scala-2.12/classes'

#fileToChange = "/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/src/main/java/com/example/android/lnotifications/HeadsUpNotificationFragment.java" 
#fileToChange = "/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/src/main/java/com/example/android/lnotifications/VisibilityMetadataFragment.java" 
#originalFileToChange = "/Users/zack/git/DirectiveTool/testFolder/Application/src/main/java/com/example/android/lnotifications/VisibilityMetadataFragment.java" 


#I should consider putting the created files in there own directory so it
#is easier to keep track of them if the script fails without deleting the files
createdFileListToDelete = []
#methodDeclarationStringToCompare = "public void onCreate" 
#methodDeclarationStringToCompare = "public void onViewCreated" 
#I can't think of a better variable name at the moment, might want to change
#later since I'm currently not happy with it
#methodSpecification = "public View"
#methodDeclarationStringToCompare = "{0} onCreateView".format(methodSpecification)
#set to False to use the diff comparison method - add lines that are different to
#the current method
#set to True to use the type name and method name line differences - add or remove
#lines with different method or types
useAdvancedDiff = True

doingExtraCheck = False
#doingExtraCheck = True

tempDebuggingBool = False


#need to make this a parameter later
shouldCheckForFragment = False

#this is the default experiment folder if testFolder is not defined
experimentFolder = "/Users/zack/git/DirectiveTool/temporaryTestOfChange"

runFlowDroidFolder = "/Users/zack/git/DirectiveTool/FlowDroidTest"

class GitHubRepairItem:
  def __init__(self,runFlowDroidCommand, checkerToRun, methodDeclarationStringToCompare, originalFolder, fileToChange, newAPKLocation, termsOfInterest, savedDataDirectory = None, testFolder = None, problemInfoList = None):
    self.runFlowDroidCommand = runFlowDroidCommand
    self.checkerToRun = checkerToRun
    self.methodDeclarationStringToCompare = methodDeclarationStringToCompare
    self.originalFolder = originalFolder
    self.fileToChange = fileToChange
    self.newAPKLocation = newAPKLocation
    self.termsOfInterest = termsOfInterest
    self.savedDataDirectory = savedDataDirectory
    self.methodsToCompare = []
    self.testFolder = testFolder
    #eventually create a way to set this
    self.runFlowDroidFolder = runFlowDroidFolder
    self.problemInfoList = problemInfoList

#TODO: some of these parameter lists are getting large. I should probably group
#them into an object to reduce the line sizes and improve readability

def saveLines(linesToSave, nestingCount, line): 
  linesToSave.append(line)
  for c in line:
    if c == '{':
      nestingCount = nestingCount + 1
    if c == '}':
      nestingCount = nestingCount - 1
  return (linesToSave, nestingCount)

def extractOriginalMethodsOfInterest(repairItem):
  #I was going to search all Java files in the original project, 
  #but then I remembered that the checker prints out the file 
  #name with the problem, so finding all methods isn't needed
  #
  #I will need to later extract the file name of interest from the 
  #error message, but I'll hard code it now for development speed
  #since I probably need to make it easier to extract the class
  #name from the error message before I write code to extract the 
  #error message
  #
  #originalApplicationLocation = "/Users/zack/git/DirectiveTool/testFolder"
  #filesOfInterest = []j
  #for root, directories, filenames = os.walk(originalApplicationLocation):
    #for file in filenames:
      #if file.endswith('.java'):
        #Can't remember if I need to add the path seperator betweeen the
        #two variables or not
        #filesOfInterest.append(root+os.path.sep+file)
  #fileToExtractFrom = originalFileToChange
  print('file to change: {0}'.format(repairItem.fileToChange))
  #at this time, use original folder, because we haven't copied anything to the
  #test folder
  print('project dir: {0}'.format(repairItem.originalFolder))
  repairItem.fileToChange = utilitiesForRepair.getFilesFullPath(repairItem.originalFolder, repairItem.fileToChange)
  print('file to extract from: {0}'.format(repairItem.fileToChange))
  #input('confirming that file extracted from is the one injected into')
  #print('file to extract from: {0}'.format(fileToExtractFrom))
  with open(repairItem.fileToChange,'r') as fin:
    nestingCountWasGreaterThanZero = False
    nestingCount = 0
    linesToSave = []
    foundMethodOfInterest = False
    for line in fin:
      if foundMethodOfInterest or nestingCount > 0:
        (linesToSave, nestingCount) = saveLines(linesToSave, nestingCount, line)
        #only use foundMethodOfInterest until we find the first { of the method
        if nestingCount > 0:
          nestingCountWasGreaterThanZero = True
          foundMethodOfInterest = False
              #this string check captures both the onCreate method and the onCreateOptionsMenu method
      elif repairItem.methodDeclarationStringToCompare and repairItem.methodDeclarationStringToCompare in line:
        methodName = line.split()[2].split('(')[0]
        (linesToSave, nestingCount) = saveLines(linesToSave, nestingCount, line)
        foundMethodOfInterest = True
        if nestingCount > 0:
          nestingCountWasGreaterThanZero = True
      elif nestingCountWasGreaterThanZero:
        nestingCountWasGreaterThanZero = False
        repairItem.methodsToCompare.append(methodName)
        newFileName = 'original_{0}.txt'.format(methodName)
        if len(linesToSave) < 3:
          print('error: {0} is too small; likely parsing error'.format(newFileName))
          print(linesToSave)
          sys.exit(1)
        with open(newFileName,'w') as fout:
          for line in linesToSave:
            fout.write(line)
            #can't remember if the extra \n is needed. I should test and see
            #- tested and doesn't seem to be necessary here
            #fout.write('\n')
        linesToSave = []
  #print('reading methods from file: {0}'.format(repairItem.fileToChange))
  print('methods to compare: {0}'.format(repairItem.methodsToCompare))
  input('stopping to check original methods to compare')


#newAPKLoation originally points to the apk location in the provided repo;
#if we copy the repo to create a new test file, we need to update the repo
#path
#def changeAPKLocationForNewTestFolder(projectDir, path, newAPKLocation):
#  def getFoldernameFromPath(p):
#    pItems = p.split(os.path.sep)
#    startIndex = 1
#    foldername = ''
#    while foldername == '':
#      foldername = pItems[-startIndex]
#      startIndex += 1
#    return foldername
#  newAPKLocation = newAPKLocation.replace(projectDir, path)
#  #some times the apk base name changes based on the repo it was compiled in
#  originalBasename = getFoldernameFromPath(projectDir)
#  newBasename = getFoldernameFromPath(path)
#  if originalBasename in newAPKLocation:
#    newAPKLocation = newAPKLocation.replace(originalBasename, newBasename)
#  #print(newAPKLocation)
#  return newAPKLocation
# 

#def handleDiff(repairItem, changeSet, methodDeclarationStringToCompare):
#  for method in repairItem.methodsToCompare:
#    originalFileName = "original_{0}.txt".format(method)
#    downloadedFileName = "downloaded_{0}.txt".format(method)
#    commandList = ["diff", originalFileName, downloadedFileName]
#    #diff returns a failure if the files are different, so setting
#    #check to False so the code doesn't die with the files are not
#    #equal
#    commandOutput = subprocess.run(commandList, check=False, stdout=subprocess.PIPE).stdout.decode('utf-8') 
#    #currently changes are just what others have added to the method
#    #will need to improve the generality of this later
#    for line in commandOutput.splitlines():
#      #avoid checking if the methods are declared slightly differently
#      if line.startswith('>') and not methodDeclarationStringToCompare in line:
#        change = line[1:].strip()
#        changeSet.add((change,method))
#    #print(len(changeSet))
#    for (change, method) in changeSet:
#      print("found change: {0} in method {1}".format(change, method))
#    #print(commandOutput)
#    #print("")
#  return changeSet

def addChangeToFile(repairItem, change, method):
  #need to go back later and remove the common paths in the two different path variables 
  fileContents = []
  #this stays true after the method is found
  #unlike the variable with the similar name below
  everFoundMethodOfInterest = False
  fullFileToChange = utilitiesForRepair.getFilesFullPath(repairItem.testFolder, repairItem.fileToChange)
  with open(fullFileToChange,'r') as fin:
    fileContents = fin.read().splitlines()
  #this is only true right when the method is found
  foundMethodOfInterest = False
  nestingCount = 0
  declarationItems = repairItem.methodDeclarationStringToCompare.split(" ")
  methodSpecificationItems = declarationItems[:-1]
  methodSpecification = " ".join(methodSpecificationItems)
  methodDeclaration = "{0} {1}".format(methodSpecification, method)
  for lineCount, line in enumerate(fileContents):
    #This public void declaration might be too specific
    if foundMethodOfInterest or nestingCount > 0:
      everFoundMethodOfInterest = True
      #use nesting count if they are both true
      if nestingCount > 0:
        foundMethodOfInterest = False
      for c in line:
        if c == '{':
          nestingCount = nestingCount + 1
        elif c == '}':
          nestingCount = nestingCount - 1
          #TODO: check this next part if you decide to use this method again;
          #looking at it again after I wrote it, it looks wrong
          if nestingCount < 1:
            print("inserting {0} into position {1}".format(change, lineCount))
            fileContents.insert(lineCount, change)
            print("inserted value: {0}".format(fileContents[lineCount]))
            #print(fileContents)
            if len(fileContents) < 3:
              print('error: file contents are too small')
              print(fileContents)
              sys.exit(1)
            print('testing out new file ')
            print(fullFileToChange)
            with open(fullFileToChange,'w') as fout:
              for line in fileContents:
                #\n's are needed here
                fout.write(line)
                fout.write('\n')
            # we added the change to the end of the method, so we are done
            return
    elif line.strip().startswith(methodDeclaration):
      foundMethodOfInterest = True
      everFoundMethodOfInterest = True
      for c in line:
        if c == '{':
          nestingCount = nestingCount + 1
        elif c == '}': 
          nestingCount = nestingCount - 1
  if not everFoundMethodOfInterest:
    print('error: never found method of interest {0} in {1}'.format(methodDeclaration, fullFileToChange))

#methodToFindTheCall is the method to delete from
def deleteMethodCallFromFile(methodCallToDelete, methodToFindTheCall, fileToChange, projectDir):
  def adjustNestingCountForLine(nestingCount, line):
    for c in line:
      if c == '{':
        nestingCount = nestingCount + 1
      if c == '}':
        nestingCount = nestingCount - 1
    return nestingCount
  fullFileToChange = utilitiesForRepair.getFilesFullPath(projectDir, fileToChange)
  resultLines = []
  deletedALine = False
  with open(fullFileToChange, 'r') as fin:
    nestingCount = 0
    foundMethodOfInterestInLine = False
    for lineCount, line in enumerate(fin):
      #not sure of the best way to check if we are in the method of interest
      #or not
      if methodToFindTheCall in line:
        foundMethodOfInterestInLine = True
        nestingCount = adjustNestingCountForLine(nestingCount, line)
      if nestingCount > 0 or foundMethodOfInterestInLine:
        #prefer the nesting count check over the foundMethodOfInterestInLine check
        foundMethodOfInterestInLine = False
        nestingCount = adjustNestingCountForLine(nestingCount, line)
        if not methodCallToDelete in line:
          resultLines.append(line)
        else:
          print('deleting line: {0} - {1}'.format(lineCount, line))
          #if 'setPackage' in line or 'setSelector' in line:
          #  input('deleting line of interest')
      else:
        resultLines.append(line)
  if len(resultLines) < 3:
    print('error: result lines are too small')
    print(resultLines)
    sys.exit(1)
  #print('testing result file')
  #print(resultLines)
  with open(fullFileToChange,'w') as fout:
    for line in resultLines:
      #I don't think I need to add the \n at the end, but check to make sure
      fout.write(line)
  #print('checking the file written to :{0}'.format(fullFileToChange))
  #print('a line was deleted: {0}, methodCallToDelete: {1}, methodToFindTheCall: {2}, {3}'.format(deletedALine, methodCallToDelete, methodToFindTheCall, everFoundMethod))
  #sys.exit(1)


def updateRepairItemForNewCopy(repairItem):
  repairItem.newAPKLocation = repairItem.newAPKLocation.replace(repairItem.originalFolder, repairItem.testFolder)
  if not repairItem.fileToChange is None:
    repairItem.fileToChange = repairItem.fileToChange.replace(repairItem.originalFolder, repairItem.testFolder)

   
#might eventually want to combine this with the code in changeMethodOrderRepair
def createNewCopyOfTestProgram(repairItem, newTestFolder = None):

 #assume that if newTestFolder is defined, we want to make it the new
  #test folder in the future
  if not newTestFolder is None:
    repairItem.testFolder = newTestFolder 
  #create a new directory if necessary
  #path is the location of the program to copy from
  if repairItem.testFolder is None:
    repairItem.testFolder = experimentFolder

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
  shutil.copytree(repairItem.originalFolder,repairItem.testFolder)
  #get the formatting fo the originalFolder and the experiment folder to match -
  #using the originalFolder path as the guide
  #if originalFolder has the path separator at the end, ensure it is on the
  #end of the experiment folder
  if repairItem.originalFolder[-1] == os.path.sep and repairItem.testFolder[-1] != os.path.sep:
    repairItem.testFolder = repairItem.testFolder + os.path.sep
  #if the originalFolder does not have the path separator, remove it from the
  #experiment folder if it is there
  elif repairItem.testFolder[-1] == os.path.sep and repairItem.originalFolder[-1] != os.path.sep:
    repairItem.testFolder[:-1]
  #otherwise the test folder name doesn't need to be changed
  updateRepairItemForNewCopy(repairItem)


def ensureMethodOfInterestWasntDeleted(repairItem):
  if repairItem.checkerToRun == 'DetectInvalidInflateCallMain':
    extraCheckString = '.inflate('
  elif repairItem.checkerToRun == 'DetectSetArgumentsMain':
    extraCheckString = 'setArguments('
  elif repairItem.checkerToRun == 'DetectMissingSetHasOptionsMenu':
    #extraCheckStringList = ['setHasOptionsMenu(true);', 'onCreateOptionsMenu']
    extraCheckString = 'setHasOptionsMenu(true);' #I'll need to adjust the logic here 
    #when I add repair support for onCreateOptionsMenu
  else:
    #need to add support for the other checkers later, since they need to be
    #specific to the checker, I'll need to think about each one. I'll throw 
    #an error now and look into the specific problems later
    print('unsupported checker ({0}) for ensure method of interest wasn\'t deleted'.format(repairItem.checkerToRun))
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
  fullFileToChange = utilitiesForRepair.getFilesFullPath(repairItem.testFolder, repairItem.fileToChange)
  with open(fullFileToChange,'r') as fin:
    fileContents = fin.read().splitlines()
  #this is only true right when the method is found
  inMethodOfInterest = False
  nestingCount = 0
  #need to handle the case when the method declaration extends over two lines
  inMethodDeclaration = False
  for lineCount, line in enumerate(fileContents):
    #This public void declaration might be too specific
    if inMethodDeclaration and not inMethodOfInterest:
      for c in line:
        if c == '{':
          nestingCount = nestingCount + 1
          inMethodOfInterest = True
          inMethodDeclaration = False
        elif c == '}':
          nestingCount = nestingCount - 1
    elif inMethodOfInterest and nestingCount > 0:
      if extraCheckString in line:
        return True
      if nestingCount < 1:
        inMethodOfInterest = False
      for c in line:
        if c == '{':
          nestingCount = nestingCount + 1
        elif c == '}':
          nestingCount = nestingCount - 1
    elif line.strip().startswith(repairItem.methodDeclarationStringToCompare):
      inMethodDeclaration = True
      for c in line:
        if c == '{':
          nestingCount = nestingCount + 1
          inMethodOfInterest = True
          inMethodDeclaration = False
        elif c == '}': 
          nestingCount = nestingCount - 1
  return False


def executeChecker(repairItem):
  originalDir = os.getcwd()
  unquotedAndQuotedList = repairItem.runFlowDroidCommand.split('"')
  commandList = []
  for index, item in enumerate(unquotedAndQuotedList):
    if index % 2 == 0:
      #these should be the unquoted parts of the command
      commandList.extend(item.strip().split(' '))
    else:
      commandList.append("{0}".format(item))
  commandList.append('analysis.{0}'.format(repairItem.checkerToRun))
  #newAPKLocation = '/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/build/outputs/apk/debug/Application-debug.apk'
  if os.path.exists(repairItem.newAPKLocation):
    commandList.append(repairItem.newAPKLocation)
  else:
    repairItem.newAPKLocation = levenshteinDistance.findAPKInRepo(repairItem.testFolder, repairItem.newAPKLocation)
    commandList.append(repairItem.newAPKLocation)
  try: 
    os.chdir(repairItem.runFlowDroidFolder)
    #print("current directory for command: {0}".format(os.getcwd()))
    #print("running command: {0}".format(' '.join(commandList)))
    print('running checker on app: {0}'.format(repairItem.newAPKLocation))
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if printingDebugInfo:# or containsFalse:
      print('start of error')
      for line in commandOutput.stderr.decode('utf-8').splitlines():
        print(line)
    #print(commandOutput)
    #print(commandOutput.stderr)
    #for line in commandOutput.stderr.decode('utf-8').splitlines():
      #print(line)
    checkerResultLines = []
    for line in commandOutput.stdout.decode('utf-8').splitlines():
      checkerResultLines.append(line)
      
  except: 
    print('had an exception when running the checker')
    print('command: {0}'.format(' '.join(commandList)))
    input('stopping to check why the checker exception occurred')
    return []
  #input('stopping to see checker result in repair method from github')
  #if containsFalse:
  #  input('stopping here to see result')
  os.chdir(originalDir)
  return checkerResultLines

#change and method are just needed for the final print statement
#consider changing later
def executeTestOfChangedApp(repairItem):
  global tempDebuggingBool
  #if containsFalse:
  #  input('stopping to see contains false before testing')
  if not ensureMethodOfInterestWasntDeleted(repairItem):
    return False
  builds = utilitiesForRepair.buildApp(repairItem.testFolder)
  if len(builds) > 0:
    buildSuccessful = True
  else:
    buildSuccessful = False
  if not buildSuccessful:
    return False
  checkerResultLines = executeChecker(repairItem)
  importantLines = utilitiesForRepair.extractImportantCheckerLines(checkerResultLines)
  problemCount = utilitiesForRepair.extractProblemCountFromCheckerOutput(importantLines)
  if problemCount < len(repairItem.problemInfoList):
    #print("succeeded - change: {0}, method {1}".format(change, method))
    return True
  else:
  #  if tempDebuggingBool:
  #    tempDebuggingBool = False
  #    print('set tempDebuggingBool to false due to problems still existing!!!!!!!!!!!!!!!!!!!!!!!!!!')
  #    inputValue = input("press enter to continue")
    return False

 #add the change to the method call of the copied app
 #run the application and see if it still produces the problem
 #if the application does not produce the problem, then print the change
 #that fixed the issue and stop

#def testDiffChanges(runFlowDroidCommand, changeSet, checkerToRun, methodDeclarationStringToCompare, fileToChange, projectDir, newAPKLocation):
#  #for all subsets of the changes
#  for changeItem in itertools.chain.from_iterable(itertools.combinations(changeSet,n) for n in range(len(changeSet)+1)):
#    print("starting directory: {0}".format(os.getcwd()))
##    path = createNewCopyOfTestProgram(projectDir)
#    apkLocation = changeAPKLocationForNewTestFolder(projectDir, path, apkLocation)
#    if len(changeItem) > 0:
#      for (change, method) in changeItem:
#        addChangeToFile(change, method, methodDeclarationStringToCompare, fileToChange, path)
#        #essentially breaking the code here with the return - done for debugging
#        wasFixed = executeTestOfChangedApp(runFlowDroidCommand, path, checkerToRun, fileToChange, methodDeclarationStringToCompare, newAPKLocation)
#        if wasFixed:
#          print("succeeded - change: added {0} to the end of method {1}".format(change, method))
#          return

def testAddingOrRemovingMethodCalls(repairItem):
  wasFixed = False
  print(repairItem.methodsToCompare)
  for method in repairItem.methodsToCompare:
    print('comparing method: {0}'.format(method))
    originalFileName = "original_{0}.txt".format(method)
    downloadedFileName = "downloaded_{0}.txt".format(method)
    fullDownloadedPath = os.path.join(os.getcwd(), downloadedFileName)
    if os.path.exists(fullDownloadedPath):
      print('downloaded file: {0}'.format(os.path.join(os.getcwd(), downloadedFileName)))
      with open(downloadedFileName,'r') as fin:
        print('file contents: {0}'.format(fin.read()))
      #input('stopping to check downloaded file')

      (originalDependencyChains, originalVariableTypeDict, originalFileTree) = \
        determineMethodDifferences.getParseInfo(originalFileName)
      (downloadedDependencyChains, downloadedVariableTypeDict, downloadedFileTree) = \
        determineMethodDifferences.getParseInfo(downloadedFileName)
      methodCallMismatches = determineMethodDifferences.checkMethodCallsInLines(originalFileTree, downloadedFileTree)
      print('number of method ')
      for mismatchTestItem in itertools.chain.from_iterable(itertools.combinations(methodCallMismatches,n) for n in range(len(methodCallMismatches)+1)):
        createNewCopyOfTestProgram(repairItem)
        if len(mismatchTestItem) > 0:
          #TODO: see if you also need the filename here        
          for (missingMethodName, listNumber, lineNumber) in mismatchTestItem:  
            #handle the adding case at the moment
            #later, you need to implement a deleting case for list 1
            if listNumber == 1:
              #renaming the variable to make the use of the variable more obvious
              #in this context
              #renaming the variable to make the use of the variable more obvious
              #in this context
              methodCallToDelete = missingMethodName
              methodToFindTheCall = repairItem.methodDeclarationStringToCompare
              deleteMethodCallFromFile(methodCallToDelete, methodToFindTheCall, repairItem.fileToChange, repairItem.testFolder)
            elif listNumber == 2:
              with open(downloadedFileName,'r') as fin:
                downloadedFileLines = fin.readlines()
              lineOfInterest = downloadedFileLines[lineNumber+1].strip()
              changeString = lineOfInterest
              #split the line of interest by periods, commas, and both parenthesis typesj
              variablesInLine = []
              lineItems = lineOfInterest.split('.')
              lineItemsList = map(operator.methodcaller("split", "("), lineItems)
              lineItems = [ item for itemList in lineItemsList for item in itemList if not item == "" ]
              lineItemsList = map(operator.methodcaller("split", ")"), lineItems)
              lineItems = [ item for itemList in lineItemsList for item in itemList if not item == "" ]
              lineItemsList = map(operator.methodcaller("split", ","), lineItems)
              lineItems = [ item for itemList in lineItemsList for item in itemList if not item == "" ]
              for item in lineItems:
                #get the type of the item in the downloaded item set
                #find an item of that type in the original item set and replace it
                if item in downloadedVariableTypeDict:
                  for var, typeName in originalVariableTypeDict.items():
                    if downloadedVariableTypeDict[item] == typeName:
                      lineOfInterest = lineOfInterest.replace(item, var)
                      print('changed line: {0}'.format(lineOfInterest))
                      print('replace {0} with {1}'.format(item, var))
                      #sys.exit(1)
                      break
              addChangeToFile(repairItem, lineOfInterest, method)
              #essentially breaking the code here with the return - done for debugging
              wasFixed = executeTestOfChangedApp(repairItem)
          #print('was fixed: {0}'.format(wasFixed))
          #input('checking if was fixed')
              if wasFixed:
                if listNumber == 2:
                  print("succeeded - change: added {0} to the end of method {1}".format(lineOfInterest, method))
                return True
    else:
      print('unable to find download file: {0}'.format(fullDownloadedPath))
  print('Unable to find fix')
  return False

#def deleteTypeDifferences(runFlowDroidCommand, fileName, mismatchList, methodDeclaration, projectDir, fileToChange):
#  for changeItemList in itertools.chain.from_iterable(itertools.combinations(mismatchList,n) for n in range(len(mismatchList)+1)):
#    path = createNewCopyOfTestProgram()
#    foundMethodOfInterest = False
#    newFileContents = []
#    nestingCount = 0
#    everFoundMethodOfInterest = False
#    if len(changeItemList) > 0:
#      deleteList = []
#      for i in changeItemList:
#        deleteList.append(i[2])
#      print(deleteList)
#      with open(fileToChange, 'r') as fin:
        #might not need this line count in this method; delete later if so
#        lineCountInMethodOfInterest = 0
#        incrementLineCountInMethodOfInterest = False
#        deleteCount = 0
#        for line in fin:
#          #print('line count in method of interest (top): {0}'.format(lineCountInMethodOfInterest))
#          #print(line)
#          #This public void declaration might be too specific
#          if foundMethodOfInterest or nestingCount > 0:
#            everFoundMethodOfInterest = True
#            #use nesting count if they are both true
#            if nestingCount > 0:
#              foundMethodOfInterest = False
#            for c in line:
#              if c == '{':
#                nestingCount = nestingCount + 1
#              elif c == '}':
#                nestingCount = nestingCount - 1
#                if nestingCount < 1:
#                  foundMethodOfInterest = False
#                  incrementLineCountInMethodOfInterest = False
#            if not(line.strip() == '{' or line.strip() == '}'):
#              incrementLineCountInMethodOfInterest = True
#          elif not everFoundMethodOfInterest and methodDeclaration in line:
#            foundMethodOfInterest = True         
#            for c in line:
#              if c == '{':
#                nestingCount = nestingCount + 1
#              elif c == '}': 
#                nestingCount = nestingCount - 1
#                if nestingCount < 1:
#                  foundMethodOfInterest = False
#                  incrementLineCountInMethodOfInterest = False
#          if incrementLineCountInMethodOfInterest:
#            if not lineCountInMethodOfInterest in deleteList:
#              newFileContents.append(line)
#            else:
#              print('deleting line: {0}'.format(line))
#              deleteCount = deleteCount  + 1
#              #print('line in delete list ({0} in {1})'.format(lineCountInMethodOfInterest, deleteList))
#            lineCountInMethodOfInterest = lineCountInMethodOfInterest + 1
#            #print('line count in method of interest: {0}'.format(lineCountInMethodOfInterest))
#          else:
#            newFileContents.append(line)
#      if len(newFileContents) < 3:
#        print('error: new file contents are too small (first)')
#        print(newFileContents)
        #skipping for now
#        return
        #sys.exit(1)
#      print('testing new file')
#      print(newFileContents)
#      print('deleted {0} lines'.format(deleteCount))
#      if deleteCount < 1:
#        print('error: no lines deleted')
#        print('list to delete: {0}'.format(deleteList))
#        print('final line count in method of interest: {0}'.format(lineCountInMethodOfInterest))
#        print('file to change: {0}'.format(fileToChange))
#        print('method call of interest: {0}'.format(methodDeclaration))
#        sys.exit(1)
#      with open(fileToChange, 'w') as fout:
#        for line in newFileContents:
#          fout.write(line)
#    wasFixed = executeTestOfChangedApp(path, checkerToRun, projectDir, fileToChange)
#    if wasFixed:
#      return wasFixed
#  return False
#     
#def addTypeDifferences(runFlowDroidCommand, originalFileName, downloadedFileTree, mismatchList, methodDeclaration, originalVariableTypeDict, downloadedVariableTypeDict):
#  global tempDebuggingBool
#  lineIndexList = list(map(lambda x: x[2], mismatchList))
#  print(lineIndexList)
#  #get the strings for the lines to add
#  lineList = determineMethodDifferences.getLinesFromTree(downloadedFileTree, lineIndexList)
#  #convert the variable names from variable names in the original code to a valid 
#  #object of the same type in the file to change
#  updatedLineList = []
#  savedFoundMatch = False
#  for l in lineList:
#    for v in downloadedVariableTypeDict:
#      if v in l:
#        foundMatch = False
#        vReplace = ""
#        vType = downloadedVariableTypeDict[v]
#        for newV in originalVariableTypeDict:
##          if vType == originalVariableTypeDict[newV]:
#            vReplace = newV
#            foundMatch = True
#            break
#        #TODO: this may replace unwanted sections of the code (will mistakenly change
#        #part of one name if it contains the method of interest - for example, if the
#        #variable is i, this will change all i's in the line, even for another 
        #variable named min)
#        if foundMatch:
#          l = l.replace(v, vReplace)
#          print('replace {0} with {1}'.format(v, vReplace))
#          savedFoundMatch = True
##        else: 
#          print('did not find match for {0} <type: {1}> in {2}'.format(v, vType, originalVariableTypeDict))
#    updatedLineList.append(l)
#  lineList = updatedLineList
#  print(lineList)
#  #if savedFoundMatch:
#  #  sys.exit(0)
  #create a tuple list of the line indexes and the strings
#  lineIndexStringPairs = list(zip(lineIndexList, lineList))
#  #can't get the length of lineIndexStringPairs - can't get the len of a zip object for some reason
#  for changeItemList in itertools.chain.from_iterable(itertools.combinations(lineIndexStringPairs,n) for n in range(len(lineList)+1)):
#    path = createNewCopyOfTestProgram()
#    if len(changeItemList) > 0:
#      newFileContents = []
#      tempLineIndexList = sorted(list(map(lambda x: x[0], changeItemList)))
##      tempStringList = list(map(lambda x: x[1], changeItemList))
#      lineStringMap = dict((x, y) for x, y in changeItemList) 
#      #if len(changeItemList) > 0:
      #  addList = []
      #  for i in changeItemList:
      #    addList.append(i[3])
#      addedLineCount = 0
#      with open(fileToChange, 'r') as fin:
        #initializing the line count to negative one so that 0 starts on the 
        #first valid line in the method
#        lineCountInMethodOfInterest = -1
#        newFileContents = []
#        beforeEndOfMethodOfInterest = True
#        foundMethodOfInterest = False
##        everFoundMethodOfInterest = False
#        nestingCount = 0
#        fileContents = fin.read().splitlines()
#        lineCount = 0
##        for line in fileContents:
#          print(line)
#          incrementLineCountInMethodOfInterest = False
##          #This public void declaration might be too specific
#          if foundMethodOfInterest or nestingCount > 0:
#            everFoundMethodOfInterest = True
#            #use nesting count if they are both true
#            if nestingCount > 0:
##              foundMethodOfInterest = False
#            for c in line:
#              if c == '{':
##                nestingCount = nestingCount + 1
#              elif c == '}':
#                nestingCount = nestingCount - 1
#                if nestingCount < 1:
#                  foundMethodOfInterest = False
#            if not(line.strip() == '{' or line.strip() == '}'):
#              incrementLineCountInMethodOfInterest = True
#          elif not everFoundMethodOfInterest and methodDeclaration in line:
#            foundMethodOfInterest = True         
#            for c in line:
##              if c == '{':
#                nestingCount = nestingCount + 1
#              elif c == '}': 
#                nestingCount = nestingCount - 1
#          if nestingCount < 1 and everFoundMethodOfInterest and beforeEndOfMethodOfInterest:
#            beforeEndOfMethodOfInterest = False
#            for i in tempLineIndexList:
#              if i > lineCountInMethodOfInterest:
#                newFileContents.append(lineStringMap[i])
##                print('added line: {0}'.format(lineStringMap[i]))
#                addedLineCount = addedLineCount + 1
#          newFileContents.append(line)
#          if incrementLineCountInMethodOfInterest:
#            lineCountInMethodOfInterest = lineCountInMethodOfInterest + 1
#            if lineCountInMethodOfInterest in tempLineIndexList:
#              newFileContents.append(lineStringMap[lineCountInMethodOfInterest])
#              print('added line: {0}'.format(lineStringMap[lineCountInMethodOfInterest]))
#              if(lineStringMap[lineCountInMethodOfInterest].strip().endswith('false);')):
#                tempDebuggingBool = True
#                print('set tempDebuggingBool to true !!!!!!!!!!!!!!!!!!!!!!!!!!')
#              addedLineCount = addedLineCount + 1
#      if len(newFileContents) < 3:
#        print('error: new file contents are too small (second)')
#        print(newFileContents)
#      if addedLineCount < 1:
#        print('error: did not add any lines')
#        print(lineStringMap)
#        print(mismatchList)
#        print('method declaration to look for: {0}'.format(methodDeclaration))
#        print('ever found declaration of interest: {0}'.format(everFoundMethodOfInterest))
#        print('line count: {0}'.format(lineCountInMethodOfInterest))
#        print('file to change: {0}'.format(fileToChange))
#        sys.exit(1)
#      with open(fileToChange, 'w') as fout:
#        for line in newFileContents:
#          fout.write(line)
#          fout.write('\n')
#    wasFixed = executeTestOfChangedApp(runFlowDroidCommand, path, checkerToRun, projectDir, fileToChange)
#    if wasFixed:
#      return wasFixed
#  return False
#

def addAndDeleteTypeDifferences(repairItem, originalFileName, downloadedFileTree, mismatchList, originalVariableTypeDict, downloadedVariableTypeDict):
  global tempDebuggingBool
  global debugCounter
  #containsFalse was added for debugging - can remove later
  #global containsFalse
  #containsFalse = False
  foundFixOfInterest = False
  linesToAddIndexList = []
  linesToAddIndexSet = set()
  for i in mismatchList:
    if i[1] == 2:
      linesToAddIndexSet.add(i[2])
  print('original lines to add index list: {0}'.format(linesToAddIndexSet))
  #get the strings for the lines to add
  linesToAddIndexList = list(linesToAddIndexSet)
  lineListToAdd = determineMethodDifferences.getLinesFromTree(downloadedFileTree, linesToAddIndexList)
  #convert the variable names from variable names in the original code to a valid 
  #object of the same type in the file to change
  updatedLineList = []
  savedFoundMatch = False
  #oneVWasAStaticFile = False
  for l in lineListToAdd:
    for v in downloadedVariableTypeDict:
      #if v.startswith('R.'):
      #  oneVWasAStaticFile = True
      #  print('v: {0} is a Static File'.format(v))
      if v in l:
        foundMatch = False
        vReplace = ""
        vType = downloadedVariableTypeDict[v]
        for newV in originalVariableTypeDict:
          if vType == originalVariableTypeDict[newV]:
            vReplace = newV
            foundMatch = True
            break
        #TODO: this may replace unwanted sections of the code (will mistakenly change
        #part of one name if it contains the method of interest - for example, if the
        #variable is i, this will change all i's in the line, even for another 
        #variable named min)
        if foundMatch:
          l = l.replace(v, vReplace)
          print('replace {0} with {1}'.format(v, vReplace))
          savedFoundMatch = True
        else: 
          print('did not find match for {0} <type: {1}> in {2}'.format(v, vType, originalVariableTypeDict))
    updatedLineList.append(l)
    #if oneVWasAStaticFile:
    #  print('one v was a static file')
    #else:
    #  print('no v was a static file')
    #sys.exit(1)
  lineListToAdd = updatedLineList
  print('!!!!!!!!!!!!{0}'.format(lineListToAdd))
  #if savedFoundMatch:
  #  sys.exit(0)
  #create a tuple list of the line indexes and the strings
  linesToAddDict = dict(zip(linesToAddIndexList, lineListToAdd))
  #can't get the length of lineIndexStringPairs - can't get the len of a zip object for some reason

  # I don't care about which specific types are different on the different lines,
  # just which lines are different, thus filter the mismatchList to one type item
  # that represents each line
  #print(mismatchList)
  uniqueMismatchLineDict = {}
  for m in mismatchList:
    if not (m[1],m[2]) in uniqueMismatchLineDict:
      uniqueMismatchLineDict[(m[1],m[2])] = m
  uniqueMismatchList = uniqueMismatchLineDict.values()
  #print(uniqueMismatchList)
  #input('stopping to check filter function ')
  for changeItemList in itertools.chain.from_iterable(itertools.combinations(uniqueMismatchList,n) for n in range(len(uniqueMismatchList)+1)):
    wasFixed = False
    #containsFalse = False
    createNewCopyOfTestProgram(repairItem)
    if len(changeItemList) > 0:
      newFileContents = []
      #linesToChange = list(map(lambda x: x[2], changeItemList))

      #if len(changeItemList) > 0:
      #  addList = []
      #  for i in changeItemList:
      #    addList.append(i[3])
      addedLineCount = 0
      deletedLineCount = 0
      addedLineList = []
      deletedLineList = []
      indexOfMethodStart = -1
      fullFileToChange = utilitiesForRepair.getFilesFullPath(repairItem.testFolder, repairItem.fileToChange)
      with open(fullFileToChange, 'r') as fin:
        #initializing the line count to negative one so that 0 starts on the 
        #first valid line in the method
        lineCountInMethodOfInterest = -1
        newFileContents = []
        beforeEndOfMethodOfInterest = True
        foundMethodOfInterest = False
        everFoundMethodOfInterest = False
        nestingCount = 0
        fileContents = fin.read().splitlines()
        #line counts may not correspond exactly with what I was doing before 
        #because I've changed it so all () are on the same line when checking 
        #the type differences
        lineCount = 0
        hasOpenParensBetweenLines = False
        for line in fileContents:
          if line.strip() == '':
            newFileContents.append(line)
            continue
          #print(line)
          incrementLineCountInMethodOfInterest = False
          if foundMethodOfInterest or nestingCount > 0:
            #use nesting count if they are both true
            everFoundMethodOfInterest = True
            #use the previous line's nesting count for the current line - 
            #otherwise lines that open up the function get deleted
            if nestingCount == 1:
              incrementLineCountInMethodOfInterest = True
            if nestingCount > 0:
              foundMethodOfInterest = False
            for c in line:
              if c == '{':
                nestingCount = nestingCount + 1
              elif c == '}':
                nestingCount = nestingCount - 1
                if nestingCount < 1:
                  foundMethodOfInterest = False
            #trying to avoid deleting the second line of a two line method declaration with
            #nestingCountZeroAtStart
            #print(nestingCountZeroAtStart = )
            #I think there I meant to use foundMethodOfInterest instead of nestingCountAtStart;
            #test to see
            #if not(line.strip() == '{' or line.strip() == '}') and not nestingCountZeroAtStart:
            #if not(line.strip() == '{' or line.strip() == '}') and foundMethodOfInterest:
            
            if indexOfMethodStart == -1:
              indexOfMethodStart = len(newFileContents)
          elif not everFoundMethodOfInterest and repairItem.methodDeclarationStringToCompare in line:
            foundMethodOfInterest = True         
            for c in line:
              if c == '{':
                nestingCount = nestingCount + 1
              elif c == '}': 
                nestingCount = nestingCount - 1
          if nestingCount < 1 and everFoundMethodOfInterest and beforeEndOfMethodOfInterest:
            beforeEndOfMethodOfInterest = False
            #get all items with a line greater than the end of the method of interest
            #
            #sort and then add
            itemsToAdd = [i for i in changeItemList if i[2] > lineCountInMethodOfInterest and i[1] == 2]
            if len(itemsToAdd) > 0:
              indexesStillToAdd = [i[2] for i in itemsToAdd]
              indexesStillToAdd.sort()
              for i in indexesStillToAdd:
                if i not in linesToAddDict:
                  print('error: missing key {0}'.format(i))
                  print('linesToAddDict keys: {0}'.format(linesToAddDict.keys()))
                  print('change item list: {0}'.format(changeItemList))
                addedLine = linesToAddDict[i]
                addedLine = addedLine.replace('return ','')
                #These few lines are for debugging
                if 'inflate' in addedLine and ('false)' in addedLine or 'false )' in addedLine):
                  print('addedLine: {0}'.format(addedLine))
                  input('stopping to check added line that might fix the problem')
                #print('length of new file contents before adding: {0}'.format(len(newFileContents)))
                newFileContents.append(addedLine)
                #print('length of new file contents after adding: {0}'.format(len(newFileContents)))
                #print('added line: {0}'.format(addedLine))
                addedLineCount = addedLineCount + 1
                addedLineList.append(addedLine)
                if(addedLine.strip().endswith('false);')):
                  tempDebuggingBool = True
                  print('set tempDebuggingBool to true !!!!!!!!!!!!!!!!!!!!!!!!!!')
            #needed to make sure the return statement is at the end of a method
            #for methods that return values
            if not repairItem.methodDeclarationStringToCompare.split(' ')[1] == 'void':
              try:
                lineToChange = ''
                linesBack = 1
                while lineToChange == '' and linesBack < len(newFileContents) + 1:
                  lineToChange = newFileContents[-linesBack].strip()
                  linesBack += 1
                if lineToChange.split()[0] != "return":
                  newFileContents[-linesBack] = "return " + newFileContents[-linesBack] 
              except IndexError as e:
                #print(newFileContents)
                print(e)
                print('last line of new file contents: {0}'.format(newFileContents[-1]))
                sys.exit(1)
              #print('added return')
              #global debugCounter
              #if debugCounter > 1:
              #  print('new line with return : {0}'.format(newFileContents[-1]))
              #  sys.exit(1)
              #debugCounter = debugCounter + 1
            #print('new method with additions and deletions:')
            #print('start index: {0}, end index: {1}'.format(indexOfMethodStart, len(newFileContents)))
            #for i in range(indexOfMethodStart, len(newFileContents)):
            #  print(newFileContents[i])
              #if 'false' in newFileContents[i]:
               # containsFalse = True
               # print('false here!!!')
                #if containsFalse and len(newFileContents) - indexOfMethodStart == 2:
                #  input('stop with false and single line changed')
          if incrementLineCountInMethodOfInterest:
            #print('length of new file contents at this point: {0}'.format(len(newFileContents)))
            lineCountInMethodOfInterest = lineCountInMethodOfInterest + 1
            changesToLine = [ i for i in changeItemList if i[2] == lineCountInMethodOfInterest]
            #print('line count in method of interest: {0}'.format(lineCountInMethodOfInterest))
            #if there are no changes to the line, just keep it in the file
            if len(changesToLine) < 1:
              newFileContents.append(line)
            else:
              deleteItems = [ i for i in changesToLine if i[1] == 1]
              #doesn't seem to be a problem if multiple delete requests are 
              #for the same line - can happen due to having one for each type in 
              #the line
              #if len(deleteItems) > 1:
                #not sure if this is actually an error, but want to stop and check if 
                #it happens at the moment
              #  print('error: too many deletions in the same line')
              #  print('delete items: {0}'.format(deleteItems))
              #  print('line to delete: {0}'.format(line))
              #  sys.exit(1)

              #delete the line if it should be deleted, otherwise, keep the line
              #and remove any returns
              deletedLine = None
              if len(deleteItems) > 0:
                print('deleting line: {0}'.format(line))
                deletedLineList.append(line)
                deletedLine = line
                deletedLineCount = deletedLineCount  + 1
              else:
                line = line.replace('return ','')
                newFileContents.append(line)
              addItems = [ i for i in changesToLine if i[1] == 2]
              #also not a problem - happens but due to the fact that multiple
              #types could want the same line added
              #if len(addItems) > 1:
                #not sure if this is actually an error, but want to stop and check if 
                #it happens at the moment
                #print('error: too many additions in the same line')
                #print('add items: {0}'.format(addItems))
                #print('line to add: {0}'.format(line))
                #sys.exit(1)
              #if len(addItems) > 0:
              #  print('adding line: {0}'.format(line))
              #  addedLineCount = addedLineCount  + 1

              #add the line count that corresponded to this line count in the other file
              if len(addItems) > 0:
                addedLine = linesToAddDict[lineCountInMethodOfInterest] 
                addedLine = addedLine.replace('return ', '')
                #try to replace the part of the deleted line if the deleted line contained it
                if not deletedLine is None:
                    addedLineContents = addedLine.strip()
                    addedMethodCallItems = addedLineContents.split('(')
                    replacePosition = deletedLine.find(addedMethodCallItems[0]+'(')
                    if replacePosition > 1:
                      addedLine = deletedLine[:replacePosition] + addedLine
                      input('stopping to confirm new added line: {0}'.format(addedLine))
                print('length of new file contents before adding 2: {0}'.format(len(newFileContents)))
                newFileContents.append(addedLine)
                print('length of new file contents after adding 2: {0}'.format(len(newFileContents)))
                print('added line 2: {0}'.format(addedLine))
                addedLineCount = addedLineCount + 1
                addedLineList.append(addedLine)
                #if 'inflate' in addedLine and ('false)' in addedLine or 'false )' in addedLine):
                  #print('addedLine: {0}'.format(addedLine))
                  #input('stopping to check added line that might fix the problem')
          else: 
            newFileContents.append(line)
      if len(newFileContents) < 3:
        print('error: new file contents are too small (second)')
        print(newFileContents)
        sys.exit(1)
      if addedLineCount < 1 and deletedLineCount < 1:
        print('error: did not add or delete any lines')
        print(lineListToAdd)
        print(changeItemList)
        print('method declaration to look for: {0}'.format(repairItem.methodDeclarationStringToCompare))
        print('ever found declaration of interest: {0}'.format(everFoundMethodOfInterest))
        print('line count: {0}'.format(lineCountInMethodOfInterest))
        print('file to change: {0}'.format(fullFileToChange))
        print('file contents size: {0}'.format(len(fileContents)))
        #might eventually want to convert this back from just skipping the error
        #to throwing the error and the fix it; I'm testing it to see
        continue
        #sys.exit(1)
      addedInflate = False
      deletedInflate = False
      #for l in addedLineList:
      #  if '.inflate' in l:
      #    addedInflate = True
      #    break
      #for l in deletedLineList:
      #  if '.inflate' in l:
      #    deletedInflate = True
      #    break
      #if addedInflate and deletedInflate:
      #  foundFixOfInterest = True
      print('changing: {0}'.format(fullFileToChange))
      with open(fullFileToChange, 'w') as fout:
        for line in newFileContents:
          fout.write(line)
          fout.write('\n')
      if addedLineCount > 0 and deletedLineCount > 0:
        commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFileToChange))
        subprocess.run(commandList)
        input('stopping to check changed file')
      wasFixed = executeTestOfChangedApp(repairItem)
    ##containsFalse = False
    #if foundFixOfInterest:
    #  print('was fixed: {0}'.format(wasFixed))
    #  global printingDebugInfo
    #  printingDebugInfo = True
    #  wasFixed = executeTestOfChangedApp(path)
    #  sys.exit(1)
    #if containsFalse:
    #  input('{0}: contains false: press enter to continue'.format(debugCounter))
    debugCounter += 1
    if wasFixed:
      return wasFixed
  return False


#pretty sure I need to combine the ability to add and remove lines so I can 
#support changing lines

def testTypeDifferences(repairItem) :
#  print('in test type differences')
  for method in repairItem.methodsToCompare:
    originalFileName = "original_{0}.txt".format(method)
    downloadedFileName = "downloaded_{0}.txt".format(method)
    typeMismatches = None
    if os.path.exists(downloadedFileName):
      #debating if I should group these 7 variables into an object. Leaving them
      #separate for now and may combine them later
      (originalDependencyChains, originalVariableTypeDict, originalFileTree) = \
        determineMethodDifferences.getParseInfo(originalFileName)
      (downloadedDependencyChains, downloadedVariableTypeDict, downloadedFileTree) = \
        determineMethodDifferences.getParseInfo(downloadedFileName)
      typeMismatches = determineMethodDifferences.checkUnmatchedTypesForBothLists(originalDependencyChains, downloadedDependencyChains)
    else:
      print('download file not found: {0}'.format(downloadedFileName))
    if typeMismatches is None or len(typeMismatches) < 1:
      print('type mismatches is 0; returning False')
      return False
    else:
      return addAndDeleteTypeDifferences(repairItem, originalFileName, downloadedFileTree, typeMismatches, originalVariableTypeDict, downloadedVariableTypeDict)

def handleAndTestAdvancedDiff(repairItem):
  isSolved = testAddingOrRemovingMethodCalls(repairItem)
  #commented out previous line and next line is for testing
  #isSolved = False
  if not isSolved:
    isSolved = testTypeDifferences(repairItem)
  return isSolved

def main(repairItem):
  print(repairItem.methodDeclarationStringToCompare)
  extractOriginalMethodsOfInterest(repairItem)
  #input('stopping to check the method declaration string')
  pageNumber = 1
  notDone = True
  changeSet = set()
  #the number of repos needed to check before finding a solution - just for 
  #personal interest and debugging
  reposComparedCount = 0
  while notDone: 
    # I might want to eventually remove this optimization - while it works, 
    # it currently doesn't have a good way to determine when the saved data
    # is out of date - might also be able to come up with some way to determine
    # the code is out of date
    saveFileName = None
    if not repairItem.savedDataDirectory is None:
      saveFileName = '{0}savedGitHubSearches/savedSearch{1}.json'.format(repairItem.savedDataDirectory, pageNumber)
    #removing the save file code - I might bring the optimization back in later, 
    #but right now it is throwing off my tests..
    #if os.path.isfile(saveFileName):
    #  print('opened save file')
    #  with open(saveFileName,'r') as fin:
    #    searchResult = json.loads(fin.read())
    #else:
    #I don't want to change the indentation and leaving it easy to go back 
    #to the check above
    #command = 'curl -n https://api.github.com/search/code?q=onCreate+Fragment+onCreateOptionsMenu+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
    #command = 'curl -n https://api.github.com/search/code?q=onCreateView+Fragment+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
    #need to figure out how to determine if I should use the word Fragment in the search
    methodDeclarationItems = repairItem.methodDeclarationStringToCompare.split(' ')
    keywords = [methodDeclarationItems[-1]]
    #handle either the case when terms of interest is a string or when terms of 
    #interest is a string of multiple words
    if repairItem.termsOfInterest:
      if isinstance(repairItem.termsOfInterest, str):
        repairItem.termsOfInterest = repairItem.termsOfInterest.split()
      keywords = keywords + repairItem.termsOfInterest
    #this if isn't needed at the moment, but it might be used in later versions of the code
    if len(keywords) < 2:
      keyWordString = keywords[0]
    else:
      keyWordString = "+".join(keywords)
    command = 'curl -n https://api.github.com/search/code?q={0}+in:file+language:java?page={1}&per_page=100&sort=stars&order=desc'.format(keyWordString, pageNumber)
    print(command)
    #if containsFalse:
    #  input('stopping here to see command')
    commandList = command.split(" ")
    commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
    searchResult = json.loads(commandOutput)
    if not saveFileName is None:
      os.makedirs(os.path.dirname(saveFileName), exist_ok=True)
      with open(saveFileName,'w') as fout:
        json.dump(searchResult,fout)
    print('pulled from github')
    #print(searchResult['total_count'])
    currentCount = 0
    pageLimit = 100
    #input('stopping before page search loop')
    while notDone and currentCount < pageLimit - 1:
      containsFragment = False
    #urlToSearch='https://github.com/search?l=Java&q=onCreate+&type=Code'
    #response = session.get(urlToSearch).content.decode('utf-8')
    #print(type(response))
    #print(response)
    #with open('searchResult.txt','w') as fout:
    #print('start of page')
    #for line in response.splitlines():
    #  print(line)
    #print('end of page')
        #if('java' in line.decode('utf-8')):
        #  print(line)
        #fout.write(line.decode("utf-8"))

      currentCount = currentCount + 1
      if 'items' not in searchResult:
        print('no more GitHub results')
        print(searchResult)
        sys.exit(0)
      urlToSearch = searchResult['items'][currentCount]['html_url']
      #print(searchResult['items'][currentCount])
     #print(urlToSearch)
      if urlToSearch.endswith('.java'):
        #response = session.get(urlToSearch).content.decode('utf-8')
        #soup = BeautifulSoup(response, 'html.parser')
        #for link in soup.find_all('a'):
          #print(link.contents)
        #  if(link.contents[0].endswith('.java')):
        time.sleep(1)
        #pageRequest = session.get(urlToSearch).content
        try:
          with urllib.request.urlopen(urlToSearch) as pageRequest:
            #read is read once, so save the result
            pageResult = pageRequest.read()
            soup2 = BeautifulSoup(pageResult, 'html.parser')
            rawLink = soup2.find_all(id='raw-url')[0]
            time.sleep(1)
            #print('raw link: {0}'.format(rawLink))
            rawLinkString = "https://github.com/" + rawLink['href']
            with urllib.request.urlopen(rawLinkString) as finalResults:
              programOfInterest = finalResults.read().decode('utf-8', errors="ignore")
              if shouldCheckForFragment:
                lookingForFragment = True
                lineIndex = 0 
                if printingSearchUpdates:
                  print('looking through:\n{0}'.format(programOfInterest))
                linesInProgram = programOfInterest.splitlines()
                while lookingForFragment and lineIndex < len(linesInProgram):
                  line = linesInProgram[lineIndex]
                  if ' Fragment ' in line:
                    lookingForFragment = False
                    containsFragment = True
                  lineIndex = lineIndex + 1
              else:
                lookingForFragment = False
              foundMethodOfInterest = False
              everFoundMethodOfInterest = False
              if not lookingForFragment: 
                savingLines = False
                linesToSave = []
                nestingCount = 0
                nestingCountWasGreaterThanZero = False
                methodName = ""
                createdFiles = False
                for line in programOfInterest.splitlines():
                  if foundMethodOfInterest or nestingCount > 0:
                    everFoundMethodOfInterest = True
                    (linesToSave, nestingCount) = saveLines(linesToSave, nestingCount, line)
                    # only use foundMethodOfInterest until we find the first {
                    if nestingCountWasGreaterThanZero > 0:
                      nestingCountWasGreaterThanZero = True
                      foundMethodOfInterest = False
                  #this string check captures both the onCreate method and the onCreateOptionsMenu method
                  elif repairItem.methodDeclarationStringToCompare and repairItem.methodDeclarationStringToCompare in line:
                    if printingSearchUpdates:
                      print('found method of interest')
                    methodName = line.split()[2].split('(')[0]
                    (linesToSave, nestingCount) = saveLines(linesToSave, nestingCount, line)
                    foundMethodOfInterest = True
                    if nestingCount > 0:
                      nestingCountWasGreaterThanZero = True
                  elif nestingCountWasGreaterThanZero:
                    nestingCountWasGreaterThanZero = False
                    newFileName = 'downloaded_{0}.txt'.format(methodName)
                    createdFileListToDelete.append(newFileName)
                    if len(linesToSave) < 3:
                      print('error: lines to save are too small')
                      print(linesToSave)
                      sys.exit(1)
                    with open(newFileName,'w') as fout:
                      print('writing to download file: {0}'.format(os.path.join(os.getcwd(), newFileName)))
                      for line in linesToSave:
                        if len(linesToSave) < 3:
                          print('error: method is too short, likely parsing error')
                          print(linesToSave)
                          sys.exit(1)
                        fout.write(line)
                        #\n seems to be required here
                        fout.write('\n')
                      createdFiles = True
                    linesToSave = []
                if createdFiles:
                  #print('reading program from: {0}'.format(rawLinkString))
                  #input('stopping to check found file')
                  reposComparedCount += 1
                  hasSucceeded = handleAndTestAdvancedDiff(repairItem)
                  #input('stop after test of Github repo')
                  if hasSucceeded:
                    print('repos compared to produce a fix: {0}'.format(reposComparedCount))
                    print('found a successful repair!')
                    notDone = False
              else:
                if printingSearchUpdates:
                  print('lines of program: \n{0}'.format(programOfInterest))
                  print('error: never found Fragment in file (error in main)')
                  #sys.exit(1)
              if not lookingForFragment and not everFoundMethodOfInterest:
                print('lines of program: \n{0}'.format(programOfInterest))
                print('error: never found method of interest (error in main)')
                print('method declaration to compare: {0}'.format(repairItem.methodDeclarationStringToCompare))
              #sys.exit(1)
        except urllib.error.HTTPError:
          print('failed with url: {0}'.format(urlToSearch))
          sys.exit(1)
    #if not containsFragment: 
    #  print('page {0} does not contain any Fragments!!!'.format(pageNumber))
    pageNumber = pageNumber + 1
  for f in createdFileListToDelete:
    #This is a quick and hacky solution to speed up development without digging
   #into the issue;
   #You should probably figure out why the script is trying to delete files
   #that don't exist later
    try:
      os.remove(f)
    except:
      pass
  return True

#extractOriginalMethodsOfInterest()
#handleAndTestAdvancedDiff()

if __name__ == "__main__":
  runFlowDroidCommand = sys.argv[1]
  #print("$$$$$$$$$$$$$$$$${0}".format(runFlowDroidCommand))
  #print('number of arguments: {0}'.format(len(sys.argv)))
  #print('second argument: {0}'.format(sys.argv[2]))
  #sys.exit(0)
  checkerToRun = sys.argv[2]
  savedDataDirectory = sys.argv[3]
  methodDeclarationStringToCompare = sys.argv[4]
  originalFolder = sys.argv[5]
  fileToChange = sys.argv[6]
  print('original file to change: {0}'.format(fileToChange))
  newAPKLocation = sys.argv[7]
  termsOfInterestInput = sys.argv[8]
  if termsOfInterestInput == "None":
    termsOfInterest = []
  else: 
    termsOfInterest = termsOfInterestInput.split(' ')
  repairItem = GitHubRepairItem(runFlowDroidCommand, checkerToRun, methodDeclarationStringToCompare, originalFolder, fileToChange, newAPKLocation, termsOfInterest)
  main(repairItem)