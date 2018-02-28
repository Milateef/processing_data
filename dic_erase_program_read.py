file_address = 'C:\\workspace\\job\\data\\4DIC board Correlation\\LB01\\tb_e_p_r_LB01_HT.txt'
f = open(file_address, 'r')

test_mode = []
for line in f.readlines():
    if 'TestBlock' in line:
        test_mode.append(line)

f.seek(0)

i = 0
while i < 4:
    for line in f.readlines():
        if ('Dut: ' + str(i)) in line:
            print(line.replace(' byte_fail ', ' ').strip())
        elif '_SLC_X2' in line:
            print('\n')
    print('\n--------------------------------------')
    f.seek(0)
    i += 1
