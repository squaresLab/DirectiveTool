import soot.jimple.{IntConstant, InvokeExpr, SpecialInvokeExpr}
import soot.jimple.internal._
import soot.{SootClass, SootMethod, Value}

object DetectionUtils {

def classIsSubClassOfFragment(c: SootClass): Boolean = {
    if(c.toString() == "android.app.Fragment"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfFragment(c.getSuperclass)
      } else {
        return false
      }
    }
  }

  //May want to combine with the above method because they
  //are very similar
  def classIsSubClassOfActivity(c: SootClass): Boolean = {
    if(c.toString() == "android.app.Activity"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfActivity(c.getSuperclass)
      } else {
        return false
      }
    }
  }

  //now that you have the extract Invoke statement method, you might want to
  //reduce this down to just calling getMethod on the return from the
  //get invoke statement call
  def extractMethodCallInStatement(u: soot.Unit): Option[SootMethod] = {
    def handleStmt(stmt: soot.jimple.Stmt): Option[SootMethod] = {
      stmt match {
        case assignmentStatement: JAssignStmt => {
          assignmentStatement.rightBox.getValue match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr.getMethod)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr.getMethod)

            }
            case linkedBox: SpecialInvokeExpr=> {
              return Some(linkedBox.getMethod)
            }
            case _ => {
              //println(s"is statement with class: ${assignmentStatement.rightBox.getValue}")
              return None}
          }
        }
        case invokeExpr: InvokeExprBox => {
          invokeExpr match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr.getMethod)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr.getMethod)
            }
            case _ => return None
          }
        }
        case invokeSmt: JInvokeStmt => {
          return Some(invokeSmt.getInvokeExpr.getMethod)
        }
        case _ => return None
      }
    }

    u match {
      case s: soot.jimple.Stmt => return handleStmt(s)
      case _ => {
        //println(s"unmatched statement: ${u.getClass}")
        return None
      }
    }
  }
def extractInvokeStmtInStmt(u: soot.Unit): Option[InvokeExpr] = {
    def handleStmt(stmt: soot.jimple.Stmt): Option[InvokeExpr] = {
      stmt match {
        case assignmentStatment: JAssignStmt => {
          assignmentStatment.rightBox.getValue match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr)

            }
            case linkedBox: SpecialInvokeExpr=> {
              return Some(linkedBox)
            }
            case _ => {
              return None}
          }
        }
        case invokeExpr: InvokeExprBox => {
          invokeExpr match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr)
            }
            case _ => return None
          }
        }
        case invokeSmt: JInvokeStmt => {
          return Some(invokeSmt.getInvokeExpr)
        }
        case _ => return None
      }
    }

    u match {
      case s: soot.jimple.Stmt => return handleStmt(s)
      case _ => return None
    }
  }

  def isTrue(v: Value) : Boolean = {
    v match {
      case i: IntConstant => {
        if(i.value == 1){
          return true
        } else {
          return false
        }
      }
      case _ => return false
    }
  }

  def isCustomClassName(s:String): Boolean ={
    if (s.startsWith("java.lang")){
      return false;
    }
    else if (s.startsWith("android.app")){
      return false;
    }
    else if (s.startsWith("android.os")){
      return false;
    }
    else if (s.startsWith("android.widget")){
      return false;
    }
    return true;
  }

   def getAPKLocation(args: Array[String]): String = {
    //Scala doesn't seem to have the first argument default to the program name like Java
    if (args.length > 0){
      return args(0)
    } else {
      return "/Users/zack/git/ViolationOfDirectives/Application/build/outputs/apk/debug/Application-debug.apk"
    }
  }
}
