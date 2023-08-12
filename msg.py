#!/usr/bin/python3.10
import sys
import colorama
from shutil import get_terminal_size

class msg:
  """
  Print simple, coloured, formatted messages to the terminal.
  Features include automatic terminal size detection, global 
  message prefix, and functions to print standard, info, 
  warning, and error messages.


  Example usage:
  m = msg()

  m.msg('Hello World, to stdout.')
  m.set_prefix('myprog')
  m.msg('This is msg.msg(), with a prefix "myprog", to stdout')
  m.error("This is msg.error(), to stderr")
  m.warn('This is msg.warn(), to stderr')
  m.warn('This is a multi-line msg.warn() message.', 
      'This is the next line.', '... and so on ..., to stderr')
  m.info('This is msg.info(), to stdout')
  
  # Make new default colours for msg.info() and msg.WARN()
  m.set_prefix('myprog, colorstalk') # set a double level prefix
  m.info(f"Double prefix '{m.prefix}', from msg.info(), to stdout")
  m.msg(f"msg.msg() with prefix '{m.prefix}'")
  m.set_msg_colors(
      info_fore=colorama.Fore.RED, 
      info_style=colorama.Style.BRIGHT, 
      warn_fore=colorama.Fore.LIGHTBLACK_EX, 
      warn_back=colorama.Back.WHITE
    )
  m.info('This is now msg.info()', 'with new default colours.')
  m.warn('This is now msg.warn()', 'with new default colours.')
  m.set_prefix('')
  m.msg('', 'Now back to msg.msg() without prefixes.', '')

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
    # Initialise message prefix
    self.prefix = ''
    self.prefix_separator = ': '
    self.set_msg_colors()

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

  def set_color(self, use_color: bool = None) -> bool:
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
      m.set_color(True)
    """
    if use_color is None:
      self.use_color = is_terminal(sys.stdout)
    else:
      self.use_color = use_color
    # Reset colour only if turning off or turning on colour
    if self.use_color:
      print(colorama.Style.RESET_ALL, end='')
    # Initialize/De-initialise colour using the current state
    colorama.init() if self.use_color else colorama.deinit()
    return self.use_color

  def set_msg_colors(self, 
    msg_fore=colorama.Fore.WHITE,   msg_back=colorama.Back.BLACK,   msg_style=colorama.Style.NORMAL,
    info_fore=colorama.Fore.BLUE,   info_back=colorama.Back.BLACK,  info_style=colorama.Style.NORMAL,
    warn_fore=colorama.Fore.YELLOW, warn_back=colorama.Back.BLACK,  warn_style=colorama.Style.NORMAL,
    error_fore=colorama.Fore.RED,   error_back=colorama.Back.BLACK, error_style=colorama.Style.BRIGHT
  ):
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
    Valid colorama.Fore and colorama.Back colours are:
      BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE LIGHTBLACK_EX 
      LIGHTRED_EX LIGHTGREEN_EX LIGHTYELLOW_EX LIGHTBLUE_EX 
      LIGHTMAGENTA_EX LIGHTCYAN_EX LIGHTWHITE_EX RESET 
    Valid colorama.style setting are:
      DIM NORMAL BRIGHT RESET_ALL

    Args:
      msg_fore, msg_back, msg_style: 
          Colours for standard messages.
      info_fore, info_back, info_style: 
          Colours for information messages.
      warn_fore, warn_back, warn_style: 
          Colours for warning messages.
      error_fore, error_back, error_style: 
          Colours for error messages.
      
    Raises:
      ValueError: If arguments are not valid colorama values.
      
    Example:
      m.set_msg_colors(
          info_fore=colorama.Fore.GREEN, \
          info_back=colorama.Back.WHITE, \
          warn_fore-colorama.Fore.YELLOW
        )
    """
    self.msg_fore    = msg_fore
    self.msg_back    = msg_back
    self.msg_style   = msg_style
    self.info_fore   = info_fore
    self.info_back   = info_back
    self.info_style  = info_style
    self.warn_fore   = warn_fore
    self.warn_back   = warn_back
    self.warn_style  = warn_style
    self.error_fore  = error_fore
    self.error_back  = error_back
    self.error_style = error_style

  def set_prefix(self, newprefix:str) -> str:
    """
    Sets the message prefix.
    
    Args:
      newprefix: The new message prefix.
      
    Returns:
      str: The current message prefix.
      
    Raises:
      ValueError: If the newprefix is not a string.
      
    Example:
      m.set_prefix('myprog')
    """
    if not isinstance(newprefix, str):
      raise ValueError('Prefix must be a string.')
    self.prefix = newprefix.strip()
    return self.prefix

  def print_message(self, *args: any, **kwargs: any) -> None:
    """
    Prints a message to the terminal with optional formatting.
    This is a wrapper function is used by the `msg*` functions.
    For most purposes, just use the msg* functions for printing.
    
    Args:
      *args: The print message arguments.
      **kwargs: Additional options for the message print. 
      Valid options are 'prefix', 'sep', 'end', 'back', 'fore', 
      'style', and 'file'.
      
    Raises:
      ValueError: If kwargs contains keys not allowed.
      
    Example:
      m.print_message('Hello', 'World', sep=' ', end='!', \
          fore=colorama.Fore.RED)
    """
    kwdefaults = {
      'prefix': '',
      'sep':    '\n',
      'end':    '',
      'back':   self.msg_back,
      'fore':   self.msg_fore,
      'style':  self.msg_style,
      'file':   sys.stdout
    }
    # Update defaults with any custom values provided in kwargs
    kwdefaults.update(kwargs)
    if self.use_color:
      print(kwdefaults['back'] + kwdefaults['fore'] + kwdefaults['style'], sep='', end='', file=kwdefaults['file'])
    prefs = (self.prefix+' '+kwdefaults['prefix']).translate(str.maketrans(',;\n\t', '    ')).split()
    ppref = (self.prefix_separator.join(prefs))
    for arg in args:
      # global prefix
      if ppref:
        print(ppref+self.prefix_separator, end='', file=kwdefaults['file'])
#        print(self.prefix_separator.join(prefs)+self.prefix_separator, end='', file=kwdefaults['file'])
#      if kwdefaults['prefix']: 
#        print(kwdefaults['prefix'] + self.prefix_separator, end='', file=kwdefaults['file'])
      print(arg, kwdefaults['sep'], end='', file=kwdefaults['file'])
    if self.use_color:
      print(colorama.Style.RESET_ALL, sep='', end='', file=kwdefaults['file'])

  def msg(self, *args: any, **kwargs: any) -> None:
    """
    Prints a message to stdout, with optional additional formatting.
    
    Args:
      *args: The print message arguments.
      **kwargs: Additional options for the message print. 
      Valid options are 'prefix', 'sep', 'end', 'back', 'fore', 
      'style', and 'file'.
      
    Example:
      m.msg('this is a standard message.')
    """
    kwdefaults = {'prefix': '', 'fore': self.msg_fore, 'back': self.msg_back, 'style': self.msg_style}
    kwdefaults.update(kwargs)
    self.print_message(*args, **kwargs)

  def info(self, *args: any, **kwargs: any) -> None:
    """
    Prints an info message to stdout, with optional additional 
    formatting. 
    
    Args:
      *args: The print message arguments.
      **kwargs: Additional options for the message print. 
      Valid options are 'prefix', 'sep', 'end', 'back', 'fore', 
      'style', and 'file'.

    Example:
      m.info('this is an info message.')
    """
    kwdefaults = {'prefix': 'info', 'fore': self.info_fore, 'back': self.info_back, 'style': self.info_style}
    kwdefaults.update(kwargs)
    self.print_message(*args, **kwdefaults)

  def warn(self, *args: any, **kwargs: any) -> None:
    """
    Prints a warning message to stderr, with optional additional 
    formatting.
    
    Args:
      *args: The print message arguments.
      **kwargs: Additional options for the message print. 
      Valid options are 'prefix', 'sep', 'end', 'back', 'fore', 
      'style', and 'file'.

    Example:
      m.warn('this is a warning.')
    """
    kwdefaults = {'prefix': 'warning', 'fore': self.warn_fore, 'back': self.warn_back, 'style': self.warn_style, 'file': sys.stderr}
    kwdefaults.update(kwargs)
    self.print_message(*args, **kwdefaults)

  def error(self, *args: any, **kwargs: any) -> None:
    """
    Prints an error message to stderr, with optional additional 
    formatting.
    
    Args:
      *args: The print message arguments.
      **kwargs: Additional options for the message print. 
      Valid options are 'prefix', 'sep', 'end', 'back', 'fore', 
      'style', and 'file'.

    Example:
      m.error('this is an error.')
    """
    kwdefaults = {'prefix': 'error', 'fore': self.error_fore, 'back': self.error_back, 'style': self.error_style, 'file': sys.stderr}
    kwdefaults.update(kwargs)
    self.print_message(*args, **kwdefaults)


if __name__ == '__main__':
  # for testing only
  m = msg()

  m.msg('Hello World, to stdout.')
  m.set_prefix('myprog')
  m.msg('This is msg.msg(), with a prefix "myprog", to stdout')
  m.error("This is msg.error(), to stderr")
  m.warn('This is msg.warn(), to stderr')
  m.warn('This is a multi-line msg.warn() message.', 
      'This is the next line.', '... and so on ..., to stderr')
  m.info('This is msg.info(), to stdout')
  
  # Make new default colours for msg.info() and msg.WARN()
  m.set_prefix('myprog, colorstalk') # set a double level prefix
  m.info(f"Double prefix '{m.prefix}', from msg.info(), to stdout")
  m.msg(f"msg.msg() with prefix '{m.prefix}'")
  m.set_msg_colors(
      info_fore=colorama.Fore.RED, 
      info_style=colorama.Style.BRIGHT, 
      warn_fore=colorama.Fore.LIGHTBLACK_EX, 
      warn_back=colorama.Back.WHITE
    )
  m.info('This is now msg.info()', 'with new default colours.')
  m.warn('This is now msg.warn()', 'with new default colours.')
  m.set_prefix('')
  m.msg('', 'Now back to msg.msg() without prefixes.', '')