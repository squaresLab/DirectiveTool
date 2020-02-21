#!/usr/local/bin/python3/

import os
import sys
import subprocess
import shutil
import defusedxml.ElementTree
import utilitiesForRepair
import levenshteinDistance

defaultAppDir = '/Users/zack/git/ViolationOfDirectives'
defaultFileWithProblem = '/Users/zack/git/ViolationOfDirectives/Application/src/main/java/com/example/android/lnotifications/HeadsUpNotificationFragment.java'
checkerRootDir = "/Users/zack/git/DirectiveTool/FlowDroidTest"
experimentFolder = "/Users/zack/git/DirectiveTool/temporaryTestOfChange"

def fileIsMenuFile(fullFilename):
  fileTree = defusedxml.ElementTree.parse(fullFilename)
  if fileTree.getroot().tag == 'menu':
    return True
  return False
  #with open(fullFilename,'r', encoding="utf-8", errors="surrogateescape") as fin:
  #  for line in fin:

def buildStaticFileName(root, resDir, fileBasename):
  resultFileName = root.replace(resDir, "")
  resultFileName = resultFileName.replace(os.path.sep, ".")
  resultFileName = 'R' + resultFileName
  resultFileName += "." + fileBasename.split('.')[0]
  return resultFileName

def getStaticFileName(appDir):
#I'd love to do something more targeted than this, but doing the best I can
  #think of for now
  #There are other res dirs in the directory than the one I want
  resDirList = []
  for root,dirs,files in os.walk(appDir):
    for d in dirs:
      if d == 'res':
        resDir = os.path.join(root, d)
        resDirList.append(resDir)
  if len(resDirList) < 1:
    print("never found res dir in {0}".format(appDir))
    sys.exit(1)
  for resDir in resDirList:
    for root, dirs, files in os.walk(resDir):
      for f in files:
        if f.endswith('.xml'):
          if fileIsMenuFile(os.path.join(root,f)):
            #print('{0} {1}'.format(root, resDir))
            staticFileName = buildStaticFileName(root, resDir, f)
            return staticFileName
  return None

def createOnCreateTemplate(staticFileName):
  return """@Override
public void onCreateOptionsMenu(Menu menu,MenuInflater menuInflater)
{{
    super.onCreateOptionsMenu(menu,menuInflater);
    menu.clear();
    menuInflater.inflate({0},menu);
}}\n""".format(staticFileName)

def getMenuInflaterImportLine():
  return 'import android.view.MenuInflater;\n'

def getMenuImportLine():
  return 'import android.view.Menu;\n'

def getNestingCountOfLine(line, nestingCount):
  for c in line:
    if c == '{':
      nestingCount += 1
    elif c == '}':
      nestingCount -= 1
  return nestingCount


def addFunctionToFile(fileToAddTo, functionToAdd):
  fileContents = []
  nestingCount = 0
  inClass = False
  with open(fileToAddTo, 'r', encoding="utf-8",errors="surrogateescape") as fin:
    for line in fin:
      nestingCount = getNestingCountOfLine(line,nestingCount)
      if nestingCount > 0:
        inClass = True
      elif inClass and nestingCount == 0:
        fileContents.append(functionToAdd)
      fileContents.append(line)
  #add the function into the right spot
  with open(fileToAddTo, 'w', encoding="utf-8",errors="surrogateescape") as fout:
    for line in fileContents:
      print(line, end="", file=fout)
  print('finished adding function to file: {0}'.format(fileToAddTo))

