package analysis

class ParseCodeObj(var stringToParse: String, var codeResult:Option[_ =>Int], var instanceType:Option[String] = None,
                   var inNot:Boolean = false, var contexts: List[String]= List()) {



  /*This assumes and inside out build. I might have to do it the
  other way
   */
  def addToCodeResult(newSurroundingFunction: Any => Any): Unit = {
    /*if (codeResult == "") {
      codeResult = before + after
    }
    else {
      codeResult = before + "\n" + codeResult + "\n" + after
    }
  }*/
  }

  def checkEndOfContexts(): Unit = {
    if (stringToParse(0) == ')') {
       val contextToHandle = contexts.head
      contexts = contexts.tail
      stringToParse = stringToParse.tail
      //also remove any periods after the context
      if (stringToParse(0) == '.'){
        stringToParse = stringToParse.tail
      }
      println(s"new string to parse: ${stringToParse}")
      if(contextToHandle == "not") {
        inNot = false
      }else{
        println(s"error: context ${contextToHandle} is not implemented yet")
        sys.exit(1)
      }
    }
  }

  def addToContexts(newContext: String): Unit ={
    if(newContext == "not"){
      inNot = true
      contexts = newContext::contexts
    }
  }

}


object ParseCodeObj {
  def apply(parseString: String, currentCode: Option[_=>Int]): ParseCodeObj = {
    var p = new ParseCodeObj(parseString, currentCode)
    p
  }
}

