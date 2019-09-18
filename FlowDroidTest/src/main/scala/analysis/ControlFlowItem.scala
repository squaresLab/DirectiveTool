package analysis

import soot.SootMethod

class ControlFlowItem(val methodCall: SootMethod, isCheckingClasses: Boolean = true) {
  def isMethodEquals(methodToCheck: SootMethod): Boolean = {
    //I'm checking if this assert works, since I"m not sure and the rest of the code
    //depends on it. If the assert fails, then I'll go back and change the code
    assert((methodCall == methodToCheck) == (methodCall.toString == methodToCheck.toString))
    if(isCheckingClasses) {
      return (methodCall == methodToCheck) && (methodCall.getDeclaringClass == methodToCheck.getDeclaringClass)
    } else {
      return (methodCall == methodToCheck)
    }
  }
  def canEqual(a: Any) = a.isInstanceOf[ControlFlowItem]


  override def equals(that: Any): Boolean =
    that match {
      case that: ControlFlowItem => that.canEqual(this) && this.hashCode == that.hashCode
      case _ => false
    }

  override def hashCode:Int = {
    val prime = 31
    var result = 1
    //might need to change this to the hashCode of the string if the objects are not equal when the names are
    if(isCheckingClasses) {
      result = prime * result + methodCall.hashCode;
    } else {
      result = prime * result + methodCall.getName.hashCode
    }
    return result
  }

  override def toString: String = {
    if (isCheckingClasses){
      return methodCall.toString()
    } else {
      return methodCall.getName
    }
  }
}
