# dbtfetch

A neofetch-style system information tool for dbt projects.

```
.:===-..                .:===-.       my_dbt_project@dbt
.========-..          .:========:     ------------------
:===========-.     .-============.    Project: my_dbt_project
.:=============-:. .-===========.     Version: 1.0.0
 .:================..=========-.      Profile: my_profile
  .:==========================.       dbt Version: 1.6.0
    :=======================-         
    .:=====================-.         Models: 45
      =========. .-========.          Tests: 23
     .=========:..-========.          Macros: 8
    .:======================.         Snapshots: 2
    :========================.        Seeds: 3
  .-==========================.       Packages: 5
 .-=========:..================.      
.-===========:. .:-=============.     SQL Lines: 3,247
:===========:.     ..============.    
.-=======:.           ..-=======.     Git Branch: main
 ..-==..                  .:=-..      Last Commit: 2 days ago
```

## Features

- 🎨 Beautiful ASCII art display of your dbt project statistics
- 📊 Project metrics including models, tests, macros, snapshots, and seeds
- 📦 Package dependency counting
- 🔢 Total SQL lines of code
- 🌿 Git branch and last commit information
- 🎯 Automatic project detection (searches current and parent directories)
- 🛠️ Support for custom project directory paths

## Installation

### Using pipx (recommended)

```bash
pipx install dbtfetch
```

### Using pip

```bash
pip install dbtfetch
```

## Usage

### Analyze current directory

```bash
dbtfetch
```

### Analyze a specific dbt project

```bash
dbtfetch /path/to/your/dbt/project
```

### Show help

```bash
dbtfetch --help
```

## Example Output

```
.:===-..                .:===-.       my_dbt_project@dbt
.========-..          .:========:     ------------------
:===========-.     .-============.    Project: my_dbt_project
.:=============-:. .-===========.     Version: 1.0.0
 .:================..=========-.      Profile: my_profile
  .:==========================.       dbt Version: 1.6.0
    :=======================-         
    .:=====================-.         Models: 45
      =========. .-========.          Tests: 23
     .=========:..-========.          Macros: 8
    .:======================.         Snapshots: 2
    :========================.        Seeds: 3
  .-==========================.       Packages: 5
 .-=========:..================.      
.-===========:. .:-=============.     SQL Lines: 3,247
:===========:.     ..============.    
.-=======:.           ..-=======.     Git Branch: main
 ..-==..                  .:=-..      Last Commit: 2 days ago
```

## Requirements

- Python 3.8 or higher
- PyYAML
- dbt installed (optional, for version detection)
- Git (optional, for repository information)

## Development

### Clone the repository

```bash
git clone https://github.com/yourusername/dbtfetch.git
cd dbtfetch
```

### Install in development mode

```bash
pip install -e .
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Your Name - [your.email@example.com](mailto:your.email@example.com)

## Acknowledgments

- Inspired by [neofetch](https://github.com/dylanaraps/neofetch)
- Built for the [dbt](https://www.getdbt.com/) community