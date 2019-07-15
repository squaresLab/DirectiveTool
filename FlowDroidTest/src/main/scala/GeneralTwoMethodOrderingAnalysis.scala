import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.ForwardFlowAnalysis

//TODO: made a change and need to test this again
class GeneralTwoMethodOrderingAnalysis(graph: UnitGraph, method1Name: String, method2Name: String) extends ForwardFlowAnalysis[soot.Unit, AnalyzeMethodOrdering.AnalysisInfo](graph) {
  var numberOfCaughtProblems = 0
  doAnalysis()
  //println("setting number of caught problems to 0")
  /**
    * Given the merge of the <code>out</code> sets, compute the <code>in</code> set for <code>s</code> (or in to out,
    * depending on direction).
    *
    * This function often causes confusion, because the same interface is used for both forward and backward flow analyses.
    * The first parameter is always the argument to the flow function (i.e. it is the "in" set in a forward analysis and the
    * "out" set in a backward analysis), and the third parameter is always the result of the flow function (i.e. it is the
    * "out" set in a forward analysis and the "in" set in a backward analysis).
    *
    * @param in
    * the input flow
    * @param d
    * the current node
    * @param out
    * the returned flow
    **/
  override protected def flowThrough(in: AnalyzeMethodOrdering.AnalysisInfo, d: soot.Unit, out: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if(possibleM.isDefined){
      copy(in,out)
      val methodName = possibleM.get.getName
      println(s"${methodName}")
      if (methodName.contains(s"$method1Name")) {
        println(s"found $method1Name")
        out.di.hasMethod1 = true
      } else if (methodName.contains(s"method2Name")) {
        out.di.hasMethod2 = true
        println(s"found $method2Name")
        checkForViolation(out)
      }
    } else {
      copy(in,out)
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): AnalyzeMethodOrdering.AnalysisInfo = {
    return new AnalyzeMethodOrdering.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: AnalyzeMethodOrdering.AnalysisInfo, in2: AnalyzeMethodOrdering.AnalysisInfo, out: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
  }

  /** Creates a copy of the <code>source</code> flow object in <code>dest</code>. */
  override protected def copy(source: AnalyzeMethodOrdering.AnalysisInfo, dest: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
    dest.di.hasMethod2 = source.di.hasMethod2
    dest.di.hasMethod1 = source.di.hasMethod1
  }

  def checkForViolation(a: AnalyzeMethodOrdering.AnalysisInfo): Boolean = {
    if (a.di.hasMethod2 && !a.di.hasMethod1){
      numberOfCaughtProblems += 1
      return true
    }
    else {
      return false
    }
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}


object AnalyzeMethodOrdering{

  class DirectiveInfo (var hasMethod1: Boolean = false, var hasMethod2: Boolean = false){

  }
  class AnalysisInfo(){
    //has the path already called hasSetContentView or hasFindViewByIdOrdering
    val di: DirectiveInfo = new DirectiveInfo()

    def meet(other: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
      return new DirectiveInfo(di.hasMethod1 && other.di.hasMethod1, di.hasMethod2 && other.di.hasMethod2)
    }
  }
}