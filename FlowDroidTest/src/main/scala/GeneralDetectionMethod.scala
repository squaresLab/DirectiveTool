import org.xmlpull.v1.XmlPullParserException
import java.io.IOException
import java.util

import soot.jimple.Stmt
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.infoflow.solver.cfg.InfoflowCFG
import soot.jimple.toolkits.ide.icfg.OnTheFlyJimpleBasedICFG
import soot.options.Options

import scala.collection.JavaConverters._



//I left this in an unfinished state. I'll come back to it later if I decide
//I need it.
object GeneralDetectionMethod {
  @throws[IOException]
  @throws[XmlPullParserException]
  def detectionTemplate(args: Array[String]): Unit = { // Initialize Soot
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    val analyzer = new SetupApplication(
      "/Users/zack/Library/Android/sdk/platforms/android-21/android.jar",
      "/Users/zack/git/ViolationOfDirectives/Application/build/outputs/apk/debug/Application-debug.apk")
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
    analyzer.constructCallgraph()
    val cfg = new InfoflowCFG(new OnTheFlyJimpleBasedICFG(Scene.v().getEntryPoints()));
    var problemCount = 0
    for(cl:SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      if (DetectionUtils.classIsSubClassOfFragment((cl))) {
        for (m: SootMethod <- cl.getMethods().asScala) {
          if (m.isConcrete && m.hasActiveBody) {
            if (m.getName.contains("onCreateView")) {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                if (stmt.toString().contains("android.view.LayoutInflater: android.view.View inflate(")) {
                  // 0 is how soot stores the final false parameter
                  if (!stmt.toString().endsWith("0)")) {
                    println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName)
                    System.out.flush()
                    System.err.println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName)
                    System.err.flush();
                    problemCount = problemCount + 1
                  }
                }
              }
              println("")
            }
          }
        }
      }
    }
    println(s"total number of caught problems: ${problemCount}")

    //println(s"main method of scene: ${Scene.v().getMainMethod}")

    // Iterate over the callgraph
    /* println("printing callgraph")
     val callGraph = Scene.v.getCallGraph
     //val callGraph = cfg.
     println(s"size of call graph: ${callGraph.size()}")
     for (edge <- Scene.v.getCallGraph.iterator.asScala) {
       val smSrc = edge.src
       val uSrc = edge.srcStmt
       val smDest = edge.tgt
       println(s"Edge from ${uSrc} in ${smSrc} to ${smDest}")
     }
     */
    /*val lifecycleMethods = AndroidEntryPointConstants.getActivityLifecycleMethods
    for( l <- lifecycleMethods){
      cfg.
    }*/
  }


}


