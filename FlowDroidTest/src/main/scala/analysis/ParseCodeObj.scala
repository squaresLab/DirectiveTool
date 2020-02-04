package analysis

class ParseCodeObj(var stringToParse: String, var codeResult:Option[_ =>Int], var instanceType:Option[String] = None) {



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

}


object ParseCodeObj {
  def apply(parseString: String, currentCode: Option[_=>Int]): ParseCodeObj = {
    var p = new ParseCodeObj(parseString, currentCode)
    p
  }
}

