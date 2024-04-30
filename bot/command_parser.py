import re


def parse_command(command_str: str):
    # Define regular expressions for extracting the command type and reason
    command_regex = r'(![a-zA-Z]+|/[a-zA-Z]+)\s*(\d+h)?\s*(.*)'

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
