# Msg: Terminal Messaging Module

This Python `Msg` class handle printing of simple, coloured, and formatted messages to the terminal.  Features include automatic terminal size detection, global message prefix, custom formatting, colour and style control, and optional text wrapping.

## Features

- **Automatic Terminal Size Detection:** Adjusts to the current terminal's size.
- **Global Message Prefix:** Prefixes can be added, removed, and manipulated.
- **Message Types:** Standard, info, warning, and error messages with custom formatting.
- **Colour and Style Control:** Customisable foreground, background, and styles.
- **Text Wrapping:** Optional text wrapping based on terminal width.

## Installation

The class requires the `colorama` package for colour handling. 

\`\`\`bash
pip install colorama
\`\`\`

## Usage

Import the `Msg` class and create an instance to begin printing messages:

\`\`\`python
from msg import Msg
m = Msg()
m.info('This is an info message.')
m.set_columns(40) # reset columns to 40
m.enable_color(True)
m.warn('This is a warning message.')
m.line()
\`\`\`

## Methods

### `set_columns(newcolumns: int)`

Sets the number of screen columns for the terminal.

### `set_rows(newrows: int)`

Sets the number of rows for the terminal screen.

### `enable_color(color_enable: bool)`

Sets whether to print messages in colour.

### `msg, info, warn, error`

Print messages of different types.

### `line`

Print lines.

## Examples

See the examples provided at the end of the `msg.py` file to explore various ways to use the `Msg` class.

For more detailed examples and comprehensive method documentation, please refer to the docstrings within the `msg.py` file.

The `unittests` subdirectory contains `msg-test.py` for testing and validation.

## Notes

- Colours can also be set using abbreviations (see `set_colors()` method in the code).
- Ensure you have the required dependencies installed.

## License

This project is released under the GPL 3 License. See the LICENSE file for more details.

## Contributing

Feel free to submit pull requests or open issues to improve the modules in this package.

https://github.com/Open-Technology-Foundation/msg.git
