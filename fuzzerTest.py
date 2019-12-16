#!/usr/local/bin/python3

import subprocess
import os

def main():
  #adb shell monkey -p your.package.name -v 500 
  crashSeed = "1568503947674"
  originalDir = os.getcwd()
  packageDir = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
  packageName = 'a2dp.Vol_137'
  apkName = '{0}{1}.apk'.format(packageDir, packageName)
  commandList = ["adb","install", apkName]
  subprocess.run(commandList)
  commandList = ["adb", "shell", "monkey", "-p"]
  commandList.append(packageName.split('_')[0])
  commandList.append('-s')
  commandList.append(crashSeed)
  commandList = commandList + ["-v", "100"]
  os.chdir(packageDir)
  print('executing in {0}'.format(packageDir))
  subprocess.run(commandList)
  os.chdir(originalDir)

if __name__ == "__main__":
  main()