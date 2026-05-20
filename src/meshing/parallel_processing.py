import concurrent.futures
import numpy as np
from typing import List, Optional
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def meshing_operation(file_path: str) -> None:
    """
    Perform meshing operation on a single file.
    Args:
        file_path: Path to the file to be meshed
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file format is unsupported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not file_path.lower().endswith(('.obj', '.stl')):
        raise ValueError(f"Unsupported file format: {file_path}")

    logger.info(f"Starting meshing operation for {file_path}")
    # Actual meshing implementation would go here
    # For now, we'll simulate processing
    np.random.seed(42)  # For reproducible testing
    processing_time = np.random.uniform(0.1, 0.5)
    np.sleep(processing_time)  # Simulate processing time
    logger.info(f"Completed meshing for {file_path}")

def parallel_meshing(file_paths: List[str], max_workers: Optional[int] = None) -> None:
    """
    Process multiple files in parallel using thread pool.
    Args:
        file_paths: List of file paths to process
        max_workers: Maximum number of worker threads (None for automatic)
    """
    if not file_paths:
        logger.warning("No files provided for meshing")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(meshing_operation, file_path): file_path
            for file_path in file_paths
        }

        for future in concurrent.futures.as_completed(futures):
            file_path = futures[future]
            try:
                future.result()
                logger.info(f"Successfully processed {file_path}")
            except Exception as exc:
                logger.error(f"Failed to process {file_path}: {str(exc)}")

def validate_input_files(file_paths: List[str]) -> bool:
    """Validate that all input files exist and are of supported formats."""
    valid_files = []
    for file_path in file_paths:
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                continue
            if not file_path.lower().endswith(('.obj', '.stl')):
                logger.error(f"Unsupported format: {file_path}")
                continue
            valid_files.append(file_path)
        except Exception as e:
            logger.error(f"Error validating {file_path}: {str(e)}")

    if not valid_files:
        logger.error("No valid files found for processing")
        return False
    return True

def main() -> None:
    """Main execution function with proper error handling."""
    try:
        # Example usage - in production this would come from command line args
        input_dir = "/opt/axentx/surrogate-1/input"
        file_paths = [
            str(f) for f in Path(input_dir).glob("*.obj")
            if f.is_file()
        ]

        if not validate_input_files(file_paths):
            return

        parallel_meshing(file_paths)
        logger.info("Meshing operations completed")

    except Exception as e:
        logger.critical(f"Fatal error in main execution: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()