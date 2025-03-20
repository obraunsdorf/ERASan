// minimal memory-safety error: heap buffer overflow
// from https://github.com/japaric/rust-san/blob/master/asan/examples/use-after-free.rs

fn main() {
    let xs = vec![0, 1, 2, 3];
    let y = xs.as_ptr();
    drop(xs);
    let z = unsafe { *y };
}