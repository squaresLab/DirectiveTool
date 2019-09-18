package analysis

import soot.ValueBox
import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.ForwardFlowAnalysis

import scala.collection.JavaConverters._
import scala.collection.mutable

//in original file, varTypeName was Intent method1 was setSelector and method2 was setPackage
class AnalyzeExclusiveCallsOnAVariableType(graph: UnitGraph, varTypeName: String, method1: String, method2: String) extends ForwardFlowAnalysis[soot.Unit, AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo](graph) {
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
  override protected def flowThrough(in: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo, d: soot.Unit, out: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo): Unit = {
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if(possibleM.isDefined){
      copy(in,out)
      //this could throw an error for Intents
      if(possibleM.get.getDeclaringClass.getName.contains(varTypeName)) {
        val methodName = possibleM.get.getName
        //we know we can cast d to a Stmt because extractMethodCallInStatement did not return false
        //d.asInstanceOf[soot.jimple.Stmt].
        //  (soot.jimple.Stmt)d
        //println(s"method to check ${methodName}")
        for (ub <- d.getUseBoxes.asScala) {
          ub match {
            case vb: ValueBox =>
              val valueName = vb.getValue.toString()
              //println("found value box")
              //the null) check excludes calls on null instances, but this check may not be
              //correct in the general case - will need to check later
              if (methodName.contains(method1) && !d.toString().endsWith("null)")) {
                //println(s"found setSelector with ${valueName}: ${d.toString()}")
                //println(s"${possibleM.get.}")
                val varInfoOption = out.getVar(valueName)
                if (varInfoOption.isDefined) {
                  varInfoOption.get.hasMethod1 = true
                  checkForViolation(varInfoOption.get)
                  //println(s"var option info: hasSetSelector: ${varInfoOption.get.hasSetSelector}, hasSetPackage ${varInfoOption.get.hasSetPackage}")
                }
                else {
                  out.addVar(valueName, true, false)
                }

              } else if (methodName.contains(method2) && !d.toString().endsWith("null)")) {
                //println(s"found setPackage with ${valueName}: ${d.toString()}")
                val varInfoOption = out.getVar(valueName)
                if (varInfoOption.isDefined) {
                  varInfoOption.get.hasMethod2 = true
                  checkForViolation(varInfoOption.get)
                }
                else {
                  out.addVar(valueName, false, true)
                }
              }
            case _ => ()
          }
        }
      }
    } else {
      copy(in,out)
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo = {
    return new AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo, in2: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo, out: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo): Unit = {
    out.clear()
    for (variable <- in1.varMap.keySet){
      if (in2.varMap.contains(variable)){
        out.addVar(variable, (in1.varMap(variable).hasMethod1.||(in2.varMap(variable).hasMethod1)),(in1.varMap(variable).hasMethod2.||(in2.varMap(variable).hasMethod2)))
        checkForViolation(out.getVar(variable).getOrElse(null))
      } else {
        out.addVar(variable, in1.varMap(variable).hasMethod1, in1.varMap(variable).hasMethod2)
      }
    }
    for(variable <- in2.varMap.keySet) {
      if (!out.varMap.contains(variable)) {
        out.addVar(variable, in2.varMap(variable).hasMethod1, in2.varMap(variable).hasMethod2)
      }
    }
  }

  /** Creates a copy of the <code>source</code> flow object in <code>dest</code>. */
  override protected def copy(source: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo, dest: AnalyzeExclusiveCallsOnAVariableType.AnalysisInfo): Unit = {
    dest.varMap = source.varMap
  }

  def checkForViolation(d: AnalyzeExclusiveCallsOnAVariableType.DirectiveInfo): Boolean = {
    if (d== null){
      return false
    }
    if(d.hasMethod1 && d.hasMethod2){
      Predef.println(s"error: code calls both ${method1} and ${method2} on the same ${varTypeName}")
      numberOfCaughtProblems += 1
      println(s"number of caught problems: ${numberOfCaughtProblems}")
      return true
    }
    return false
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}


object AnalyzeExclusiveCallsOnAVariableType {

  class DirectiveInfo(var hasMethod1: Boolean = false, var hasMethod2: Boolean = false){

  }
  class AnalysisInfo(var varMap: mutable.HashMap[String, DirectiveInfo] = new mutable.HashMap[String, DirectiveInfo]()){ //extends java.util.BitSet{

    def addVar(varName:String, hasMethod1: Boolean = false, hasMethod2:Boolean = false): Unit ={
      varMap.+=(varName -> new DirectiveInfo(hasMethod1,hasMethod2))
    }

    def getVar(varName: String): Option[DirectiveInfo] = {
      if (varMap.contains(varName)){
        return new Some(varMap(varName))
      } else {
        return None
      }
    }

    def clear(): Unit = {
      varMap = new mutable.HashMap[String,DirectiveInfo]()
    }


  }

}

