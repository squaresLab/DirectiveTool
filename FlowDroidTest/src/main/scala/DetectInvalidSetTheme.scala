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
import scala.collection.JavaConverters._

object DetectInvalidSetTheme {
  @throws[IOException]
  @throws[XmlPullParserException]
  def main(args: Array[String]): Unit = { // Initialize Soot
  System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
  val apkLocation = DetectionUtils.getAPKLocation(args)
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
    println("printing bodies")

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
      if (DetectionUtils.classIsSubClassOfActivity((cl))) {
        //may not need both of these variables; delete any unneeded
        //ones late if so
        var hasSetContentView = false
        var hasSetThemeInMethodOtherThanOnCreate = false
        var methodSetThemeIsCalledIn = ""
        for (m: SootMethod <- cl.getMethods().asScala) {
          //may not need both of these variables; delete any unneeded
          //ones late if so
          var hasSetThemeInOnCreate = false
          var hasSetContentViewInOnCreate = false
          //println(s"method: ${m.getName}")
          if (cl.getName == "com.example.android.lnotifications.OtherMetadataFragment" && m.getName == "onCreateView") {
            println("here")
            println(s"is concrete: ${m.isConcrete}")
            println(s"has active body: ${m.hasActiveBody}")
          }
          if (m.isConcrete && m.hasActiveBody) {
            if (m.getName == "onCreate") {
              println("found onCreate")
              println(s"class: ${m.getDeclaringClass.getName} method: ${m.getName}")
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                println(stmt)
                val methodInStatementOption = DetectionUtils.extractMethodCallInStatement(stmt)
                methodInStatementOption match {
                  case Some(methodInStatement) =>
                    // 0 is how soot stores the final false parameter
                      if (methodInStatement.getName == "setTheme" ){
                        println("found set theme")
                        hasSetThemeInOnCreate = true
                        if (hasSetContentView){
                          println("@@@@@ Found a problem: set theme is called after setContentView in " + m.getDeclaringClass.getName)
                          System.out.flush()
                          System.err.println("@@@@@ Found a problem:  set theme is called after setContentView in" + m.getDeclaringClass.getName)
                          System.err.flush();
                          problemCount = problemCount + 1
                        }
                      }
                      else if (methodInStatement.getName == "setContentView") {
                        println("found set content view")
                        hasSetContentView = true
                        hasSetContentViewInOnCreate = true
                        if (hasSetThemeInMethodOtherThanOnCreate) {
                          println("@@@@@ Found a problem: set theme is called after setContentView in " + methodSetThemeIsCalledIn)
                          System.out.flush()
                          System.err.println("@@@@@ Found a problem:set theme is called after setContentView in" + methodSetThemeIsCalledIn)
                          System.err.flush();
                          problemCount = problemCount + 1
                        }
                      }
                      /*else{
                        println(s"method was not found: ${methodInStatement.getName}")
                      }*/
                  case None =>
                    ()
                  //  print(s"error for line: ${stmt.toString()}")
                }
              }
              println("")
            }
            else {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                val methodInStatementOption = DetectionUtils.extractMethodCallInStatement(stmt)
                methodInStatementOption match {
                  case Some(methodInStatement) =>
                    // 0 is how soot stores the final false parameter
                    if (methodInStatement.getName == "setTheme") {
                      println("found set theme")
                      hasSetThemeInMethodOtherThanOnCreate = true
                      methodSetThemeIsCalledIn = m.getName()
                      if (hasSetContentView) {
                        println("@@@@@ Found a problem: set theme is called after setContentView in " + methodSetThemeIsCalledIn)
                        System.out.flush()
                        System.err.println("@@@@@ Found a problem: set theme is called after setContentView in " + methodSetThemeIsCalledIn)
                        System.err.flush();
                        problemCount = problemCount + 1
                      }
                    }
                  case None =>
                    ()
                }
              }
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
