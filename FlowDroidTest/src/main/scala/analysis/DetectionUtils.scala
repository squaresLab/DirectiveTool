package analysis

import soot.jimple.{IntConstant, InvokeExpr, SpecialInvokeExpr}
import soot.jimple.internal._
import soot.{SootClass, SootMethod, Value}

object DetectionUtils {

def classIsSubClassOfFragment(c: SootClass): Boolean = {
    if(c.toString() == "android.app.Fragment" || c.toString() == "android.support.v4.app.Fragment"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfFragment(c.getSuperclass)
      } else {
        return false
      }
    }
  }

  def classIsSubClassOfDialogFragment(c: SootClass): Boolean = {
    if(c.toString() == "android.app.DialogFragment" || c.toString() == "android.support.v4.app.DialogFragment"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfDialogFragment(c.getSuperclass)
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

  //May want to combine with the above method because they
  //are very similar
  def classIsSubClassOfAsyncTask(c: SootClass): Boolean = {
    if(c.toString() == "android.os.AsyncTask"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfAsyncTask(c.getSuperclass)
      } else {
        return false
      }
    }
  }

  def classIsSubClass(c: SootClass, possibleParentClassName: String): Boolean = {
    if (possibleParentClassName == "Activity" || possibleParentClassName == "android.app.Activity"){
      classIsSubClassOfActivity(c)
    } else if (possibleParentClassName == "Fragment" || possibleParentClassName == "android.app.Fragment"){
      classIsSubClassOfFragment(c)
    } else if (possibleParentClassName == "AsyncTask" || possibleParentClassName == "android.os.AsyncTask"){
      classIsSubClassOfAsyncTask(c)
    } else {
      throw new RuntimeException(s"unexpected parent class ${c} and possibleParentClassName ${possibleParentClassName}. Please create a handler for it")
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
    if (s.startsWith("java.lang")) {
      return false
    }
    else if (s.startsWith("android.app")){
      return false
    }
    else if (s.startsWith("android.os")){
      return false
    }
    else if (s.startsWith("android.widget")){
      return false
    }
    else if (s.startsWith("android.util")){
      return false
    }
    else if (s.startsWith("android.content")){
      return false
    }
    else if (s.startsWith("android.support")){
      return false
    }
    else if (s.startsWith("org.xmlpull")){
      return false
    }
    else if (s.startsWith("androidx")){
      return false
    }
    return true
  }

  def getAndroidJarLocation(args: Array[String]): String = {
    if (args.length > 1){
      return args(1)
    } else {
      return "/Users/zack/Library/Android/sdk/platforms/android-21/android.jar"
    }
  }

   def getAPKLocation(args: Array[String]): String = {
    //Scala doesn't seem to have the first argument default to the program name like Java
    if (args.length > 0){
      return args(0)
    } else {
      //return "/Users/zack/git/ViolationOfDirectives/Application/build/outputs/apk/debug/Application-debug.apk"
      //return "/Users/zack/git/ViolationOfDirectives/app/build/outputs/apk/debug/app-debug.apk"
      //return "/Users/zack/git/DirectiveTool/testFolder/app/build/outputs/apk/debug/app-debug.apk"
      //return "/Users/zack/git/DirectiveTool/testFolder/Application/build/outputs/apk/debug/Application-debug.apk"
      //return "/Users/zack/Documents/CMU/testRepos/MyApplication/app/build/outputs/apk/debug/app-debug.apk"
      //return "/Users/zack/git/DirectiveTool/temporaryTestOfChange/Application/build/outputs/apk/debug/Application-debug.apk"
      //return "/Users/zack/git/DirectiveTool/temporaryTestOfChange/app/build/outputs/apk/debug/app-debug.apk"
      //return "/Users/zack/git/DirectiveTool/org.xapek.andiodine_6.apk"
      //return "/Users/zack/git/DirectiveTool/eu.mrogalski.saidit_13.apk"
      //return "/Users/zack/git/DirectiveTool/apkWithError.apk"
      //return "/Users/zack/Desktop/singleTestCountApps/DetectSetArgumentsMain.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/com.etesync.syncadapter_83.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/nightlock.peppercarrot_7.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/org.secuso.privacyfriendlytodolist_4.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/io.github.trytonvanmeer.libretrivia_2.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/nodomain.freeyourgadget.tpmsmonitor_1.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/com.itds.sms.ping_6.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/com.eventyay.organizer_16.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/org.totschnig.myexpenses_377.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/de.baumann.pdfcreator_25.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/cz.vitSkalicky.klavesnice_2.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/com.physphil.android.unitconverterultimate_50500.apk"
      //return "/Users/zack/git/DirectiveTool/appsFromFDroid/org.linphone_4125.apk"
      return "/Users/zack/git/DirectiveTool/injectFaultsDir/tempRepoForInjection/app/build/outputs/apk/debug/app-debug.apk"
    }
  }
}
