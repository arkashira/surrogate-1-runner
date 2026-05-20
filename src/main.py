import argparse
from sop_creator import SOPCreator

def main():
    parser = argparse.ArgumentParser(description='Create and sync SOPs.')
    parser.add_argument('--template', type=str, required=True, help='Template name')
    parser.add_argument('--variables', type=str, required=True, help='Variables in JSON format')
    parser.add_argument('--sync_to', type=str, choices=['slack', 'github', 'notion'], help='Sync to a specific tool')
    parser.add_argument('--channel', type=str, help='Slack channel')
    parser.add_argument('--repo', type=str, help='GitHub repository')
    parser.add_argument('--branch', type=str, help='GitHub branch')
    parser.add_argument('--page_id', type=str, help='Notion page ID')

    args = parser.parse_args()

    sop_creator = SOPCreator('templates', 'output')

    variables = eval(args.variables)
    output_path = sop_creator.create_sop(args.template, variables)

    if args.sync_to == 'slack' and args.channel:
        sop_creator.sync_to_slack(output_path, args.channel)
    elif args.sync_to == 'github' and args.repo and args.branch:
        sop_creator.sync_to_github(output_path, args.repo, args.branch)
    elif args.sync_to == 'notion' and args.page_id:
        sop_creator.sync_to_notion(output_path, args.page_id)

if __name__ == '__main__':
    main()