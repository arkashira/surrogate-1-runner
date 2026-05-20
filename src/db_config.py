import os
from typing import Dict, Any, Optional
import mysql.connector
from mysql.connector import Error

class DBConfig:
    """Comprehensive database configuration and connection management for MySQL and MariaDB"""

    def __init__(self):
        self.configs = {
            'mysql': self._load_config('MYSQL_'),
            'mariadb': self._load_config('MARIADB_')
        }
        self._validate_configs()

    def _load_config(self, prefix: str) -> Dict[str, Any]:
        """Load database configuration from environment variables with given prefix"""
        return {
            'host': os.getenv(f'{prefix}HOST', 'localhost'),
            'user': os.getenv(f'{prefix}USER', 'root'),
            'password': os.getenv(f'{prefix}PASSWORD', ''),
            'database': os.getenv(f'{prefix}DATABASE', 'test_db'),
            'port': int(os.getenv(f'{prefix}PORT', 3306 if prefix == 'MYSQL_' else 3307)),
            'charset': 'utf8mb4',
            'use_pure': True
        }

    def _validate_configs(self) -> None:
        """Validate all database configurations"""
        required_fields = ['host', 'user', 'password', 'database']

        for db_type, config in self.configs.items():
            for field in required_fields:
                if not config.get(field):
                    raise ValueError(f"Missing required field '{field}' in {db_type.upper()} config")

    def get_connection(self, db_type: str = 'mysql') -> Optional[mysql.connector.MySQLConnection]:
        """
        Establish database connection

        Args:
            db_type: Either 'mysql' or 'mariadb'

        Returns:
            Database connection object or None if connection fails
        """
        if db_type not in self.configs:
            raise ValueError(f"Unsupported database type: {db_type}")

        try:
            return mysql.connector.connect(**self.configs[db_type])
        except Error as e:
            print(f"Error connecting to {db_type.upper()}: {e}")
            return None

    @property
    def mysql_config(self) -> Dict[str, Any]:
        """Get MySQL configuration"""
        return self.configs['mysql']

    @property
    def mariadb_config(self) -> Dict[str, Any]:
        """Get MariaDB configuration"""
        return self.configs['mariadb']