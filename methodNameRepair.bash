#!/bin/bash

#1. Get an app with a problem
#Currently, the app is located in ~/git/ViolationOfDirectives
testDir=/Users/zack/git/DirectiveTool/testFolder=
originalAppDir=~/git/ViolationOfDirectives 
cp -r $originalAppDir $testDir

#2. run the tool to detect the problem
cd $testDir
cd `basename $originalAppDir`
./gradlew applicationDebug