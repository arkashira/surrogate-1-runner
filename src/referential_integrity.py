
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, and_
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)