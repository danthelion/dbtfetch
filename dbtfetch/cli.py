#!/usr/bin/env python3
"""
dbtfetch - A neofetch-style system information tool for dbt projects

This tool displays project statistics and information for dbt projects
in a visually appealing format similar to neofetch. It can analyze the current directory
or a specified dbt project directory.

Usage:
    dbtfetch [PROJECT_DIR]

Arguments:
    PROJECT_DIR    Optional path to dbt project directory (default: current directory)

Examples:
    dbtfetch                    # Analyze current directory
    dbtfetch /path/to/project   # Analyze specific project
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import yaml


# ASCII art for dbt logo
DBT_LOGO = """
.:===-..                .:===-.
.========-..          .:========:
:===========-.     .-============.
.:=============-:. .-===========.
 .:================..=========-.
  .:==========================.
    :=======================-
    .:=====================-.
      =========. .-========.
     .=========:..-========.
    .:======================.
    :========================.
  .-==========================.
 .-=========:..================.
.-===========:. .:-=============.
:===========:.     ..============.
.-=======:.           ..-=======.
 ..-==..                  .:=-..
"""

# ANSI color codes for terminal output
COLORS = {
    'reset': '\033[0m',
    'orange': '\033[38;5;208m',
    'blue': '\033[38;5;33m',
    'green': '\033[38;5;76m',
    'yellow': '\033[38;5;226m',
    'red': '\033[38;5;196m',
    'gray': '\033[38;5;244m',
    'bold': '\033[1m',
}


def colorize(text: str, color: str) -> str:
    """
    Apply ANSI color codes to text.

    Args:
        text: The text to colorize
        color: Color name from COLORS dictionary

    Returns:
        Colorized text string with reset code appended
    """
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"


def find_dbt_project(start_path: Optional[Path] = None) -> Tuple[Optional[Path], Optional[Path]]:
    """
    Find dbt_project.yml in the specified directory or parent directories.

    Args:
        start_path: Starting directory to search from (default: current working directory)

    Returns:
        Tuple of (project_root_path, dbt_project_yml_path) or (None, None) if not found
    """
    current = start_path or Path.cwd()
    
    # Ensure we're working with an absolute path
    current = current.resolve()
    
    # Search in current directory and all parent directories
    for parent in [current] + list(current.parents):
        dbt_project = parent / 'dbt_project.yml'
        if dbt_project.exists():
            return parent, dbt_project
    
    return None, None


def load_yaml(file_path: Path) -> Optional[Dict]:
    """
    Safely load YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed YAML content as dictionary, or None if loading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except (yaml.YAMLError, IOError, OSError) as e:
        print(f"Warning: Failed to load {file_path}: {e}", file=sys.stderr)
        return None


def count_files(directory: Path, extension: str) -> int:
    """
    Count files with specific extension in directory and subdirectories.

    Args:
        directory: Directory to search in
        extension: File extension to count (without dot)

    Returns:
        Number of files with the specified extension
    """
    if not directory.exists():
        return 0
    return len(list(directory.rglob(f'*.{extension}')))


def count_sql_lines(directory: Path) -> int:
    """
    Count total lines of SQL code in directory and subdirectories.

    Args:
        directory: Directory to search for SQL files

    Returns:
        Total number of lines across all SQL files
    """
    if not directory.exists():
        return 0
    
    total_lines = 0
    for sql_file in directory.rglob('*.sql'):
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                total_lines += sum(1 for _ in f)
        except (IOError, OSError):
            # Skip files that can't be read
            continue
    
    return total_lines


