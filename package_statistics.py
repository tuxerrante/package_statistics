#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import yaml

# ------ GLOBAL VARS ------
cmdargs = None
CONFIG = None
# ------


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


class File:
    arch = None
    repo = None
    name = None
    archive_name = None
    statistics = ""
    last_update_date = ""

    def __init__(self):
        self.arch = cmdargs.arch
        self.repo = CONFIG["repo"]["url"]
        self.name = "Contents-" + self.arch
        self.archive_name   = self.name + ".gz"
        self.file_directory = "download"
        self.statistics     = ""
        self.last_update_date    = os.path.getmtime(os.path.join(self.file_directory,self.archive_name))

    def get_last_update_date(self):
        return self.last_update_date

    def get_arch(self):
        return self.arch

    def get_archive_name(self):
        return self.archive_name

    def get_url(self):
        return self.repo

    def get_stats(self):
        return self.statistics

    def compute_stats(self, engine):
        """ Based on the type of engine it will compute the stats for the file
            bash: will run a fast external script, located in the lib folder
            python: should elaborate in a more pythonic and modern way
        :return: the statistics as a string
        """
        if engine == 'bash':
            file_path = "./" + self.file_directory + "/" + self.name + "_small"
            command = ["./lib/package_statistics.sh", file_path]
            bash_child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

            for line in iter(bash_child.stdout.readline, b''):
                out_string = line.decode(sys.stdout.encoding)
                # sys.stdout.write(out_string)
                self.statistics += out_string
        else:
            # TODO: use pandas to compute big data files
            pass

        return self.statistics

    def download_file(arch, filename):
        """ download the given file from the repo
        :param filename
        :return:
        """
        pass



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
    last_update_date = datetime.fromtimestamp(contentsFile.get_last_update_date())\
                        .strftime("%Y%m%d_%H%M%S")
    filename = contentsFile.get_archive_name()
    out_file_name = os.path.join("statistics","statistics_" + filename +"_"+ last_update_date)

    # print(" Last modification of the archive file "+ filename +": "+ last_update_date)
    # TODO: csv
    with open(out_file_name, mode='w') as f:
        f.write(contentsFile.get_stats())


if __name__ == '__main__':
    print
    define_arguments()

    contentsFile = File()
    print(" Architecture was set to " + contentsFile.get_arch())
    print(" Repository URL is: " + contentsFile.get_url())

    stats = contentsFile.compute_stats(cmdargs.engine)

    store_stats(contentsFile)

    print("\n Here the 10 most used packages for the file: " + contentsFile.name \
          + "\n-----------------------------"\
          + "\n" + str(stats)
          + "-----------------------------")

    # plot_results(stats)
