const DATA_EXAMPLE: &str = r#"987654321111111
811111111111119
234234234234278
818181911112111
"#;

fn largest_num(x: &str) -> (usize, i32) {
    let max = x
        .chars()
        .map(|c| c.to_string().parse::<i32>().unwrap())
        .max()
        .expect("find max");
    let idx = x.find(max.to_string().chars().next().unwrap()).unwrap();
    (idx, max)
}

fn part1(data: &str) {
    let res: i32 = data
        .lines()
        .map(|line| {
            let (idx, first) = largest_num(&line[0..(line.len() - 1)]);
            let (_, last) = largest_num(&line[(idx + 1)..line.len()]);
            let num = first * 10 + last;
            num
        })
        .sum();
    dbg!(res);
}

fn part2(data: &str) {
    let res: u64 = data
        .lines()
        .map(|line| {
            let line_len = line.len();
            let mut joltage = 0u64;
            let mut from: usize = 0;
            for remaining in (0..12).rev() {
                let (idx, num) = largest_num(&line[from..(line_len - remaining)]);
                joltage += (num as u64) * (10u64.pow(remaining as u32));
                from += idx + 1;
            }
            // dbg!(joltage);
            joltage
        })
        .sum();
    dbg!(res);
}

fn main() {
    let data = std::fs::read_to_string("data/day03.txt").expect("Failed to read input file");
    part1(&data);
    part2(&data);
}
