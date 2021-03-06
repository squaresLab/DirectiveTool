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
#.   or you can reuse the old results
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
fullCommand="${checkerCommand[@]::${#checkerCommand[@]}-1}> $saveFile 2>/dev/null"
#tempErrorFile=${saveFile/testResults/testErrors}
#fullCommand="${checkerCommand[@]::${#checkerCommand[@]}-1}> $saveFile 2> $tempErrorFile"
#echo $fullCommand
eval $fullCommand
#exit 0
cd $previousDir
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
       termsOfInterest="None";;
    #works! But I need to add a heuristic later to make the repair more sensical;
    #partially done, currently moving the method to a method in the class 
    #with the problem; but could add lifecycle guided information to the repair
    2) gitBranch=FAULT_013_SO_6215239
       checker=DetectIncorrectGetActivityMain
       appName=Application
       methodOfInterest1=getActivity
       repairType=Method;;
    #works for missing setHasOptionsMenu(true); haven't successfully repaired
    #missing onCreateOptionsMenu
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
  runCheckerCommand=(/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/bin/java \"-javaagent:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar=58721:/Applications/IntelliJ IDEA CE.app/Contents/bin\" -Dfile.encoding=UTF-8 -classpath /Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/dt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/javafx-mx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/jconsole.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/packager.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/sa-jdi.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_211.jdk/Contents/Home/lib/tools.jar:/Users/zack/git/DirectiveTool/FlowDroidTest/target/scala-2.12/classes:/Users/zack/.sbt/boot/scala-2.12.7/lib/scala-library.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/git/FlowDroid/soot-infoflow-android/lib/protobuf-java-2.5.0.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/cos.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/j2ee.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/junit.jar:/Users/zack/git/FlowDroid/soot-infoflow/lib/org.hamcrest.core_1.3.0.jar:/Users/zack/.ivy2/cache/commons-io/commons-io/jars/commons-io-2.6.jar:/Users/zack/.ivy2/cache/com.google.guava/guava/bundles/guava-18.0.jar:/Users/zack/.ivy2/cache/com.beust/jcommander/jars/jcommander-1.64.jar:/Users/zack/.ivy2/cache/com.google.code.findbugs/jsr305/jars/jsr305-1.3.9.jar:/Users/zack/.ivy2/cache/org.smali/dexlib2/jars/dexlib2-2.2.5.jar:/Users/zack/.ivy2/cache/org.smali/util/jars/util-2.2.2.jar:/Users/zack/.ivy2/cache/xmlpull/xmlpull/jars/xmlpull-1.1.3.4d_b4_min.jar:/Users/zack/.ivy2/cache/xerces/xmlParserAPIs/jars/xmlParserAPIs-2.6.2.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-simple/jars/slf4j-simple-1.7.5.jar:/Users/zack/.ivy2/cache/org.slf4j/slf4j-api/jars/slf4j-api-1.7.5.jar:/Users/zack/.ivy2/cache/org.ow2.asm/asm-debug-all/jars/asm-debug-all-5.2.jar:/Users/zack/.ivy2/cache/net.sf.trove4j/trove4j/jars/trove4j-3.0.3.jar:/Users/zack/git/soot/target/classes:/Users/zack/git/heros/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow/target/scala-2.12/classes:/Users/zack/git/soot/src/main/target/scala-2.12/classes:/Users/zack/git/FlowDroid/soot-infoflow-android/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/axml:/Users/zack/git/FlowDroid/soot-infoflow-summaries/target/scala-2.12/classes:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/ca.mcgill.sable.soot:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/test:/Users/zack/git/DirectiveTool/FlowDroidTest/out/production/arrayclone:/Users/zack/git/FlowDroid/soot-infoflow-cmd/build/classes)
  #echo $runCheckerCommand
  #exit 0
  cd $originalAppDir
  git checkout $gitBranch
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
  runChecker ${runCheckerCommand[@]} $checker $appLocation $outputFile
  #currently matching the line 'total number of caught problems: #'
  #might need to change if other totals are printed
  problemCount=$(awk '$1 ~ /^total/ {print $NF}' $outputFile)
  classWithProblem=$(awk '$1 ~ /^@@@@@/ {print $NF}' $outputFile)
  echo "initial problem count: $problemCount"
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
  appLocationForRepair=${appLocation/testFolder/temporaryTestOfChange}
  #echo $appLocationForRepair
  #echo $repairType
  if [ "$repairType" == "Method" ]
  then
    echo "strings are equal"
  else
    echo "strings are not equal"
  fi
  if [ "$repairType" == "Method" ]
  then
    if [ -z ${methodOfInterest2+x} ]
    then    
      if [ -z ${additionalInfo+x} ]
      then
        /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocationForRepair $methodOfInterest1
      else
        /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocationForRepair $methodOfInterest1 $additionalInfo
      fi
    else
      /Users/zack/git/DirectiveTool/changeMethodOrderRepair.py "$runCheckerString" $checker $testDir $appLocationForRepair $methodOfInterest1 $methodOfInterest2
    fi 
  else
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
    temporaryTestDir=${testDir/testFolder/temporaryTestOfChange}
    cp -r $testDir $temporaryTestDir
    #echo "^$runCheckerString"
    #echo /Users/zack/git/DirectiveTool/repairMethodFromExampleOnGitHub.py "$runCheckerString" $checker $scriptDir "$methodDeclarationStringToCompare" $temporaryTestDir $fileToChange "$termsOfInterest"
    #exit 0
    /Users/zack/git/DirectiveTool/repairMethodFromExampleOnGitHub.py "$runCheckerString" $checker $scriptDir "$methodDeclarationStringToCompare" $temporaryTestDir $fileToChange $appLocationForRepair "$termsOfInterest"
  fi
  if [ $? -eq 0 ] 
  then
    temporaryTestFolder=${testFolder/testFolder/temporaryTestOfChange}
    cp -r $testDir $temporaryTestFolder
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
  fi

  #while [ $problemCount -ne 0 ]
  #do
  #  echo "in loop"
  #  sleep 2
  #done
#done



