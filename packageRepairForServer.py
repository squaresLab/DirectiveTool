#!/usr/local/bin/python3

import os
import shutil

packagedDirectory = '/Users/zack/git/DirectiveTool/packagedRepairTool'
directiveToolDir = '/Users/zack/git/DirectiveTool'
jarBuildDir = '/Users/zack/git/DirectiveTool/FlowDroidTest/out/artifacts/AllJarsAttempt2'

#if the directory exists, delete it so we can make a new copy
if os.path.exists(packagedDirectory):
  shutil.rmtree(packagedDirectory)
os.mkdir(packagedDirectory)

#create a directory to store the jar builds and copy the jars there
newJarDir = os.path.join(packagedDirectory, 'checkerJars')
os.mkdir(newJarDir)
shutil.copytree(jarBuildDir, newJarDir)


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
shutil.copyfile(os.path.join())





