import itertools
import subprocess as sub
from label_converter.label_converter import convert_labels_to_registers
from utils.utils import write_to_file
from typing import List

''' Takes code, save it to a intermediate file, remove labels from it and then
    saves it into executable file. At the end runs the executable file on virtual machine.
    Returns output from virtual machine as string.'''


def run_code(code: str, intermediate_filename: str,
             executable_filename='executable',
             *args,
             path_to_vm='../maszyna_wirtualna/maszyna-wirtualna-cln',
             ) -> str:
    write_to_file(f'out/{intermediate_filename}', code)
    convert_labels_to_registers(f'out/{intermediate_filename}', f'out/{executable_filename}')
    # p = sub.Popen(f'echo {args}', stdout=sub.PIPE)
    out: str = sub.run([f"{path_to_vm}",
                        f"out/{executable_filename}"],
                       stdout=sub.PIPE, stderr=sub.STDOUT,
                       input=f"{' '.join(args)}", text=True).stdout
    # out: bytes = sub.check_output(["../../maszyna_wirtualna/maszyna-wirtualna-cln",
    #                                f"out/{executable_filename}"], stdin=p.stdout)
    # out: str = out.decode()
    return out


def get_numbers_from_run_code(
        code: str,
        intermediate_filename: str,
        executable_filename='executable',
        should_print_output=True
) -> List[int]:
    out: str = run_code(code, intermediate_filename, executable_filename)
    if should_print_output:
        print(out)
    returned = []
    for line in out.splitlines()[1:-1]:
        if line.startswith('>'):
            num: int = int(line[2:])
            returned.append(num)
    return returned


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
