package analysis

import soot.SootMethod

object FragmentLifecyleMethods {

  //can't decide how general to make this. I'll make this
  //specific for now and generalize later if something comes up

  //A better but more complicated solution to get the Fragment methods (not subclass specific)
  //that could be called from an outside component would be to
  //try to use the deduplexing library to read the methods of the Fragment class
  //for that API - I'll put that off for now and come back to it later if I decide that
  //would be helpful
  def isMethodWhenFragmentInitialized(methodToCheck: SootMethod): Boolean = {
    //commented out to test if I can catch the error without this check; this check is probably
    //correct, but it throws off my current analysis due to the number of anonymous inner classes
    //whose parents are not subclasses of Fragment - maybe also check for that in the future?
    //if (DetectionUtils.classIsSubClassOfFragment(methodToCheck.getDeclaringClass)) {
      val fragmentLifecycleMethods = List("onAttach", "onCreate", "onCreateView", "onViewCreated",
        "onActivityCreated", "onStart", "onResume", "onPause", "onStop", "onDestroyView",
        "onDestroy", "onDetach", "onActivityResult", "onClick")
      return (fragmentLifecycleMethods.contains(methodToCheck.getName))
    /*}
    else {
      return false
    }
    */

  }

  def isMethodWhenFragmentIsAttached(methodToCheck: SootMethod): Boolean = {
    if ((methodToCheck.getDeclaringClass.isInnerClass && DetectionUtils.classIsSubClassOfFragment(methodToCheck.getDeclaringClass.getOuterClass))
      || DetectionUtils.classIsSubClassOfFragment(methodToCheck.getDeclaringClass)) {
      val fragmentAttachedMethods = List("onAttach", "onCreate", "onCreateView", "onViewCreated",
      "onActivityCreated", "onStart", "onResume", "onPause", "onStop", "onDestroyView",
      "onDestroy", "onDetach", "onActivityResult", "onClick","onPreferenceClick")
      return (fragmentAttachedMethods.contains(methodToCheck.getName))
    }
    else {
      return false
    }

  }

}
