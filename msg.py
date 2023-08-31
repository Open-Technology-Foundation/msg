#!/usr/bin/env python
"""
  Module msg
  Class Msg

  A class to handle printing of simple, coloured, formatted 
  messages to the terminal.
  
  Features include automatic terminal size detection, global 
  message prefix, and functions to print standard, info, 
  warning, and error messages.

  Features:
  - Automatic terminal size detection: Adjusts to the current 
    terminal's size.
  - Global message prefix: Prefixes can be added, removed, and 
    manipulated.
  - Message types: Standard, info, warning, and error messages 
    with custom formatting.
  - Colour and style control: Customisable foreground, 
    background, and styles.
  - Text wrapping: Optional text wrapping based on terminal 
    width.

  For unittests see `unittests/msg-test.py`.

"""
__version__ = '0.8.2'
import sys
import colorama
from shutil import get_terminal_size
import textwrap as tw

class Msg:
  """
  Attributes:
    columns (int): Terminal column size, auto-detected or set 
        manually.
    rows (int): Terminal row size, auto-detected or set 
        manually.
    use_color (bool): Enable or disable colour in messages.
    use_textwrap (bool): Enable or disable text wrapping.
    prefixes (list): List of global prefixes for messages.
    prefix_separator (str): Separator used between prefixes.
    msg_fore, msg_back, msg_style (str): Standard message 
        colours and style.
    info_fore, info_back, info_style (str): Info message 
        colours and style.
    warn_fore, warn_back, warn_style (str): Warning message 
        colours and style.
    error_fore, error_back, error_style (str): Error message 
        colours and style.

  Methods:
    set_columns(newcolumns: int): Set terminal column size.
    set_rows(newrows: int): Set terminal row size.
    enable_color(color_enable: bool): Enable/disable colour.
    msg, info, warn, error: Print messages of different types.
    line: Print lines.

  Example Usage:
    
    ```
    from msg import Msg
    m = Msg()
    m.info('This is an info message.')
    m.set_columns(40) # reset columns to 40
    m.enable_color(True)
    m.warn('This is a warning message.')
    m.line()
    ```

  Dependencies:
    The class requires the `colorama` package for colour 
    handling.  Colours can also be set using abbreviations
    (see `set_colors()`).
    
    The class also requires module `sys`, `shutil`, and `textwrap`. 

  """
  def __init__(self, columns:int=None, rows:int=None, use_color:bool=None,
      use_textwrap:bool=True, prefixes:list=[], prefix_separator:str=': ',
      msg_fore:str=colorama.Fore.WHITE,   msg_back:str=colorama.Back.BLACK,   msg_style:str=colorama.Style.NORMAL,
      info_fore:str=colorama.Fore.GREEN,  info_back:str=colorama.Back.BLACK,  info_style:str=colorama.Style.DIM,
      warn_fore:str=colorama.Fore.YELLOW, warn_back:str=colorama.Back.BLACK,  warn_style:str=colorama.Style.NORMAL,
      error_fore:str=colorama.Fore.RED,   error_back:str=colorama.Back.BLACK, error_style:str=colorama.Style.BRIGHT):

    """
    Initialises the msg object, setting default terminal size, 
    colour usage and message prefix.
    """
    self.version = __version__
    if not columns:
      # Query the terminal columns size
      self.columns, _ = get_terminal_size()
    else:
      self.columns = columns
    if not rows:
      # Query the terminal rows size
      _, self.rows = get_terminal_size()
    else:
      self.rows = rows
    if use_color is None:
      # Determine if the terminal supports colour
      self.use_color = self.is_terminal(sys.stdout)
    else:
      self.use_color = use_color
    # global textwrap flag
    self.use_textwrap     = use_textwrap
    # Initialise default message prefix and separator
    self.prefixes         = prefixes.copy() # Using copy() to avoid mutable default argument
    self.prefix_separator = prefix_separator
    # Initialise colours.
    self.msg_fore         = msg_fore
    self.msg_back         = msg_back
    self.msg_style        = msg_style
    self.info_fore        = info_fore
    self.info_back        = info_back
    self.info_style       = info_style
    self.warn_fore        = warn_fore
    self.warn_back        = warn_back
    self.warn_style       = warn_style
    self.error_fore       = error_fore
    self.error_back       = error_back
    self.error_style      = error_style

  def is_terminal(self, stream) -> bool:
    """
    Checks if a terminal is available for a given stream.
    Args:
      stream: The stream to check for terminal availability.
    Returns:
      bool: True if a terminal is available, False otherwise.
    """
    if not hasattr(stream, 'isatty'): return False
    if not stream.isatty(): return False
    return True

  def set_columns(self, newcolumns: int) -> int:
    """ 
    Sets the number of screen columns for the terminal.
    Args:
      newcolumns: The new column size for the terminal.
    Returns:
      int: The current column size.
    Raises:
      ValueError: If the newcolumns value is not a positive integer.
    Example:
      m.set_columns(80)
    """
    if not isinstance(newcolumns, int) or newcolumns <= 0:
      raise ValueError('newcolumns must be a positive integer.')
    self.columns = newcolumns
    return self.columns

  def set_rows(self, newrows: int) -> int:
    """ 
    Sets the number of rows for the terminal screen.
    Args:
      newrows: The new row size for the terminal.
    Returns:
      int: The current row size.
    Raises:
      ValueError: If the newrows value is not a positive integer.
    Example:
      m.set_rows(40)
    """
    if not isinstance(newrows, int) or newrows <= 0:
      raise ValueError('newrows must be a positive integer.')
    self.rows = newrows
    return self.rows

  def enable_color(self, color_enable: bool = None) -> bool:
    """
    Sets whether to print messages in colour.
    Args:
      use_color: The flag to turn on/off the colour for the print 
      messages.
      Defaults to None. If None, uses 'is_terminal(sys.stdout)' to 
      determine whether to use colour.
    Returns:
      bool: The current state of use of colour.
    Raises:
      ValueError: If the use_color flag is not a boolean.
    Example:
      m.enable_color(True)
    """
    if color_enable is None:
      self.use_color = is_terminal(sys.stdout)
    else:
      self.use_color = color_enable
    # Reset colour only if turning off or turning on colour
    if self.use_color:
       print(colorama.Style.RESET_ALL, end='')
    # Initialize/De-initialise colour using the current state
    colorama.init() if self.use_color else colorama.deinit()
    return self.use_color

  def enable_textwrap(self, textwrap_enable: bool = None) -> bool:
    """
    Sets whether to enable textwrapping.
    Args:
      textwrap_enable: The flag to turn on/off textwrapping.
      Defaults to None. If None, simply returns current state
      of self.textwrap_enable.
    Returns:
      bool: self.textwrap_enable
    Example:
      m.enable_textwrap(False)
    """
    if textwrap_enable is None:
      return self.use_textwrap
    self.use_textwrap = textwrap_enable
    return self.use_textwrap

  def set_colors(self, **kwargs):
    """
    Sets custom 'colorama' colours for standard, info, warning, and 
    error messages.
    Each type accepts a Foreground color, Background color and Style 
    attribute.
    Default msg* colours are as follows:
      msg_fore=colorama.Fore.WHITE
      msg_back=colorama.Back.BLACK
      msg_style=colorama.Style.NORMAL
      info_fore=colorama.Fore.BLUE
      info_back=colorama.Back.BLACK
      info_style=colorama.Style.NORMAL
      warn_fore=colorama.Fore.YELLOW
      warn_back=colorama.Back.BLACK
      warn_style=colorama.Style.NORMAL
      error_fore=colorama.Fore.RED
      error_back=colorama.Back.BLACK
      error_style=colorama.Style.BRIGHT
    Args:
      msg_fore, msg_back, msg_style: 
          Colours for standard messages.
      info_fore, info_back, info_style: 
          Colours for information messages.
      warn_fore, warn_back, warn_style: 
          Colours for warning messages.
      error_fore, error_back, error_style: 
          Colours for error messages.
    'Fore' and 'Back' can use these abbreviations instead of 
    colorama ansi strings. 
      BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE 
      LIGHTBLACK_EX LIGHTRED_EX LIGHTGREEN_EX LIGHTYELLOW_EX 
      LIGHTBLUE_EX LIGHTMAGENTA_EX LIGHTCYAN_EX LIGHTWHITE_EX 
      RESET 
    'Style' can use these abbreviations instead of colorama 
    ansi strings:
      DIM NORMAL BRIGHT RESET_ALL
    Raises:
      ValueError: If arguments are not valid colorama values.
    Example:
      # example using simplified colour-name values:
      m.set_colors(
          info_fore='LIGHTBLUE_EX', 
          info_back='WHITE', 
          warn_fore='YELLOW'
          warn_style='BRIGHT'
        )
      # example using colorama ansi values:
      m.set_colors(
          info_fore=colorama.Fore.LIGHTBLUE_EX, 
          info_back=colorama.Back.WHITE, 
          warn_fore=colorama.Fore.YELLOW
          warn_style=colorama.Style.BRIGHT
        )
    """
    for key, value in kwargs.items():
      if hasattr(self, key):
        setattr(self, key, self._get_color_code(value, 
            colorama.Fore if key.endswith('_fore') 
            else colorama.Back if key.endswith('_back') 
            else colorama.Style))
      else:
        raise ValueError(f'Invalid argument: {key}')

  def _get_color_code(self, color, color_type):
    # If it's already an ansi code, then let it go.
    try:
      return getattr(color_type, color.upper())
    except AttributeError:
      return color
    else:
      return color  # Assume it's already an ANSI code.

  def prefix_set(self, newprefix:str) -> list:
    """
    Sets/Resets message prefixes.
    Args:
      newprefix: The new message prefix.
    Returns:
      list: Current prefixes.
    Raises:
      ValueError: If the newprefix is not a string.
    See Also:
      prefix_add(), prefix_pop()
    Example:
      m.prefix_set('myprog')
    """
    if not isinstance(newprefix, str):
      raise ValueError('Prefix must be a string.')
    self.prefixes = [ newprefix.strip() ]
    return self.prefixes

  def prefix_add(self, addprefix:str) -> list:
    """
    Adds element to global message prefixes.
    Args:
      newprefix: The new message prefix at add.
    Returns:
      list: Current prefixes.
    Raises:
      ValueError: If the addprefix is not a string.
    See Also:
      prefix_set(), prefix_pop()
    Example:
      m.prefix_add('myprocess')
    """
    if not isinstance(addprefix, str):
      raise ValueError('Added Prefix must be a string.')
    self.prefixes.append(addprefix.strip())
    return self.prefixes

  def prefix_pop(self) -> list:
    """
    Remove last element from global message prefixes list.
    Returns:
      list: Current prefixes.
    See Also:
      prefix_set(), prefix_add()
    Example:
      m.prefix_set('myprog')
      m.prefix_add('myprocess')
      ...
      # remove last prefix from prefixes list.
      prefs:list = m.prefix_pop()
      m.msg(prefs)
    """
    if len(self.prefixes): self.prefixes.pop()
    return self.prefixes

  def print_msg(self, *args: any, back=None, fore=None, style=None, wrap=None, file=None, msg_type='', sep='\n', end='') -> None:
    """
    Prints a message to the terminal with optional formatting.
    This is a wrapper function is used by the `msg*` functions.
    For most purposes, use the msg* functions for printing.
    Args:
      *args: The print message arguments.
      back, fore, style: colorama formatting options.
      wrap: Enable/Disable textwrapping.
      file: The file to print to. Defaults to sys.stdout.
      msg_type: Type of message. 
      sep: Separator for print function.
      end: Ending character for print function.
    Raises:
      ValueError: If kwargs contains keys not allowed.
    Example:
      m.print_msg('Hello', 'World', sep=' ', end='!', fore=colorama.Fore.RED)
    """
    # Set defaults if no values were provided
    if back  is None: back  = self.msg_back
    if fore  is None: fore  = self.msg_fore
    if style is None: style = self.msg_style
    if wrap  is None: wrap  = self.use_textwrap
    if file  is None: file  = sys.stdout
    ppref = self.prefix_separator.join(self.prefixes).strip()
    if msg_type:
      if ppref: ppref += self.prefix_separator
      ppref += msg_type
    if ppref: ppref += self.prefix_separator
    if self.use_color:
      print(f'{back}{fore}{style}', sep='', end='', file=file)
    textwrap_cols:int = 65534 if not wrap else self.columns
    for line in args:
      print(tw.fill(line, textwrap_cols, 
                    initial_indent=ppref, 
                    subsequent_indent=ppref,
                    fix_sentence_endings=True),
          file=file)
    if self.use_color:
      print(colorama.Style.RESET_ALL, sep='', end='', file=file)

  def msg(self, *args: any, sep='\n', end='', file=sys.stdout) -> None:
    """
    Prints a message to stdout, with optional additional formatting.
    Args:
      *args: The print message arguments.
    Example:
      m.msg('this is a standard message.')
    """
    self.print_msg(*args, fore=self.msg_fore, back=self.msg_back, 
        style=self.msg_style, sep=sep, end=end, file=file)

  def info(self, *args: any, sep='\n', end='', file=sys.stdout) -> None:
    """
    Prints an info message to stdout, with optional additional 
    formatting. 
    Args:
      *args: The print message arguments.
    Example:
      m.info('this is an info message.')
    """
    self.print_msg(*args, fore=self.info_fore, back=self.info_back, 
        style=self.info_style, sep=sep, end=end, file=file, msg_type='info')

  def warn(self, *args: any, sep='\n', end='', file=sys.stderr) -> None:
    """
    Prints a warning message to stderr, with optional additional 
    formatting.
    Args:
      *args: The print message arguments.
    Example:
      m.warn('this is a warning.')
    """
    self.print_msg(*args, fore=self.warn_fore, back=self.warn_back, 
        style=self.warn_style, sep=sep, end=end, file=file, msg_type='warn')

  def error(self, *args: any, sep='\n', end='', file=sys.stderr) -> None:
    """
    Prints an error message to stderr, with optional additional 
    formatting.
    Args:
      *args: The print message arguments.
    Example:
      m.error('this is an error.')
    """
    self.print_msg(*args, fore=self.error_fore, back=self.error_back, 
        style=self.error_style, sep=sep, end=end, file=file, msg_type='error')

  def line(self, cols:int=None, char:str='-', sep='\n', end='', file=sys.stdout) -> None:
    """
    Prints a `cols` number of 'char'.
    Args:
      cols: Number of columns; default is current screen columns. 
      char: Character to repeat; default is -.
    Example:
      m.line(char='_')
    """
    if cols is None: cols = self.columns
    ppref_len = len(self.prefix_separator.join(self.prefixes).strip())
    if ppref_len:
      ppref_len += len(self.prefix_separator)
      cols = cols - ppref_len
      if cols < 1: cols = 0
    self.print_msg(char * cols, fore=self.msg_fore, back=self.msg_back, 
        style=self.msg_style, sep=sep, end=end, file=file, msg_type='')

#fin
