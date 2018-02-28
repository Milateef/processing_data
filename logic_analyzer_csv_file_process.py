import csv

file_name = 'C:/Users/40038/Desktop/t7.csv'     # the file we want to process
file_intermediate = 'C:/Users/40038/Desktop/intermediate.txt'
file_result = 'C:/Users/40038/Desktop/result.txt'

# ---------------------above are all files---------------------------

flag = 0        # flag of cmd == 78
count = 0       # counter using for recognize die addr
colomn_index = 0    # counter using for recognize which colomn is IO, WE, CLE, ALE...

die_addr = 0    # die addr
die_addr_mask = 7   # die addr mask

we = ''         # store the value of WE of last row
cle = ''        # store the value of CLE of last row
ale = ''        # store the value of ALE of last row

IO_index = 0    # the colomn number of IO
we_index = 0    # the colomn number of WE
cle_index = 0   # the colomn number of CLE
ale_index = 0   # the colomn number of ALE
time_index = 0  # the colomn number of time
header_group = {'IO': IO_index, 'WE': we_index, 'CLE': cle_index, 'ALE': ale_index, 'Time': time_index}

is_sig_cmd = True       # flag of prefix cmd
is_tri_cmd = True       # flag of 2P Operation
is_bi_cmd = True        # flag of 1P Operation
lst_cmd_adjacent = []   # a list to store the adjacent cmd

# ---------------------above are all variables---------------------------


def single_command(sig_cmd):        # the comment of each prefix cmd
    try:
        return {
            'A2': 'SLC',
            '01': 'LP',
            '02': 'MP',
            '03': 'UP',
            '09': 'LM',
            '0D': 'Foggy',
            'E0': 'Data out',
            '5D': 'Dynamic Read'
        }[sig_cmd]
    except Exception as e:
        return False


def tri_command(tri_cmd):       # the comment of each 2P Operation
    try:
        return {
            "['11', '80', '10']": '2P Normal Program',
            "['11', '80', '15']": '2P Cache Program',
            "['11', '80', '1A']": '2P Program 1A CMD',
            "['11', '85', '10']": '2P Normal Folding Program',
            "['11', '85', '15']": '2P Cache Folding Program',
            "['11', '85', '1A']": '2P Program Folding 1A CMD',
            "['32', '00', '30']": '2P Read'
        }[tri_cmd]
    except Exception as e:
        return False


def bi_command(bi_cmd):         # the comment of each 2P Operation
    try:
        return {
            "['80', '10']": '1P Normal Program',
            "['80', '15']": '1P Cache Program',
            "['80', '1A']": '1P Program 1A CMD',
            "['85', '1A']": '1P Normal Folding Program',
            "['85', '15']": '1P Cache Folding Program',
            "['85', '1A']": '1P Program Folding 1A CMD',
            "['00', '30']": '1P Read'
        }[bi_cmd]
    except Exception as e:
        return False


# ---------------------above are all variables--------------------------

with open(file_name, 'r') as csv_file:

    reader = csv.reader(csv_file)
    for row in reader:
        # colomn_index add one after one cycle
        colomn_index = colomn_index + 1
        # the string 'VALUE_SEPARATOR="' is the begining signal to count colomn_index
        if 'VALUE_SEPARATOR="' in row:
            colomn_index = 0
        # break loop when we meet the "HEADER_END" row
        if 'HEADER_END' in row:
            break
        # update the value of IO_index, we_index, cle_index, ale_index, and time_index
        for key in header_group:
            if key in row[0]:
                header_group[key] = colomn_index
        IO_index = header_group['IO']
        we_index = header_group['WE']
        cle_index = header_group['CLE']
        ale_index = header_group['ALE']
        time_index = header_group['Time']

csv_file.close()

