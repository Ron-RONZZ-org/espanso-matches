#!/usr/bin/env python3
"""Sort espanso match files by trigger alphabetically."""

import argparse
import os
import sys
import re

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


def natural_sort_key(s):
    """Sort key that handles numbers in strings."""
    parts = re.split(r'([0-9]+)', s)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def sort_matches(matches, reverse=False):
    """Sort matches by trigger alphabetically."""
    if not matches:
        return matches
    
    # Sort by trigger
    return sorted(matches, key=lambda m: natural_sort_key(m.get('trigger', '')), reverse=reverse)


def represent_str(dumper, data):
    """Represent strings with quotes if they contain special chars."""
    if any(c in data for c in [':', '#', "'", '"', '$', '&', '*', '!', '|', '{', '}', '[', ']']):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def process_file(filepath, reverse=False):
    """Process a single YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    if not data or 'matches' not in data:
        print(f"Skipping {filepath}: no 'matches' key found")
        return True
    
    matches = data.get('matches', [])
    if not matches:
        print(f"Skipping {filepath}: empty matches")
        return True
    
    # Sort matches
    data['matches'] = sort_matches(matches, reverse=reverse)
    
    # Custom YAML dump to preserve formatting
    class FlowStyleFalseDumper(yaml.SafeDumper):
        pass
    
    def list_representer(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=False)
    
    FlowStyleFalseDumper.add_representer(list, list_representer)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, Dumper=FlowStyleFalseDumper, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2)
    
    print(f"Sorted: {filepath} ({len(matches)} matches)")
    return True


def main():
    parser = argparse.ArgumentParser(description='Sort espanso match files by trigger')
    parser.add_argument('-i', '--inverse', action='store_true', help='Sort Z to A instead of A to Z')
    parser.add_argument('files', nargs='*', help='YML files to process (default: all .yml in current dir)')
    args = parser.parse_args()
    
    # Get files
    if args.files:
        files = args.files
    else:
        files = [f for f in os.listdir('.') if f.endswith('.yml') and f != 'alphabetic-sort.bash']
    
    if not files:
        print("No yml files found")
        return
    
    for f in files:
        if os.path.isfile(f):
            process_file(f, args.inverse)
    
    print("Done")


if __name__ == '__main__':
    main()
