BEGIN;

CREATE TABLE IF NOT EXISTS surrogate1.benchmarks (
    id SERIAL PRIMARY KEY,
    cpu VARCHAR(255) NOT NULL,
    gpu VARCHAR(255) NOT NULL,
    ram VARCHAR(255) NOT NULL,
    fps DECIMAL(10, 2) NOT NULL,
    price_usd DECIMAL(10, 2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_benchmarks_cpu ON surrogate1.benchmarks (cpu);
CREATE INDEX IF NOT EXISTS idx_benchmarks_gpu ON surrogate1.benchmarks (gpu);

COMMIT;