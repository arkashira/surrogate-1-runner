import pytest
from surrogate_1.collector import parse_metrics, MetricParseError

# Sample raw output from SMC command (mocked)
SMC_OUTPUT_SAMPLE = """
Voltage: 12.6 V
Current: 1.2 A
Temperature: 35.0 C
Charge Cycles: 250
Design Capacity: 5000 mAh
"""

# Expected parsed result
EXPECTED_METRICS = {
    "voltage_mv": 12600,          # 12.6 V -> 12600 mV
    "current_ma": 1200,           # 1.2 A -> 1200 mA
    "temperature_c": 35.0,        # 35.0 C
    "charge_cycles": 250,         # cycles
    "design_capacity_mah": 5000,  # mAh
}

def test_parse_metrics_basic():
    """
    Verify that parse_metrics correctly extracts and converts
    the metrics from a typical SMC output string.
    """
    metrics = parse_metrics(SMC_OUTPUT_SAMPLE)
    assert metrics == EXPECTED_METRICS

def test_parse_metrics_missing_fields():
    """
    When some fields are missing, parse_metrics should still return
    a dictionary with the available keys and default None for missing ones.
    """
    partial_output = """
    Voltage: 11.8 V
    Temperature: 40.0 C
    """
    metrics = parse_metrics(partial_output)
    assert metrics["voltage_mv"] == 11800
    assert metrics["temperature_c"] == 40.0
    # Missing fields should be None
    assert metrics.get("current_ma") is None
    assert metrics.get("charge_cycles") is None
    assert metrics.get("design_capacity_mah") is None

def test_parse_metrics_invalid_format():
    """
    If the input string does not match expected patterns,
    parse_metrics should raise a ValueError.
    """
    bad_output = "This is not a valid SMC output"
    with pytest.raises(ValueError):
        parse_metrics(bad_output)

def test_parse_metrics_multiple_lines():
    """
    Ensure that parse_metrics can handle outputs where lines are
    not in the expected order or have extra whitespace.
    """
    mixed_output = """
    Design Capacity: 4800 mAh
    Voltage: 12.4 V
    Charge Cycles: 300
    Current: 0.9 A
    Temperature: 33.5 C
    """
    metrics = parse_metrics(mixed_output)
    assert metrics == {
        "voltage_mv": 12400,
        "current_ma": 900,
        "temperature_c": 33.5,
        "charge_cycles": 300,
        "design_capacity_mah": 4800,
    }

def test_parse_metrics_unit_conversion():
    """
    Verify that unit conversions are performed correctly:
    - Voltage in V to mV
    - Current in A to mA
    - Design capacity in mAh stays as is
    """
    unit_output = """
    Voltage: 13.2 V
    Current: 2.5 A
    Design Capacity: 5200 mAh
    """
    metrics = parse_metrics(unit_output)
    assert metrics["voltage_mv"] == 13200
    assert metrics["current_ma"] == 2500
    assert metrics["design_capacity_mah"] == 5200

def test_parse_metrics_partial_float():
    """
    Temperature can be a float; ensure parsing handles it.
    """
    raw = """
    Voltage: 11500 mV
    Current: 1500 mA
    Temperature: 42 C
    Charge Cycles: 250
    Design Capacity: 5000 mAh
    """
    metrics = parse_metrics(raw)
    assert metrics["temperature_c"] == 42.0

def test_parse_metrics_whitespace_and_case():
    """
    Parser should be tolerant to whitespace and case variations.
    """
    raw = """
    Voltage: 11500 mV
    Current: 1500 mA
    Temperature: 35.5 C
    Charge Cycles: 200
    Design Capacity: 5000 mAh
    """
    metrics = parse_metrics(raw)
    assert metrics["voltage_mv"] == 11500
    assert metrics["current_ma"] == 1500
    assert metrics["temperature_c"] == pytest.approx(35.5)
    assert metrics["charge_cycles"] == 200
    assert metrics["design_capacity_mah"] == 5000

def test_parse_metrics_invalid_numeric_value():
    """
    Non-numeric values should raise a ValueError.
    """
    invalid_output = """
    Voltage: abc mV
    Current: 1500 mA
    Temperature: 35.5 C
    Charge Cycles: 200
    Design Capacity: 5000 mAh
    """
    with pytest.raises(ValueError):
        parse_metrics(invalid_output)

def test_parse_metrics_missing_required_field():
    """
    Missing required fields should raise a ValueError.
    """
    incomplete_output = """
    Voltage: 11500 mV
    Current: 1500 mA
    Temperature: 35.5 C
    Design Capacity: 5000 mAh
    """
    with pytest.raises(ValueError):
        parse_metrics(incomplete_output)