#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import itertools
import sys
from pathlib import Path

import yaml

from lib import File
from lib import file_utils

with open(Path("config/config.yaml"), mode='r') as configFile:
    CONFIG = yaml.load(configFile, Loader=yaml.Loader)

cmdargs = None


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
                        help="the core module computing the statistics can be a bash script" \
                             "or a Python one.")
    parser.add_argument('--clear', default=False, action='store_true')
    parser.add_argument('--showPlot', default=False, action='store_true',
                        help="show the plot at the end of the script executio")
    cmdargs = parser.parse_args()


def print_results(stats, isFile=False):
    useless_bar = '-' * 70
    print("\n Here the 10 most used packages for the file: " + contentsFile.filename_path.name \
          + "\n" + useless_bar)
    if isFile:
        with open(stats_file) as f:
            for line in f:
                print(line, end='')
    else:
        print(stats)
    print(useless_bar + "\n")


#################################
#      MAIN                   ##
################################
if __name__ == '__main__':
    define_arguments()

    contentsFile = File.File(cmdargs)
    print(" Architecture was set to " + contentsFile.get_arch())
    print(" Repository URL is: " + contentsFile.get_url())

    # clear all artifacts
    if cmdargs.clear:
        print(" Cleaning old files..")
        plot_list = Path(CONFIG["statistics"]["plot_folder"]).glob("*.png")
        csv_list  = Path(CONFIG["statistics"]["plot_folder"]).glob("*.csv")
        stat_list = Path(CONFIG["statistics"]["folder"]).glob("statistics_*")
        down_list = Path(CONFIG["downloadFolder"]).glob("*")
        for file in itertools.chain(plot_list, csv_list, stat_list, down_list):
            file.unlink()

    # check repo metadata to avoid downloading the same file twice
    stats_file = file_utils.check_remote_file(contentsFile)

    if stats_file:
        print("\n This stats are already computed! ")
        print_results(stats_file, True)
        file_utils.plot_results(contentsFile, cmdargs.showPlot)
        sys.exit()

    print(" Downloading file " + contentsFile.get_filename_path().name + " ..")
    file_utils.download_file(contentsFile)
    print(" File downloaded")

    print(" File extraction in progress..")
    file_utils.extract_archive(contentsFile)
    print(" Extraction ended.")

    print(" Computing statistics, this may take a minute..")
    stats = contentsFile.compute_stats(cmdargs.engine)

    file_utils.store_stats(contentsFile)
    print(" Statistics will be stored in " + CONFIG["statistics"]["folder"] + " folder")

    print_results(stats)

    file_utils.plot_results(contentsFile, cmdargs.showPlot)
