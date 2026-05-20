import pandas as pd
from typing import Dict, List
from datetime import datetime

class BenchmarkingDataLayer:
    def __init__(self):
        self.benchmark_data = pd.DataFrame()

    def load_benchmark_data(self, file_path: str) -> None:
        """Load benchmarking data from a CSV file."""
        self.benchmark_data = pd.read_csv(file_path)

    def get_benchmark_data(self) -> pd.DataFrame:
        """Get the loaded benchmarking data."""
        return self.benchmark_data

    def compare_with_benchmarks(self, startup_data: Dict[str, float]) -> Dict[str, float]:
        """Compare startup metrics with benchmarks."""
        comparison = {}
        for metric, value in startup_data.items():
            if metric in self.benchmark_data.columns:
                benchmark_value = self.benchmark_data[metric].mean()
                comparison[metric] = value - benchmark_value
        return comparison

    def get_benchmark_comparison(self, startup_data: Dict[str, float]) -> Dict[str, float]:
        """Get benchmark comparison for startup metrics."""
        return self.compare_with_benchmarks(startup_data)

    def save_comparison_to_csv(self, comparison: Dict[str, float], file_path: str) -> None:
        """Save the benchmark comparison to a CSV file."""
        comparison_df = pd.DataFrame([comparison])
        comparison_df.to_csv(file_path, index=False)

    def save_comparison_to_pdf(self, comparison: Dict[str, float], file_path: str) -> None:
        """Save the benchmark comparison to a PDF file."""
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Benchmark Comparison", ln=True, align="C")
        pdf.ln(10)

        for metric, value in comparison.items():
            pdf.cell(200, 10, txt=f"{metric}: {value}", ln=True, align="L")

        pdf.output(file_path)