package analysis

import soot.jimple.infoflow.InfoflowConfiguration
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.options.Options
import scala.collection.JavaConverters._

object DetectMissingSetHasOptionsMenu {

  def main(args: Array[String]): Unit = {
    runAnalysis(args)
  }
  def runAnalysis(args: Array[String]): Unit = {
    val startTime = System.nanoTime()
    println(s"number of command line arguments: ${args.length}")
    println(args)
    val apkLocation = DetectionUtils.getAPKLocation(args)
    println(s"apk location variable: ${apkLocation}")
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    val analyzer = new SetupApplication(
      DetectionUtils.getAndroidJarLocation(args),
      apkLocation
      )
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
    //fast analyzer adds all possible callbacks, not just those that are reachable
    //unfortunately, the analyzer is saying that onClick methods which are reachable
    //are not, so currently using the fast analyzer
    analyzer.getConfig.getCallbackConfig.setCallbackAnalyzer(CallbackAnalyzer.Fast)
    analyzer.constructCallgraph()
    var containsOnCreateOptionsMenu = false
    var containsHasSetOptionsMenu = false
    var problemCount = 0

    for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      /*if(cl.toString().contains("ResultFragment")) {
        println(cl.toString())
        println(DetectionUtils.isCustomClassName(cl.getName))
        println(!cl.getName.contains("xmlpull"))
        println(DetectionUtils.classIsSubClassOfFragment(cl))
        println(cl.getMethodCount())
      }*/
      var containsOnCreateOptionsMenu = false
      var containsHasSetOptionsMenu = false
      //println("in class loop")
      //no idea why I need this xmlpull check. These for loops through the classes and methods seem to
      //work on other checkers
      if (DetectionUtils.isCustomClassName(cl.getName) && !cl.getName.contains("xmlpull")
        && DetectionUtils.classIsSubClassOfFragment(cl) && cl.getMethodCount > 0) {
        //trying to change the abstract check: !cl.isAbstract()) {
        /*println(cl.toString())
        println("here")
        println(cl.getMethods.size())
        println(cl.getMethods())*/
        for (m: SootMethod <- cl.getMethods().asScala) {
          if(cl.toString().contains("com.secuso.privacyfriendlycodescanner.qrscanner.resultfragments.ResultFragment")) {
            println(m.getName())
            println("printing method")
          }
          if(m.getName() == "onCreateOptionsMenu" || m.getName() == "onPrepareOptionsMenu") {
            containsOnCreateOptionsMenu = true
            //println("contains onCreateOptionsMenu")
          } else if (m.getName == "onCreate" || m.getName == "onCreateView" || m.getName == "onActivityCreated" ||
            m.getName == "onStart"){
            //println(m.hasActiveBody)
            //println(m.getSource())
            if(m.hasActiveBody) {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if(cl.toString().contains("com.secuso.privacyfriendlycodescanner.qrscanner.resultfragments.ResultFragment")) {
                  println(stmt.toString())
                }
                val invokeCall = DetectionUtils.extractInvokeStmtInStmt(stmt)
                //println(s"invoke call ${invokeCall.toString}")
                if (invokeCall.isDefined && invokeCall.get.getMethod.getName == "setHasOptionsMenu"
                  && DetectionUtils.isTrue(invokeCall.get.getArg(0))) {
                  containsHasSetOptionsMenu = true
                  //println("has setOptionsMenu")
                }
              }
            }
          }
        }
      }
      //Commenting out because I can't fix this case and throwing errors for both is messing up
      //the injection code
      /* if(containsHasSetOptionsMenu && !containsOnCreateOptionsMenu){
        val errorString = "@@@@ Found a problem: onCreateOptionMenu must " +
          s"be overridden in ${cl.getName} to display the OptionsMenu"
        problemCount = notifyOfProblem(problemCount, cl.getName, errorString)

      } else */
      if (containsOnCreateOptionsMenu && !containsHasSetOptionsMenu){

        val errorString = "@@@@ Found a problem: setHasOptionsMenu(true) must " +
          s"be called in the onCreate method of ${cl.getName} to display the " +
          "OptionsMenu"
        problemCount = notifyOfProblem(problemCount, cl.getName, errorString)

      }
    }
    println(s"total number of caught problems: ${problemCount}")
    val totalTime = System.nanoTime() - startTime
    println(s"total time (in nanoseconds): ${totalTime}")
    println(s"total time (in seconds): ${totalTime/1000000000}")

  }

  def notifyOfProblem(problemCount: Int, className: String, errorString: String): Int = {
    println("@@@@@ Found a problem:  the options menu is incorrectly configured in " + className)
    System.err.println("@@@@@ Found a problem:  the options menu is incorrectly configured in " + className)
    println()
    println(errorString)
    System.out.flush()
    System.err.println(errorString)
    System.err.flush()
    return problemCount + 1
  }
}
