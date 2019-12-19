# no registers used
def write_to_file(filename: str, text: str, append_halt=True):
    if append_halt:
        text = text + 'HALT'
    with open(filename, "w", newline='\n') as file:
        file.write(text + '\n')


# no registers used
def clean_p0() -> str:
    return 'SUB 0\n'
