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
  callgraphErrorCount = 0
  analyzedApplicationCount = 0
  sleepSeconds=120
  firstPartOfCheckerCommand = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java'
  secondPartOfCheckerCommand = '-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=58721:/Applications/IntelliJ IDEA CE.app/Contents/bin'
  checkerCommand = '-Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes'.split(' ')
  checkerCommand.insert(0,secondPartOfCheckerCommand)
  checkerCommand.insert(0,firstPartOfCheckerCommand)
  checkerNames = ['DetectInvalidInflateCallMain','DetectIncorrectGetActivityMain',
    'DetectMissingSetHasOptionsMenu', 'DetectSetArgumentsMain',
    'DetectInvalidSetContentViewFindViewByIDOrdering', 'DetectInvalidGetResources',
    'DetectIncorrectSetInitialSavedState', 'DetectInvalidSetTheme',
    'DetectSetSelectorSetPackageProblem']
 
  fdroidBase = "https://f-droid.org/"
  #fdroidMainPage = "https://f-droid.org/en/packages/" 
  fdroidMainPage = "{0}en/packages/".format(fdroidBase)
  logFileName = '/Users/zack/git/DirectiveTool/fDroidLog.txt' 
  errorFileName = '/Users/zack/git/DirectiveTool/fDroidErrors.txt'
  checkedRepos = []
  if os.path.exists(logFileName):
    with open(logFileName,'r') as fin:
      for line in fin:
        lineItems = line.strip().split(',')
        checkedRepos.append(lineItems[0])
        #always set so that the final value will be the last value
        #in the lopp
        analyzedApplicationCount = int(lineItems[1])
        callgraphErrorCount = int(lineItems[2])
  checkedReposCount = len(checkedRepos)
  packagesCheckedOnThisRun = 0
  with open(logFileName,'a') as fout:
    with open(errorFileName,'a') as ferrOut:
      #30 is the number of repos per page
      reposPerFDroidPage = 30
      pagesFinished = math.floor(checkedReposCount/reposPerFDroidPage) 
      packagesCheckedOnThisRun = 30 * pagesFinished
      for i in range(pagesFinished + 1,67):
        if i != 1:
          currentFdroidMainPage = "{0}{1}/".format(fdroidMainPage,i)
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
            if packagesCheckedOnThisRun < checkedReposCount:
              packagesCheckedOnThisRun = packagesCheckedOnThisRun + 1
            else:
              packagesCheckedOnThisRun = packagesCheckedOnThisRun + 1
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
                apkLocationOnMyMachine = '/Users/zack/Downloads/test.apk' 
                downloadAPK(apkLocation, apkLocationOnMyMachine)
                print('testing app: {0}'.format(apkLocation))
                analyzedApplicationCount = analyzedApplicationCount + 1
                for checker in checkerNames:
                  currentCheckerCommand = checkerCommand
                  checkerCommand.append(checker)
                  checkerCommand.append(apkLocationOnMyMachine)
                  originalDir = os.getcwd()
                  os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
                  checkerResult = subprocess.run(checkerCommand, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                  #checkerResult = subprocess.check_output(checkerCommand)
                  os.chdir(originalDir)
                  if checkerResult.returncode == 0:
                    print('checker result: {0}'.format(checkerResult))
                    for line in checkerResult.stdout.decode('utf-8').splitlines():
                      print('line: {0}'.format(line))
                      #for some reason the first line returned is processed as an integer
                      if isinstance(line, str):
                        if line.startswith('total'):
                          lineItems = line.split(' ')
                          if int(lineItems[-1]) != 0:
                            print("found an error with checker {0} in app {1}".format(checker, apkLocation))
                            ferrOut.write("success! error found: with checker {0} in app {1}\n".format(checker, apkLocation))
                            ferrOut.flush()
                            os.fsync(ferrOut.fileno())
                            #input("stopping to let you investigate. Press enter to continue")
                  else: 
                    wasCallGraphError = False
                    for line in checkerResult.stderr.decode('utf-8').splitlines():
                      if line.strip() == "[main] ERROR soot.jimple.infoflow.android.SetupApplication - Could not construct callgraph":
                        wasCallGraphError = True
                        callgraphErrorCount = callgraphErrorCount + 1
                        break
                    if not wasCallGraphError:
                      print('there was an error running {0} on {1}'.format(checker, apkLocation))
                      ferrOut.write("error; couldn't run: checker {0} on app {1}\n".format(checker, apkLocation))
                      ferrOut.flush()
                      os.fsync(ferrOut.fileno())
  #input('stopping to let you check. Press enter to continue')
                fout.write('{0},{1},{2}\n'.format(apkLocation, analyzedApplicationCount, callgraphErrorCount))
                fout.flush()
                os.fsync(fout.fileno())

  print('number of applications downloaded/analyzed: {0}'.format(analyzedApplicationCount))
  print('number of call graph errors: {0}'.format(callgraphErrorCount))


if __name__ == "__main__":
  main()