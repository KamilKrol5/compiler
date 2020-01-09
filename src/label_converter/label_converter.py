import re


def convert_labels_to_registers(filename='filename.txt', output_filename='imp_executable'):

    labels_dest = dict()
    labels_to_replace = dict()

    with open(filename, 'r+') as file:
        data: str = ''
        line_counter = 0
        lines = file.readlines()
        for line in lines:
            if re.match(r'^(##).*\n', line):
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
                    #print(line)
                data = data + line

        for label, reg in labels_dest.items():
            regex = rf'%{label}$'
            data = re.sub(regex, str(reg), data, flags=re.MULTILINE)
            labels_to_replace[label] = None

        if all(map(lambda x: x is None, labels_to_replace.values())):
            print("Label converter info: All labels, found as needing to be replaced, were replace successfully")
        else:
            raise Exception('Not all labels were replaced!')

        data = re.sub(r'^(##).*\n', '', data, flags=re.MULTILINE)
        print('_____________________________________________________')
        #print(data)
        with(open(output_filename, 'w', newline='\n')) as file2:
            file2.write(data)


if __name__ == '__main__':
    convert_labels_to_registers('command_test.txt', 'exe_command_test.txt')
    convert_labels_to_registers('command_test_all.txt', 'exe_command_test_all.txt')
