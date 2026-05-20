use std::time::{Instant, Duration};
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use surrogate_1::router::{Router, TestCase};

fn benchmark_routing(c: &mut Criterion) {
    let mut router = Router::new();
    let test_cases = vec![
        TestCase { /* Initialize test case fields here */ },
        // Add more test cases as needed
    ];

    c.bench_function("routing_benchmark", |b| {
        b.iter(|| {
            let start = Instant::now();
            for test_case in &test_cases {
                router.route(black_box(test_case));
            }
            let duration = start.elapsed();
            // Avoid printing inside the benchmark loop for accurate measurements
            // println!("Routing duration: {:?}", duration);
            duration
        });
    });
}

criterion_group!(benches, benchmark_routing);
criterion_main!(benches);