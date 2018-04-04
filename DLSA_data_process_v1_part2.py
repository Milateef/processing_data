import os
from openpyxl import Workbook

current_dir = os.getcwd()   # get current directory
file_list = os.listdir(current_dir)  # list file under dir

SDE_DAC = []        # store SDE shmoo value
VDD_DAC = []        # store VDD shmoo value
VDDSA_DAC = []      # store VDDSA shmoo value
SDE_shmoo_step = 2  # SDE shmoo step
def_SDE_index = []

Vcc = []
Pattern = []
FBC = []
Margin = []

for i in range(0x3F, 0x00, -SDE_shmoo_step):
    SDE_DAC.append(i)       # generate SDE_DAC

for i in range(0xF, 0x00, -1):
    VDD_DAC.append(i)
    VDDSA_DAC.append(i)     # generate VDD_DAC and VDDSA_DAC

VDD_DAC.append(0x00)
VDDSA_DAC.append(0x00)


# get index of a sub string, reture -1 if when whole string didn't include sub string
def get_index(whole, sub):
    try:
        index = whole.index(sub)
        return index
    except Exception:
        return -1


def get_Vcc_Pattern_FBC(var_str):
    if 'Vcc' in var_str:
        return 'Vcc', var_str.strip().split()[-1]
    elif 'Pattern' in var_str:
        return 'Pattern', var_str.strip().split()[-1]
    elif 'SDE' in var_str:
        return 'FBC', var_str.strip().split(',')[1:]
    else:
        return False


def cal_margin(var_2d_list, row, col):
    for r in range(1, min(row, len(var_2d_list) - row - 1) + 1):
        if var_2d_list[row - r][col] != '0' or var_2d_list[row + r][col] != '0':
            r -= 1
            break
    for c in range(1, min(col, len(var_2d_list[0]) - col - 1) + 1):
        if var_2d_list[row][col - c] != '0' or var_2d_list[row][col + c] != '0':
            c -= 1
            break
    return 2*r, c


for source_file_name in file_list:
    if '.txt' in source_file_name and 'DUT' in source_file_name:
        with open(source_file_name, 'r') as sf:
            default_values = sf.readline().rstrip().split(',')

            for value in default_values:

                if 'SDE' in value:
                    SDE_default = value.split('=')[-1]
                    try_SDE_index = get_index(
                        SDE_DAC, int(SDE_default, 16))

                    if try_SDE_index != -1:
                        def_SDE_index.append(try_SDE_index)

                    else:
                        def_SDE_index.append(get_index(
                            SDE_DAC, int(SDE_default, 16) - 1))
                        def_SDE_index.append(get_index(
                            SDE_DAC, int(SDE_default, 16) + 1))

                elif 'VDD' in value and 'VDDSA' not in value:
                    VDD_default = value.split('=')[-1]
                    def_VDD_index = get_index(
                        VDD_DAC, int(VDD_default, 16))

                elif 'VDDSA' in value:
                    VDDSA_default = value.split('=')[-1]
                    def_VDDSA_index = get_index(
                        VDDSA_DAC, int(VDDSA_default, 16))

            for line in sf:
                get_value = get_Vcc_Pattern_FBC(line)
                if get_value == False:
                    continue
                elif get_value[0] == 'Vcc':
                    Vcc.append(get_value[1])
                    Pattern.append([])
                    Margin.append([])
                elif get_value[0] == 'Pattern':
                    Pattern[len(Vcc)-1].append(get_value[1])
                    Margin[-1].append([])
                    FBC = []
                elif get_value[0] == 'FBC':
                    FBC.append(get_value[1])

                    if len(FBC) == len(SDE_DAC):
                        temp_margin = [[], []]
                        for i in range(0, len(def_SDE_index)):
                            for j in range(0, len(temp_margin)):
                                temp_margin[j].append(cal_margin(
                                    FBC, def_SDE_index[i], def_VDD_index)[j])
                        Margin[-1][-1].append(min(temp_margin[0]))
                        Margin[-1][-1].append(min(temp_margin[1]))

print(Margin)
print(len(Margin[0]))
