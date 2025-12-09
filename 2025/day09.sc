import scala.compiletime.ops.boolean
val example = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

case class Point(x: Long, y: Long)

def part1(input: String): Unit = {
  val points = input.split("\n").map(_.split(",").map(_.toLong)).map {
    case Array(x, y) => Point(x, y)
  }
  val total = points
    .combinations(2)
    .map { case Array(a, b) =>
      ((a.x - b.x).abs + 1) * ((a.y - b.y).abs + 1)
    }
    .max
  println(total)
}

def inRect(p: Point, a: Point, b: Point): Boolean =
  val left = a.x.min(b.x)
  val right = a.x.max(b.x)
  val top = a.y.min(b.y)
  val bottom = a.y.max(b.y)

  val leftInner = (left + 1).min(right)
  val rightInner = (right - 1).max(left)
  val topInner = (top + 1).min(bottom)
  val bottomInner = (bottom - 1).max(top)

  p.x >= leftInner && p.x <= rightInner && p.y >= topInner && p.y <= bottomInner

def rectSize(a: Point, b: Point): Long =
  ((a.x - b.x).abs + 1) * ((a.y - b.y).abs + 1)

def edgeBetween(a: Point, b: Point): Seq[Point] =
  val left = a.x.min(b.x)
  val right = a.x.max(b.x)
  val top = a.y.min(b.y)
  val bottom = a.y.max(b.y)
  left.to(right).flatMap(x => top.to(bottom).map(y => Point(x, y)))

def part2(input: String): Unit = {
  val points = input.split("\n").map(_.split(",").map(_.toLong)).map {
    case Array(x, y) => Point(x, y)
  }
  val edges = points
    .sliding(2, 1)
    .flatMap { case Array(a, b) => edgeBetween(a, b) }
    .toSeq ++ edgeBetween(points.last, points.head)
  println(edges.length)
  println(points.length)
  val candidates = points
    .combinations(2)
    .map { case Array(a, b) =>
      (a, b)
    }
    .filterNot((a, b) => edges.exists(p => inRect(p, a, b)))
  // .foreach((a, b) => println(s"$a,$b = ${rectSize(a, b)}"))
  // candidates.foreach(println)
  val total = candidates.map((a, b) => rectSize(a, b)).max
  print(total)
  // points.foreach(p => println(s"$p ${inRect(p, Point(9, 7), Point(2, 3))}"))
}

val data = scala.io.Source.fromFile("data/day09.txt").mkString
// part1(data)
part2(data)
