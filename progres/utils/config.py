def check_config_exists(lines):
    """
    Check if the CONFIG command exists anywhere in `lines`
    """
    return any([line.strip().startswith('CONFIG') for line in lines])
