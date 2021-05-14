import subprocess
import pathlib
import os

print("=== program start ===")
path = pathlib.Path('.')
out_path = str(path) + '/result'
src_path = str(path) + '/src'
exist_flg = ""
inputfile = []
outputfile = ""
bitrate = "100000000"
output_size = "5760x2880"
pgname = "C:/work/MediaSDK/bin/stitcherSDKDemo.exe "
fnum = 0
fnummax = 0

if (os.path.exists(out_path)):
    print("folder exist")
else:
    os.mkdir(out_path)

input_path = pathlib.Path('./src')
for po in input_path.iterdir():
    if po.match('*.insv'):
        print(po)
        exist_flg = True
        inputfile.append(str(po) + " ")
    else:
        print("no file")
        exist_flg = False
        break
if len(inputfile) < 2:
    print("File missing")
    exist_flg =False

fnummax = len(inputfile)

while(fnum < fnummax):
    if str(inputfile[fnum][8:23]) == str(inputfile[fnum + 1][8:23]):
        # print("Output file name")
        # print(str(inputfile[fnum][8:23]))
        out_filename = str(inputfile[fnum][8:23]) + ".mp4"
    else:
        exist_flg = False
        print("File name mismatch")
    if exist_flg:
        outputfile = str(out_path) + "/" + out_filename
        para = " -inputs " + inputfile[fnum] + inputfile[fnum + 1] + " -output " + outputfile + " -stitch_type dynamicstitch -hdr_type singleimagehdr -bitrate " + bitrate + " -enable_flowstate -output_size " + output_size
        exename = pgname + para
        # print(exename)
        subprocess.run(exename)
    fnum = fnum + 2

print("=== program end ===")
