import re
from datetime import datetime, timedelta


def parse_command(command_str: str):
    # Define regular expressions for extracting the command type and reason
    command_regex = r'(![a-zA-Z]+|/[a-zA-Z]+)\s*(\d+[a-zA-Z])?\s*(.*)'

    # Match the command string with the regular expression
    match = re.match(command_regex, command_str)

    if match:
        command_type = match.group(1)
        duration = match.group(2)
        reason = match.group(3)

        return {
            'command_type': command_type,
            'duration': duration,
            'reason': reason.strip()
        }
    else:
        return None


def parse_time(time_string: str | None) -> datetime | None:
    if not time_string:
        return None

    match_ = re.match(r"(\d+)([a-z])", time_string.lower().strip())
    current_datetime = datetime.utcnow()

    if match_:
        value, unit = int(match_.group(1)), match_.group(2)
        match unit:
            case "h":
                time_delta = timedelta(hours=value)
            case "d":
                time_delta = timedelta(days=value)
            case "w":
                time_delta = timedelta(weeks=value)
            case _:
                return None
    else:
        return None

    new_datetime = current_datetime + time_delta
    return new_datetime


# command_str1 = '!ban 24h test hellow_world'
# command_str2 = '!mute 20d testing'
# parsed_command1 = parse_command(command_str1)
# parsed_command2 = parse_command(command_str2)
# print(parsed_command1)
# print(parsed_command2)
# print(parse_time(parsed_command2['duration']))