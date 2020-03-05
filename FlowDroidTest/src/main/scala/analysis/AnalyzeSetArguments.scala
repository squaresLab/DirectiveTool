package analysis

import soot.ValueBox
import soot.jimple.internal.{JAssignStmt, JNewExpr}
import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.ForwardFlowAnalysis

import scala.collection.JavaConverters._
import scala.collection.mutable

//this class is not being used at the moment - I haven't finished implementing the logic

//TODO: check this analysis. I wasn't checking only intent variables earlier. Now I am but I haven't
//tested the change yet.
class AnalyzeSetArguments(graph: UnitGraph) extends ForwardFlowAnalysis[soot.Unit, AnalyzeSetArguments.AnalysisInfo](graph) {
  var numberOfCaughtProblems = 0
  //The analysis seems to get stuck on multiple case statements in a function, so ending the analysis early in that case
  val endTime = System.currentTimeMillis + 300 * 1000 // 60 seconds * 1000 ms/sec
  doAnalysis()
  //println("setting number of caught problems to 0")


  val initializationPattern = "=(| )new ([a-zA-Z_][a-zA-Z0-9_\\.]*)".r

  def getInstanceFromStatement(stmt: soot.Unit): Option[String] = {
    val initializationMatch = initializationPattern.findFirstMatchIn(stmt.toString())
    if (initializationMatch.isDefined) {
      if (stmt.isInstanceOf[JAssignStmt]) {
        val assignStmt = stmt.asInstanceOf[JAssignStmt]
        if (DetectionUtils.classIsSubClassOfFragment(assignStmt.rightBox.getValue.asInstanceOf[JNewExpr].getBaseType.getSootClass)) {
          val instanceToAdd = assignStmt.leftBox.getValue.toString()
          println(s"adding instance: ${assignStmt.leftBox.getValue.toString()}")
          return Some(instanceToAdd)
        }
      }
    }
    return None
  }

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
  override protected def flowThrough(in: AnalyzeSetArguments.AnalysisInfo, d: soot.Unit, out: AnalyzeSetArguments.AnalysisInfo): Unit = {
    if (System.currentTimeMillis() > endTime) {
      throw new RuntimeException("analysis timed out")
    }
    copy(in, out)
    //println("in flow through")
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if (possibleM.isDefined) {
      /*if(possibleM.get.toString().contains("setArguments")){
        out.
      }
       */
      val possibleDeclaration = getInstanceFromStatement(d)
      if (possibleDeclaration.isDefined) {
        out.addVar(possibleDeclaration.get, false)
      } else {
        val possibleM = DetectionUtils.extractMethodCallInStatement(d)
        if (possibleM.isDefined) {
          //this could throw an error for Intents
          if (DetectionUtils.classIsSubClassOfFragment(possibleM.get.getDeclaringClass)) {
            val methodName = possibleM.get.getName
            for (ub <- d.getUseBoxes.asScala) {
              ub match {
                case vb: ValueBox =>
                  val valueName = vb.getValue.toString()
                  if (methodName.contains("setArguments")) {
                    val varInfoOption = out.getVar(valueName)
                    if (varInfoOption.isDefined) {
                      checkForViolation(varInfoOption.get)
                    }
                  } else if (methodName.contains("show(") || methodName.contains("add(") ||
                    methodName.contains("replace(")){
                    val varInfoOption = out.getVar(valueName)
                    if (varInfoOption.isDefined) {
                      varInfoOption.get.isAttached = true
                    }
                  }
              }
            }


            //println(s"found setSelector with ${valueName}: ${d.toString()}")
            //println(s"${possibleM.get.}")
            //println("found setSelector")

            //println(s"var option info: hasSetSelector: ${varInfoOption.get.hasSetSelector}, hasSetPackage ${varInfoOption.get.hasSetPackage}")
          }
        }
      }
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): AnalyzeSetArguments.AnalysisInfo = {
    return new AnalyzeSetArguments.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: AnalyzeSetArguments.AnalysisInfo, in2: AnalyzeSetArguments.AnalysisInfo, out: AnalyzeSetArguments.AnalysisInfo): Unit = {
    out.clear()
    for (variable <- in1.varMap.keySet) {
      if (in2.varMap.contains(variable)) {
        out.addVar(variable, (in1.varMap(variable).isAttached || in2.varMap(variable).isAttached))
        checkForViolation(out.getVar(variable).getOrElse(null))
      } else {
        out.addVar(variable, in1.varMap(variable).isAttached)
      }
    }
    for (variable <- in2.varMap.keySet) {
      if (!out.varMap.contains(variable)) {
        out.addVar(variable, in2.varMap(variable).isAttached)
      }
    }
  }

  /** Creates a copy of the <code>source</code> flow object in <code>dest</code>. */
  override protected def copy(source: AnalyzeSetArguments.AnalysisInfo, dest: AnalyzeSetArguments.AnalysisInfo): Unit = {
    dest.varMap = source.varMap.clone()
  }

  def checkForViolation(d: AnalyzeSetArguments.DirectiveInfo): Boolean = {
    if (d == null) {
      return false
    }
    if (numberOfCaughtProblems != 1 && d.isAttached) {
      Predef.println("error: setArguments is called after the object is already attached")
      //just determine if there is an error - earlier I was trying to count all errors and
      //I was getting the number of control flow paths that included the error instead.
      //Since this analysis only checks one method at a time, we only throw an error per
      //method call
      numberOfCaughtProblems = 1
      println(s"number of caught problems: ${numberOfCaughtProblems}")
      return true
    }
    return false
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}

object AnalyzeSetArguments {

  class DirectiveInfo(var isAttached: Boolean = false) {

  }

  class AnalysisInfo(var varMap: mutable.HashMap[String, DirectiveInfo] = new mutable.HashMap[String, DirectiveInfo]()) { //extends java.util.BitSet{

    def addVar(varName: String, isAttached: Boolean = false): Unit = {
      varMap.+=(varName -> new DirectiveInfo(isAttached))
    }

    def getVar(varName: String): Option[DirectiveInfo] = {
      if (varMap.contains(varName)) {
        return new Some(varMap(varName))
      } else {
        return None
      }
    }

    def clear(): Unit = {
      varMap = new mutable.HashMap[String, DirectiveInfo]()
    }

    override def equals(obj: Any): Boolean = {
      obj match {
        case ai: AnalysisInfo => {
          if (this.varMap.size != ai.varMap.size) {
            return false
          }
          else {
            for ((varName, di) <- ai.varMap) {
              if (!varMap.contains(varName)) {
                return false
              } else {
                if (ai.varMap(varName).isAttached != varMap(varName).isAttached) {
                  return false
                }
              }
            }
            return true
          }
        }
        case _ => return false
      }
    }
  }
}


