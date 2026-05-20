class Catalog:
    def __init__(self):
        self.benchmarks = {}

    def update_benchmarks(self, new_benchmarks):
        """
        Updates the catalog with new benchmark scores.
        """
        self.benchmarks.update(new_benchmarks)

    def get_benchmarks(self):
        return self.benchmarks