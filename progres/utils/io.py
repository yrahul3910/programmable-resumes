import os
from typing import Union


class IOWrapper:
    """
    A wrapper library for I/O with multiple configs.
    """
    def __init__(self, configs: Union[dict, None]):
        """
        :param configs: A dictionary of configs.
        """
        if configs is None:
            self.configs = { "default": [] }

        if "configs" not in configs:
            raise ValueError("configs.json must have a key named 'configs'.")

        self.configs = configs["configs"]
        self._check_files_dont_exist()
        self.files = { config: open(config + ".py", "w") for config in self.configs }

    def _check_files_dont_exist(self):
        """
        Check if the files in the configs don't exist.
        """
        for config in self.configs:
            if os.path.exists(config):
                raise FileExistsError(f"{config} already exists.")
    
    def write_to_all(self, message: str) -> None:
        """
        Write to all files.

        :param message: The message to write.
        """
        for file in self.files.values():
            file.write(message)
    
    def write_to_file(self, config: str, message: str) -> None:
        """
        Write to a file.

        :param config: The config to write to.
        :param message: The message to write.
        """
        if config not in self.configs:
            raise ValueError(f"{config} is not a valid config.")

        self.files[config].write(message)
    
    def close_all_files(self) -> None:
        """
        Close all files.
        """
        for file in self.files.values():
            file.close()
