import os

# file_name = 'C:/workspace/job/data/4DIC board Correlation/LB01/tb_ac_timing_LB01_LT.txt'
file_name = input("Please input the file you want to process: \n")
# if the file user input is not exist, input again
while True:
    if os.path.exists(file_name):
        break
    else:
        file_name = input("Can't find this file, Please input the right path and file name: \n")

file_name_path = os.path.dirname(file_name)

# the result file, the path is user-defined
file_result = file_name_path + '/result.txt'

f = open(file_name, 'r')
# timing and data are deposited in these two lists, respectively
list_data = []
list_timing = []

for line in f.readlines():
    if '0x0' not in line and '=' in line:
        list_data.append(line)
i = 0
while i < 4:
    list_data.remove(list_data[0])
    i = i + 1
list_data.pop()
list_data.pop()

# this step is neccsary
f.seek(0)

for line in f.readlines():
    if 'tb' in line and not('Warning' in line):
        list_timing.append(line)

# now, handle the list_data, remove the redundant data except timing
data_temp = []
for term in list_data:
    data_temp.append(term.split('=')[len(term.split('=')) - 1])
#    print(data_temp[len(data_temp) - 1])

j = 0
while j < len(list_timing):
    list_timing[j] = list_timing[j].lstrip('CHAR_LOOP')
    j += 1
f.close()
# list_timing , data_temp
with open(file_result, 'w') as result_f:
    k = 0
    for timing in list_timing:
        # print(timing.endswith('\n'))
        # there must be an assignment, otherwise, the string won't change
        timing = timing.strip().split('ac_')[1]
        result_f.write('{0:25}'.format(timing) + '\t')

        while k < len(data_temp):
            if (k + 1) < len(data_temp) and 'RPT' in data_temp[k + 1]:
                k += 1
            else:
                result_f.write('{:6}'.format(data_temp[k].lstrip()))
                k += 1
                break
result_f.close()
