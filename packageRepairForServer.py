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
repairFoundErrorsFile = 'repairFoundErrors.py'
#shutil.copyfile(os.path.join(directiveToolDir, repai))


injectionFolder = 'injectFaultsDir'
shutil.copytree(os.path.join(directiveToolDir, injectionFolder), os.path.join(packagedDirectory, injectionFolder))





