#!/usr/bin/env python
"""
This script is meant to take the concatenated output of ROI image data from 
Nikon imaging software and then separate it into files based on the source name
(second column). The summary statistics at the end of each ROI entry for each image ARE NOT included. 

USAGE: split_nikon_roi_csv.py -i <input.csv> -o [output_directory]

Updated 180617 by Ronald Cutler
"""
import sys, os, csv
from glob import glob
from optparse import OptionParser

__version__ = '1.0.0'

def splitRun(input_CSV, output_dir):
    """Read in CSV file and split based on Source ID"""

    # put everything into a list
    csv_list = []
    with open(input_CSV, 'r') as in_CSV:
        csvreader = csv.reader(in_CSV, delimiter=',')
        for line in csvreader:
            csv_list.append(line)

    # get amount of files to split
    print("Total Images =", csv_list.count(['Item', 'Source', 'FieldID', 'RoiID', 'BinaryID', 'ND.T', 'ND.M', 'ND.Z', \
    'NumberObjects', 'ObjectAreaFraction', 'ROIArea', 'MeasuredArea', 'Perimeter', 'MeanChord', \
    'SurfVolumeRatio', 'MeanIntensity', 'SumIntensity', 'IntensityVariation', 'MinIntensity', \
    'MaxIntensity', 'MeanRed', 'MeanGreen', 'MeanBlue', 'SumRed', 'SumGreen', 'SumBlue', 'HueTypical',\
     'HueVariation', 'MeanSaturation', 'MeanBrightness', 'SumBrightness', 'BrightVariation', 'MeanDensity',\
      'SumDensity', 'DensityVariation', 'Channel', 'MeanFITC', 'MeanTRITC', 'MeanCY5', 'MeanTD', 'MeanRatio',\
       'MeanCa2+', 'MeanCorrFRET', 'MeanFRETEff', 'MeanTitration', 'AcqTime', 'CentreX', 'CentreY', 'CentreXpx',\
        'CentreYpx', 'CentreXabs', 'CentreYabs', 'Comment']), "\n")

    temp_list = []
    file_switch = False
    file_name = ""

    for line in csv_list:
        if 'Item' in line:
            print("Splitting", csv_list[csv_list.index(line) + 1][1])
            file_name = csv_list[csv_list.index(line) + 1][1]
            file_switch = True

        if file_switch == True:
            temp_list.append(line)

        if 'Feature' in csv_list[csv_list.index(line) + 1]:
            file_switch = False
            with open(output_dir + file_name[:-4] + ".csv", 'w') as out_CSV:
                csvwriter = csv.writer(out_CSV, delimiter=',')
                for line in temp_list:
                    csvwriter.writerow(line)

def main():
    """parser user interface with required input parameters"""
    usage="split_nikon_roi_csv.py -i <input_CSV> -o [output_directory]\n"
    parser = OptionParser(usage,version="split_nikon_roi_csv.py" + __version__)
    parser.add_option("-i","--input_CSV",action="store",type="string",dest="input_CSV",help="CSV containing multiple Nikon image data")
    parser.add_option("-o","--output_directory",action="store",type="string",dest="output_dir",help="Output directory path. Default: Directory where input CSV is located")

    (options,args) = parser.parse_args()
    if not (options.input_CSV):
        parser.print_help()
        sys.exit(0)
    if not os.path.exists(options.input_CSV):
        print('\n' + options.input_CSV + " does NOT exist" + '\n')
        sys.exit(0)
    if options.output_dir and os.path.exists(options.output_dir):
        print('\n' + options.output_dir + " does NOT exist" + '\n')
        sys.exit(0)
    if not options.output_dir:
        options.output_dir = os.path.dirname(os.path.realpath(options.input_CSV)) + "/"

    splitRun(options.input_CSV, options.output_dir)

if __name__ == "__main__":
    main()




