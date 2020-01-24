#!/usr/local/bin/python3

import os
import subprocess
import re
import random
import shlex

compilingRepoList = ['muzei-commons',
'Riksdagskollen',
'TUI-ConsoleLauncher',
'PostWriter',
'VlcFreemote',
'privacy-friendly-2048',
'android-sms-gate',
'YouTubeStream',
'aRevelation',
'webcom-reader',
'giggity',
'muzei-nationalgeographic',
'rxdroid',
'privacy-friendly-finance-manager',
'Handy-News-Reader',
'PrivacyHelper',
'child-resus-calc',
'bepo-android',
'powerbutton',
'hacs',
'bird-monitor',
'badge-magic-android']

repoLocation='/Users/zack/git/reposFromFDroid' 

#commandLineEscapeSequences = re.compile(r'(\x1b\[|\x9b)[^@-_]*[@-_1-9]|\x1b[@-_]')
commandLineEscapeSequences = re.compile(r'\[[0-9]+m')

onCreateTemplatesLocation = '/Users/zack/git/DirectiveTool/injectFaultsDir/onCreateOptionsMenuTemplates'
extendsFragmentPattern = re.compile('.*extends [^ ]+Fragment .*')
combyInflateNoChangeCommand = shlex.split('comby "inflate(:[firstParam], :[secondParam], false);" "inflate(:[firstParam],:[secondParam], true);" .java -match-only')
combyInflateWithChangeCommandTemplate = 'comby "inflate(:[firstParam], :[secondParam], false);" "inflate(:[firstParam],:[secondParam], true);" -f {0} -d {1} -in-place'

