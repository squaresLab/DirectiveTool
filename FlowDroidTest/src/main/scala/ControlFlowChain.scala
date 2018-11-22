class ControlFlowChain(val controlChain: List[ControlFlowItem], var wasExtended : Boolean = false) {

  def canEqual(a: Any) = a.isInstanceOf[ControlFlowChain]

  override def equals(that: Any): Boolean =
    that match {
      case that: ControlFlowChain => {
        if(that.canEqual(this)) {
          assert ((this.hashCode == that.hashCode) == alternativeEqualsCheck(that))
          return this.hashCode == that.hashCode
        } else {
          return false
        }
      }
      case _ => false
    }

  def alternativeEqualsCheck(chainToCheck: ControlFlowChain): Boolean = {
    if(this.controlChain.size != chainToCheck.controlChain.size){
      return false
    } else {
      for( (item1: ControlFlowItem, item2: ControlFlowItem) <- (this.controlChain zip chainToCheck.controlChain)){
        if(item1.toString() != item2.toString()){
          return false
        }
      }
      return true
    }
  }

  override def hashCode:Int = {
    val prime = 31
    var result = 1
    //might need to change this to the hashCode of the string if the objects are not equal when the names are
    for(item <- controlChain){
      result = prime * result + item.hashCode
    }
    return result
  }
}
