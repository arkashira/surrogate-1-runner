def parse_diff(diff_output):
    """Parse git diff output to extract changed lines and files."""
    # Placeholder implementation; actual parsing logic will depend on the format of diff_output
    parsed_diff = {}
    current_file = None
    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            current_file = line.split()[-1]
            parsed_diff[current_file] = []
        elif line.startswith('@@'):
            parsed_diff[current_file].append(line)
    return parsed_diff