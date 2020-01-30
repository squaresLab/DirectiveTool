package analysis

object JarMain {

  //The main class for packaging this into a jar
  def main(args: Array[String]): Unit = {
    if (args.length < 1) {
      println("please put the name of the checker to run")
    }
    else {
      val newArgs = args.toList.drop(1).toArray
      args(0) match {
        case "DetectIncorrectGetActivityMain" => DetectIncorrectGetActivityMain.runAnalysis(newArgs)
        case "DetectIncorrectSetInitialSavedState" => DetectIncorrectSetInitialSavedState.runAnalysis(newArgs)
        case "DetectInvalidGetResources" => DetectInvalidGetResources.runAnalysis(newArgs)
          //I don't think this next one is implemented yet
        //case "DetectInvalidGetView" => DetectInvalidGetView.runAnalysis(newArgs)
        case "DetectInvalidSetContentViewFindViewByIDOrdering" => DetectInvalidSetContentViewFindViewByIDOrdering.runAnalysis(newArgs)
        case "DetectInvalidSetTheme" => DetectInvalidSetTheme.runAnalysis(newArgs)
        case "DetectInvalidInflateCallMain" => DetectInvalidInflateCallMain.runAnalysis(newArgs)
        case "DetectMissingSetHasOptionsMenu" => DetectMissingSetHasOptionsMenu.runAnalysis(newArgs)
        case "DetectMissingSetHasOptionsMenu" => DetectMissingSetHasOptionsMenu.runAnalysis(newArgs)
        case "DetectMissingOptionsMenuDefinition" => DetectMissingOptionsMenuDefinition.runAnalysis(newArgs)
        case "DetectSetArgumentsMain" => DetectSetArgumentsMain.runAnalysis(newArgs)
        case "DetectSetSelectorSetPackageProblem" => DetectSetSelectorSetPackageProblem.runAnalysis(newArgs)
        case anyString => println(s"${anyString} not a currently implemented detector")
      }
    }
  }

}
