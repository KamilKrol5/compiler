import re


def convert_labels_to_registers(filename='filename.txt'):
    filename: str = 'command_test.txt'

    labels_dest = dict()
    labels_to_replace = dict()

    with open(filename, 'r+') as file:
        data: str = ''
        line_counter = 0
        lines = file.readlines()
        for line in lines:
            if re.match(r'^(##).*\n', line):
                continue
            if line.startswith('#label'):
                labels_dest[line[1:-1]] = line_counter
            else:
                line_counter = line_counter + 1
                if re.match(r'.+#label.*\n', line):
                    r = re.search('.+#(label [0-9]+).*\n', line)
                    if r:
                        lbl = r.group(1)
                        labels_to_replace[lbl] = line_counter
                    else:
                        raise Exception('No valid label in line.')
                    print(line)
                data = data + line

        for label, reg in labels_dest.items():
            data = re.sub(r'#'+label + r'.*', str(reg), data)
            labels_to_replace[label] = None

        if all(map(lambda x: x is None, labels_to_replace.values())):
            print("IT'S GOOD!")
        else:
            raise Exception('Not all labels were replaced!')

        data = re.sub(r'^(##).*\n', '', data, flags=re.MULTILINE)
        print('________________________')
        print(data)
        with(open(f'label_converter_{filename}.out', 'w', newline='\n')) as file2:
            file2.write(data)


if __name__ == '__main__':
    convert_labels_to_registers()
