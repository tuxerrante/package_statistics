#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys

import yaml

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
    parser.add_argument('--showPlot', default=False, action='store_true')
    cmdargs = parser.parse_args()


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
        file_utils.plot_results(contentsFile, cmdargs.showPlot)
        sys.exit()

    print(" Downloading file "+ contentsFile.get_name() +" ..")
    file_utils.download_file(contentsFile)
    print(" File downloaded")

    print(" File extraction in progress..")
    file_utils.extract_archive(contentsFile)
    print(" Extraction ended.")

    print(" Computing statistics, this may take a minute..")
    stats = contentsFile.compute_stats(cmdargs.engine)

    file_utils.store_stats(contentsFile)
    print(" Statistics will be stored in "+ CONFIG["statistics"]["path"] + " folder")

    print_results(stats)

    file_utils.plot_results(contentsFile, cmdargs.showPlot)
