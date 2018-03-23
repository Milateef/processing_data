from openpyxl import Workbook
from openpyxl import load_workbook

num_of_row = 20
num_of_col = 39

SDE_default = '0x1B'
VDD_default = '0x8'
VDDSA_default = '0x8'
SDE_DAC = []
VDD_DAC = []
VDDSA_DAC = []
voltages = []
shmoo_points = []
for i in range(0x00, 0x40):
    SDE_DAC.append(i)

for i in range(0x0, 0x10):
    VDD_DAC.append(i)
    VDDSA_DAC.append(i)


wb = load_workbook('test.xlsx')
"""
for sheet_name in wb.sheetnames:
    if 'DUT' in sheet_name:
        ws = wb[sheet_name]"""

ws = wb['SDE_vs_VDD_16K_DUT1']

for r in range(1, num_of_row + 1):
    for c in range(1, num_of_col + 1):
        cell_value = ws.cell(row=r, column=c).value
        if isinstance(cell_value, str):
            if 'Vcc' in cell_value:
                voltages.append(cell_value)
            if 'Pattern' in cell_value:
                shmoo_points = []
            if 'SDE' in cell_value:
                shmoo_points.append([])
        elif isinstance(cell_value, int):
            shmoo_points[len(shmoo_points) - 1].append(cell_value)

print(shmoo_points)
