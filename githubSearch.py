#!/usr/local/bin/python3

import subprocess
import json
import time
import urllib
import requests
from bs4 import BeautifulSoup

def checkProgramOfInterest(rawLinkString, programOfInterest):
  containsAsyncTask = False
  containsGetResources = False
  print('\n\n')
  for line in programOfInterest.splitlines():
    print(line)
    if 'AsyncTask' in line:
      containsAsyncTask = True
    if 'getResources' in line:
      containsGetResources = True
    if containsAsyncTask and containsGetResources:
      print('!!!!!!!!!!!!!!!!!!!!!')
      print('{0} contains types of interest'.format(rawLinkString))
      return


def main():
  pageNumber = 1
  command = 'curl -n https://api.github.com/search/code?q=getResources+AsyncTask+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
  commandList = command.split(" ")
  commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
  searchResult = json.loads(commandOutput)
  currentCount = 0
  while currentCount < 99:
    urlToSearch = searchResult['items'][currentCount]['html_url']
    if urlToSearch.endswith('.java'):
      #print('searching first url: {0}'.format(urlToSearch))
      print('{0}'.format(currentCount))
      #response = session.get(urlToSearch).content.decode('utf-8')
      #soup = BeautifulSoup(response, 'html.parser')
      #for link in soup.find_all('a'):
           #print(link.contents)
      #  if(link.contents[0].endswith('.java')):
      time.sleep(1)
      #pageRequest = session.get(urlToSearch).content
      with urllib.request.urlopen(urlToSearch) as pageRequest:
        #read is read once, so save the result
        pageResult = pageRequest.read()
        soup2 = BeautifulSoup(pageResult, 'html.parser')
        rawLink = soup2.find_all(id='raw-url')[0]
        time.sleep(1)
        #print('raw link: {0}'.format(rawLink))
        rawLinkString = "https://github.com/" + rawLink['href']
        with urllib.request.urlopen(rawLinkString) as finalResults:
          programOfInterest = finalResults.read().decode('utf-8', errors="ignore")
          checkProgramOfInterest(rawLinkString,programOfInterest)
    currentCount = currentCount + 1

#pageNumber = 1
  #notDone = True
  #changeSet = set()
  #while notDone: 
  #  saveFileName = 'savedGitHubSearches/savedSearch{0}.json'.format(pageNumber)
  #  if os.path.isfile(saveFileName):
  #    with open(saveFileName,'r') as fin:
  #      searchResult = json.loads(fin.read())
  #  else:
  #    #command = 'curl -n https://api.github.com/search/code?q=onCreate+Fragment+onCreateOptionsMenu+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
  #    command = 'curl -n https://api.github.com/search/code?q=onCreateView+Fragment+in:file+language:java?page={0}&per_page=100&sort=stars&order=desc'.format(pageNumber)
  #    commandList = command.split(" ")
  #    commandOutput = subprocess.run(commandList, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8') 
  #    searchResult = json.loads(commandOutput)
  #    with open(saveFileName,'w') as fout:
  #      json.dump(searchResult,fout)

if __name__ == "__main__":
  main()
