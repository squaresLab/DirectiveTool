import soot.jimple.infoflow.InfoflowConfiguration
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.options.Options
import scala.collection.JavaConverters._

object DetectMissingSetHasOptionsMenu {

  def main(args: Array[String]): Unit = {
    def getAPKLocation(args: Array[String]): String = {
      //Scala doesn't seem to have the first argument default to the program name like Java
      if (args.length > 0){
        return args(0)
      } else {
        return "/Users/zack/git/ViolationOfDirectives/Application/build/outputs/apk/debug/Application-debug.apk"
      }
    }
    println(s"number of command line arguments: ${args.length}")
    println(args)
    val apkLocation = getAPKLocation(args)
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

    for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      var containsOnCreateOptionsMenu = false
      var containsHasSetOptionsMenu = false
      //println("in class loop")
      //no idea why I need this xmlpull check. These for loops through the classes and methods seem to
      //work on other checkers
      if (ExtractCFGMain.isCustomClassName(cl.getName) && !cl.getName.contains("xmlpull")
        && DetectionUtils.classIsSubClassOfFragment(cl)) {
        for (m: SootMethod <- cl.getMethods().asScala) {
          if(m.getName == "onCreateOptionsMenu") {
            containsOnCreateOptionsMenu = true
          } else if (m.getName == "onCreate" || m.getName == "onCreateView" || m.getName == "onActivityCreated" ||
            m.getName == "onStart"){
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              //println(stmt.getClass.toString() + ": "  + stmt)
              //1 is true in FlowDroid
              val invokeCall = DetectionUtils.extractInvokeStmtInStmt(stmt)
              if(invokeCall.isDefined && invokeCall.get.getMethod.getName == "setHasOptionsMenu"
                && DetectionUtils.isTrue(invokeCall.get.getArg(0))) {
                containsHasSetOptionsMenu = true
              }
            }
          }
        }
      }
      if(containsHasSetOptionsMenu && !containsOnCreateOptionsMenu){
        val errorString = "@@@@ Found a problem: onCreateOptionMenu must " +
          s"be overridden in ${cl.getName} to display the OptionsMenu"
        problemCount = notifyOfProblem(problemCount, errorString)

      } else if (containsOnCreateOptionsMenu && !containsHasSetOptionsMenu){
        val errorString = "@@@@ Found a problem: setHasOptionsMenu(true) must " +
          s"be called in the onCreate method of ${cl.getName} to display the " +
          "OptionsMenu"
        problemCount = notifyOfProblem(problemCount, errorString)

      }
    }
    println(s"total number of caught problems: ${problemCount}")
  }

  def notifyOfProblem(problemCount: Int, errorString: String): Int = {
    println(errorString)
    System.out.flush()
    System.err.println(errorString)
    System.err.flush()
    return problemCount + 1
  }
}
