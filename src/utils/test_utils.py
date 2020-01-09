import itertools
import subprocess as sub
from label_converter.label_converter import convert_labels_to_registers
from utils.utils import write_to_file

''' Takes code, save it to a intermediate file, remove labels from it and then
    saves it into executable file. At the end runs the executable file on virtual machine.
    Returns output from virtual machine as string.'''


def run_code(code: str, intermediate_filename: str, executable_filename='executable') -> str:
    write_to_file(f'out/{intermediate_filename}', code)
    convert_labels_to_registers(f'out/{intermediate_filename}', f'out/{executable_filename}')
    out: bytes = sub.check_output(["../maszyna_wirtualna/maszyna-wirtualna-cln",
                                   f"out/{executable_filename}"])
    out: str = out.decode()
    return out


def expected(*args):
    def decorator(f):
        f.expected = args
        return f
    return decorator


def flatten(iterable):
    return list(itertools.chain(*iterable))


def chain(*iterables):
    for item in iterables:
        yield from item
