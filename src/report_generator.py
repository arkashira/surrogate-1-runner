import json
import os
from typing import Dict, List, Any

class DiskGeometryReportGenerator:
    """
    A class to generate disk geometry reports from various hard disk models.
    """
    
    def __init__(self):
        self.geometry_data = {}
        
    def load_disk_geometry_data(self, data_source: str) -> None:
        """
        Load disk geometry data from a specified source.
        
        Args:
            data_source (str): Path to the data source file or directory
        """
        if os.path.isfile(data_source):
            with open(data_source, 'r') as f:
                self.geometry_data = json.load(f)
        elif os.path.isdir(data_source):
            # Load all JSON files in the directory
            for filename in os.listdir(data_source):
                if filename.endswith('.json'):
                    filepath = os.path.join(data_source, filename)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        disk_model = filename.replace('.json', '')
                        self.geometry_data[disk_model] = data
        else:
            raise FileNotFoundError(f"Data source not found: {data_source}")
    
    def parse_disk_geometry(self, disk_model: str) -> Dict[str, Any]:
        """
        Parse disk geometry data for a specific disk model.
        
        Args:
            disk_model (str): Name of the disk model
            
        Returns:
            Dict containing parsed geometry information
        """
        if disk_model not in self.geometry_data:
            raise ValueError(f"Disk model '{disk_model}' not found in loaded data")
            
        raw_data = self.geometry_data[disk_model]
        
        # Extract geometry information
        geometry_info = {
            'model': disk_model,
            'cylinders': raw_data.get('cylinders'),
            'heads': raw_data.get('heads'),
            'sectors_per_track': raw_data.get('sectors_per_track'),
            'total_sectors': raw_data.get('total_sectors'),
            'bytes_per_sector': raw_data.get('bytes_per_sector'),
            'capacity_bytes': raw_data.get('capacity_bytes'),
            'capacity_gb': raw_data.get('capacity_gb')
        }
        
        return geometry_info
    
    def generate_report(self, disk_models: List[str]) -> Dict[str, Any]:
        """
        Generate a detailed report of disk geometry for specified models.
        
        Args:
            disk_models (List[str]): List of disk model names
            
        Returns:
            Dict containing detailed report information
        """
        report = {
            'report_generated_at': '2026-05-04T00:00:00Z',
            'disk_models': []
        }
        
        for model in disk_models:
            try:
                geometry_info = self.parse_disk_geometry(model)
                report['disk_models'].append(geometry_info)
            except Exception as e:
                report['disk_models'].append({
                    'model': model,
                    'error': str(e)
                })
                
        return report
    
    def integrate_with_storage_system(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate the generated report with existing storage management systems.
        
        Args:
            report (Dict): Generated disk geometry report
            
        Returns:
            Dict with integrated report data
        """
        integrated_report = {
            'storage_system_integration': {
                'status': 'success',
                'timestamp': '2026-05-04T00:00:00Z',
                'report_data': report
            }
        }
        
        return integrated_report

def main():
    """
    Main function to demonstrate usage of the DiskGeometryReportGenerator.
    """
    # Initialize the report generator
    generator = DiskGeometryReportGenerator()
    
    # Example data structure (in practice, this would come from actual data sources)
    sample_data = {
        "WD_BLACK_1TB": {
            "cylinders": 65535,
            "heads": 255,
            "sectors_per_track": 63,
            "total_sectors": 1953514584,
            "bytes_per_sector": 512,
            "capacity_bytes": 1000204886016,
            "capacity_gb": 931.51
        },
        "SEAGATE_ST1000DM003": {
            "cylinders": 65535,
            "heads": 255,
            "sectors_per_track": 63,
            "total_sectors": 1953514584,
            "bytes_per_sector": 512,
            "capacity_bytes": 1000204886016,
            "capacity_gb": 931.51
        }
    }
    
    # For demonstration purposes, we'll simulate loading data
    generator.geometry_data = sample_data
    
    # Generate report for specific disk models
    disk_models = ["WD_BLACK_1TB", "SEAGATE_ST1000DM003"]
    report = generator.generate_report(disk_models)
    
    # Integrate with storage system
    integrated_report = generator.integrate_with_storage_system(report)
    
    # Print results
    print(json.dumps(integrated_report, indent=2))

if __name__ == "__main__":
    main()