# msg - Message Printing Module

The `msg` module provides a simple and convenient way to print coloured, formatted messages to the terminal. It supports automatic terminal size detection, global message prefixing, and offers functions to print standard, info, warning, and error messages with customization.

## Features

- **Automatic Terminal Size Detection**: Automatically detects the terminal's columns and rows.
- **Global Message Prefix**: Allows setting a global prefix for all messages.
- **Customizable Colours**: Set custom colours for different types of messages.
- **Message Types**: Print standard, info, warning, and error messages with custom formatting.

## Installation

Ensure that the `colorama` package is installed, as it is a required dependency.

```bash
pip install colorama
```

Then, download the `msg.py` file and import it into your project.

## Usage

Here's a quick example of how to use the `msg` module:

```python
from msg import msg

m = msg()
m.msg('Hello World, to stdout.')
m.set_prefix('myprog')
m.error("This is an error message, to stderr")
m.warn('This is a warning, to stderr')
m.info('This is info, to stdout')
```

## Methods Overview

### Initialization

- `__init__`: Initializes the `msg` object, setting default terminal size, colour usage, and message prefix.

### Terminal Configuration

- `set_columns`: Sets the number of screen columns for the terminal.
- `set_rows`: Sets the number of rows for the terminal screen.
- `set_color`: Sets whether to print messages in colour.

### Message Customization

- `set_msg_colors`: Sets custom colours for standard, info, warning, and error messages.
- `set_prefix`: Sets the global prefix for messages.

### Message Printing

- `msg`: Prints a standard message to stdout.
- `info`: Prints an info message to stdout.
- `warn`: Prints a warning message to stderr.
- `error`: Prints an error message to stderr.

## Examples and Documentation

For more detailed examples and comprehensive method documentation, please refer to the docstrings within the `msg.py` file.

## Contributing

If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is released under the GPL 3 License. See the LICENSE file for more details.
