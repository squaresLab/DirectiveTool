#!/usr/local/bin/python3

import os

currentAppFolder = '/Users/zack/git/DirectiveTool/appsFromFDroid/'

appFileLineCount = 0
downloadedAppSet = set()
for file in os.listdir(currentAppFolder):
  filename = os.fsdecode(file)
  if filename.endswith(".apk"):  
    appFileLineCount = appFileLineCount + 1
    downloadedAppSet.add(filename)
missingAppCount = 0
for file in os.listdir('/Users/zack/Downloads/moreAPKs/'):
  filename = os.fsdecode(file)
  apkName = "{0}.apk".format(filename)
  if not apkName in downloadedAppSet:
    print(apkName)
    missingAppCount = missingAppCount + 1
print(missingAppCount)

