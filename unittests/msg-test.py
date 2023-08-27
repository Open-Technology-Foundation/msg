#!/usr/bin/env python
"""
Unit tests for module `msg`.
"""
from msg import Msg

if __name__ == '__main__':
  # for testing only
  #import msg
  m = Msg()
  m.enable_color(True) # only required to force coloured output to file
  m.prefix_set('myprog') # make a prefix for following msg's 
  m.info('Hello World (to stdout)')
  m.msg('This is m.msg(), with a prefix "myprog" (to stdout)')
  m.info('This is m.info() (to stdout)')
  m.warn('This is m.warn() (to stderr)')
  m.error("This is m.error() (to stderr)")
  m.line()
  m.warn('This is a multi-line m.warn() message.', 
      'This is the next line.', '(to stderr)')
  m.prefix_add('color') # set a double level prefix
  m.info(f"Double prefix '{m.prefixes}', from m.info() (to stdout)")
  m.msg(f"m.msg() with prefix '{m.prefixes}'")
  m.line()
  m.msg('Make new default colours for m.info() and m.warn()')
  m.set_colors(info_fore='LIGHTBLUE_EX', info_style='BRIGHT', 
      warn_fore='RED', warn_back='WHITE', warn_style='BRIGHT')
  m.info('This is m.info()', 'with new default colours.')
  m.warn('This is m.warn()', 'with new default colours.')
  m.prefix_set('')
  m.line()
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
    m.line(52)
    for style in all_styles:
      m.prefix_add(style)
      m.set_colors(info_style=style)
      m.info('Hello World.')
      m.prefix_pop()
    m.prefix_pop()
  m.line()

  m = Msg(prefixes=['textwrap'], use_color=True, columns=60, prefix_separator='> ')
  m.prefix_add(f'default {m.columns} cols')
  m.warn('This is a very, very, very long line that needs to be wrapped. Or else it will look like crap.', '')
  m.prefix_pop()
  m.prefix_add('disabled')
  m.enable_textwrap(False)
  m.line()
  m.warn("This is a very, very, very long line that doesn't want to be wrapped. Even if it will look like crap.")
  m.prefix_pop()

