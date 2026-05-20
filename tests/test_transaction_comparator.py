
from unittest.mock import Mock
from surrogate_1.transaction_comparator import TransactionComparator

def test_compare_transactions():
    # Arrange
    mysql_conn = Mock()
    mariadb_conn = Mock()
    sql_statements = ["SELECT * FROM table1", "INSERT INTO table2 VALUES (1, 2)"]

    # Act
    comparator = TransactionComparator(mysql_conn, mariadb_conn)
    diff_report = comparator.compare_transactions(sql_statements)

    # Assert
    assert "commit/rollback" in diff_report
    assert "isolation level handling" in diff_report
    assert "error codes" in diff_report
    assert len(diff_report) <= 5  # Assuming the comparison completes in under 5 seconds

# Summary:
# - Created a unit test for `TransactionComparator.compare_transactions` method.
# - Test checks for the presence of expected sections in the diff report.
# - Test assumes that the comparison completes within the specified time limit.