def get_git_info(project_root: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Get git branch and last commit information.

    Args:
        project_root: Root directory of the project

    Returns:
        Tuple of (branch_name, last_commit_time) or (None, None) if not a git repository
    """
    try:
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=project_root,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        
        last_commit = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cr'],
            cwd=project_root,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        
        return branch, last_commit
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, None


def get_dbt_version() -> str:
    """
    Get installed dbt version.

    Returns:
        dbt version string or "Not installed" if dbt is not available
    """
    try:
        result = subprocess.check_output(
            ['dbt', '--version'],
            stderr=subprocess.DEVNULL,
            text=True
        )
        
        # Parse the Core version line
        for line in result.split('\n'):
            if 'Core:' in line or 'core:' in line:
                return line.split(':')[1].strip()
        
        # Fallback to first line if Core version not found
        return result.split('\n')[0].strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Not installed"


def get_project_stats(project_root: Path, dbt_config: Dict) -> Dict:
    """
    Gather all project statistics.

    Args:
        project_root: Root directory of the dbt project
        dbt_config: Parsed dbt_project.yml content

    Returns:
        Dictionary containing all project statistics
    """
    stats = {}
    
    # Basic project information
    stats['name'] = dbt_config.get('name', 'Unknown')
    stats['version'] = dbt_config.get('version', '1.0.0')
    stats['profile'] = dbt_config.get('profile', 'Unknown')
    stats['dbt_version'] = get_dbt_version()
    
    # Count models and lines of SQL
    models_dir = project_root / 'models'
    stats['models'] = count_files(models_dir, 'sql')
    stats['sql_lines'] = count_sql_lines(models_dir)
    
    # Count other dbt resources
    stats['tests'] = count_files(project_root / 'tests', 'sql')
    stats['macros'] = count_files(project_root / 'macros', 'sql')
    stats['snapshots'] = count_files(project_root / 'snapshots', 'sql')
    stats['seeds'] = count_files(project_root / 'seeds', 'csv')
    
    # Count packages
    packages_yml = project_root / 'packages.yml'
    if packages_yml.exists():
        packages_data = load_yaml(packages_yml)
        stats['packages'] = len(packages_data.get('packages', [])) if packages_data else 0
    else:
        stats['packages'] = 0
    
    # Get git information
    branch, last_commit = get_git_info(project_root)
    stats['git_branch'] = branch
    stats['last_commit'] = last_commit
    
    # Target database configuration
    stats['target'] = dbt_config.get('target-path', 'target')
    
    return stats


def format_info_line(label: str, value: str, label_color: str = 'orange', 
                    value_color: str = 'reset') -> str:
    """
    Format an information line with colors.

    Args:
        label: The label text
        value: The value text
        label_color: Color for the label
        value_color: Color for the value

    Returns:
        Formatted colored string
    """
    return f"{colorize(label + ':', label_color)} {colorize(str(value), value_color)}"


def print_dbtfetch(stats: Dict) -> None:
    """
    Print the neofetch-style output.

    Args:
        stats: Dictionary containing project statistics
    """
    # Add blank lines before output
    print("\n")
    
    # Split logo into lines
    logo_lines = DBT_LOGO.strip().split('\n')
    
    # Prepare information lines
    # Calculate proper separator length based on visible characters (not ANSI codes)
    separator_length = len(stats['name']) + len('dbt') + 1  # +1 for the @ symbol
    info_lines = [
        f"{colorize(stats['name'], 'bold')}@{colorize('dbt', 'bold')}",
        colorize('-' * separator_length, 'gray'),
        format_info_line('Project', stats['name'], 'orange', 'reset'),
        format_info_line('Version', stats['version'], 'orange', 'reset'),
        format_info_line('Profile', stats['profile'], 'orange', 'reset'),
        format_info_line('dbt Version', stats['dbt_version'], 'orange', 'blue'),
        '',
        format_info_line('Models', stats['models'], 'green', 'bold'),
        format_info_line('Tests', stats['tests'], 'green', 'bold'),
        format_info_line('Macros', stats['macros'], 'green', 'bold'),
        format_info_line('Snapshots', stats['snapshots'], 'green', 'bold'),
        format_info_line('Seeds', stats['seeds'], 'green', 'bold'),
        format_info_line('Packages', stats['packages'], 'green', 'bold'),
        '',
        format_info_line('SQL Lines', f"{stats['sql_lines']:,}", 'yellow', 'bold'),
    ]
    
    # Add git information if available
    if stats['git_branch']:
        info_lines.extend([
            '',
            format_info_line('Git Branch', stats['git_branch'], 'blue', 'bold'),
        ])
        if stats['last_commit']:
            info_lines.append(
                format_info_line('Last Commit', stats['last_commit'], 'blue', 'reset')
            )
    
    # Print side by side
    max_lines = max(len(logo_lines), len(info_lines))
    
    # Calculate the width of the logo for proper alignment
    logo_width = max(len(line) for line in logo_lines) if logo_lines else 40
    
    for i in range(max_lines):
        if i < len(logo_lines):
            logo = logo_lines[i].ljust(logo_width)
        else:
            logo = ' ' * logo_width
        info = info_lines[i] if i < len(info_lines) else ''
        print(f"{colorize(logo, 'orange')}  {info}")
    
    # Add blank lines after output
    print("\n")


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description='Display dbt project statistics in neofetch style',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Analyze current directory
  %(prog)s /path/to/project   # Analyze specific project
  %(prog)s ~/my-dbt-project   # Analyze project in home directory
        """
    )
    
    parser.add_argument(
        'project_dir',
        nargs='?',
        default='.',
        type=str,
        help='Path to dbt project directory (default: current directory)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_args()
    
    # Resolve the project directory
    project_path = Path(args.project_dir).resolve()
    
    # Check if directory exists
    if not project_path.exists():
        print(f"Error: Directory '{project_path}' does not exist", file=sys.stderr)
        return 1
    
    if not project_path.is_dir():
        print(f"Error: '{project_path}' is not a directory", file=sys.stderr)
        return 1
    
    # Find dbt project
    project_root, dbt_project_yml = find_dbt_project(project_path)
    
    if not project_root:
        print(
            f"Error: No dbt_project.yml found in '{project_path}' or parent directories",
            file=sys.stderr
        )
        print("This doesn't appear to be a dbt project.", file=sys.stderr)
        return 1
    
    # Load dbt configuration
    dbt_config = load_yaml(dbt_project_yml)
    
    if not dbt_config:
        print(f"Error: Failed to load {dbt_project_yml}", file=sys.stderr)
        return 1
    
    # Gather statistics and display
    stats = get_project_stats(project_root, dbt_config)
    print_dbtfetch(stats)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())