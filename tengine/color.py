import re

frmt = type(str())    # Format type
fgcolor = type(str()) # Foreground color type
bgcolor = type(str()) # Background color type 

def len_no_ansi(s: str) -> int:
    """Calculate string length excluding ANSI color codes"""
    ansi_pattern = re.compile(r'\033\[[0-9;]*m')
    if not isinstance(s, str):
        return len(s)
    return len(ansi_pattern.sub('', s))

def split_and_group_ansi(text: str) -> list[str]:
    """
    Splits text into list where ANSI codes are grouped with following character.
    If next character is another ANSI code, continues grouping until non-ANSI char.
    If no following character, groups with previous character or space if none exists.
    
    Args:
        text: Input string potentially containing ANSI codes
        
    Returns:
        List of strings with ANSI codes properly grouped with characters
    """
    ansi_pattern = re.compile(r'(\033\[[0-9;]*m)')
    segments = []
    buffer = ""
    pending_ansi = []
    
    # First pass: split into ANSI codes and other content
    parts = ansi_pattern.split(text)
    
    for part in parts:
        if not part:
            continue
            
        if ansi_pattern.fullmatch(part):
            pending_ansi.append(part)
        else:
            if pending_ansi:
                # Group all pending ANSI codes with each character
                for char in part:
                    if char == '\n':
                        # Handle newlines as separate elements
                        if pending_ansi:
                            segments.append(''.join(pending_ansi) + ' ')
                            pending_ansi = []
                        segments.append('\n')
                    else:
                        segments.append(''.join(pending_ansi) + char)
                        pending_ansi = []
            else:
                # No pending ANSI, add characters normally
                segments.extend(list(part))
    
    # Handle any remaining ANSI codes without following characters
    if pending_ansi:
        # Try to attach to previous character
        if segments and not ansi_pattern.fullmatch(segments[-1]):
            segments[-1] = ''.join(pending_ansi) + segments[-1]
        else:
            # No previous character to attach to
            segments.append(''.join(pending_ansi) + '\0')
    
    return segments

class Color:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''

    reset: frmt = '\033[0m'
    bold: frmt = '\033[01m'
    disable: frmt = '\033[02m'
    underline: frmt = '\033[04m'
    reverse: frmt = '\033[07m'
    strikethrough: frmt = '\033[09m'
    invisible: frmt = '\033[08m'

    class fg:
        black: fgcolor = '\033[30m'
        red: fgcolor = '\033[31m'
        green: fgcolor = '\033[32m'
        orange: fgcolor = '\033[33m'
        blue: fgcolor = '\033[34m'
        purple: fgcolor = '\033[35m'
        cyan: fgcolor = '\033[36m'
        lightgrey: fgcolor = '\033[37m'
        darkgrey: fgcolor = '\033[90m'
        lightred: fgcolor = '\033[91m'
        lightgreen: fgcolor = '\033[92m'
        yellow: fgcolor = '\033[93m'
        lightblue: fgcolor = '\033[94m'
        pink: fgcolor = '\033[95m'
        lightcyan: fgcolor = '\033[96m'

    class bg:
        black: bgcolor = '\033[40m'
        red: bgcolor = '\033[41m'
        green: bgcolor = '\033[42m'
        orange: bgcolor = '\033[43m'
        blue: bgcolor = '\033[44m'
        purple: bgcolor = '\033[45m'
        cyan: bgcolor = '\033[46m'
        lightgrey: bgcolor = '\033[47m'