#this method determines if the repo contains a file that can be replaces with the inflate comby
#template; currently this is dead code. I'm trying out the method determineInvalidInflateRepo 
#at the moment
def getMatchingFiles(repo):
  originalDir = os.getcwd()
  os.chdir(repo)
  #print('changed to {0}'.format(repo))
  #combyInflateCommand = ['comby', 'inflate(:[firstParam], :[secondParam], false);', 'inflate(:[firstParam],:[secondParam], true);', '.java', '-default-no']
  combyProcess = subprocess.run(combyInflateNoChangeCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  possibleFiles = []
  if combyProcess.returncode == 0:
    for line in combyProcess.stdout.decode('utf-8').splitlines():
      #print(line)
      lineItems = line.split(':')
      if lineItems[0].endswith('.java'):
        possibleFiles.append(lineItems[0])
  matchingFiles = []
  for f in possibleFiles:
    foundFragmentClassInFile = False
    with open(f, 'r',encoding="utf-8",errors="surrogateescape") as fin:
      for line in fin:
        fragmentMatchResult = extendsFragmentPattern.match(line)
        if fragmentMatchResult:
          #print('line with match: {0}'.format(line))
          foundFragmentClassInFile = True
          break
    if foundFragmentClassInFile:
      matchingFiles.append(f)
  
  os.chdir(originalDir)
  return matchingFiles

def determineValidInflateRepoWithoutComby(repo):
  matchingFiles = []
  for root, dirs, files in os.walk(repo):
    for f in files:
      if f.endswith('.java'):
        fullFilename = os.path.join(root, f)
        foundFragmentClassInFile = False
        foundInflate = False
        with open(fullFilename, 'r', encoding="utf-8",errors="surrogateescape") as fin:
          for line in fin:
            if not foundFragmentClassInFile:
              fragmentMatchResult = extendsFragmentPattern.match(line)
              if fragmentMatchResult:
                foundFragmentClassInFile = True
            elif not foundInflate and 'inflate(' in line:
              foundInflate = True
            if foundInflate and foundFragmentClassInFile:
              matchingFiles.append(fullFilename)
              break
  return matchingFiles


def determineInjectionInfoForInflateRepo(repo): 
  #repo = os.path.join(repoLocation,compilingRepoList[1])
  #print('running on repo: {0}'.format(repo))
  #trying out the non comby injection way
  #matchingFiles = getMatchingFiles(repo)
  matchingFiles = determineValidInflateRepoWithoutComby(repo)
  if len(matchingFiles) > 0:
    return True
  return False
 
  #rc = combyProcess.poll()
  #processOutput = "starting text"
  #randChoice = None
  #possibleChangeCount = 0
  #changedFileList = []
  #matchesFound = None
  #while (rc is None or processOutput is not b'') and matchesFound is None:
    #out,err = combyProcess.communicate()
  #  processOutput = combyProcess.stdout.readline()
  #  for line in processOutput.decode('utf-8').splitlines():
  #    line = re.sub(commandLineEscapeSequences,'',line.strip())
  #    line = re.sub('\x1b','',line.strip())
  #    if 'There are' in line or 'There is' in line:
  #      #for c in line:
        #  print(c)
  #      lineItems = line.split()
        #print(lineItems)
  #      #print('found {0} matches'.format(lineItems[2]))
  #      matchesFound = int(lineItems[2])
  #      combyProcess.kill()
  #      break
  #if matchesFound > 0:
  #return matchesFound

def injectInflateProblemWithoutComby(fullFilename):
  #input('starting inject inflate problem')
  isAFileToChange = False
  injectLine = None
  fileContents = []
  with open(fullFilename, 'r', encoding="utf-8",errors="surrogateescape") as fin:
    for lineCount,line in enumerate(fin):
      fileContent.append(line)
      if not fragmentMatchResult:
        fragmentMatchResult = extendsFragmentPattern.match(line)
        if fragmentMatchResult:
            foundFragmentClassInFile = True
      elif not foundInflate and 'inflate(' in line:
        foundInflate = True
        injectLine = lineCount
  if not isAFileToChange:
    return False
  else:
    inflateLineToChange = fileContents[injectLine]
    inflateIndex = inflateLineToChange.find('inflate(')
    endOfCallIndex = inflateLineToChange.find(')')
    paramStrings = inflateLineToChange[inflateIndex + len('inflate('): endOfCallIndex]
    params = paramStrings.split(',')
    parameterOfInterest = params[-1].strip()
    if parameterOfInterest == 'true':
      #don't inject if the problem is already there
      return False
    elif parameterOfInterest == 'false':
      #if the parameter is the wrong type, change it
      params[-1] = 'true'
      paramString = ','.join(params)
      newInflateString = inflateLineToChange[:inflateIndex + len('inflate(') + 1] + paramString + inflateLineToChange[endOfCallIndex:]
      fileContents[injectLine] = newInflateString
    else:
      #if the parameter is missing, add the wrong one
      newInflateString = inflateLineToChange[:endOfCallIndex] + ', true' + inflateLineToChange[endOfCallIndex:]
      fileContents[injectLine] = newInflateString
  with open(fullFilename, 'w', encoding="utf-8",errors="surrogateescape") as fout:
    for line in fileContents:
      print(line, file=fout, end='')
  commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
  subprocess.run(commandList)
  input('stopping to check the injection')
  #if we got to this point then the file has been successfully changed
  return True






def injectInflateProblem(repo):
  #input('starting inject inflate problem')
  matchingFiles = getMatchingFiles(repo)
  fileToChange = matchingFiles[random.randrange(len(matchingFiles))]
  dirName, baseName = os.path.split(fileToChange)
  combyCommand = shlex.split(combyInflateWithChangeCommandTemplate.format(baseName, dirName))
  combyProcess = subprocess.run(combyCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  print('result of comby process: {0}'.format(combyProcess.returncode))
  for line in combyProcess.stdout.decode('utf-8').splitlines():
    print(line)
  fullFilename = os.path.join(dirName, baseName)
  print('changed file: {0}'.format(fullFilename))
  print('comby command to cause change: {0}'.format(' '.join(combyCommand)))
  commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
  subprocess.run(commandList)
  input('stopping to check the injection')


def injectInflateProblem(repo):
  #input('starting inject inflate problem')
  matchingFiles = getMatchingFiles(repo)
  fileToChange = matchingFiles[random.randrange(len(matchingFiles))]
  dirName, baseName = os.path.split(fileToChange)
  combyCommand = shlex.split(combyInflateWithChangeCommandTemplate.format(baseName, dirName))
  combyProcess = subprocess.run(combyCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  print('result of comby process: {0}'.format(combyProcess.returncode))
  for line in combyProcess.stdout.decode('utf-8').splitlines():
    print(line)
  fullFilename = os.path.join(dirName, baseName)
  print('changed file: {0}'.format(fullFilename))
  print('comby command to cause change: {0}'.format(' '.join(combyCommand)))
  commandList = shlex.split('open -a "Sublime Text" {0}'.format(fullFilename))
  subprocess.run(commandList)
  input('stopping to check the injection')
  #input('stopped here for debugging')

  #repo = os.path.join(repoLocation,compilingRepoList[1])
  #os.chdir(repo)
  #print('changed to {0}'.format(repo))
  #combyInflateCommand = ['comby', 'inflate(:[firstParam], :[secondParam], false);', 'inflate(:[firstParam],:[secondParam], true);', '.java', '-default-no']
  #combyProcess = subprocess.Popen(combyInflateCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
  #rc = combyProcess.poll()
  #processOutput = "starting text"
  #randChoice = None
  #possibleChangeCount = 0
  #changedFileList = []
  #while rc is None or processOutput is not b'':
  #  #out,err = combyProcess.communicate()
  #  processOutput = combyProcess.stdout.readline()
  #  for line in processOutput.decode('utf-8').splitlines():
  #    line = re.sub(commandLineEscapeSequences,'',line.strip())
  #    line = re.sub('\x1b','',line.strip())
  #    if 'There are' in line or 'There is' in line:
  #      #for c in line:
  #      #  print(c)
  #      lineItems = line.split()
  #      #print(lineItems)
  #      #print('found {0} matches'.format(lineItems[2]))
  #      matchesFound = int(lineItems[2])
  #      if matchesFound == 0:
  #        #print('no matches found')
  #        combyProcess.kill()
  #        #sys.exit()
  #      elif matchesFound > 2:
  #        randChoice = random.randrange(int(lineItems[2]))
  #      else:
  #        randChoice = 0
  #      #print('rand choice: {0}'.format(randChoice))
  #      #input('stopping to see rand choice')
  #    elif line.startswith('Press'):
  #      #print('found match')
  #      #combyProcess.stdin.write('a\r\n\nb'.encode('utf-8'))
  #      #combyProcess.stdin.write('\r\n'.encode("utf-8"))
  #      os.write(combyProcess.stdin.fileno(),'\r\n'.encode('utf-8'))
  #      #combyProcess.stdin.write(b"\r\n")
  #    elif '------' in line:
  #      filename = line.split()[1][5:]
  #      #print('filename: {0}'.format(filename[5:]))
  #    elif randChoice is not None and line.startswith('Accept change'):
  #      #print('found accept change')
  #      if randChoice == possibleChangeCount:
  #        #print('writing y')
  #        #print('changed: {0}'.format(filename))
  #        changedFileList.append(filename)
  #        os.write(combyProcess.stdin.fileno(),'y\r\n'.encode('utf-8'))
  #        #input('stop here for a second')
  #      else:
  #        #print('writing n')
  #        os.write(combyProcess.stdin.fileno(),'n\r\n'.encode('utf-8'))
  #        #input('stop here for a second')
  #      possibleChangeCount += 1
  #    #print('{0} {1}'.format(randChoice, line.startswith('Accept change')))
  #    #print('|line: {0}|'.format(line.strip()))
  #  rc = combyProcess.poll()
  #  #print('in while loop (rc: {0}, processOutput: {1}'.format(rc is None,processOutput == b''))
  #for cf in changedFileList:
  #  print('changed file: {0}'.format(os.path.join(repo,cf)))

def injectOptionsMenuProblem():
  for r in compilingRepoList:
    repo = os.path.join(repoLocation,r)
    injectSetHasOptionsMenuProblem(repo)
  #injectOnCreateOptionsMenuProblem()

#this method removes the onCreateOptions menu method from a file
def injectOnCreateOptionsMenuProblem():
  onCreateCombyFullPattern = """@Override
    public void onCreateOptionsMenu(:[parameters]) {
        :[body]    
    }"""
  onCreateCombyInput = ""
  for line in onCreateCombyFullPattern.split('\n'):
    line = line.strip()
    onCreateCombyInput += "{0}\n".format(line)
  extendsFragmentPattern = re.compile('extends [\.\w]*Fragment ')
  for r in compilingRepoList:
    repo = os.path.join(repoLocation,r)
    print('repo: {0}'.format(repo))
    #os.chdir(repo)
    filesToCheck = []
    for r,d,f in os.walk(repo):
      for file in f:
        if file.endswith('.java'):
          filesToCheck.append(os.path.join(r,file))
    filesOfInterest = []
    for f in filesToCheck:
      with open(f, 'r',encoding="utf-8",errors="surrogateescape") as fin:
        fileContainsFragment = False
        fileContainsOptionsMenu = False
        for line in fin:
          line = line.strip()
          #if 'Fragment' in line:
          if re.search(extendsFragmentPattern,line):
            fileContainsFragment = True
          elif 'onCreateOptionsMenu' in line:
            fileContainsOptionsMenu = True
          if fileContainsFragment and fileContainsOptionsMenu:
            filesOfInterest.append(f)
            break
    #for f in filesOfInterest:
    #  print(f)
    if len(filesOfInterest) > 0:
      randChoice = random.randrange(len(filesOfInterest))
      dirName, baseName = os.path.split(filesOfInterest[randChoice])
      removeSetHasOptionsMenuLine = shlex.split('comby -i -f {0} -d {1} -templates {2}'.format(baseName, dirName, onCreateTemplatesLocation))
      combyProcess = subprocess.run(removeSetHasOptionsMenuLine,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
      print('result of comby process: {0}'.format(combyProcess.returncode))
      for line in combyProcess.stdout.decode('utf-8').splitlines():
        print(line)
      print('changed file: {0}'.format(os.path.join(dirName, baseName)))
      print('comby command to cause change: {0}'.format(removeSetHasOptionsMenuLine))
      #input('stopped here for debugging')

#this method checks if the method definition of onCreateOptionsMenu exists
#in a file
def canInjectSetHasOptionsMenuProblem(repo):
  extendsFragmentPattern = re.compile('extends [\.\w]*Fragment ')
  #os.chdir(repo)
  filesToCheck = []
  for r,d,f in os.walk(repo):
    for file in f:
      if file.endswith('.java'):
        filesToCheck.append(os.path.join(r,file))
  filesOfInterest = []
  for f in filesToCheck:
    with open(f, 'r',encoding="utf-8",errors="surrogateescape") as fin:
      fileContainsFragment = False
      fileContainsOptionsMenu = False
      fileContainsOnCreate = False
      for line in fin:
        line = line.strip()
        #if 'Fragment' in line:
        if re.search(extendsFragmentPattern,line):
          fileContainsFragment = True
        #should I change to setHasOptionsMenu? I'm unsure at the moment
        #elif 'onCreateOptionsMenu' in line:
        elif 'setHasOptionsMenu(true)' in line:
          fileContainsOptionsMenu = True
        elif 'public void onCreate(' in line:
          fileContainsOnCreate = True
        if fileContainsFragment and fileContainsOptionsMenu and fileContainsOnCreate:
          print('file with all: {0}'.format(f))
          return True
          #filesOfInterest.append(f)
          #break
  #for f in filesOfInterest:
  #  print(f)
  return False

def injectSetHasOptionsMenuProblem(injectionFile):
  #print('running inject options menu issue')
  extendsFragmentPattern = re.compile('extends [\.\w]*Fragment ')
  #os.chdir(repo)
  #filesToCheck = []
  #for r,d,f in os.walk(repo):
    #for file in f:
      #if file.endswith('.java'):
        #filesToCheck.append(os.path.join(r,file))
  filesChanged = []
  #print(filesToCheck)
  #for f in filesToCheck:
  with open(injectionFile, 'r',encoding="utf-8",errors="surrogateescape") as fin:
    fileContainsFragment = False
    fileContainsOptionsMenu = False
    fileContainsOnCreate = False
    for line in fin:
      line = line.strip()
      #if 'Fragment' in line:
      if re.search(extendsFragmentPattern,line):
        fileContainsFragment = True
      #should I change to setHasOptionsMenu? I'm unsure at the moment;
      #I'll try it and see
      #elif 'onCreateOptionsMenu' in line:
      elif 'setHasOptionsMenu(true)' in line:
        fileContainsOptionsMenu = True
      elif 'public void onCreate(' in line:
        fileContainsOnCreate = True
      if fileContainsFragment and fileContainsOptionsMenu and fileContainsOnCreate:
        filesChanged.append(injectionFile)
        break
  #for f in filesOfInterest:
  #  print(f)
  if len(filesChanged) > 0:
    #randChoice = random.randrange(len(filesChanged))
    dirName, baseName = os.path.split(filesChanged[0])
    removeSetHasOptionsMenuLine = shlex.split('comby "setHasOptionsMenu(true);\n" "" -i {0} -d {1}'.format(baseName, dirName))
    commandList = shlex.split('open -a "Sublime Text" {0}'.format(injectionFile))
    subprocess.run(commandList)
    input('checking file before running comby')
    combyProcess = subprocess.run(removeSetHasOptionsMenuLine,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    for line in combyProcess.stdout.decode('utf-8').splitlines():
      print(line)
    print('changed file: {0}'.format(os.path.join(dirName, baseName)))

    print(filesChanged[0] == injectionFile)
    input('stopped here for debugging')
    return True
  else:
    return False


def resetAllRepos():
  resetCommand = shlex.split("git reset --hard HEAD")
  originalDir = os.getcwd()
  for r in compilingRepoList:
    repo = os.path.join(repoLocation,r)
    os.chdir(repo)
    print('changing to {0}'.format(repo))
    resetProcess = subprocess.run(resetCommand,stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    for line in resetProcess.stdout.decode('utf-8').splitlines():
      print(line)
 

#injectOptionsMenuProblem()
#resetAllRepos()
#repo = os.path.join(repoLocation,compilingRepoList[1])
#injectInflateProblem(repo)




#grepCommand = ['grep','inflate(','-r','.']
#grepResult = subprocess.run(grepCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
#print('comby result:')
#for line in combyResult.stdout.decode('utf-8').splitlines():
  #print('line: {0}'.format(line))
#print('')
 
