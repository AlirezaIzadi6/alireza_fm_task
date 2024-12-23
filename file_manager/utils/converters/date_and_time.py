def time_to_int(time_string: str) -> int:
    '''
    time_string must be in format hh:mm:ss.MMM
    '''
    colon_separated = time_string.split(':')
    dot_separated = colon_separated[2].split('.')
    hours = int(colon_separated[0])
    minutes = int(colon_separated[1])
    seconds = int(dot_separated[0])
    milliseconds = int(dot_separated[1])
    return (hours*3600000) + (minutes*60000) + (seconds*1000) + milliseconds