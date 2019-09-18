package analysis

object FragmentLifecyleMethods {

  //can't decide how general to make this. I'll make this
  //specific for now and generalize later if something comes up

  //A better but more complicated solution to get the Fragment methods (not subclass specific)
  //that could be called from an outside component would be to
  //try to use the deduplexing library to read the methods of the Fragment class
  //for that API - I'll put that off for now and come back to it later if I decide that
  //would be helpful
  def isMethodWhenFragmentInitialized(methodToCheck:String): Boolean = {
    val fragmentLifecycleMethods = List("onAttach", "onCreate", "onCreateView", "onViewCreated",
      "onActivityCreated", "onStart", "onResume", "onPause", "onStop", "onDestroyView",
      "onDestroy", "onDetach", "onActivityResult", "onClick")
    return (fragmentLifecycleMethods.contains(methodToCheck))

  }

}
