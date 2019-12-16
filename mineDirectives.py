#!/usr/local/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import time
import random

userAgentString='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
startingPage = 'https://developer.android.com/reference/packages'
basePageString = 'https://developer.android.com'
sleepTime=10
timeoutTime=20


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

def getAPIPageLinks():
  with requestPage(startingPage) as response:
    soup = BeautifulSoup(response.read(), 'html.parser') 
    with open("startingPageOutput.txt",'w') as fout:
      for line in soup:
        print("{0}\n".format(line),file=fout)
    #print(soup)
    dropDownList = soup.find('devsite-book-nav')
    apiPages = dropDownList.find_all('a')
    with open('apiPageLinks.txt','w') as fout:
      for linkItem in apiPages:
        try:
          print("{0}{1}".format(basePageString,linkItem['href']),file=fout)
          fout.flush()
          os.fsync(fout.fileno())
        except:
          #print('error with item:')
          #print(linkItem)
          #input('press enter to continue')
          #just skip the ones I can't handle for now
          pass
  time.sleep(sleepTime)

def checkIfStringIsDirective(inputString):
  #print('checking: {0}'.format(inputString))
  #inputString = inputString.decode('utf-8',"ignore")
  try:
    inputString = inputString.contents[0]
  except:
    #sometimes I seem to get elements that don't have contents
    #not sure why but don't extract those cases
    inputString = inputString
  if 'must' in inputString:
    return True
  elif 'Must' in inputString:
    return True
  elif 'forget' in inputString:
    return True
  elif 'Forget' in inputString:
    return True
  else:
    return False

def searchThroughAPIdocs():
  foundCount = 0
  with open('apiPageLinks.txt','r') as fin:
    with open('possibleDirectives.txt','w') as fout:
      for site in fin:
        site = site.strip()
        with requestPage(site) as response:
          soup = BeautifulSoup(response.read(), 'html.parser')
          textSegments = soup.find_all('p')
          for textItem in textSegments:
            #print(textItem)
            if checkIfStringIsDirective(textItem):
              print('{0} {1}'.format(site,textItem),file=fout)
              print('found item of interest: {0}'.format(foundCount))
              foundCount = foundCount + 1
        time.sleep(sleepTime)

def testOnePage():
  foundCount = 0
  testSite = 'https://developer.android.com/guide/topics/ui/layout/recyclerview'
  with requestPage(testSite) as response:
    soup = BeautifulSoup(response.read(), 'html.parser')
    textSegments = soup.find_all('p')
    for textItem in textSegments:
      #print(textItem)
      if checkIfStringIsDirective(textItem):
        #print('{0} {1}'.format(testSite,textItem),file=fout)
        print('found item of interest: {0}'.format(foundCount))
        foundCount = foundCount + 1
    time.sleep(sleepTime)
    print('found count: {0}'.format(foundCount))

def main():
  searchThroughAPIdocs()



if __name__ == "__main__":
  main()