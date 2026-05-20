#!/usr/bin/env python3
"""Transaction Consistency Check Tool with Comprehensive Error Handling"""

import sys
import argparse
from enum import IntEnum
from typing import List, Optional, Dict, Tuple

class ExitCode(IntEnum):
    """Standardized exit codes for consistency checks"""
    SUCCESS = 0
    CRITICAL = 1
    WARNING = 2
    INFO = 3
    CONNECTION_ERROR = 4
    INVALID_ARGUMENT = 5

class IssueSeverity(IntEnum):
    """Severity levels for consistency issues"""
    CRITICAL = 1
    WARNING = 2
    INFO = 3

class ConsistencyChecker:
    """Core consistency checking functionality"""

    def __init__(self):
        self.issues: Dict[IssueSeverity, List[Dict]] = {
            IssueSeverity.CRITICAL: [],
            IssueSeverity.WARNING: [],
            IssueSeverity.INFO: []
        }
        self.database_type: Optional[str] = None

    def add_issue(self, severity: IssueSeverity, message: str, details: Optional[str] = None):
        """Add an issue with specified severity"""
        self.issues[severity].append({
            'message': message,
            'details': details or ''
        })

    def set_database_type(self, db_type: str):
        """Set the database type for context"""
        self.database_type = db_type

    def has_critical_issues(self) -> bool:
        """Check for critical issues"""
        return len(self.issues[IssueSeverity.CRITICAL]) > 0

    def get_exit_code(self) -> int:
        """Determine appropriate exit code based on issues"""
        if self.has_critical_issues():
            return ExitCode.CRITICAL
        if len(self.issues[IssueSeverity.WARNING]) > 0:
            return ExitCode.WARNING
        if len(self.issues[IssueSeverity.INFO]) > 0:
            return ExitCode.INFO
        return ExitCode.SUCCESS

    def generate_report(self) -> str:
        """Generate comprehensive human-readable report"""
        report = []
        report.append("=" * 60)
        report.append("TRANSACTION CONSISTENCY CHECK REPORT")
        report.append("=" * 60)

        if self.database_type:
            report.append(f"Database Type: {self.database_type}")
        report.append("")

        for severity in IssueSeverity:
            issues = self.issues[severity]
            if issues:
                report.append(f"{severity.name} Issues: {len(issues)}")
                for issue in issues:
                    report.append(f" [{severity.name}] {issue['message']}")
                    if issue['details']:
                        report.append(f"   Details: {issue['details']}")
                report.append("")

        report.append("=" * 60)
        return "\n".join(report)

def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description='Run comprehensive transaction consistency checks',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    db_group = parser.add_mutually_exclusive_group(required=True)
    db_group.add_argument('--mysql', action='store_true', help='Check MySQL database')
    db_group.add_argument('--mariadb', action='store_true', help='Check MariaDB database')

    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', type=int, default=3306, help='Database port')
    parser.add_argument('--user', default='axentx', help='Database username')
    parser.add_argument('--password', default='', help='Database password')
    parser.add_argument('--database', default='axentx', help='Database name')

    return parser

def validate_arguments(args: argparse.Namespace) -> Tuple[bool, str]:
    """Validate command line arguments"""
    if args.port <= 0 or args.port > 65535:
        return False, "Port must be between 1 and 65535"

    if not args.user:
        return False, "Database username is required"

    return True, ""

def run_checks(checker: ConsistencyChecker, args: argparse.Namespace) -> bool:
    """Execute all consistency checks"""
    try:
        # Set database type for reporting
        checker.set_database_type("mysql" if args.mysql else "mariadb")

        # Example checks (replace with actual database logic)
        checker.add_issue(IssueSeverity.INFO, "Checking for orphaned transactions...")
        checker.add_issue(IssueSeverity.WARNING, "Found 3 duplicate entries in table 'orders'")
        checker.add_issue(IssueSeverity.CRITICAL, "Missing required field 'timestamp' in 5 records")

        return True

    except Exception as e:
        checker.add_issue(IssueSeverity.CRITICAL, f"Check failed: {str(e)}")
        return False

def main():
    """Main execution flow"""
    parser = create_parser()
    args = parser.parse_args()
    checker = ConsistencyChecker()

    # Validate arguments
    valid, error = validate_arguments(args)
    if not valid:
        checker.add_issue(IssueSeverity.CRITICAL, f"Invalid arguments: {error}")
        print(checker.generate_report())
        sys.exit(ExitCode.INVALID_ARGUMENT)

    # Run checks
    success = run_checks(checker, args)

    # Generate report and exit with appropriate code
    print(checker.generate_report())
    sys.exit(checker.get_exit_code())

if __name__ == "__main__":
    main()