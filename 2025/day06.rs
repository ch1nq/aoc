const DATA_EXAMPLE: &str = r#"123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  "#;

#[derive(Debug)]
enum Op {
    Sum,
    Prod,
}

#[derive(Debug)]
struct Problem {
    nums: Vec<u64>,
    op: Op,
}

impl Problem {
    fn compute(&self) -> u64 {
        match self.op {
            Op::Sum => self.nums.iter().sum(),
            Op::Prod => self.nums.iter().product(),
        }
    }
}

fn parse_row_num(row: &str) -> Vec<u64> {
    row.trim()
        .split_ascii_whitespace()
        .map(|num| num.parse().expect("parse"))
        .collect()
}

fn parse_row_op(row: &str) -> Vec<Op> {
    row.split_ascii_whitespace()
        .map(|op| match op {
            "*" => Op::Prod,
            "+" => Op::Sum,
            x => panic!("skibidi what: {}", x),
        })
        .collect()
}

fn part1(data: &str) {
    let lines: Vec<_> = data.lines().collect();
    let n_parts = lines.len() - 1;
    let nums = lines
        .clone()
        .into_iter()
        .take(n_parts)
        .map(parse_row_num)
        .collect::<Vec<_>>();
    let ops = lines
        .into_iter()
        .skip(n_parts)
        .next()
        .map(parse_row_op)
        .unwrap();
    let problems: Vec<_> = ops
        .into_iter()
        .enumerate()
        .map(|(i, op)| Problem {
            nums: (0..n_parts).map(|j| nums[j][i]).collect(),
            op,
        })
        .collect();
    dbg!(&problems);
    // let problems =
    // let answers = todo!()
    let total: u64 = problems.iter().map(Problem::compute).sum();
    dbg!(total);
}

fn part2(data: &str) {
    let lines: Vec<_> = data.lines().collect();
    let n_parts = lines.len() - 1;
    let ops = lines
        .iter()
        .skip(n_parts)
        .next()
        .map(|&op| parse_row_op(op))
        .unwrap();

    let mat: Vec<_> = lines
        .into_iter()
        .take(n_parts)
        .map(|r| r.to_string().into_bytes())
        .collect();
    let mut num_cols = vec![];
    let mut current = vec![];
    for j in 0..mat[0].len() {
        let num_vec: Vec<_> = (0..n_parts).map(|i| mat[i][j]).collect();
        let num_str = std::str::from_utf8(&num_vec).unwrap();
        dbg!(&num_str);
        if num_str.trim().len() == 0 {
            num_cols.push(current);
            current = vec![];
        } else {
            let num: u64 = num_str.trim().parse().unwrap();
            current.push(num);
        }
    }
    num_cols.push(current);

    let problems: Vec<_> = ops
        .into_iter()
        .zip(num_cols)
        .map(|(op, nums)| Problem { nums, op })
        .collect();
    dbg!(&problems);

    let total: u64 = problems.iter().map(Problem::compute).sum();
    dbg!(total);
}

fn main() {
    let data = std::fs::read_to_string("data/day06.txt").expect("Failed to read input file");
    part1(&data);
    part2(&data);
}
