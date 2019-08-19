import soot.jimple.infoflow.InfoflowConfiguration
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.options.Options
import scala.collection.JavaConverters._

//This detects the sample error but I'm not sure that it would work on the correct case - I'm not sure
//I have the correct way to know if unregister is called on the same global variable as register
object DetectUnregistrationProblem {

  def main(args: Array[String]): Unit = {

    println(s"number of command line arguments: ${args.length}")
    println(args)
    val apkLocation = DetectionUtils.getAPKLocation(args)
    println(s"apk location variable: ${apkLocation}")
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    val analyzer = new SetupApplication(
      "/Users/zack/Library/Android/sdk/platforms/android-21/android.jar",
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
    var receiverMap = scala.collection.mutable.Map[String, Boolean]()

    for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      var containsOnCreateOptionsMenu = false
      var containsHasSetOptionsMenu = false
      //println("in class loop")
      //no idea why I need this xmlpull check. These for loops through the classes and methods seem to
      //work on other checkers
      if (DetectionUtils.isCustomClassName(cl.getName) && !cl.getName.contains("xmlpull")
        && DetectionUtils.classIsSubClassOfActivity(cl) && !cl.isAbstract()) {
        receiverMap = scala.collection.mutable.Map[String, Boolean]()
        for (m: SootMethod <- cl.getMethods().asScala) {
          if(m.getName == "onResume") {
            println("found onResume")
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              //println(stmt.getClass.toString() + ": "  + stmt)
              //1 is true in FlowDroid
              val invokeCall = DetectionUtils.extractInvokeStmtInStmt(stmt)
              println(s"invoke call in onResume: ${invokeCall.getOrElse("None").toString()}")
              if (invokeCall.isDefined) {
                println(invokeCall.get.getMethod.getName())
              }
              if (invokeCall.isDefined && invokeCall.get.getMethod.getName == "registerReceiver") {
                println("found registerReceiver")
                receiverMap.+=(invokeCall.get.getArg(0).toString() -> true)
              }
            }
          }
          else if ( m.getName == "onPause") {
            println("found onPause")
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              //println(stmt.getClass.toString() + ": "  + stmt)
              //1 is true in FlowDroid
              val invokeCall = DetectionUtils.extractInvokeStmtInStmt(stmt)
              println(s"invoke call in onPause ${invokeCall.getOrElse("None").toString()}")
              if (invokeCall.isDefined) {
                println(invokeCall.get.getMethod.getName())
              }
              if (invokeCall.isDefined && invokeCall.get.getMethod.getName == "unregisterReceiver") {
                println("found unregisterReceiver")
                val unregisteredReceiver = invokeCall.get.getArg(0).toString()
                //actually I'm not checking the receiver was unregistered but not registered in the directive;
                //commenting this out so I can add it back in if I want to
                /*
                if( ! receiverMap.contains(unregisteredReceiver)){
                  val errorString = s"#### Found a problem: ${unregisteredReceiver} was not registered"
                  problemCount = notifyOfProblem(problemCount, cl.getName, errorString)
                }
                 */
                receiverMap + (unregisteredReceiver -> false)
              }
            }
          }
        }
        for ((k,v) <- receiverMap) {
          if (v) {
            val errorString = s"#### Found a problem: ${k} was never unregistered in onPause"
            problemCount = notifyOfProblem(problemCount, cl.getName, errorString)
          }
        }
      }
    }
    println(s"total number of caught problems: ${problemCount}")
  }

  def notifyOfProblem(problemCount: Int, className: String, errorString: String): Int = {
    println(errorString)
    System.out.flush()
    System.err.println(errorString)
    System.err.flush()
    return problemCount + 1
  }
}
