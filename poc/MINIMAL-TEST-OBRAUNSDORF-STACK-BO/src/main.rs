// minimal memory-safety error: stack buffer overflow
// from https://github.com/japaric/rust-san/blob/master/asan/examples/out-of-bounds.rs

fn main() {
    let xs = [0, 1, 2, 3];
    let y = unsafe { *xs.as_ptr().offset(4) };
}