def runCheckerAndGetOutput(runFlowDroidCommand, checkerToRun, apkLocation, testFolder):
  # I need to split by space but not on quoted parts of the string
  originalDir = os.getcwd()
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
  if os.path.exists(apkLocation):
    commandList.append(apkLocation)
  else:
    repairItem.apkLocation = levenshteinDistance.findAPKInRepo(testFolder, apkLocation)
    commandList.append(apkLocation)
  try: 
    #print("running command: {0} {1} {2}".format("\"".join(unquotedAndQuotedList),checkerToRun, repairItem.apkLocation))
    os.chdir(checkerRootDir)
    print("current directory for checker command: {0}".format(os.getcwd()))
    print('apk location: {0}'.format(apkLocation))
    commandOutput = subprocess.run(commandList, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    #if printingDebugInfo:
      #for line in commandOutput.stderr.decode('utf-8').splitlines():
        #print(line)
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

def updateRepairItemForNewCopy(apkLocation, originalFolder, newFolder, fileToChange):
  newAPKLocation = apkLocation.replace(originalFolder, newFolder)
  newFileToChange = None
  if not fileToChange is None:
    newFileToChange = fileToChange.replace(originalFolder, newFolder)
  return newAPKLocation, newFileToChange

   
#might eventually want to combine this with the code in changeMethodOrderRepair
def createNewCopyOfTestProgram(originalFolder, fileToChange, apkLocation, newTestFolder = None):

 #assume that if newTestFolder is defined, we want to make it the new
  #test folder in the future
  newFolder = None
  if not newTestFolder is None:
    newFolder = newTestFolder 
  #create a new directory if necessary
  #path is the location of the program to copy from
  if newFolder is None:
    newFolder = experimentFolder

  if os.path.exists(newFolder):
    shutil.rmtree(newFolder)
  #try: 
  #  os.makedirs(path)
  #except OSError as e:
  #  print("Creation of the directory {0} failed".format(path))
  #  print(e)
  #  sys.exit(1)
  #distutils.dir_util.copy_tree("/Users/zack/git/DirectiveTool/testFolder/",path)
  #copy the application to the new directory
  shutil.copytree(originalFolder, newFolder)
  #get the formatting fo the originalFolder and the experiment folder to match -
  #using the originalFolder path as the guide
  #if originalFolder has the path separator at the end, ensure it is on the
  #end of the experiment folder
  if originalFolder[-1] == os.path.sep and newFolder[-1] != os.path.sep:
    newFolder = newFolder + os.path.sep
  #if the originalFolder does not have the path separator, remove it from the
  #experiment folder if it is there
  elif newFolder[-1] == os.path.sep and newFolder[-1] != os.path.sep:
    newFolder[:-1]
  #otherwise the test folder name doesn't need to be changed
  newApkLocation, newFileToChange = updateRepairItemForNewCopy(apkLocation, originalFolder, newFolder, fileToChange)
  return newFolder, newApkLocation, newFileToChange


#currently this only works for when onCreateOptionsMenu is missing; I'll need
#to make this more general later
def main(sourceDir, fileWithProblem, runFlowDroidCommand, checkerToRun, apkLocation, originalProblemCount = 1):
  fileWithProblem = utilitiesForRepair.getFilesFullPath(sourceDir, fileWithProblem) 
  newFolder, newApkLocation, newFileWithProblem = createNewCopyOfTestProgram(sourceDir, fileWithProblem, apkLocation)
  staticFileName = getStaticFileName(newFolder)
  if staticFileName is None:
    print('error: no static file name found')
    sys.exit(1)
  onCreateFunction = createOnCreateTemplate(staticFileName)
  #print(onCreateFunction)
  addFunctionToFile(newFileWithProblem, onCreateFunction)
  utilitiesForRepair.addImportLineIfRequired(newFileWithProblem, getMenuInflaterImportLine())
  utilitiesForRepair.addImportLineIfRequired(newFileWithProblem, getMenuImportLine())
  utilitiesForRepair.buildApp(newFolder)
  testResultLines = runCheckerAndGetOutput(runFlowDroidCommand, checkerToRun, newApkLocation, newFolder)
  print('finished main of template repair')
  importantLines = utilitiesForRepair.extractImportantCheckerLines(testResultLines)
  currentProblems = utilitiesForRepair.extractProblemCountFromCheckerOutput(importantLines)
  if currentProblems >= originalProblemCount:
    input('stopping to check unsuccessful template fix')
  return currentProblems < originalProblemCount
 



if __name__ == "__main__":
  #calling getFullFile here may not be the right decision if I later copy the code
  #before changing it
  print(sys.argv)
  if len(sys.argv) > 1:
    sourceDir = sys.argv[1]
  else:
    sourceDir = defaultAppDir
  if len(sys.argv) > 2:
    fileWithProblem = sys.argv[2]
  else:
    fileWithProblem = defaultFileWithProblem
  runFlowDroidCommand = sys.argv[3]
  checkerToRun = sys.argv[4]
  apkLocation = sys.argv[5]
  fileWithProblem = utilitiesForRepair.getFilesFullPath(sourceDir, fileWithProblem)
  main(sourceDir, fileWithProblem, runFlowDroidCommand, checkerToRun, apkLocation)