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

timeoutTime=120
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


def main():
  firstTime = True
  sleepSeconds=120
  fdroidBase = "https://f-droid.org/"
  #fdroidMainPage = "https://f-droid.org/en/packages/" 
  fdroidMainPage = "{0}en/packages/".format(fdroidBase)
  startingDir = os.getcwd()
  logFileName = '{0}/fDroidAppSiteList.txt'.format(startingDir)
  apkFolderLocation = '{0}/appsFromFDroid'.format(startingDir)
  if not os.path.exists(apkFolderLocation):
    os.makedirs(apkFolderLocation)
  checkedRepos = []
  if os.path.exists(logFileName):
    with open(logFileName,'r') as fin:
      for line in fin:
        lineItems = line.strip()
        checkedRepos.append(lineItems[0])
        #always set so that the final value will be the last value
        #in the loop
  checkedReposCount = len(checkedRepos)
  packagesCheckedOnThisRun = 0
  with open(logFileName,'a') as fout:
    #30 is the number of repos per page
    reposPerFDroidPage = 30
    pagesFinished = math.floor(checkedReposCount/reposPerFDroidPage) 
    appsAlreadyDownloaded = 30 * pagesFinished
    for i in range(pagesFinished + 1,67):
      if i != 1:
        currentFdroidMainPage = "{0}{1}/".format(fdroidMainPage,i)
      else:
        currentFdroidMainPage = fdroidMainPage
      if not firstTime:
        time.sleep(sleepSeconds)
      print('trying to open: {0}'.format(currentFdroidMainPage))
      with requestPage(currentFdroidMainPage) as response:
        print('got new page')
        soup = BeautifulSoup(response.read(), 'html.parser') 
        packageList = soup.find(id="full-package-list")
        for packageLink in soup.find_all("a", class_="package-header"):
          print(packageLink['href'])
          print('{0}'.format(packageLink['href']), file=fout)
  print('number of applications downloaded: {0}'.format(checkedReposCount))


if __name__ == "__main__":
  main()