#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys

import yaml
from matplotlib import pyplot as plt

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





def plot_results(stats_file):
    """ plot the results in a shiny statistics
    TODO: to move in external module
    :param stats_file:
    :return:
    """
    with open(stats_file) as csv_in:
        pkg_name, files = [line.strip().split(',') for line in csv_in]
        plt.plot(pkg_name, files)
    plt.show()


def store_stats(contentsFile):
    """
    Repo time format:
        last modified date: 03-Jul-2019 14:16
        creation date:
    :param contentsFile:
    :return:
    """
    filename = contentsFile.get_name().split("/")[1]
    out_file_name = os.path.join(CONFIG["statistics"]["path"], CONFIG["statistics"]["prefix"] + filename)

    # print(" Last modification of the archive file "+ filename +": "+ last_update_date)
    # TODO: plots/csv
    with open(out_file_name, mode='w') as f:
        f.write(contentsFile.get_stats())


def print_results(stats, isFile=False):
    print("\n Here the 10 most used packages for the file: " + contentsFile.name \
          + "\n----------------------------------------")
    if isFile:
        with open(stats_file) as f:
            for line in f:
                print(line, end='')
    else:
        print(stats)


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
        print(" The stats are already computed! ")
        print_results(stats_file, True)
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
    '''
    print("\n Here the 10 most used packages for the file: " + contentsFile.name \
          + "\n-----------------------------"\
          + "\n" + str(stats)
          + "-----------------------------")
    '''
    # plot_results(stats)
