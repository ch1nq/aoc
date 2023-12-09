fn main() {
    part1();
    part2();
}

fn part1() {
    let x: u32 = std::env::args()
        .last()
        .expect("input")
        .split("\n")
        .map(|line| {
            let mut d = line.chars().filter(|c| c.is_numeric());
            let f: u32 = d.next().map_or(0, |f| f.to_digit(10).expect("to_digit"));
            let l: u32 = d
                .next_back()
                .map_or(f, |l| l.to_digit(10).expect("to_digit"));
            f * 10 + l
        })
        .sum();
    dbg!(&x);
}

fn part2() {
    let digit_map: Vec<(&str, u32)> = vec![
        ("0", 0),
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
    ];
    let x: u32 = std::env::args()
        .last()
        .expect("input")
        .split("\n")
        .map(|line| {
            let d = digit_map.iter().flat_map(|(k, v)| {
                let mut matches = vec![];
                let mut offset = 0;
                while let Some(idx) = line[offset..].find(*k) {
                    matches.push(offset + idx);
                    offset += idx + 1;
                }
                matches.into_iter().map(move |idx| (idx, v))
            });
            let first = d.clone().min_by(|x, y| x.0.cmp(&y.0)).unwrap().1;
            let last = d.max_by(|x, y| x.0.cmp(&y.0)).unwrap().1;
            first * 10 + last
        })
        .sum();
    dbg!(x);
}
