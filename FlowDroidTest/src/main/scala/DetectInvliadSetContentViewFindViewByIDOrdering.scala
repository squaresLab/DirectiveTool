import java.io.IOException

import org.xmlpull.v1.XmlPullParserException
import soot.jimple.Stmt
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.infoflow.solver.cfg.InfoflowCFG
import soot.jimple.toolkits.ide.icfg.OnTheFlyJimpleBasedICFG
import soot.options.Options
import soot.toolkits.graph.ExceptionalUnitGraph

import scala.collection.JavaConverters._

object DetectInvalidSetContentViewFindViewByIDOrdering {
  @throws[IOException]
  @throws[XmlPullParserException]
  def main(args: Array[String]): Unit = { // Initialize Soot
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    val apkLocation = DetectionUtils.getAPKLocation(args)
    println(s"the apk location: ${apkLocation}")
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
    analyzer.constructCallgraph()
    val cfg = new InfoflowCFG(new OnTheFlyJimpleBasedICFG(Scene.v().getEntryPoints()));
    var problemCount = 0
    for (edge <- Scene.v().getCallGraph.iterator().asScala){
      println(s"source: + ${edge.getSrc.method().getDeclaringClass.getName} ${edge.getSrc.method.getName}")
      for (uBox <- edge.getSrc.method().retrieveActiveBody().getAllUnitBoxes.asScala){
        uBox.getUnit() match {
          case stmt: Stmt =>
            println(stmt.toString())
          case x =>
            println(x.toString())
        }
      }
      println(s"target: + ${edge.getSrc.method().getDeclaringClass.getName} ${edge.getTgt.method.getName}")
      println("")
    }

    /*println("printing cfg")
     for( entry <- Scene.v().getReachableMethods.listener().asScala){
       entry match {
         case m: SootMethod =>
           if (DetectionUtils.isCustomClassName(m.getDeclaringClass.toString)) {
             println(s"calls for ${m}")
             for (call <- cfg.getCallsFromWithin(m).asScala) {
               println(call)
             }
             println("")
           }
         case _ =>
           ()
       }
     }
     */
    println("running analysis")

    for(cl:SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      if (cl.getName == "com.example.android.lnotifications.LNotificationActivity") {
        var c: SootClass = cl;

        println(c.getName)
        while (c.hasSuperclass) {
          c = c.getSuperclass
          println(c.getName)
        }
      }
      //println(s"class: ${cl.getName}")
      //may not need both of these variables; delete any unneeded
      //ones late if so
      var hasSetContentView = false
      var hasSetThemeInMethodOtherThanOnCreate = false
      var methodSetThemeIsCalledIn = ""
      if(DetectionUtils.classIsSubClassOfActivity(cl)){
        //don't think I need the check below since I added the check above but I'll leave it
        //here in case I am wrong
      //if(DetectionUtils.isCustomClassName(cl.getName())) {
        for (m: SootMethod <- cl.getMethods().asScala) {
          if(m.hasActiveBody && m.isConcrete) {
            if(m.getName.equals("onCreate")) {
              println(s"running analysis class: ${cl.getName()} method: ${m.getName()}")
              val s = new AnalyzeSetContentViewFindViewByIDOrdering(new ExceptionalUnitGraph(m.getActiveBody))
              println(s"caught problems: ${s.getCaughtProblems()}")
              problemCount += s.getCaughtProblems()

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
