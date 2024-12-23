import re
import subprocess

from file_manager.utils.converters.date_and_time import time_to_int
from file_manager.utils.file_processor import verify_directory_existance

def create_video_thumbnail(name, source_path, destination_path):
    verify_directory_existance(destination_path)
    subprocess.call(['ffmpeg', '-i', f'{source_path}/{name}', '-ss', '00:00:00.000', '-vframes', '1', '-vf', 'scale=100:100', f'{destination_path}/{name}.jpg'])


def is_valid_video(file_path):
    result = subprocess.run(['ffmpeg', '-i', file_path], capture_output=True, text=True)
    output = result.stderr
    pattern = 'Duration: \\d'
    if re.search(pattern, output) is None:
        return False
    return True

def get_video_dimensions(file_path: str) -> tuple[int, int, int]:
    result = subprocess.run(['ffmpeg', '-i', file_path], capture_output=True, text=True)
    output = result.stderr
    parsed_output = output.split(', ')
    dimension_string = ''
    dimensions_pattern = '^\\d+x\\d+'
    for p in parsed_output:
        if re.search(dimensions_pattern, p):
            dimension_string = p
            break
    duration_pattern = r'Duration: \d{2}:\d{2}:\d{2}\.\d{2}'
    match = re.search(duration_pattern, output)
    start_index = match.start()+10
    end_index = match.end()
    duration_string = output[start_index:end_index]
    splitted_dimensions = dimension_string.split('x')
    width = int(splitted_dimensions[0])
    height = int(splitted_dimensions[1])
    duration = time_to_int(duration_string)
    return duration, height, width