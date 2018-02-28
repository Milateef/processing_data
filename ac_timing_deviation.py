file_location = 'C:/workspace/job/data/4DIC board Correlation/ac_timing_diff_dut/DUT1_HT.txt'
f = open(file_location, 'r')

for line in f.readlines():
    deviation = []
    data = line.split('\t')
    i = 1
    while i < len(data):
        if float(data[0]) != 0:
            deviation.append(round(((float(data[i]) - float(data[0])) / float(data[0])), 2))
            i += 1
        else:
            deviation.append(0)
            i += 1
    for item in deviation:
        print(item, end='\t')
    print('\n')
