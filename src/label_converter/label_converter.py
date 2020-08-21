import re

from utils.utils import write_to_file


def convert_labels_to_registers(
        intermediate_code_with_labels: str,
        output_filename='unnamed_executable',
        save_intermediate_code=False
) -> None:
    labels_dest = dict()
    labels_to_replace = dict()

    intermediate_code_with_labels = intermediate_code_with_labels + 'HALT\n'
    if save_intermediate_code:
        write_to_file(output_filename + '.intermediate', intermediate_code_with_labels)
    lines = intermediate_code_with_labels.splitlines(keepends=True)
    data: str = ''
    line_counter = 0
    for line in lines:
        if re.match(r'^(##).*\n', line):
            continue
        if re.match(r'^\n', line):
            continue
        if line.startswith('%label_'):
            labels_dest[line[1:-1]] = line_counter
        else:
            line_counter = line_counter + 1
            if re.match(r'.+%label_.*\n', line):
                r = re.search(r'.+%(label_[0-9]+).*\n', line)
                if r:
                    lbl = r.group(1)
                    labels_to_replace[lbl] = line_counter
                else:
                    raise Exception('No valid label in line.')
            data = data + line

    for label, reg in labels_dest.items():
        regex = rf'%{label}$'
        data = re.sub(regex, str(reg), data, flags=re.MULTILINE)
        labels_to_replace[label] = None

    if all(map(lambda x: x is None, labels_to_replace.values())):
        print("[[[ INFO ]]]: Label converter: All labels, found as needing to be replaced, were replaced successfully.")
    else:
        raise Exception(f'Not all labels were replaced! Labels left: '
                        f'{list(filter(lambda x: labels_to_replace[x] is not None, labels_to_replace.keys()))}')

    data = re.sub(r'^(##).*\n', '', data, flags=re.MULTILINE)
    # print('_____________________________________________________')
    with(open(output_filename, 'w', newline='\n')) as file2:
        file2.write(data)
