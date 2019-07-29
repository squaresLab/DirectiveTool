#!/usr/local/bin/python3

import subprocess
import sys
import json
import os
import shutil
from codecs import BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE

BOMS = (
    (BOM_UTF8, "UTF-8"),
    (BOM_UTF32_BE, "UTF-32-BE"),
    (BOM_UTF32_LE, "UTF-32-LE"),
    (BOM_UTF16_BE, "UTF-16-BE"),
    (BOM_UTF16_LE, "UTF-16-LE"),
)

def check_bom(data):
    return [encoding for bom, encoding in BOMS if data.startswith(bom)]
#I don't expect the number of interesting files to change
#often between commits. I'm going to use this dictionary
#to save the file locations of interest, so they don't have
#to be checked every time. This assumption could lead to
#missing files of interest that undergo name changes during
#the commit history, or files of interest that were deleted.
#I could rescan all the files again at certain intervals if
#I need to find these missing files
savedImportantFiles = {}

#consider later passing this through the program instead of using it as a global variable
buggyFileCount = 0
errorCountForRepoDict = {}

def tryEncodingSetSelectorSetPackage(fin, fileName, commitName, repoNumber, commitNumber, outputFile, repoName):
  fileContainsActivity = False 
  fileContainsSetSelector = False
  fileContainsSetPackage = False
  #current problem is that you start counting the nesting count again on the 
  #next method. Need to stop when onCreate finishes
  for line in fin:
    if not fileContainsActivity and 'android.app.Activity' in line:
      fileContainsActivity = True
    elif not fileContainsSetSelector and 'setSelector' in line:
      fileContainsSetSelector = True
    elif not fileContainsSetPackage and 'setPackage' in line:
      fileContainsSetPackage = True
  if fileContainsActivity and fileContainsSetPackage and fileContainsSetSelector:
    print('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('\n')
    print('repo name: {0}'.format(repoName))
    outputFile.write('repo name: {0}'.format(repoName))
    outputFile.write('\n')
    print('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('\n')
    outputFile.write('---------------------------------\n')
    global buggyFileCount
    buggyFileCount = buggyFileCount + 1
    #having trouble figuring out why the sys.exit is being caught
    #os._exit(1)
    #sys.exit(0)
    #sys.exit(0)
    return True
  return False

def tryEncodingGetResources(fin, fileName, commitName, repoNumber, commitNumber, outputFile, repoName):
  fileContainsFragment = False 
  fileContainsAsyncTask = False
  fileContainsGetResources = False
  #current problem is that you start counting the nesting count again on the 
  #next method. Need to stop when onCreate finishes
  for line in fin:
    if not fileContainsFragment and 'android.app.Fragment' in line:
      fileContainsFragment = True
    elif not fileContainsAsyncTask and 'AsyncTask' in line:
      fileContainsAsyncTask = True
    elif not fileContainsGetResources and 'getResources' in line:
      fileContainsGetResources = True
  if fileContainsFragment and fileContainsAsyncTask and fileContainsGetResources:
    print('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('\n')
    print('repo name: {0}'.format(repoName))
    outputFile.write('repo name: {0}'.format(repoName))
    outputFile.write('\n')
    print('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('\n')
    outputFile.write('---------------------------------\n')
    global buggyFileCount
    commandList = ['open','-a', "Sublime Text", fileName]
    #print(commandList)
    if repoName in errorCountForRepoDict and errorCountForRepoDict[repoName] < 5:
      commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
      inputResult = input('press enter to see the next file')
      errorCountForRepoDict[repoName] = errorCountForRepoDict[repoName] + 1
    elif repoName not in errorCountForRepoDict:
      commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
      inputResult = input('press enter to see the next file')
      errorCountForRepoDict[repoName] = 1
    buggyFileCount = buggyFileCount + 1
    #having trouble figuring out why the sys.exit is being caught
    #os._exit(1)
    #sys.exit(0)
    #sys.exit(0)
    return True
  return False

def tryEncodingOnCreate(fin, fileName, commitName, repoNumber, commitNumber, outputFile, repoName):
  fileContainsFragment = False 
  fileContainsSetHasOptionsMenu = False
  fileContainsOnCreateOptionsMenu = False
  foundOnCreate = False
  currentNestingCount = 0
  nestingWentAboveZero = False
  leftOnCreate = False
  #current problem is that you start counting the nesting count again on the 
  #next method. Need to stop when onCreate finishes
  for line in fin:
    #print(line)
    if not leftOnCreate and (foundOnCreate or currentNestingCount > 0):
      for c in line: 
        if c == '{':
          currentNestingCount = currentNestingCount + 1
          nestingWentAboveZero = True
        elif c == '}':
          currentNestingCount = currentNestingCount - 1
          if currentNestingCount < 1:
            leftOnCreate = True
    if not fileContainsFragment and 'android.app.Fragment' in line:
      fileContainsFragment = True
    elif not fileContainsOnCreateOptionsMenu and 'public void onCreateOptionsMenu' in line:
      fileContainsOnCreateOptionsMenu = True
      #I should expand the check below to include the case where setHasOptionsMenu is called in
      #another method other than onCreate
    elif not foundOnCreate and 'public void onCreate(' in line:
      foundOnCreate = True
      for c in line: 
        if c == '{':
          currentNestingCount = currentNestingCount + 1
          nestingWentAboveZero = True
        elif c == '}':
          currentNestingCount = currentNestingCount - 1
          if currentNestingCount < 1:
            leftOnCreate = True
    elif not fileContainsSetHasOptionsMenu and currentNestingCount > 0 and 'setHasOptionsMenu' in line:
      fileContainsSetHasOptionsMenu = True
    elif fileContainsSetHasOptionsMenu and fileContainsOnCreateOptionsMenu:
      break
  #print('finished reading file')
  if fileContainsFragment and ((not fileContainsOnCreateOptionsMenu and fileContainsSetHasOptionsMenu) or (fileContainsOnCreateOptionsMenu and not fileContainsSetHasOptionsMenu)):
    print('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('error in file: {0} in commit {1}'.format(fileName, commitName))
    outputFile.write('\n')
    print('repo name: {0}'.format(repoName))
    outputFile.write('repo name: {0}'.format(repoName))
    outputFile.write('\n')
    print('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('stopped on repo number: {0}, commit number: {1}'.format(repoNumber, commitNumber))
    outputFile.write('\n')
    if fileContainsSetHasOptionsMenu:
      print ('file is missing onCreateOptionsMenu')
      outputFile.write ('file is missing onCreateOptionsMenu')
      outputFile.write('\n')
    else:
      print('file is missing SetHasOptionsMenu')
      outputFile.write('file is missing SetHasOptionsMenu')
      outputFile.write('\n')
    outputFile.write('---------------------------------\n')
    global buggyFileCount
    buggyFileCount = buggyFileCount + 1
    #having trouble figuring out why the sys.exit is being caught
    #os._exit(1)
    #sys.exit(0)
    #sys.exit(0)
    return True
  return False


#currently, this method calls all the different encoding types I can think of
#and then uses tryEncoding to perform the actual buggy check on the file
def isFileBuggy(fileOfInterest, commitName, repoNumber, commitNumber, outputFile, repoName):
  if not os.path.islink(fileOfInterest):
    hasEncoding = False
    hasntFinished = True
    currentEncodingIndex = 0
    encodingsToCheck = ['utf-8','utf-16','ASCII']
    checkedBom = False
    currentEncoding = ""
    while hasntFinished:
      try:
        #print('opening {0}'.format(fileOfInterest))
        if hasEncoding: 
          #print('testing encoding: {0}'.format(currentEncoding))
          with open(fileOfInterest,'r', encoding = currentEncoding) as fin:
            result = tryEncodingSetSelectorSetPackage(fin, fileOfInterest, commitName, repoNumber, commitNumber, outputFile, repoName)
        else:
          with open(fileOfInterest,'r') as fin:
            result = tryEncodingSetSelectorSetPackage(fin, fileOfInterest, commitName, repoNumber, commitNumber, outputFile, repoName)
        hasntFinished = False
      except SystemExit: 
      #later remove the double sys.exit call, but leaving for now because it is 
      #is the fastest fix
        sys.exit(1)
      #if the file wasn't created on this commit, don't worry about it
      #except Exception as e:
      #print(e)
      #pass
      except (UnicodeDecodeError, UnicodeError) as u:
        if hasEncoding:
          currentEncodingIndex = currentEncodingIndex + 1
        else:
          hasEncoding = True
        if currentEncodingIndex < len(encodingsToCheck):
          currentEncoding = encodingsToCheck[currentEncodingIndex]
        else:
          if not checkedBom and len(check_bom(open(fileOfInterest,'rb').read(100))) > 0:
            currentEncoding = check_bom(open(fileOfInterest,'rb').read(100))[0]
            checkedBom = True
          else:
            try:
              with open(fileOfInterest,'r', encoding = 'utf-8', errors='ignore') as fin:
                #print('checking utf-8 encoding ignoring errors')
                result = tryEncodingSetSelectorSetPackage(fin, fileOfInterest, commitName, repoNumber, commitNumber, outputFile, repoName)
                hasntFinished = False
            except:
              print('Error: checked all encodings and none worked')
              sys.exit(1)
    #print('finished checking encodings')
    return result

        


def checkRepoForImportantFiles(repoLocation, commitName, repoNumber, commitNumber, outputFile, repoName): 
  if repoLocation in savedImportantFiles.keys():
    filesToCheck = savedImportantFiles[repoLocation]
    for f in filesToCheck:
      #figure out what to do with the return value later
      isFileBuggy(f, commitName, repoNumber, commitNumber, outputFile, repoName)
  else:
    for root, dirs, files in os.walk(repoLocation):
      for f in files:
        #I am finding too many.copied of the official Android fragment file
        #which doesn't follow these rules
        #if f.endswith('.java') and not f == 'Fragment.java':
        if f.endswith('.java') and not f == 'Activity.java':
          isFileBuggy(root+os.path.sep+f, commitName, repoNumber, commitNumber, outputFile, repoName)

def checkCommits(repoLocation, repoNumber, outputFile, repoName):
  originalDir = os.getcwd()
  os.chdir(repoLocation)
  #first run on the final set of files to determine all useful finals at the end
  commandList = ['git','rev-parse','HEAD']
  commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
  originalCommit = commandOutput.strip()
  checkRepoForImportantFiles(repoLocation, originalCommit, repoNumber, -1, outputFile, repoName)
  commandList = ['git','log']
  commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
  commitList = []
  for line in commandOutput.splitlines():
    if line.startswith('commit '):
      commitList.append(line.strip()[7:])
  for commitNumber, commit in enumerate(commitList):
    commandList = ['git','reset','--hard',commit]
    commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
    checkRepoForImportantFiles(repoLocation, commit, repoNumber, commitNumber, outputFile, repoName)
  os.chdir(originalDir)
  shutil.rmtree(repoLocation)


def downloadRepo(repo):
  #print('current directory: {0}'.format(os.getcwd()))
  #For some reason, the git clone call fails occassionally, 
  trying = True
  while(trying):
    try: 
      commandList = ['git','clone',repo]
      commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
      trying = False
    except: 
      #just try again if it didn't work
      print('failed to download {0}. Trying again...'.format(repo))

  

locationToPutRepo = '/Users/zack/git/DirectiveTool/downloadedRepo'
#pageNumber = 0
skipToRepo = 0#30
originalDir = os.getcwd()
checkedRepoSet = set()
if os.path.exists(locationToPutRepo):
  shutil.rmtree(locationToPutRepo)
try: 
  os.makedirs(locationToPutRepo)
  print('created folder')
except OSError as e:
  print("Creation of the directory {0} failed".format(path))
  print(e)
  sys.exit(1)
repoCount = 0
#switched from w to a since I have now partially created the file
#I want, and now want to add more to it - and now reverted back since it seems 
#that GitHub still gives me the first page no matter the page number for the 
#first page I request
with open('optionsMenuSearchResults.txt','w') as outputFile:
#with open('optionsMenuSearchResults.txt','a') as outputFile:
  os.chdir(locationToPutRepo)
  for pageNumber in range(0,20):
    #try to download the page from GitHub; if it doesn't work, print the error information
    #often the error doesn't appear until I try to get the 'items' out of the return result
    #so I am wrapping the whole expression in a try block for now
    try:
      #command = 'curl -n https://api.github.com/search/code?q=onCreate+Fragment+onCreateOptionsMenu+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
      #command = 'curl -n https://api.github.com/search/code?q=AsyncTask+Fragment+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
      command = 'curl -n https://api.github.com/search/code?q=Activity+setSelector+setPackage+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
      print('trying command: {0}'.format(command))
      commandList = command.split(" ")
      commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
      searchResult = json.loads(commandOutput)
      for repoNumber, r in enumerate(searchResult['items']):
        if repoNumber >= skipToRepo:
          repoCount = repoCount + 1
          repoName = r['repository']['html_url']
          repoBase = repoName.split('/')[-1]
          repoName = repoName + ".git"
          #these next four lines are for testing a specific commit
          #repoBase = 'AndroidProject'
          #repoName = 'https://github.com/KotkovetsAndrey/AndroidProject.git'
          #repoNumber = 1
          #repoCount = 1
          if not repoName in checkedRepoSet:
            checkedRepoSet.add(repoName)
            downloadRepo(repoName)
            print('downloaded: {0}'.format(repoName.split('/')[-1]))
            checkCommits(locationToPutRepo + os.path.sep + repoBase, repoNumber, outputFile, repoName)
          if repoName == 'InternProject.git' or repoName == 'Chest.git':
            print('finished with a repo that you determined already had an error')
            print('current number of counted errors: {0}'.format(buggyFileCount))
            sys.exit(1)
    except KeyError as k:
      print(k)
      print(searchResult)
      input('press enter to skip this error')
      print('failed to download page {0}'.format(pageNumber))
      print('skipping to the next page')
os.chdir(originalDir)
print('total number of repos: {0}'.format(repoCount))
print('total number of buggy files: {0}'.format(buggyFileCount))

