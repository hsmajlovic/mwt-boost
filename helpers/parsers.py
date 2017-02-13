""" IO parsers module """
import os
from typing import Any

import yaml

from utils.enums import FileType


def write_to_file(
        data: Any,
        path_to_file: str,
        **kwargs: Any
) -> None:
    """
    Writes the provided data to specified file of specified file format.
    Accepts .txt and .yaml file types only.

    Args:
        data: - Any writable data.
        path_to_file: - Path to file in which data is ought to be stored.
        **kwargs: - Any other relevant kwargs to be passed to the actual writing method.
    """

    file_type = FileType(os.path.splitext(path_to_file)[1])

    if os.path.exists(path_to_file):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not

    with open(path_to_file, append_write) as outfile:
        if file_type == FileType.YAML:
            yaml.dump(data, outfile, **kwargs)
        elif file_type == FileType.TXT:
            outfile.write(data)
