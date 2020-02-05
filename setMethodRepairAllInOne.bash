#!/bin/bash

#manual set up steps currently required
#1. Change the Violations of directives repo to the right application to fix
#2. create the APK for the application (the code here should also do this if you skip this step, 
#.  but I haven't checked and I'm not 100% sure)
#3. change the programName variable in the runChecker function 
#4. run this file to make sure everything is set up correctly
#5. change the method declaration string to compare in repairMethodFromExampleOnGitHub.py 
# to the callback of interest
#6. change the checkerToRun variable in the repairMethodFromExampleOnGitHub
#7. change the fileToChange if required
#8. change the search (curl) command around line 730 (I say around because I keep adding 
#.  and deleting lines, so the line count may not be exactly correct)
#9. Might need to change all the paths in repairMethodFromExample.. to your path settings
#10. Delete the savedGitHubSearches folder unless the search query remained the same 
#   or you can reuse the old results
#11. repairMethodExampleOnGitHub.. is now ready to run

#call with the file to save the check results to as the first parameter
function runChecker
{
previousDir=`pwd`
cd ~/git/DirectiveTool/FlowDroidTest
#programName=DetectMissingSetHasOptionsMenu
#programName=DetectSetArgumentsMain
#programName=DetectInvalidInflateCallMain
checkerCommand=("$@")  
echo "${checkerCommmand[@]}"
#echo "second argument: $2"
#echo "third argument: $3"
#echo "--------------"
#echo ${checkerCommand[@]} $2 $3
#"$1 $2 $3"> $4 2>/dev/null
#echo ";;;;;;;;;;;;;;;;;"
#fullCommand="${checkerCommand[@]}"
#saveFile=${checkerCommand[-1]}
saveFile=${checkerCommand[${#checkerCommand[@]}-1]}
#echo "${checkerCommand[@]::${#checkerCommand[@]}-1}> $saveFile 2>/dev/null"
#echo "stopping to check checker command in setMethodRepair"
#read n
fullCommand="${checkerCommand[@]::${#checkerCommand[@]}-1}> $saveFile 2>/dev/null"
#tempErrorFile=${saveFile/testResults/testErrors}
#fullCommand="${checkerCommand[@]::${#checkerCommand[@]}-1}> $saveFile 2> $tempErrorFile"
#echo $fullCommand
eval $fullCommand
#exit 0
cd $previousDir
}

function showDiff
{
echo "in show diff"
testFolder=$1
testDir=$2
#this change currently hard codes the folder name that the repairs use to 
#test changes by default. I should probably figure out how to avoid this 
#hard coding, but it works in the default case
temporaryTestFolder=${testFolder/testFolder/temporaryTestOfChange}
#rm -rf $temporaryTestFolder
#cp -r $testDir $temporaryTestFolder
cd $temporaryTestFolder
fileCount=0
while read file 
  do 
  if [ $file ] 
  then
    echo "|$file| [ -n $file ]"
    echo "git diff -U$(wc -l $file) $file"
    lineCountOfFile=$(wc -l $file | { read first rest ; echo $first ; }) #$(wc -l $file | cut -d " " -f 1) # | sed -e 's/^[[:space:]]*//'
    echo "line count of file: $lineCountOfFile"
    diffOutputFile=$temporaryTestFolder/DiffResult$fileCount.txt
    git diff -U$lineCountOfFile $file > $diffOutputFile
    fileCount=$(($fileCount + 1))
    #sublime $diffOutputFile
    open -a "Sublime Text" $diffOutputFile
  fi
  done <<EOF
$(git diff --name-only)
EOF
echo "end of show diff"
}

#for currentCheckerNumber in 1 2 3 4 5 6 7 8 9
#do
#TODO: add methods of interest
currentCheckerNumber=1
  case $currentCheckerNumber in
    #works!
    1) gitBranch=FAULT_012_SO_19597901
       checker=DetectInvalidInflateCallMain
       appName=Application
       repairType=GitHub
       scriptDir=/Users/zack/git/DirectiveTool/
       methodDeclarationStringToCompare="public View onCreateView"
       methodOfInterest1=inflate
       #eventually I might want to have the repair just automatically include
       #the method of interest in the terms of interest, but doing this quick 
       #change now because it's faster and I'm not sure what problems the other
       #approach could cause without trying it out
       termsOfInterest="Fragment inflate";;
    #works! But I need to add a heuristic later to make the repair more sensical;
    #partially done, currently moving the method to a method in the class 
    #with the problem; but could add lifecycle guided information to the repair
    2) gitBranch=FAULT_013_SO_6215239
       checker=DetectIncorrectGetActivityMain
       appName=Application
       methodOfInterest1=getActivity
       repairType=Method;;
    #works for missing setHasOptionsMenu(true); haven't successfully repaired
    #missing onCreateOptionsMenuDefinition - Need to create a new repair for it
    3) gitBranch=FAULT_017_SO_29115050
       checker=DetectMissingSetHasOptionsMenu
       appName=Application
       repairType=GitHub
       scriptDir=/Users/zack/git/DirectiveTool/
       methodDeclarationStringToCompare="public void onCreate"
       termsOfInterest="Fragment onCreateOptionsMenu";;
    #not working at the moment; doesn't provide call chain information
    4) gitBranch=FAULT_63_SO_19999172_forRepair
       checker=DetectSetArgumentsMain
       appName=Application
       methodOfInterest1=setArguments
       scriptDir=/Users/zack/git/DirectiveTool/
       #will need to change the methodDeclarationstring later
       methodDeclarationStringToCompare="public void onCreate"
       repairType=GitHub
       termsOfInterest="None";;
    #works!
    5) gitBranch=setContentViewFindViewByIDOrdering
       checker=DetectInvalidSetContentViewFindViewByIDOrdering
       appName=app
       methodOfInterest1=setContentView
       methodOfInterest2=findViewById
       repairType=Method;;
    #not working; need to figure out how to add the missing functionality
    6) gitBranch=getResourcesIssue
       checker=DetectInvalidGetResources
       appName=Application
       methodOfInterest1=getResources
       repairType=GitHub
       termsOfInterest="None";;
    #working!
    7) gitBranch=setInitialSavedState
       checker=DetectIncorrectSetInitialSavedState
       appName=Application
       methodOfInterest1=setInitialSavedState
       additionalInfo=REQUIRES_ADDING_OBJ_REF
       repairType=Method;;
    #setThemeIssue repair currently only handles one case of the problem; when 
    #the setTheme is incorrectly called in onCreate. It doesn't handle the case
    #when setTheme is incorrectly called in another method of the lifecycle.
    8) gitBranch=setThemeIssue
       checker=DetectInvalidSetTheme
       appName=Application
       methodOfInterest1=setTheme
       methodOfInterest2=setContentView
       #This repair type should be multiple, so I'll need to adjust this later
       repairType=Method;;
    #works; but currently deletes the first out of the two methods that is found;
    #a better fix would be to remove the setPackage in all cases
    #removed the public part so I can also get the methods labeled as protected
    9) gitBranch=setPackageSetSelectorProblem
       checker=DetectSetSelectorSetPackageProblem
       appName=app
       methodOfInterest1=setPackage
       methodOfInterest2=setSelector
       scriptDir=/Users/zack/git/DirectiveTool/
       repairType=GitHub
       methodDeclarationStringToCompare="void onCreate"
       termsOfInterest="None";;
   # 10) gitBranch=setContentViewFindViewByIDOrdering
   #    checker=DetectInvalidSetContentViewFindViewByIdOrdering
   #    appName=Application;;

  esac
  testFolder=/Users/zack/git/DirectiveTool/testFolder
  appLocation=$testFolder/$appName/build/outputs/apk/debug/$appName-debug.apk
  echo $appLocation
  #1. Get an app with a problem
  #Currently, the app is located in ~/git/ViolationOfDirectives
  testDir=/Users/zack/git/DirectiveTool/testFolder
  originalAppDir=~/git/ViolationOfDirectives 
  runCheckerCommand=(/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java \"-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=55437:/Applications/IntelliJ IDEA CE.app/Contents/bin\" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/jars/scala-reflect-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.7.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-reflect/srcs/scala-reflect-2.12.7-sources.jar:/Users/zack/.ivy2/cache/org.scala-lang/scala-library/srcs/scala-library-2.12.7-sources.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/soot/target/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/axml-2.0.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-api-1.7.5.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/libraries/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.m2/repository/commons-io/commons-io/2.6/commons-io-2.6.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar)
  #echo $runCheckerCommand
  #exit 0
  cd $originalAppDir
  git checkout $gitBranch
  #added this stop in for testing - remove later
  echo "stopping after git checkout"
  read n
  rm -rf $testDir
  cp -r $originalAppDir $testDir

  #2. run the tool to detect the problem
  cd $testDir
  #This next line seems to not be needed
  #cd `basename $originalAppDir`
  #print errors to terminal but not normal build messages
  ./gradlew assembleDebug >/dev/null
  #These next two lines are just for testing
  #./gradlew assembleDebug
  #The application will be built to the file /Users/zack/git/DirectiveTool/testFolder/Application/build/outputs/apk/debug/Application-debug.apk
  #initialTestFile=$testDir/initialTest.txt
  outputFile=$testDir/testResults.txt
  echo "$checker $appLocation"
  runChecker ${runCheckerCommand[@]} "analysis.$checker" $appLocation $outputFile
  #currently matching the line 'total number of caught problems: #'
  #might need to change if other totals are printed
  #problemCount=$(awk '$1 ~ /^total number/ {print $NF}' $outputFile)
  problemCount=$(awk '/^total number/ {print $NF}' $outputFile)
  classWithProblem=$(awk '$1 ~ /^@@@@@/ {print $NF}' $outputFile)
  echo "initial problem count: |$problemCount|"
  #loop until the problem has been removed
  runCheckerString="${runCheckerCommand[@]}"
  if [ -z $problemCount ]
  then 
    echo "Error: problemCount was not found after running checker"
    exit 1
  fi
  if [ $problemCount -lt 1 ]
  then
    echo "Error: there is no initial problem to fix"
    exit 1
  fi
  #print "Error: arguments must be (checkerToRun) (originalSourceFolder) (apkLocation) (methodOfInterest1) (optional: methodOfInterest2)"
  echo "|$methodOfInterest2|"
  #appLocationForRepair=${appLocation/testFolder/temporaryTestOfChange}
  #echo $appLocationForRepair
  #echo $repairType
  #if [ "$repairType" == "Method" ]
  #then
  #  echo "strings are equal"
  #else
  #  echo "strings are not equal"
  #fi
  #if [ "$repairType" == "Method" ]
  #then
  if [ -z ${methodOfInterest2+x} ]
  then    
    if [ -z ${additionalInfo+x} ]
    then
      echo "/Users/zack/git/DirectiveTool/changeMethodOrderRepair.py \"$runCheckerString\" $checker $testDir $appLocation $methodOfInterest1"
      /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocation $methodOfInterest1
      checkerResult=$?
    else
      echo "/Users/zack/git/DirectiveTool/changeMethodOrderRepair.py \"$runCheckerString\" $checker $testDir $appLocation $methodOfInterest1 $additionalInfo"
      /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocation $methodOfInterest1 $additionalInfo
      checkerResult=$?
    fi
    skippedTwoMethod=false
  else
    skippedTwoMethod=true 
  fi
  if [ $skippedTwoMethod = true ] || [ $checkerResult -ne 0 ] 
  then
    echo "/Users/zack/git/DirectiveTool/changeMethodOrderRepair.py \"$runCheckerString\" $checker $testDir $appLocation $methodOfInterest1 $methodOfInterest2"
    /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocation $methodOfInterest1 $methodOfInterest2
    checkerResult=$?

    #echo "stopping after change method order"
    #read stoppingHere
  #else
    if [ $checkerResult -ne 0 ]
    then 
      if [ -z $classWithProblem ]
      then 
        echo "Error: classWithProblem was not found after running checker"
        exit 1
      fi
      #echo "class with problem $classWithProblem"
      fileToChange=$(awk -F"." '{print $NF}' <<< "$classWithProblem")
      #classNameItems=(${classWithProblem//./ }) 
      #echo "class name items: $classNameItems"
      fileToChange=$fileToChange.java
      #echo "file to change $fileToChange"
      #echo "^$runCheckerString"
      #echo /Users/zack/git/DirectiveTool/repairMethodFromExampleOnGitHub.py "$runCheckerString" $checker $scriptDir "$methodDeclarationStringToCompare" $temporaryTestDir $fileToChange "$termsOfInterest"
      #exit 0
      echo "file to change before github repair: $fileToChange"
      /Users/zack/git/DirectiveTool/repairMethodFromExampleOnGitHub.py "$runCheckerString" $checker $scriptDir "$methodDeclarationStringToCompare" $testDir $fileToChange $appLocation "$termsOfInterest"
    fi
  #fi
  fi
showDiff $testFolder $testDir

  #while [ $problemCount -ne 0 ]
  #do
  #  echo "in loop"
  #  sleep 2
  #done
#done



