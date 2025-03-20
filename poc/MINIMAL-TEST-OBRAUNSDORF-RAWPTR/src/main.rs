// minimal memory-safety error: heap buffer overflow
// from https://github.com/japaric/rust-san/blob/master/asan/examples/use-after-free.rs

fn foo(rawptr: *const i32) -> &'static i32 {
    let safe = unsafe { &*rawptr };
    safe
}

fn main() {
    let xs = vec![0, 1, 2, 3];
    let rawptr = unsafe { xs.as_ptr().offset(4) };
    let safe: &i32 = foo(rawptr);
    let y = *safe;
}