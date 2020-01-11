# no registers used
def write_to_file(filename: str, text: str, append_halt=True):
    if append_halt:
        text = text + 'HALT'
    with open(filename, "w", newline='\n') as file:
        file.write(text + '\n')


def write_to_str(text: str, append_halt=True) -> str:
    if append_halt:
        text = text + 'HALT\n'
    return text


# no registers used
def clean_p0() -> str:
    return 'SUB 0\n'
