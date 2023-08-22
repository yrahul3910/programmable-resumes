import re

def parse_key_value_pairs(line):
    pattern = r'(\w+)=("[^"]+"|\S+)'
    pairs = re.findall(pattern, line)
    formatted_pairs = [f'{key}={value}' for key, value in pairs]
    return ", ".join(formatted_pairs)
