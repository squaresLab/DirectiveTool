#!/usr/local/bin/python3

import os
import shutil

packagedDirectory = '/Users/zack/git/DirectiveTool/packagedRepairTool'
directiveToolDir = '/Users/zack/git/DirectiveTool'
jarBuildDir = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2'
androidJar = '/Users/zack/git/DirectiveTool/runCheckerPackage/android.jar'

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

#copy the python files required to run the repair to that directory
determineMethodDifferenceFile = 'determineMethodDifferences.py'
shutil.copyfile(os.path.join(directiveToolDir, determineMethodDifferenceFile), os.path.join(packagedDirectory, determineMethodDifferenceFile))
gitHubRepairFile = 'repairMethodFromExampleOnGitHub.py'
shutil.copyfile(os.path.join(directiveToolDir, gitHubRepairFile), os.path.join(packagedDirectory, gitHubRepairFile))
changeMethodRepairFile = 'changeMethodOrderRepair.py'
shutil.copyfile(os.path.join(directiveToolDir, changeMethodRepairFile), os.path.join(packagedDirectory, changeMethodRepairFile))
runAllRepairsFile = 'runAllRepairs.py'
shutil.copyfile(os.path.join(directiveToolDir, runAllRepairsFile), os.path.join(packagedDirectory, runAllRepairsFile))
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





