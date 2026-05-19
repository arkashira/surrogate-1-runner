from __future__ import annotations

import subprocess
import sys
from typing import Dict, Optional

from .test_config_manager import TestConfigManager


class PipelineRunner:
    """
    Very small abstraction that:
    1. Loads a JSON config.
    2. Prints a helpful message.
    3. (Placeholder) runs the real pipeline.
    """

    def __init__(self, config_manager: Optional[TestConfigManager] = None):
        self.config_manager = config_manager or TestConfigManager()

    def run_pipeline_with_config(self, pipeline_name: str, config_name: str) -> None:
        cfg = self.config_manager.load_config(config_name)
        print(f"[{pipeline_name}] Running with config: {cfg}", file=sys.stderr)

        # ---- Replace this with your real pipeline logic ----
        # For demo purposes we just echo the config.
        subprocess.run([sys.executable, "-c", f"print('Pipeline {pipeline_name} executed')"], check=True)

    def update_and_run_pipeline(
        self, pipeline_name: str, config_name: str, updates: Dict[str, any]
    ) -> None:
        self.config_manager.update_config(config_name, updates)
        self.run_pipeline_with_config(pipeline_name, config_name)