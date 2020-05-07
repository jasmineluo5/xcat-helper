from argparse import ArgumentParser
from os.path import isfile
from os import popen

import numpy as np
import SimpleITK as sitk


# argument parsing
parser = ArgumentParser()
parser.add_argument('-i', '--input', help='Please enter the name of the parameter file', required=False)
parser.add_argument('-o', '--output', help='file name to export, please do not include the extension', required=False)
parser.add_argument('-size',help='array size, and number of slices, (default is 256 for array size and 500 for number of slices)', nargs=2)
args = parser.parse_args()

if(args.size != None):
    array_size=int(args.size[0])
    num_slices=int(args.size[1])
else:
    array_size=256 # each image is of array_size*array_size
    num_slices=500 #total number of slices, default is 500 from the sample parameter file
if args.output:
    output_file=args.output
else:
    output_file="results"

#takes in inputs to create a new parameter file
if args.input:
    if isfile(args.input):
        with open(args.input) as input_file:
            parfile=open("temp.samp.par","w+b")
            lines=input_file.readlines()
            for line in lines:
                if line[:10]=="array_size":
                    line="array_size = "+str(array_size)+'\n'
                
                if line[:8]=="endslice":
                    line="endslice"+str(num_slices)
                parfile.write(line)

    else:
        print('input file does not exist')
else:
    with open('general.samp.par') as input_file:
        parfile=open("temp.samp.par","w+b")
        lines=input_file.readlines()
        for line in lines:
            if line[:10]=="array_size":
                line="array_size = "+str(array_size)+'\n'
            
            if line[:8]=="endslice":
                line="endslice = "+str(num_slices)
            parfile.write(line)

# run xcat
command="./dxcat2_linux_64bit temp.samp.par "+output_file
stream=popen(command)
output_msg=stream.read()
print(output_msg) #print out any error message

#convert the generated activity/attenuation file
act_file=open(output_file+"_act_1.bin")
atn_file=open(output_file+"_atn_1.bin")
output_act_file=output_file+"_act.mha"
output_atn_file=output_file+"_atn.mha"
img_act=np.fromfile(act_file,dtype=np.float32).reshape(num_slices,array_size,array_size)
img_atn=np.fromfile(atn_file,dtype=np.float32).reshape(num_slices,array_size,array_size)
sitk.WriteImage(sitk.GetImageFromArray(img_act),output_act_file)
sitk.WriteImage(sitk.GetImageFromArray(img_atn),output_atn_file)

            
