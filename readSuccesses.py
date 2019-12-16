#!/usr/local/bin/python3

import os
import os.path
import urllib.request
import shutil
import subprocess
import socket
import time
import random

#number 11 seems like a real problem - 3 options menu issues
#difficult to find #18. Skipping for now. Also skipping #28 - large number of errors
#skipped a lot of setSelectorSetPackage analyses because they take too long
#also skipping getActivity checks since they are relatively high false positive rate
#36 looks like it might be an error but the error seems to obvious to be a problem;
#it would occur right when the app is logged in. The app is in a different language;
#doesn't compile from source; and requires me to log in to get to the problem, which
#I can't do at the moment
#45 could be an error but it won't load on the emulator due to a missing native library
#skipped 54 - need to get a better error message to tell me the specific class with the
#inflate problem
#63 is also tough to test because I'm not sure how to get to it
#A lot the errors seem to not happen the second time. I must have done something 
#wrong
#128 could be an options menu problem; but not the type that I can fix
#149 interesting getResources case I need to investigate more
#162 might be good to look into further
#currently stopped before finishing 22

requestTimeoutTime=500
checkerTimeoutTime=60
userAgentString='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
#skipCount = 149
skipCount = 29

def downloadAPK(apkLocation, apkSaveLocationOnMyMachine):
  socket.setdefaulttimeout(30)
  print('trying to download {0}'.format(apkLocation))
  req = urllib.request.Request(apkLocation, headers={'User-Agent': userAgentString})
  #req.retrieve(apkLocation, apkLocationOnMyMachine)
  done = False
  requestFailedCount = 0
  while not done:
    try:
      with urllib.request.urlopen(req, timeout=requestTimeoutTime) as response, open(apkSaveLocationOnMyMachine, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
        print('download succeeded')
        done = True
    except:
      requestFailedCount = requestFailedCount + 1 
      print('download request failed: {0} times'.format(requestFailedCount))
      time.sleep(random.randrange(300,400))

def runCheckerCommand(checkerToRun, apkLocationOnMyMachine, originalAPKName, successCount):
  firstPartOfCheckerCommand = '/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java'
  secondPartOfCheckerCommand = '-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=58721:/Applications/IntelliJ IDEA CE.app/Contents/bin'
  checkerCommand = '-Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes'.split(' ')
  checkerCommand.insert(0,secondPartOfCheckerCommand)
  checkerCommand.insert(0,firstPartOfCheckerCommand)
  currentCheckerCommand = checkerCommand
  checkerCommand.append(checkerToRun)
  checkerCommand.append(apkLocationOnMyMachine)
  originalDir = os.getcwd()
  os.chdir('/Users/zack/git/DirectiveTool/FlowDroidTest')
  outputCommand = checkerCommand.copy()
  outputCommand[1] = '"{0}"'.format(outputCommand[1])
  #print('running: {0}'.format(' '.join(outputCommand)))
  print('running checker: {0}'.format(checkerToRun))
  try:
    checkerResult = subprocess.run(checkerCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, timeout= checkerTimeoutTime)
  except subprocess.TimeoutExpired:
    print('skipping due to timeout')
    return -1

  #checkerProcess = subprocess.Popen(checkerCommand, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, close_fds=True)
  #outPipe = checkerProcess.communicate().stdout
  #line = outPipe.readline()
  #while line != '':
  #  print(line)
  #  line = outPipe.readline()
  #input('after checker result')
  print('past run')
  #checkerResult = subprocess.check_output(checkerCommand)
  os.chdir(originalDir)
  if checkerResult.returncode == 0:
    #print('checker result: {0}'.format(checkerResult))
    for line in checkerResult.stdout.decode('utf-8').splitlines():
      #print('line: {0}'.format(line))
      #for some reason the first line returned is processed as an integer
      if isinstance(line, str):
        if line.startswith('total'):
          print(line)
          lineItems = line.split(' ')
          if int(lineItems[-1]) == 0:
            print('checker found no errors this time')
            return 0
          else:
            print('checker ({0}) still found {1} errors in {2}'.format(checkerToRun, lineItems[-1], originalAPKName))
            return int(lineItems[-1])
        elif line.startswith('@@@@'):
          print(line)
        elif line.startswith('caught problems:'):
          print(line)

  else:
    print('!!!!checker encountered an error')
    for line in checkerResult.stdout.decode('utf-8').splitlines():
      print('line: {0}'.format(line))
    print('error on app #{0}'.format(successCount))
    input('press enter to skip due to error')
    return -1





def getMetadataFilename(metadataDir,repoName):
  repoInfoFilename = '{0}{1}.yml'.format(metadataDir,repoName)
  if not os.path.exists(repoInfoFilename):
    repoInfoFilename = '{0}{1}.txt'.format(metadataDir,repoName)
    if not os.path.exists(repoInfoFilename):
      raise Exception('unable to find {0}'.format(repoInfoFilename))
  return repoInfoFilename


def main():
  successCount = 0
  pastApk = ''
  apkSaveLocationOnMyMachine = '/Users/zack/git/DirectiveTool/apkWithError.apk'
  metadataDir = '/Users/zack/git/fdroiddata/metadata/'
  with open('/Users/zack/git/DirectiveTool/fDroidErrors.txt','r') as fin:
    for lineCount, line in enumerate(fin):
      line = line.strip()
      if line.startswith('success!'):
        if successCount >= skipCount:
          print(line)
          lineItems = line.split(' ')
          #handle the first case, and then we might come back and make 
          #it where changes do not occur between instances.
          if lineItems[-1] != pastApk:
            pastApk = lineItems[-1]
            downloadAPK(pastApk,apkSaveLocationOnMyMachine)
          checkerName = lineItems[5]
          #skipping getActivity for now since it seems to throw a lot of false positives
          if checkerName == "DetectIncorrectGetActivityMain":
            successCount = successCount + 1
            continue
          numberOfErrors = runCheckerCommand(checkerName, apkSaveLocationOnMyMachine, pastApk, successCount)
          if numberOfErrors > 0:
            #print(pastApk)
            repoName = pastApk.split('/')[-1].split('_')[0]
            #print(repoName)
            #input('stop to look')
            repoInfoFilename = getMetadataFilename(metadataDir, repoName)
            print('opening {0}'.format(repoInfoFilename))
            foundRepoLine = False
            foundSouceCodeLine = False
            with open(repoInfoFilename,'r') as mfin:
              for line in mfin:
                line = line.strip()
                if line.startswith('Repo: '):
                  lineItems = line.split(' ')
                  repoSite = lineItems[-1]
                  foundRepoLine = True
                  #break
                elif line.startswith('Repo:'):
                  lineItems = line.split(':')
                  repoSite = ':'.join(lineItems[1:])
                  foundRepoLine = True
                  #break
                elif line.startswith('Source Code:'):
                  lineItems = line.split(':')
                  sourceCodeSite = ':'.join(lineItems[1:])
                  foundSouceCodeLine = True
                if foundRepoLine and foundSouceCodeLine:
                  break
            print('opening in safari: {0}'.format(repoSite))
            commandString = 'open -a Safari {0}'.format(repoSite)
            returnCode = subprocess.call(commandString.split())
            print('return code: {0}'.format(returnCode))
            if returnCode == 1:
              print('opening in safari: {0}'.format(sourceCodeSite))
              commandString = 'open -a Safari {0}'.format(sourceCodeSite)
              returnCode = subprocess.call(commandString.split())
              if returnCode == 1:
                print('repo line in file {0}: {1}'.format(repoInfoFilename, line))
            input('press enter to finish with number {0}'.format(successCount))
          else:
            print('skipping number {0}'.format(successCount))
        successCount = successCount + 1
  print('finished with all errors')
  print('success count: {0}'.format(successCount))
  print('lines covered: {0}'.format(lineCount))

  

if __name__ == '__main__':
  main()