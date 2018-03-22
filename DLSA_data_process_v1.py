from openpyxl import Workbook
from openpyxl.styles import PatternFill
import os

current_dir = os.getcwd()
file_list = os.listdir(current_dir)

SDE_margin = {}
VDD_margin = {}
VDDSA_margin = {}
# fill cell with red
redFill = PatternFill(
    start_color='00FF9999',
    end_color='00FF9999',
    fill_type='solid'
)
# fill cell with green
greenFill = PatternFill(
    start_color='0099FF99',
    end_color='0099FF99',
    fill_type='solid'
)


def get_index(whole_str, sub_str):
    try:
        index = whole_str.index(sub_str)
        return index
    except Exception:
        return -1


def str_to_num(original_str):
    try:
        inverted_num = int(original_str)
    except Exception:
        inverted_num = -1

    if inverted_num == -1:
        try:
            inverted_num = int(original_str, 16)
        except Exception:
            inverted_num = -1
    return inverted_num


wb = Workbook()

for source_file_name in file_list:

    if 'tb_DLSA_Test_SDE' in source_file_name:
        with open(source_file_name, 'r') as sf:

            start_index = source_file_name.index('SDE')

            if get_index(source_file_name, 'DUT') != -1:
                end_index = get_index(source_file_name, 'DUT')
                sheet_name = source_file_name[start_index: end_index + 4]
            elif get_index(source_file_name, 'VDDSA') != -1:
                end_index = get_index(source_file_name, 'VDDSA')
                sheet_name = source_file_name[start_index: end_index + 5]
            elif get_index(source_file_name, 'VDD') != -1:
                end_index = get_index(source_file_name, 'VDD')
                sheet_name = source_file_name[start_index: end_index + 3]

            ws = wb.create_sheet(sheet_name)

            default_values = sf.readline().rstrip().split(',')
            for value in default_values:

                if 'SDE' in value:
                    SDE_default = value.split('=')[-1]
                elif 'VDD' in value and 'VDDSA' not in value:
                    VDD_default = value.split('=')[-1]
                elif 'VDDSA' in value:
                    VDDSA_default = value.split('=')[-1]

            row_num = 1

            for line_of_sf in sf:

                if 'Pattern' in line_of_sf:
                    pattern = line_of_sf.split(' ')[1]

                line_split_list = line_of_sf.rstrip().split(',')
                """
                if 'VDD=' in line_split_list or 'VDDSA=' in line_split_list:
                    VDD_default_column = 1
                    for cell_value in line_split_list:
                        if VDD_default in cell_value:
                            break
                        VDD_default_column = VDD_default_column + 1
                """
                column_num = 1

                for cell_value in line_split_list:

                    cell_num_value = str_to_num(cell_value)
                    if cell_num_value != -1:
                        ws.cell(row=row_num,
                                column=column_num).value = cell_num_value
                        if cell_num_value != 0:
                            ws.cell(row=row_num,
                                    column=column_num).fill = redFill
                        else:
                            ws.cell(row=row_num,
                                    column=column_num).fill = greenFill
                    else:
                        ws.cell(row=row_num, column=column_num,
                                value=cell_value)

                    column_num = column_num + 1

                row_num = row_num + 1

                # if 'SDE' in line_of_sf:
                #     shmoo_point_list = line_of_sf.rstrip().split(',')

        sf.close()

del_sheet = wb.get_sheet_by_name('Sheet')
wb.remove_sheet(del_sheet)

wb.save('test.xlsx')
