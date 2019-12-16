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
  sleepSeconds=120
  fdroidBase = "https://f-droid.org/"
  #fdroidMainPage = "https://f-droid.org/en/packages/" 
  fdroidMainPage = "{0}en/packages/".format(fdroidBase)
  startingDir = os.getcwd()
  logFileName = '{0}/fDroidDownloadLog.txt'.format(startingDir)
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
      time.sleep(sleepSeconds)
      print('trying to open: {0}'.format(currentFdroidMainPage))
      with requestPage(currentFdroidMainPage) as response:
        print('got first response')
        soup = BeautifulSoup(response.read(), 'html.parser') 
        packageList = soup.find(id="full-package-list")
        #not sleeping after we skip the repo if we already covered it.
        #shouldSleep only affects the following sleep check, not the 
        #previous one
        #shouldSleep = True
        for packageLink in soup.find_all("a", class_="package-header"):
          #print(fdroidMainPage)
          #print(packageLink)
          #assuming that packages are always listed in the same order,
          #we can skip to the next package that we haven't tested
          if appsAlreadyDownloaded < checkedReposCount:
            appsAlreadyDownloaded = appsAlreadyDownloaded + 1
          else:
            appsAlreadyDownloaded = appsAlreadyDownloaded + 1
            if appsAlreadyDownloaded > 5:
              sys.exit(0)
            newSite = "{0}{1}".format(fdroidBase, packageLink['href'][1:])
            #if shouldSleep: 
            #  time.sleep(sleepSeconds)
            #print('new site: {0}'.format(newSite))
            print('new site: {0}'.format(newSite))
            #sys.exit(0)
            with requestPage(newSite) as downloadSite:
              print('got second response')
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
              apkLocationOnMyMachine = '{0}{1}{2}.apk'.format(apkFolderLocation,os.path.sep,apkBaseName) 
              downloadAPK(apkLocation, apkLocationOnMyMachine)
              print('{0}'.format(apkLocation), file=fout)
  print('number of applications downloaded: {0}'.format(checkedReposCount))


if __name__ == "__main__":
  main()