import csv
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# the intermediate file during code runing. we don't need care about it
file_intermediate = 'C:/intermediate.txt'
flag = 0        # flag of cmd == 78
count = 0       # counter using for recognize die addr
colomn_index = 0    # counter using for recognize which colomn is IO, WE, CLE, ALE...

die_addr = 0    # die addr
die_addr_mask = 0b111   # die addr mask

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

root = Tk()
explanation = "Pyky: One Click, Do Everything"
root.title("UI")

w = Label(
    root,
    compound=CENTER,
    padx=20,
    pady=10,
    fg="Gainsboro",
    bg="black",
    font="Helvetica 30 bold",
    text=explanation).grid(row=1, column=0)


def is_csv():
    messagebox.showwarning("Warning", "Please select a '*.csv' file")


def callback():
    name = filedialog.askopenfilename()
    return name


def process_data():
    # the intermediate file during code runing. we don't need care about it
    file_intermediate = 'C:/intermediate.txt'
    flag = 0        # flag of cmd == 78
    count = 0       # counter using for recognize die addr
    colomn_index = 0    # counter using for recognize which colomn is IO, WE, CLE, ALE...

    die_addr = 0    # die addr
 #   die_addr_mask = 7   # die addr mask

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
    try:
        # the file we want to process, the path is user-defined
        file_name = callback()

        file_name_path = os.path.dirname(file_name)

        # the result file, the path is user-defined
        file_result = file_name_path + '/result.txt'

        # ---------------------above are all files---------------------------
        with open(file_name, 'r') as csv_file:

            if ".csv" not in file_name:
                is_csv()
                return 0

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
                            intermediate_f.write(str(int(row[time_index]) // 1000) + '\tCMD\t' + row[IO_index] + '\n')

                    if row[we_index] == '1' and row[ale_index] == '1':      # filter Addr row
                        # if the Addr row isn't belong to cmd 78h, and WE, CLE, ALE are not all equal to last row, then print out this row
                        if flag == 0 and not (row[we_index] == we and row[cle_index] == cle and row[ale_index] == ale):
                            count = count + 1
                            # when count = 1, we need write a begining "Addr"
                            if count == 1:
                                intermediate_f.write(str(int(row[time_index]) // 1000) + '\tAddr\t' + row[IO_index])
                            # when count = 5, we need write a ending "die0 \n"
                            elif count == 5:
                                die_addr = (int(row[IO_index], 16) >> die_addr_offset.get()) & die_addr_mask   # calculate die addr
                                intermediate_f.write('\t' + row[IO_index] + '\tdie' + str(die_addr) + '\n')

                            else:
                                intermediate_f.write('\t' + row[IO_index])
                            # print(row)

                    we = row[we_index]
                    cle = row[cle_index]
                    ale = row[ale_index]

            intermediate_f.close()    # close intermediate file

        csv_file.close()        # close csv file
    except Exception as e:
        return 0
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
    os.remove("C:/intermediate.txt")
    # ---------------------above are procesing the intermediate file--------------------------

Label(root, text="").grid(row=2)
die_addr_offset = IntVar()   # die addr mask
Radiobutton(
    root,
    text="Die address represent by IO[5:7]",
    font='Helvetica 10 bold',
    bg='DarkKhaki',
    width=50,
    variable=die_addr_offset,
    value=5).grid(row=3)

Radiobutton(
    root,
    text="Die address represent by IO[4:6]",
    font='Helvetica 10 bold',
    bg='DarkKhaki',
    width=50,
    variable=die_addr_offset,
    value=4).grid(row=4)
    
Radiobutton(
    root,
    text="Die address represent by IO[3:5]",
    font='Helvetica 10 bold',
    bg='DarkKhaki',
    width=50,
    variable=die_addr_offset,
    value=3).grid(row=5)

Label(root, text="").grid(row=6)

Button(
    root,
    text='Select a csv File',
    bg='CadetBlue4',
    fg='GhostWhite',
    font='Helvetica 20 bold',
    padx=10,
    pady=10,
    width=25,
    height=3,
    command=process_data,
    compound=BOTTOM).grid(row=7)

Label(root, text="").grid(row=8)

Button(
    root,
    text="Quit",
    bg='red4',
    fg='GhostWhite',
    font='Helvetica 20 bold',
    padx=10,
    pady=10,
    width=25,
    height=3,
    command=root.destroy).grid(row=9)

Label(root, text="").grid(row=10)

mainloop()
