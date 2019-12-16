#!/usr/local/bin/python3
import os
import os.path


def main():
  logFileList = set()
  logFileLineCount = 0
  with open('fDroidDownloadLog.txt','r') as finLog:
    for line in finLog:
      line = line.strip()
      logFileList.add(line)
      logFileLineCount = logFileLineCount + 1
  print('lines in log: {0}, uniqueApps: {1}'.format(logFileLineCount, len(logFileList)))
  uniqueAppsInLogFile = set()
  conflictedFiles = []
  for apk in logFileList:
    apkToAdd = apk.split('/')[-1].split("_")[0] 
    if apkToAdd in uniqueAppsInLogFile:
      conflictedFiles.append(apkToAdd)
    uniqueAppsInLogFile.add(apkToAdd)
  #for apk in logFileList:
  #  for c in conflictedFiles:
  #    if c in apk:
  #      print(apk)
  print('size of unique apps list: {0}'.format(len(uniqueAppsInLogFile)))
  downloadedAppSet = set()
  appFileLineCount = 0
  repeatedBasenames = []
  for file in os.listdir(os.path.join(os.getcwd(), 'appsFromFDroid')):
    filename = os.fsdecode(file)
    if filename.endswith(".apk"):  
      appFileLineCount = appFileLineCount + 1
      appBaseName = filename.split('_')[0] 
      if appBaseName in downloadedAppSet:
        print('file with matching base name: {0}'.format(filename))
        repeatedBasenames.append(appBaseName)
      downloadedAppSet.add(appBaseName)
  for file in os.listdir(os.path.join(os.getcwd(), 'appsFromFDroid')):
    filename = os.fsdecode(file)
    if filename.endswith(".apk"):  
      appBaseName = filename.split('_')[0] 
      if appBaseName in repeatedBasenames:
        print('apps with copies: {0}'.format(filename))
  print('apks in directory: {0}'.format(appFileLineCount))
  print('downloaded app count: {0}'.format(len(downloadedAppSet)))
  input('stop to see output')
  print('apps downloaded that were not in the download list') 
  notDownloadedList = uniqueAppsInLogFile.difference(downloadedAppSet) 
  print(notDownloadedList)
  input('stop to see output')
  print('apps that that were in the download list but were not downloaded')
  print(downloadedAppSet.difference(uniqueAppsInLogFile))
  print('full sites for undownloaded apps:')
  with open('fDroidDownloadLog.txt','r') as finLog:
    for line in finLog:
      line = line.strip()
      for missingApp in notDownloadedList:
        if missingApp in line:
          print(line)



if __name__ == "__main__":
  main()