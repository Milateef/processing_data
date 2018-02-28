file_name = "C:/workspace/dir_server2_utf_8.txt"
new_file_name = "C:/workspace/filt_down_server2.txt"
f = open(file_name, 'r', encoding='utf-8')  # a important problem
f_new = open(new_file_name, 'w', encoding='utf-8')

f.seek(0)
for line in f.readlines():
    if "9/15/2017" in line:
        f_new.write(line)
    elif "9/16/2017" in line:
        f_new.write(line)
    elif "9/17/2017" in line:
        f_new.write(line)
    elif "9/18/2017" in line:
        f_new.write(line)
    elif "9/19/2017" in line:
        f_new.write(line)
