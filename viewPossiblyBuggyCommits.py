#!/usr/local/bin/python3

import itertools
import sys
import os
import shutil
import subprocess

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    #creates n copies of a dependent iterator - pulling an item off one
    #iterator object pulls the item off the others
    args = [iter(iterable)] * n
    #return the first n objects from the iterables or as many options as possible
    #and then the rest are fillvalues
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def downloadRepo(locationToDownload, repo):
  #print('current directory: {0}'.format(os.getcwd()))
  #For some reason, the git clone call fails occassionally, 
  originalDir = os.getcwd()
  os.chdir(locationToDownload)
  trying = True
  while(trying):
    try: 
      commandList = ['git','clone',repo]
      commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
      trying = False
    except: 
      #just try again if it didn't work
      print('failed to download {0}. Trying again...'.format(repo))
  os.chdir(originalDir)


fileToRead = 'optionsMenuSearchResults.txt'
locationToPutRepo = '/Users/zack/git/DirectiveTool/currentlyViewedRepo'
previousRepoNumber = -1
skippingToNextRepo = False
originalDir = os.getcwd()
currentDownloadedRepo = ''
with open(fileToRead,'r') as fin:
  bugInfoList = grouper(fin, 5, "")
  for bugInfoLines in bugInfoList:
    fullFilePath = bugInfoLines[0].split(' ')[3]
    commitOfInterest = bugInfoLines[0].strip().split(' ')[-1]
    repoName = bugInfoLines[1].strip().split(' ')[-1]
    repoNumber = bugInfoLines[2].split(',')[0].split(' ')[-1]
    detectedIssue = bugInfoLines[3].strip()
    if skippingToNextRepo:
      if repoNumber == previousRepoNumber:
        previousRepoNumber = repoNumber
        continue
    previousRepoNumber = repoNumber
    if not currentDownloadedRepo == repoName:
      if os.path.exists(locationToPutRepo):
        shutil.rmtree(locationToPutRepo)
      try:
        os.makedirs(locationToPutRepo)
      except OSError as e:
        print("creation of {0} directory failed".format(locationToPutRepo))
        print(e)
        sys.exit(1)
      os.chdir(locationToPutRepo)
      downloadRepo(locationToPutRepo, repoName)
      currentDownloadedRepo = repoName
    else: 
      os.chdir(locationToPutRepo)
    #this code currently makes an assumption about the number of directories in
    #the file tree to get the repo in the fullFilePath - I could write something
    #more general that tries to find the root directory of the git repo in the 
    #file path, but I'll add that generality if I determine it is useful
    print('in {0}'.format(os.getcwd()))
    os.chdir(repoName.split('/')[-1].split('.')[0])
    commandList = ['git','reset','--hard',commitOfInterest]
    commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
    relativeFilePath = '/'.join(fullFilePath.split('/')[6:])
    print('opened: {0}'.format(relativeFilePath))
    print('has problem: {0}'.format(detectedIssue))
    os.chdir('..')
    print('current directory: {0}'.format(os.getcwd()))
    commandList = ['open','-a', "Sublime Text", relativeFilePath]
    print(commandList)
    commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8') 
    inputResult = input('press enter to see the next file\ntype r to skip to a file in the next repo\n-')
    if inputResult == 'r':
      skippingToNextRepo = True
    os.chdir(originalDir)







  #previousLine = ""
  #finishedABugReport = False
  #for line in fin:
    #if line.startswith('------------'):
      #problemInformation = previousLine
      #finishedABugReport = True
    #previousLine = line 
