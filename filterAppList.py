#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import time
import subprocess
import os
import sys
import shutil
import random
import math

timeoutTime=60
sleepSeconds = 60
userAgentString='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'

def requestPage(pageName):
  #urllib.request.urlopen(newSite)
  #req = urllib.request.Request(pageName, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
  #my current user agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15
  req = urllib.request.Request(pageName, headers={'User-Agent': userAgentString})
  #req.add_header('Referer', 'http://www.python.org/')
  # Customize the default User-Agent header value:
  #req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
  result = None
  requestFailedCount = 0
  while result == None:
    try:
      result = urllib.request.urlopen(req, timeout=timeoutTime)
    except:
      requestFailedCount = requestFailedCount + 1 
      print('page request failed: {0} times'.format(requestFailedCount))
      time.sleep(random.randrange(300,400))
  return result

def downloadAPK(apkLocation, apkSaveLocationOnMyMachine):
  req = urllib.request.Request(apkLocation, headers={'User-Agent': userAgentString})
  #req.retrieve(apkLocation, apkLocationOnMyMachine)
  done = False
  requestFailedCount = 0
  while not done:
    try:
      with urllib.request.urlopen(req, timeout=timeoutTime) as response, open(apkSaveLocationOnMyMachine, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        done = True
    except:
      requestFailedCount = requestFailedCount + 1 
      print('download request failed: {0} times'.format(requestFailedCount))
      time.sleep(random.randrange(300,400))


siteSet = set()
with open('fDroidAppSiteList.txt','r') as fin:
  for line in fin:
    line = line.strip()
    siteSet.add(line.split('/')[-1])
print(len(siteSet))
appFileLineCount = 0  
downloadedAppSet = set()
for file in os.listdir(os.path.join(os.getcwd(), 'appsFromFDroid')):
  filename = os.fsdecode(file)
  if filename.endswith(".apk"):  
    appFileLineCount = appFileLineCount + 1
    appBaseName = filename.split('_')[0]
    downloadedAppSet.add(appBaseName)
print(len(downloadedAppSet))
for s in siteSet:
  print('|{0}|'.format(s))
  break
for d in downloadedAppSet:
  print('|{0}|'.format(d))
  break
print('app diffs')
firstDiff = siteSet.difference(downloadedAppSet) 
print(len(firstDiff))
print('-----')
secondDiff = downloadedAppSet.difference(siteSet)  
print(len(secondDiff))
print(firstDiff)
print('')
print(secondDiff)
downloadCount = 0
with open('/Users/zack/Desktop/downloadProblems.txt','w') as fout:
  for package in firstDiff:
    newSite = 'https://f-droid.org/en/packages/{0}'.format(package)
    with requestPage(newSite) as downloadSite:
      print('received site {0} response'.format(downloadCount))
      packageDownloadSoup = BeautifulSoup(downloadSite.read(), 'html.parser')
      #print(packageDownloadSoup)
      apkLocations = packageDownloadSoup.find_all("p", class_='package-version-download')
      #print(apkLocations)
      #exit(0)
      apkLocation = apkLocations[0].b.a['href']
      #if apkLocation in checkedRepos:
      #  print('already tested {0}'.format(apkLocation))
        #shouldSleep = False
      #else:
        #shouldSleep = True
      time.sleep(sleepSeconds)
      print('apk location: {0}'.format(apkLocation))
      apkBaseName = apkLocation.split('/')[-1][:-4]
      apkLocationOnMyMachine = '/Users/zack/Downloads/moreAPKs/{0}'.format(apkBaseName)
      apkPackage = apkBaseName.split('_')[0]
      if apkPackage != package:
        print('apk base name: {0}'.format(apkPackage), file=fout)
        print('apk base name: {0}'.format(apkPackage))
        print('package: {0}'.format(package), file=fout)
        print('package: {0}'.format(package))
        print('----------------', file=fout)
        print('----------------')
      downloadAPK(apkLocation, apkLocationOnMyMachine)
      downloadCount = downloadCount + 1

