#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import re
import sys

import numpy as np
import yaml
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

from lib import File
from lib import file_utils

cmdargs = None

with open('config/config.yaml', mode='r') as configFile:
    CONFIG = yaml.load(configFile, Loader=yaml.Loader)
    # print(CONFIG)


def define_arguments():
    global cmdargs
    parser = argparse.ArgumentParser()
    parser.description = "This script will output the statistics of the top 10 " \
                         "packages that have the most files associated with them " \
                         "based on the Debian repo and the given architecture."
    parser.add_argument('arch', type=str, choices=CONFIG["arch"],
                        help="Please select an architecture from the supported ones. ")
    parser.add_argument('--engine', dest='engine', type=str,
                        choices=['python', 'bash'],
                        default='python',
                        help="The core module computing the statistics can be a bash script" \
                             "or a Python one.")
    cmdargs = parser.parse_args()


# TODO: to move in external module
def plot_results(contentsFile):
    """ plot the results in a shiny bar chart

    :param stats_file:
    :return:
    """
    csv_file = os.path.join(CONFIG["statistics"]["plot_folder"], CONFIG["statistics"]["prefix"] 
                            + contentsFile.get_name() +"_"
                            + contentsFile.get_creation_date()
                            + ".csv")
    print(" Searching for plot data in "+ csv_file)

    try:
        with open(csv_file) as csv_in:
            data = [line.strip().split(',') for line in csv_in]
    except IOError:
        print(" No plot data is available.")
        return
    except Exception as e:
        print(str(e))
        return

    # names are too long and in reverse order:
    packages  = list(reversed([t[0] for t in data]))
    packages  = [p.split("/")[1] for p in packages]
    #packages  = [''] + packages
    # 0 needs to be added
    files_num = list(reversed([t[1] for t in data]))
    #files_num = ['0'] + files_num
    # preparing the horizontal bar chart
    figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.barh(np.arange(len(packages)), files_num, align='center')
    plt.yticks(np.arange(len(packages)), packages)
    plt.subplots_adjust(left=0.3)
    plt.title(" Most used packages")
    plt.savefig(csv_file[:-3]+"png", bbox_inches='tight', dpi=100)
    print(" Plot saved")
    # maybe is too annoying to show the plot without asking, let's just save it
    # plt.show()

def store_stats(contentsFile):
    """
    Repo time format: 03-Jul-2019 14:16

    :param contentsFile:
    :return:
    """
    filename = contentsFile.get_name().split("/")[1]
    out_file_name = os.path.join(CONFIG["statistics"]["path"], CONFIG["statistics"]["prefix"] + filename)

    out_file_name_csv = os.path.join(CONFIG["statistics"]["plot_folder"], CONFIG["statistics"]["prefix"] + filename + ".csv")
    stats = contentsFile.get_stats()
    stats_csv = stats.replace("\t", ",")
    stats_csv = re.sub(r'^[0-9]+\.\s+', "", stats_csv, flags=re.MULTILINE)

    with open(out_file_name, mode='w') as f:
        f.write(stats)

    with open(out_file_name_csv, mode='w') as csv:
        csv.write(stats_csv)

    contentsFile.set_plot_file(out_file_name_csv)

def print_results(stats, isFile=False):
    print("\n Here the 10 most used packages for the file: " + contentsFile.name \
          + "\n----------------------------------------")
    if isFile:
        with open(stats_file) as f:
            for line in f:
                print(line, end='')
    else:
        print(stats)
    print("----------------------------------------\n")


#################################
###     MAIN                   ##
################################
if __name__ == '__main__':
    print
    define_arguments()

    contentsFile = File.File(cmdargs)
    print(" Architecture was set to " + contentsFile.get_arch())
    print(" Repository URL is: "      + contentsFile.get_url())

    # check repo metadata to avoid downloading the same file twice
    stats_file = file_utils.check_remote_file(contentsFile)

    if stats_file:
        print("\n This stats are already computed! ")
        print_results(stats_file, True)
        plot_results(contentsFile)
        sys.exit()

    print(" Downloading file "+ contentsFile.get_name() +" ..")
    file_utils.download_file(contentsFile)
    print(" File downloaded")

    print(" File extraction in progress..")
    file_utils.extract_archive(contentsFile)
    print(" Extraction ended.")

    print(" Computing statistics, this may take a minute..")
    stats = contentsFile.compute_stats(cmdargs.engine)

    store_stats(contentsFile)
    print(" Statistics will be stored in "+ CONFIG["statistics"]["path"] + " folder")

    print_results(stats)

    plot_results(contentsFile)
