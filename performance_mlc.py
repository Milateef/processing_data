file_name = "the_file_path"

file_name = "C:\workspace\job\data\BicS3 512Gb ex3 2plane RevC\
 Vt Lot\performance\SS\HT-2.25V\BLK_performance_MLC_Read_X1100C_touchdown0.txt"

f = open(file_name, 'r')


for i in range(4):
    file_name_new = "c:/users/40038/desktop/test" + str(i) + ".txt"
    fn = open(file_name_new, 'w')

    for index, line in enumerate(f):
        if index % 4 == i:
            fn.write(line)

    f.seek(0)

f.close()