with open(file_name, 'r') as csv_file:      # open csv file

    reader = csv.reader(csv_file)           # generate reader object
    intermediate_f = open(file_intermediate, 'w')       # open another file to store the result

    for row in reader:                     # loop the reader by row
        if len(row) > 5:

            if row[we_index] == '1' and row[cle_index] == '1':      # filter command row
                # if cmd = 78, flag = 1
                if row[IO_index] == '78':
                    flag = 1
                # if cmd != 78 and WE, CLE, ALE are not all equal to last row, then we print out this row
                if row[IO_index] != '78' and not (row[we_index] == we and row[cle_index] == cle and row[ale_index] == ale):
                    flag = 0
                    count = 0       # restore counter
                    intermediate_f.write(row[time_index][:-4] + '\tCMD\t' + row[IO_index] + '\n')

            if row[we_index] == '1' and row[ale_index] == '1':      # filter Addr row
                # if the Addr row isn't for cmd 78h, and WE, CLE, ALE are not all equal to last row, then print out this row
                if flag == 0 and not (row[we_index] == we and row[cle_index] == cle and row[ale_index] == ale):
                    count = count + 1
                    # when count = 1, we need write a begining "Addr"
                    if count == 1:
                        intermediate_f.write(row[time_index][:-4] + '\tAddr\t' + row[IO_index])
                    # when count = 5, we need write a ending "die0 \n"
                    elif count == 5:
                        die_addr = (int(row[IO_index], 16) >> 4) & die_addr_mask   # calculate die addr
                        intermediate_f.write('\t' + row[IO_index] + '\tdie' + str(die_addr) + '\n')

                    else:
                        intermediate_f.write('\t' + row[IO_index])
                    # print(row)

            we = row[we_index]
            cle = row[cle_index]
            ale = row[ale_index]

    intermediate_f.close()    # close intermediate file

csv_file.close()        # close csv file

# ---------------------above are procesing the original file--------------------------

with open(file_intermediate, 'r') as intermediate_f:    # open the intermediate file
    with open(file_result, 'w') as result_f:            # open the result file
        # loop the line in the intermediate file
        for line in intermediate_f:
            # strip the new line and split the line by tab, return a list
            lst_from_line = line.rstrip('\n').split('\t')
            # loop the list generated last step, and write it in the result file
            for element in lst_from_line:
                result_f.write(element + '\t')
            # if this line is cmd, we need judge which operation does it do
            # this index '1' depends on the intermedia file
            if lst_from_line[1] == 'CMD':
                # this index '2' depends on the intermedia file
                is_sig_cmd = single_command(lst_from_line[2])
                # if this cmd is a prefix, write the corrisponding comment
                if is_sig_cmd is not False:
                    result_f.write('\t\t\t\t' + is_sig_cmd + '\n')
                # if not a prefix, create a list to store the adjacent cmd to see if they are 1P or 2P
                else:
                    # this index '2' depends on the intermedia file
                    lst_cmd_adjacent.append(lst_from_line[2])
                    is_tri_cmd = tri_command(str(lst_cmd_adjacent))
                    is_bi_cmd = bi_command(str(lst_cmd_adjacent[:2]))

                    if len(lst_cmd_adjacent) == 2:
                        # if this cmd is a 1P Operation, write the corrisponding comment, and empty the list
                        if is_bi_cmd is not False:
                            result_f.write('\t\t\t\t' + is_bi_cmd + '\n')
                            lst_cmd_adjacent = []
                        # if not 1P Operation, and list contains cmd '32' or '11', that means it's a 2P opration
                        elif '32' in lst_cmd_adjacent or '11' in lst_cmd_adjacent:
                            result_f.write('\n')
                        # list left shift one element
                        else:
                            lst_cmd_adjacent = lst_cmd_adjacent[1:]
                            result_f.write('\n')
                    # if this cmd is a 1P Operation, write the corrisponding comment
                    elif len(lst_cmd_adjacent) == 3:

                        if is_tri_cmd is not False:
                            result_f.write('\t\t\t\t' + is_tri_cmd + '\n')
                            lst_cmd_adjacent = []

                        else:
                            lst_cmd_adjacent = lst_cmd_adjacent[1:]
                            result_f.write('\n')

                    else:
                        result_f.write('\n')
            # if this line is Addr, just write a ending new line
            elif lst_from_line[1] == 'Addr':
                result_f.write('\n')

    result_f.close()        # close result file
intermediate_f.close()      # close intermediate file

# ---------------------above are procesing the intermediate file--------------------------
