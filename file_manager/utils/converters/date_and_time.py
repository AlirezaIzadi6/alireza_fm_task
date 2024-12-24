def time_to_int(time_string: str) -> int:
    '''
    time_string must be in format hh:mm:ss.cc
    '''
    colon_separated = time_string.split(':')
    dot_separated = colon_separated[2].split('.')
    hours = int(colon_separated[0])
    minutes = int(colon_separated[1])
    seconds = int(dot_separated[0])
    centiseconds = int(dot_separated[1])
    return (hours*3600000) + (minutes*60000) + (seconds*1000) + (centiseconds*10)

def int_to_time(num: int, short_format: bool = True, milliseconds: bool = False)-> str:
    '''
    num must be an integer.
    If milliseconds=True then the returned string will contain milliseconds.
    For num=0 it will return empty string.
    '''
    if num == 0:
        return ''
    milliseconds = num%1000
    total_seconds = num//1000
    seconds = total_seconds%60
    total_minutes = total_seconds//60
    minutes = total_minutes%60
    hours = total_minutes//60
    if short_format == True and hours == 0:
        return f'{minutes:02}:{seconds:02}'
    if milliseconds == True and short_format == False:
        return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'
    return f'{hours:02}:{minutes:02}:{seconds:02}'