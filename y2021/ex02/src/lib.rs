use std::str::FromStr;

#[derive(Debug)]
enum Instr {
    Up(usize),
    Down(usize),
    Forward(usize),
}

impl FromStr for Instr {
    type Err = &'static str;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (instr_type, amount) = s.split_once(' ').ok_or("Cannot parse move")?;
        let amount: usize = amount.parse().map_err(|_| "Cannot parse amount as usize")?;
        let instr = match instr_type {
            "up" => Instr::Up(amount),
            "down" => Instr::Down(amount),
            "forward" => Instr::Forward(amount),
            _ => return Err("Invalid move"),
        };

        Ok(instr)
    }
}

#[derive(Debug, Default)]
struct Pos {
    horiz: usize,
    depth: usize,
}

trait Submarine {
    fn apply(&mut self, instr: Instr);
}

impl Pos {
    fn mul(&self) -> usize {
        self.horiz * self.depth
    }
}

impl Submarine for Pos {
    fn apply(&mut self, instr: Instr) {
        match instr {
            Instr::Up(v) => self.depth -= v,
            Instr::Down(v) => self.depth += v,
            Instr::Forward(v) => self.horiz += v,
        }
    }
}

struct PosWrapper<T: Submarine> {
    pos: T,
}

impl<S: Submarine + Default> FromIterator<Instr> for PosWrapper<S> {
    fn from_iter<T: IntoIterator<Item = Instr>>(iter: T) -> Self {
        let mut pos = S::default();
        for instr in iter {
            pos.apply(instr);
        }
        PosWrapper { pos }
    }
}

#[derive(Debug, Default)]
struct PosWithAim {
    aim: usize,
    horiz: usize,
    depth: usize,
}

impl PosWithAim {
    fn mul(&self) -> usize {
        self.horiz * self.depth
    }
}

impl Submarine for PosWithAim {
    fn apply(&mut self, instr: Instr) {
        match instr {
            Instr::Up(v) => self.aim -= v,
            Instr::Down(v) => self.aim += v,
            Instr::Forward(v) => {
                self.horiz += v;
                self.depth += self.aim * v
            }
        }
    }
}

pub fn part1(input: &str) -> usize {
    let pos: PosWrapper<Pos> = input.lines().map(|l| l.parse::<Instr>().unwrap()).collect();
    pos.pos.mul()
}

pub fn part2(input: &str) -> usize {
    let pos: PosWrapper<PosWithAim> = input.lines().map(|l| l.parse::<Instr>().unwrap()).collect();
    pos.pos.mul()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = include_str!("../input.txt");
        assert_eq!(part1(input), 1484118);
    }

    #[test]
    fn test_part2() {
        let input = include_str!("../input.txt");
        assert_eq!(part2(input), 1463827010);
    }
}
