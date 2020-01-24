#!/usr/local/bin/python3

import os
import shutil
import re
import sys

packagedDirectory = '/Users/zack/git/DirectiveTool/packagedRepairTool'
directiveToolDir = '/Users/zack/git/DirectiveTool'
jarBuildDir = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2'
androidJar = '/Users/zack/git/DirectiveTool/runCheckerPackage/android.jar'
extractMethodInfoJarsLocation = '/Users/zack/git/DirectiveTool/ExtractMethodInfo/squareslab.zackc/artifacts/ExtractMethodInfoJars'
checkerExecutionFromSourceStringPattern = re.compile(r'/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java "-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=[0-9]+:/Applications/IntelliJ IDEA CE.app/Contents/bin" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar')
checkerExecutionFromJarString = 'java -jar ./AllJarsAttempt2/AndroidDirectiveChecker.jar'
runGetMethodLocationsFromJarString = "'java -jar ./ExtractMethodInfoJars/ExtractMethodInfo.jar'"
getMethodsCheckString = 'runGetMethodLocations ='
startOfFilesystemString = '/Users/zack'
gitFolderString = '/Users/zack/git'

#where ever I move this code, it will either need to update the fdroid repos location
#here or later
#I could include the fDroid repos in the packaging, but they are multiple GBs in 
#size, so it's probably not worth it
fdroidReposLocationString = 'reposFromFDroid'
newFdroidReposLocation = '../../reposFromFDroid'

#these paths are for testing and may be removed later when the tests are removed from the code
listOfRepos = '/Users/zack/git/DirectiveTool/injectFaultsDir/reposWithSuccessfulTests.txt'
#organized as fileToChange, startOfLineToChange, newLine
extraChanges = {}
extraChanges['runInjectionTests.py'] = [('workingReposFile', 'workingReposFile = \'./testDirs.txt\'\n')]

#High level - first copy all the files over, then automatically change any code with paths
#to either the right path or computer independent path

#if the directory exists, delete it so we can make a new copy
if os.path.exists(packagedDirectory):
  print("packaged directory exists: {0}".format(packagedDirectory))
  shutil.rmtree(packagedDirectory)
  print('deleting old versions')
os.mkdir(packagedDirectory)

#create a directory to store the jar builds and copy the jars there
newJarDir = os.path.join(packagedDirectory, 'checkerJars')
shutil.copytree(jarBuildDir, newJarDir)
#copy the android jar to the folder
shutil.copy(androidJar, packagedDirectory)
#copy the extract info jars into the folder
shutil.copytree(extractMethodInfoJarsLocation,os.path.join(packagedDirectory, 'ExtractMethodInfoJars'))

#copy the python files required to run the repair to that directory
determineMethodDifferenceFile = 'determineMethodDifferences.py'
shutil.copyfile(os.path.join(directiveToolDir, determineMethodDifferenceFile), os.path.join(packagedDirectory, determineMethodDifferenceFile))
gitHubRepairFile = 'repairMethodFromExampleOnGitHub.py'
shutil.copyfile(os.path.join(directiveToolDir, gitHubRepairFile), os.path.join(packagedDirectory, gitHubRepairFile))
changeMethodRepairFile = 'changeMethodOrderRepair.py'
shutil.copyfile(os.path.join(directiveToolDir, changeMethodRepairFile), os.path.join(packagedDirectory, changeMethodRepairFile))
runAllRepairsFile = 'runAllRepairs.py'
shutil.copyfile(os.path.join(directiveToolDir, runAllRepairsFile), os.path.join(packagedDirectory, runAllRepairsFile))
repoInfoFile = 'extractRepoInfo.py'
shutil.copyfile(os.path.join(directiveToolDir, repoInfoFile), os.path.join(packagedDirectory, repoInfoFile))

levenshteinFile = 'levenshteinDistance.py'
shutil.copyfile(os.path.join(directiveToolDir, levenshteinFile), os.path.join(packagedDirectory, levenshteinFile))
repairFoundErrorsFile = 'repairFoundErrors.py'
#shutil.copyfile(os.path.join(directiveToolDir, repai))

filesInInjectionFolderToCopyList = ['determineInjectionReposForEachInjectionType.py',
'injectGetActivityIssue.py',
'injectGetResourcesIssue.py',
'injectInflateAndOptionsMenuIssues.py',
'injectSetArgumentsProblem.py',
'injectSetContentViewIssue.py',
'injectSetInitialSavedStateProblem.py',
'injectSetPackageSetSelectorProblem.py',
'injectSetThemeIssue.py',
'runInjectionTests.py',]

