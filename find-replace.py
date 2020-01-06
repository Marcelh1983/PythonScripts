import re
import glob, os

pattern = re.compile("<(\d{4,5})>")
os.chdir("/mydir")
for file in glob.glob("*.ts"):
    for i, line in enumerate(open(file)):
        for match in re.finditer(pattern, line):
            print('Found on line' + i+1 + ' : ' + match.groups())

