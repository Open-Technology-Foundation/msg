#!/usr/bin/python
import sys
import colorama
from shutil import get_terminal_size
import textwrap as tw

class Msg:
  """
  Print simple, coloured, formatted messages to the terminal.
  Features include automatic terminal size detection, global 
  message prefix, and functions to print standard, info, 
  warning, and error messages.

  Example usage: 
  ```
  import msg
  m = msg()

  m.msg('Hello World (to stdout)')
  m.prefix_set('myprog')
  m.msg('This is msg.msg(), with a prefix "myprog" (to stdout)')
  m.error("This is msg.error() (to stderr)")
  m.warn('This is msg.warn() (to stderr)')
  m.info('This is msg.info() (to stdout)')
  m.warn('This is a multi-line msg.warn() message.', 
      'This is the next line.', 
      '... and so on ...',
      '(to stderr)')
  
  m.prefix_add('color') # set a double level prefix
  m.info(f"Double prefix '{m.prefix}', from msg.info() (to stdout)")
  m.msg(f'msg.msg() with prefix "{m.prefix}"')
  m.msg('Making new default colours for msg.info() and msg.warn()')
  m.set_colors(info_fore='RED', info_style='BRIGHT', 
      warn_fore='RED', warn_back='WHITE', warn_style='BRIGHT')
  m.info('This is msg.info()', 'with new default colours.')
  m.warn('This is msg.warn()', 'with new default colours.')
  m.prefix_set('')
  m.msg('', 'Now back to msg.msg() without prefixes.', '')
  ```
  """
  def __init__(self):
    """
    Initialises the msg object, setting default terminal size, 
    colour usage and message prefix.
    """
    # Query the terminal size
    self.columns, self.rows = get_terminal_size()
    # Determine if the terminal supports colour
    self.use_color = self.is_terminal(sys.stdout)
    # global textwrap flag
    self.use_textwrap = True
    # Initialise default message prefix and separator
    self.prefixes = []
    self.prefix_separator = ': '
    # Initialise default colours
    self.msg_fore     = colorama.Fore.WHITE
    self.msg_back     = colorama.Back.BLACK
    self.msg_style    = colorama.Style.NORMAL
    self.info_fore    = colorama.Fore.GREEN
    self.info_back    = colorama.Back.BLACK
    self.info_style   = colorama.Style.DIM
    self.warn_fore    = colorama.Fore.YELLOW
    self.warn_back    = colorama.Back.BLACK
    self.warn_style   = colorama.Style.NORMAL
    self.error_fore   = colorama.Fore.RED
    self.error_back   = colorama.Back.BLACK
    self.error_style  = colorama.Style.BRIGHT

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
    if back is None:
      back = self.msg_back
    if fore is None:
      fore = self.msg_fore
    if style is None:
      style = self.msg_style
    if wrap is None:
      wrap = self.use_textwrap
    if file is None:
      file = sys.stdout
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
#          sep, end=end, file=file)
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


if __name__ == '__main__':
  # for testing only
  #import msg
  m = Msg()
  m.enable_color(True) # only required if you want coloured output to file
  m.prefix_set('myprog') # make a prefix for following msg's 
  m.info('Hello World (to stdout)')
  m.msg('This is m.msg(), with a prefix "myprog" (to stdout)')
  m.info('This is m.info() (to stdout)')
  m.warn('This is m.warn() (to stderr)')
  m.error("This is m.error() (to stderr)", '\n')
  m.warn('This is a multi-line m.warn() message.', 
      'This is the next line.', '(to stderr)')
  m.prefix_add('color') # set a double level prefix
  m.info(f"Double prefix '{m.prefixes}', from m.info() (to stdout)")
  m.msg(f"m.msg() with prefix '{m.prefixes}'")

  m.msg('Make new default colours for m.info() and m.warn()')
  m.set_colors(info_fore='LIGHTBLUE_EX', info_style='BRIGHT', 
      warn_fore='RED', warn_back='WHITE', warn_style='BRIGHT')
  m.info('This is m.info()', 'with new default colours.')
  m.warn('This is m.warn()', 'with new default colours.')
  m.prefix_set('')
  m.msg('', 'Now back to m.msg() without prefixes.', '')

  m.prefix_set('colors')
  m.msg('Display all available foreground colours for m.info() with black background colour.')
  all_colors = [
      'BLACK','RED','GREEN','YELLOW','BLUE','MAGENTA','CYAN','WHITE',
      'LIGHTBLACK_EX', 'LIGHTRED_EX','LIGHTGREEN_EX','LIGHTYELLOW_EX',
      'LIGHTBLUE_EX', 'LIGHTMAGENTA_EX','LIGHTCYAN_EX','LIGHTWHITE_EX'
    ]
  all_styles = [ 'NORMAL', 'BRIGHT', 'DIM' ]
  for color in all_colors:
    if color == 'BLACK': continue   # don't need black on black
    m.prefix_add(color)
    m.set_colors(info_fore=color, info_back='black')
    m.msg('-' * 40)
    for style in all_styles:
      m.prefix_add(style)
      m.set_colors(info_style=style)
      m.info('Hello World.')
      m.prefix_pop()
    m.prefix_pop()
  print('\n\n')

  m = Msg()
  m.enable_color(True) # only required if you want coloured output to file
  m.prefix_set('textwrap')

  m.prefix_add(f'default {m.columns} cols')
  m.warn('This is a very, very, very long line that needs to be wrapped. Or else it will look like crap.', '')
  m.prefix_pop()

  m.prefix_add('60 cols')
  m.set_columns(60)
  m.warn('This is a very, very, very long line that needs to be wrapped. Or else it will look like crap.  Note that wrapping cols includes the length of the current prefixes.', '')
  m.prefix_pop()

  m.prefix_add('disabled')
  m.enable_textwrap(False)
  m.warn("This is a very, very, very long line that doesn't want to be wrapped. Even if it will look like crap.")
  m.prefix_pop()

