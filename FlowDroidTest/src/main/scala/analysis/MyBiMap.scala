package analysis
//Taken from https://stackoverflow.com/questions/9850786/is-there-such-a-thing-as-bidirectional-maps-in-scala
/*object BiMap {
  private[BiMap] trait MethodDistinctor
  //implicit object MethodDistinctor extends MethodDistinctor
}


//after reading thorough
case class BiMap[X, Y](map: Map[X, Y]) {
  def this(tuples: (X,Y)*) = this(tuples.toMap)
  private val reverseMap = map map (_.swap)
  require(map.size == reverseMap.size, "no 1 to 1 relation")
  def apply(x: X): Y = map(x)
  def apply(y: Y)(implicit d: BiMap.MethodDistinctor): X = reverseMap(y)
  val domain = map.keys
  val codomain = reverseMap.keys
}
*/

//I'm taking too long to create a generic algorithm. I'll implement a limited quick version
//and come back to this if the more generic version is useful
case class MyBiMap[X](map: Map[X,X]){
  //when given a list of tuples, save the current mapping and then inverse mapping to a new map
  //def this(tuples: (X,X)*) = this(tuples.toMap ++ tuples.map(_.swap))
  def this(tuples: Seq[(X,X)]) = this(tuples.toMap ++ tuples.map(_.swap))
  def apply(x: X): X = map(x)
}
