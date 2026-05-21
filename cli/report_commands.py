import click
from typing import List
from surrogate1.reporting.exporter import CoverageData, ReportExporter

@click.group()
def report_commands():
    """Commands for generating and exporting coverage reports."""
    pass

@report_commands.command()
@click.argument('output_format', type=click.Choice(['html', 'json', 'csv']))
@click.argument('output_path')
@click.option('--coverage-data', multiple=True, help='Coverage data in JSON format')
def export_report(output_format: str, output_path: str, coverage_data: List[str]):
    """Export coverage report in specified format."""
    parsed_data = []
    for data in coverage_data:
        import json
        parsed_data.append(CoverageData(**json.loads(data)))

    exporter = ReportExporter(parsed_data)
    if output_format == 'html':
        exporter.export_to_html(output_path)
    elif output_format == 'json':
        exporter.export_to_json(output_path)
    elif output_format == 'csv':
        exporter.export_to_csv(output_path)

    click.echo(f"Report exported to {output_path} in {output_format} format.")

if __name__ == '__main__':
    report_commands()