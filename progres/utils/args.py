import re

def parse_key_value_pairs(line):
    """
    Implements argument parsing when parse_xxx functions are called.
    """
    pattern = r'(\w+)=("[^"]+"|\S+)'
    pairs = re.findall(pattern, line)
    formatted_pairs = [f'{key}={value}' for key, value in pairs]
    return ", ".join(formatted_pairs)
