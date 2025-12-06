val example = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()

case class Range(min: BigInt, max: BigInt) {
  def inRange(i: BigInt): Boolean =
    i >= min && i <= max
  def size: BigInt = max - min + 1
  def overlaps(other: Range) =
    other.inRange(min) || other.inRange(max) || inRange(other.max) || inRange(
      other.min
    )
  def combine(other: Range): Range =
    Range(min.min(other.min), max.max(other.max))
}

def part1(input: String): Unit = {
  import Range.*

  val Array(rangesRaw, ingredientsRaw) = input.split("\n\n", 2)
  val ranges = rangesRaw
    .split("\n")
    .map(_.split("-").map(BigInt(_)))
    .map {
      case Array(min, max) => Range(min, max)
      case _               => throw RuntimeException("parse range")
    }
    .toSeq

  val ingredients = ingredientsRaw.lines().map(BigInt(_))
  val numFresh = ingredients
    .filter(ingredient => {
      ranges.exists(_.inRange(ingredient))
    })
    .count
  println(numFresh)
}

def reduceRanges(
    ranges: Seq[Range]
): Seq[Range] = {
  var combined = Seq[Range]()
  var current: Option[Range] = None
  ranges
    .sortBy(_.min)
    .foreach(range => {
      current match
        case Some(c) if c.overlaps(range) => current = Some(c.combine(range))
        case Some(c)                      =>
          combined = combined :+ c
          current = Some(range)
        case None => current = Some(range)
    })
  combined = current match
    case Some(r) => combined :+ r
    case None    => combined
  combined
}

def part2(input: String): Unit = {
  val Array(rangesRaw, ingredientsRaw) = input.split("\n\n", 2)
  val ranges = rangesRaw
    .split("\n")
    .map(_.split("-").map(BigInt(_)))
    .map {
      case Array(min, max) => Range(min, max)
      case _               => throw RuntimeException("parse range")
    }
  val rangesReduced = reduceRanges(ranges)

  println(rangesReduced.map(_.size).sum)

}

val data = scala.io.Source.fromFile("data/day05.txt").mkString
part1(data)
part2(data)