injectionFolder = 'injectFaultsDir'
os.mkdir(os.path.join(packagedDirectory,injectionFolder))
for f in filesInInjectionFolderToCopyList:
  sourceFile = os.path.join(directiveToolDir, injectionFolder, f)
  destFile = os.path.join(packagedDirectory, injectionFolder, f)
  shutil.copyfile(sourceFile, destFile)
shutil.copytree('/Users/zack/git/DirectiveTool/injectFaultsDir/onCreateOptionsMenuTemplates', os.path.join(packagedDirectory, injectionFolder,'onCreateOptionsMenuTemplates'))

#now that everything is copied over, change the file paths

for root, dirs, files in os.walk(packagedDirectory):
  for f in files:
    fullFilename = os.path.join(root, f)
    fileContents = []
    madeChange = False
    extraChangeList = []
    if f in extraChanges:
      extraChangeList = extraChanges[f]
    with open(fullFilename, 'r', encoding="utf-8",errors="surrogateescape") as fin:
      for line in fin:
        #found a line that runs the code from the java source and is not a comment
        #save comments, but don't try to adjust the code in them
        if not line.strip().startswith('#'):
          if 'IntelliJ' in line:
            checkerMatch = re.search(checkerExecutionFromSourceStringPattern, line)
            if checkerMatch:
              line = re.sub(checkerExecutionFromSourceStringPattern, checkerExecutionFromJarString, line)
              print(line)
              print('file: {0}'.format(fullFilename))
              input('check to see if the checker replacement string is correct')
              madeChange = True
            elif line.strip().startswith(getMethodsCheckString):
              line = getMethodsCheckString + ' ' + runGetMethodLocationsFromJarString + '\n'
              print(line)
              print('file: {0}'.format(fullFilename))
              input('check to see if this is correct')
              madeChange = True
            else:
              print(line)
              print('need to write a way to handle IntelliJ line')
              print('file: {0}'.format(fullFilename))
              sys.exit(0)
          elif directiveToolDir in line:
            line = line.replace(directiveToolDir, '.')
            print(line)
            print('file: {0}'.format(fullFilename))
            input('stop to see if the line is correct')
            madeChange = True
          elif startOfFilesystemString in line:
            if gitFolderString in line:
              line = line.replace(gitFolderString,'.')
              madeChange = True
              print(line)
              print('file: {0}'.format(fullFilename))
              input('check to see removing FlowDroidTest is correct')
            else:
              print(line)
              print('need to write a way to handle filesystem line')
              print('file: {0}'.format(fullFilename))
              sys.exit(0)

          #also remove the references to the FlowDroidTest directory, because I
          #don't need to execute the checkers in that directory with the new set up
          if 'FlowDroidTest' in line:
            line = line.replace('FlowDroidTest','')
            madeChange = True
            if '//' in line:
              line = line.replace('//','/')
            print(line)
            print('file: {0}'.format(fullFilename))
            input('check to see removing FlowDroidTest is correct')
          if fdroidReposLocationString in line:
            line = line.replace(fdroidReposLocationString, newFdroidReposLocation)
            madeChange = True
            print(line)
            print('file: {0}'.format(fullFilename))
            input('check to see removing FlowDroidTest is correct')
          #I might want to move this extra Change list stuff to a new method
          if len(extraChangeList) > 0:
            newChangeList = []
            usedChangeItem = False
            for changeItem in extraChangeList:
              if line.strip().startswith(changeItem[0]):
                line = changeItem[1]
                madeChange=True
                print(line)
                print('file: {0}'.format(fullFilename))
                input('check to see removing FlowDroidTest is correct')
                #remove the use changedItem from the list by not saving it
                usedChangeItem = True
              else:
                #save unused changeItems again
                newChangeList.append(changeItem)
            if usedChangeItem:
              extraChanges[f] = newChangeList
        fileContents.append(line)
    if madeChange:
      with open(fullFilename, 'w', encoding="utf-8",errors="surrogateescape") as fout:
        for line in fileContents:
          print(line, file=fout, end ='')
      print('updated: {0}'.format(fullFilename))

#This code is just for testing the packaged directory and may be removed later
shutil.copyfile(listOfRepos, os.path.join(packagedDirectory, injectionFolder, 'testDirs.txt'))






