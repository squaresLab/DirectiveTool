package analysis

import org.xmlpull.v1.XmlPullParserException
import java.io.{File, IOException}
import java.util
import java.util.concurrent.TimeUnit

import DetectIncorrectGetActivityMain.{addControlFlowChain, extractMethodCallInStatement}
import soot.jimple.Stmt
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.infoflow.solver.cfg.InfoflowCFG
import soot.jimple.toolkits.ide.icfg.OnTheFlyJimpleBasedICFG
import soot.options.Options

import scala.util.control.Breaks._
import scala.collection.JavaConverters._
import scala.collection.mutable.ListBuffer
import scala.io.{Source, StdIn}

class CountObject (var apkName: String, var inflateDirectiveApplies: Boolean = false,
                  //No Dialog check is not included in the one directive applies check
                   var inflateDirectiveNoDialogCheck: Boolean = false,
                   var getActivityDirectiveApplies: Boolean = false, var setInitialSavedStateDirectiveApplies: Boolean = false,
                   var getResourcesDirectiveApplies: Boolean = false, var setThemeSetContentViewDirectiveApplies: Boolean = false,
                   var setContentViewFindViewByIdDirectiveApplies: Boolean = false,
                   var setOptionsMenuDirectiveApplies: Boolean = false, var setArgumentsDirectiveApplies: Boolean = false,
                   var setSelectorSetPackageDirectiveApplies: Boolean = false){

  def doesOneDirectiveApply(): Boolean = {
    return inflateDirectiveApplies || getActivityDirectiveApplies || setInitialSavedStateDirectiveApplies ||
      getResourcesDirectiveApplies || setThemeSetContentViewDirectiveApplies ||
      setContentViewFindViewByIdDirectiveApplies || setOptionsMenuDirectiveApplies ||
      setArgumentsDirectiveApplies || setSelectorSetPackageDirectiveApplies
  }
}

//may eventually need to implement a way to determine how to skip APKs already counted
//but leaving that for later if I need it

//TODO: implement a way to check if the app has any of the directives in it, instead of specific ones


object CountCasesWhereDirectivesApply {
  @throws[IOException]
  @throws[XmlPullParserException]
  def main(args: Array[String]): Unit = { // Initialize Soot
    /*if (args.length != 1) {
      println("Please provide the directory of APK files")
    }
    val dirnameOfApps = args(0)
     */
    //val dirnameOfApps = "/Users/zack/Desktop/apkCollectionDir"
    //val dirnameOfApps = "/Users/zack/Desktop/countTestApps"
    //val dirnameOfApps = "/Users/zack/Desktop/singleTestCountApps"
    val dirnameOfApps = "/Users/zack/git/DirectiveTool/appsFromFDroid"
    val apkList = getListOfFiles(new File(dirnameOfApps), List("apk"))
    //val apkList = getErrorFileList()
    print(s"found ${apkList.size} apks to test")
    TimeUnit.SECONDS.sleep(1)
    var skipCount = 0
    var errorList: List[String] = List()
    var countObjList: ListBuffer[CountObject] = new ListBuffer[CountObject]
    for (apk <- apkList) {
      try {
        countObjList += runAppOnApk(args, apk.getAbsolutePath)
        //countObj.totalAppCount = countObj.totalAppCount + 1
      }
      catch {
        case x: Throwable =>
          //println(x)
          //x.printStackTrace()
          //StdIn.readLine("Press enter to continue")
          errorList = apk.getAbsoluteFile.toString()::errorList
          skipCount = skipCount + 1
      }
    }
    println(s"final skip count: ${skipCount}")
    for(skippedAPK <- errorList){
      println(skippedAPK)
    }
    val finalCountList = countObjList.toList
    println(s"final skip count: ${skipCount}")
    println(s"total app count: ${finalCountList.size}")
    println(s"app count where the inflate check applies: ${countObjList.filter(_.inflateDirectiveApplies).size}")
    println(s"app count where the inflate check no dialog check applies: ${countObjList.filter(_.inflateDirectiveNoDialogCheck).size}")
    println(s"app count where the getActivity check applies: ${countObjList.filter(_.getActivityDirectiveApplies).size}")
    println(s"app count where setInitialSavedState check applies: ${countObjList.filter(_.setInitialSavedStateDirectiveApplies).size}")
    println(s"app count where getResources check applies: ${countObjList.filter(_.getResourcesDirectiveApplies).size}")
    println(s"app count where setThemeSetContentView check applies: ${countObjList.filter(_.setThemeSetContentViewDirectiveApplies).size}")
    println(s"app count where setContentViewFindViewById check applies: ${countObjList.filter(_.setContentViewFindViewByIdDirectiveApplies).size}")
    println(s"app count where setOptionsMenu check applies: ${countObjList.filter(_.setOptionsMenuDirectiveApplies).size}")
    println(s"app count where setArguments check applies: ${countObjList.filter(_.setArgumentsDirectiveApplies).size}")
    println(s"app count where setSelectorSetPackage check applies: ${countObjList.filter(_.setSelectorSetPackageDirectiveApplies).size}")
    println(s"app count where at least one check applies: ${countObjList.filter(_.doesOneDirectiveApply()).size}")
  }

