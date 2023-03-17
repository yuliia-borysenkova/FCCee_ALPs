import re
compiled_re = re.compile('([0-9]+[0-9.e+-]+)')

list_mass = ['0.5', '0.7', '1.', '3.', '5.', '7.', '10.', '15.', '20.', '25.', '30.']
list_cYY = ['0.1', '0.3', '0.5', '0.7', '0.9']

output_file = open('output_table.csv', 'w')
output_file.write('Mass, cYY, num selNone, dt num selNone, num sel0, dt num sel0, num sel1, dt num sel1, num sel2, dt num sel2, Mass, cYY, selNone, sel0, sel1, sel2\n')
                  

for mass in list_mass:
    for cYY in list_cYY:
        with open(f'/afs/cern.ch/work/y/yborysen/private/ALPs/results/ALPs_ne_100k_mass_{mass}GeV_cYY_{cYY}/output_finalSel/outputTabular.txt', 'r') as f:
            data = f.read()
            data = re.findall(compiled_re, data)
            output_file.write(','.join(data) + '\n')

output_file.close()