
import argparse

parser = argparse.ArgumentParser(description='Generate and serve synthetic Datadog data')
parser.add_argument('--data_type', type=str, help='Type of data to generate')
parser.add_argument('--volume', type=int, help='Volume of data to generate')
parser.add_argument('--output_format', type=str, help='Output format of the generated data')

args = parser.parse_args()

print(f'Data type: {args.data_type}')
print(f'Volume: {args.volume}')
print(f'Output format: {args.output_format}')