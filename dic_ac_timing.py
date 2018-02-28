file_address = 'file_path'
f = open(file_address, 'r')

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

# list_timing , data_temp
k = 0
for timing in list_timing:
    # print(timing.endswith('\n'))
    # there must be an assignment, otherwise, the string won't change
    timing = timing.strip()
    print(timing, end=' ')

    while k < len(data_temp):
        if (k + 1) < len(data_temp) and 'RPT' in data_temp[k + 1]:
            k += 1
        else:
            print(data_temp[k])
            k += 1
            break

    # while k < len(data_temp):
    #     if 'RPT' not in data_temp[k]:
    #         print(data_temp[k])
    #         if (k + 1) < len(data_temp) and 'RPT' not in data_temp[k + 1]:
    #             k += 1
    #             break
    #
    #     elif 'RPT' in data_temp[k]:
    #         print(timing, end=' ')
    #         print(data_temp[k])
    #         if (k + 1) < len(data_temp) and 'RPT' not in data_temp[k + 1]:
    #             k += 1
    #             break
    #     k += 1
