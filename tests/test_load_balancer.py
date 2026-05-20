import pytest

# Import the load balancing logic. Adjust the import path if the module resides elsewhere.
# The expected API: balance_load(gpus: List[str], tasks: List[Any]) -> Dict[str, List[Any]]
try:
    from surrogate_1.load_balancer import balance_load
except Exception as e:
    # If the import fails, provide a clear error message for debugging.
    raise ImportError(f"Failed to import balance_load from surrogate_1.load_balancer: {e}")

@pytest.fixture
def gpu_list():
    """Return a sample list of GPU identifiers."""
    return ["GPU0", "GPU1", "GPU2", "GPU3"]

def test_balance_even_distribution(gpu_list):
    """When number of tasks is a multiple of GPUs, each GPU should receive equal load."""
    tasks = list(range(8))  # 8 tasks
    distribution = balance_load(gpu_list, tasks)
    # Each GPU should have 2 tasks
    for gpu in gpu_list:
        assert len(distribution[gpu]) == 2
    # All tasks should be assigned exactly once
    assigned = [t for lst in distribution.values() for t in lst]
    assert sorted(assigned) == sorted(tasks)

def test_balance_uneven_tasks(gpu_list):
    """When tasks are not evenly divisible, the first GPUs receive the extra tasks."""
    tasks = list(range(7))  # 7 tasks
    distribution = balance_load(gpu_list[:3], tasks)  # 3 GPUs
    # Expected distribution: [3,2,2]
    expected_counts = [3, 2, 2]
    actual_counts = [len(distribution[gpu]) for gpu in distribution]
    assert actual_counts == expected_counts
    # All tasks assigned
    assigned = [t for lst in distribution.values() for t in lst]
    assert sorted(assigned) == sorted(tasks)

def test_balance_no_tasks(gpu_list):
    """If there are no tasks, the distribution should be empty lists for each GPU."""
    distribution = balance_load(gpu_list, [])
    for gpu in gpu_list:
        assert distribution[gpu] == []

def test_balance_more_gpus_than_tasks(gpu_list):
    """When GPUs outnumber tasks, each task gets its own GPU and remaining GPUs receive empty lists."""
    tasks = [101, 202]
    distribution = balance_load(gpu_list[:5], tasks)  # 5 GPUs, 2 tasks
    # Two GPUs should have one task each, others empty
    non_empty = [gpu for gpu, lst in distribution.items() if lst]
    assert len(non_empty) == 2
    assert set(distribution[non_empty[0]]) == {101}
    assert set(distribution[non_empty[1]]) == {202}
    # Remaining GPUs should have empty lists
    for gpu in set(gpu_list[:5]) - set(non_empty):
        assert distribution[gpu] == []

def test_balance_no_gpus():
    """If no GPUs are provided, balance_load should raise a ValueError."""
    with pytest.raises(ValueError):
        balance_load([], [1, 2, 3])