  def getListOfFiles(dir: File, extensions: List[String]): List[File] = {
    //test this
    dir.listFiles.filter(_.isFile).toList.filter { file =>
      extensions.exists(file.getName.endsWith(_))
    }
  }

  def getErrorFileList(): List[File] = {
    //test this
    val fileWithErrorList = "/Users/zack/git/DirectiveTool/skippedApps.txt"
    def lineToFile(line: String): File = {
      return new File(line)
    }
    return Source.fromFile(fileWithErrorList).getLines.map(line => lineToFile(line)).toList
  }

  def runAppOnApk(args: Array[String], apkFileLocation:String): CountObject = {
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    //val apkLocation = DetectionUtils.getAPKLocation(args)
    val apkLocation = apkFileLocation
    println(s"${apkLocation}")
    val analyzer = new SetupApplication(
      "/Users/zack/Library/Android/sdk/platforms/android-21/android.jar",
      apkLocation)
    //  "/Users/zack/git/ViolationOfDirectives/Application/build/intermediates/instant-run-apk/debug/Application-debug.apk")
    //There seems to be an analysis blocker at Infoflow.java on line 293 that stops building the callgraph
    //if this is not set
    analyzer.getConfig.setTaintAnalysisEnabled(true)
    analyzer.getConfig.setMergeDexFiles(true)
    analyzer.getConfig.setCodeEliminationMode(InfoflowConfiguration.CodeEliminationMode.NoCodeElimination)
    analyzer.getConfig.getAnalysisFileConfig.setSourceSinkFile("/Users/zack/Documents/intelliJWorkspace/FlowDroidTest/SourcesAndSinks.txt")
    Scene.v().releaseCallGraph()
    //Options.v().set_process_multiple_dex(true)
    Options.v().set_process_multiple_dex(false)
    PhaseOptions.v().setPhaseOption("cg", "verbose")
    println(PhaseOptions.v().getPhaseOptions("cg"))
    analyzer.getConfig.setImplicitFlowMode(ImplicitFlowMode.AllImplicitFlows)
    analyzer.getConfig().setCallgraphAlgorithm(CallgraphAlgorithm.VTA)
    analyzer.getConfig.getCallbackConfig.setCallbackAnalyzer(CallbackAnalyzer.Fast)
    analyzer.constructCallgraph()
    val countObj = new CountObject(apkFileLocation)

    for(cl:SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      if (DetectionUtils.classIsSubClassOfFragment(cl)){
        //&& !DetectionUtils.classIsSubClassOfDialogFragment(cl)

        //check for options menu
        for (m: SootMethod <- cl.getMethods().asScala) {
          if (m.getName().equals("onCreateOptionsMenu")){
            countObj.setOptionsMenuDirectiveApplies = true
          }
          else if (m.getName().equals("onPrepareOptionsMenu")){
            countObj.setOptionsMenuDirectiveApplies = true
          }
          if (m.getName().equals("onCreate")){
            if (m.hasActiveBody) {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if (stmt.toString().contains("setHasOptionsMenu(true)")) {
                  countObj.setOptionsMenuDirectiveApplies = true
                  //break
                }
              }
            }
          }
          var isDialogFragment = DetectionUtils.classIsSubClassOfDialogFragment(cl)
          if (m.isConcrete && m.hasActiveBody) {
            //check for inflate directive
            if (m.getName.contains("onCreateView")) {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if (stmt.toString().contains("android.view.LayoutInflater: android.view.View inflate(")){
                  if (!isDialogFragment) {
                    countObj.inflateDirectiveApplies = true
                  }
                  countObj.inflateDirectiveNoDialogCheck = true
                }
              }
            }
            //check for getActivity directive and setInitialSavedState
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              if (stmt.toString().contains("getActivity")) {
                countObj.getActivityDirectiveApplies = true
              }

            }
          }
        }
      }
      //count getResources case
      else if (cl.getOuterClassUnsafe() != null && DetectionUtils.classIsSubClassOfFragment(cl.getOuterClass())){
        if (DetectionUtils.classIsSubClassOfAsyncTask(cl)) {
          for (m: SootMethod <- cl.getMethods().asScala) {
            if (m.isConcrete && m.hasActiveBody) {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if (stmt.toString().contains("getResources")) {
                  countObj.getResourcesDirectiveApplies = true
                }
              }
            }
          }
        }
      }
      //count setTheme
      else if(DetectionUtils.classIsSubClassOfActivity(cl)){
        var setThemeFound = false
        var setContentViewFound = false
        for (m: SootMethod <- cl.getMethods().asScala) {
          if (m.isConcrete && m.hasActiveBody) {
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              if (stmt.toString().contains("setTheme")) {
                setThemeFound = true
              }
              if (stmt.toString().contains("setContentView")) {
                setContentViewFound = true
              }
            }
            if (setContentViewFound && setThemeFound) {
              countObj.setThemeSetContentViewDirectiveApplies = true
              //test if this works correctly - it does not; not sure why but it just adds some runtime
              //so it probably isn't important to figure out
              //break
            }
            if (m.getName().equals("onCreate")) {
              var hasSetContentView = false
              var hasFindViewById = false
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if (stmt.toString().contains("setContentView(")) {
                  hasSetContentView = true
                }
                if (stmt.toString().contains("findViewById(")) {
                  hasFindViewById = true
                }
              }
              if (hasSetContentView && hasFindViewById) {
                countObj.setContentViewFindViewByIdDirectiveApplies = true
              }
            }
          }
        }
      }

      //var foundSetSelectorOrSetPackage = false
      for (m: SootMethod <- cl.getMethods().asScala) {
        //if(m.hasActiveBody)
        //  println(s"method: ${m.getName()}, is concrete: ${m.isConcrete()}, has active body: ${m.hasActiveBody}")
        if (m.isConcrete && m.hasActiveBody) {
          for (stmt <- m.getActiveBody.getUnits.asScala) {
            //println(stmt.toString())
            if (stmt.toString().contains("setArguments")) {
              countObj.setArgumentsDirectiveApplies = true
            }
            if (stmt.toString().contains("setInitialSavedState")) {
              countObj.setInitialSavedStateDirectiveApplies = true
            }
            if (stmt.toString().contains("setPackage(")) {
              countObj.setSelectorSetPackageDirectiveApplies = true
              //foundSetSelectorOrSetPackage = true
              //break
            } else if (stmt.toString().contains("setSelector(")){
              countObj.setSelectorSetPackageDirectiveApplies = true
              //foundSetSelectorOrSetPackage = true
              //break
            }
          }
        }
        //if(foundSetSelectorOrSetPackage){
          //break
        //}
      }
    }
    return countObj
  }
}


