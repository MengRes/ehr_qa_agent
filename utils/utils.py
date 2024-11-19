import os
import numpy as np
import pandas as pd

def get_readable_file_size(file_path):
    file_size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if file_size < 1024:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024