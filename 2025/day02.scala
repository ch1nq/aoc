val data = scala.io.Source.fromFile("data/day02.txt").mkString

val data_example = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""

def part1(input: String): Unit = {

  def isInvalidId(id: Long): Boolean =
    val idStr = id.toString()
    val (l, r) = idStr.splitAt(idStr.length() / 2)
    l == r

  val sum = input
    .split(",")
    .map(
      _.split("-", 2)
        .map(_.strip().toLong)
    )
    .flatMap {
      case Array(min, max) => Iterator.range(min, max + 1)
      case x               => Iterator.empty
    }
    .filter(isInvalidId)
    .sum

  println(sum)
}

def part2(input: String): Unit =

  def isInvalidId(id: Long): Boolean =
    val idStr = id.toString()
    1.to(idStr.length())
      .filter(rep => (idStr.length().floatValue / rep.floatValue).isWhole)
      .map(rep => {
        val partLen = idStr.length() / rep
        val (part, _) = idStr.splitAt(partLen)
        partLen < idStr.length && idStr.grouped(partLen).forall(_ == part)
      })
      .exists(identity)

  val sum = input
    .split(",")
    .map(
      _.split("-", 2)
        .map(_.strip().toLong)
    )
    .flatMap {
      case Array(min, max) => min.to(max)
      case x               => Iterator.empty
    }
    .filter(isInvalidId)
    .sum

  println(sum)

@main
def main(): Unit = {
  part1(data)
  part2(data)
}
