#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys

import yaml
from matplotlib import pyplot as plt

# ------ GLOBAL VARS ------
from lib import file_utils

cmdargs = None
# CONFIG = None
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
    last_update_date = None
    creation_date = None

    def __init__(self):
        self.arch = cmdargs.arch
        self.repo = CONFIG["repo"]["url"]
        self.name = "Contents-" + self.arch
        self.archive_name   = self.name + ".gz"
        self.file_directory = "download"
        self.statistics     = ""
        self.last_update_date = None

    def get_creation_date(self):
        return self.creation_date

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

    def get_name(self):
        return self.name

    def set_archive_name(self, an):
        self.archive_name = an

    def set_name(self, n):
        self.name = n

    def set_creation_date(self, cd):
        self.creation_date = cd

    def compute_stats(self, engine):
        """ Based on the type of engine it will compute the stats for the file
            bash: will run a fast external script, located in the lib folder
            python: should elaborate in a more pythonic and modern way
        :return: the statistics as a string
        """
        if engine == 'bash':
            file_path = self.name
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


if __name__ == '__main__':
    print
    define_arguments()

    contentsFile = File()
    print(" Architecture was set to " + contentsFile.get_arch())
    print(" Repository URL is: " + contentsFile.get_url())

    # check repo metadata to avoid downloading the same file twice
    stats_file = file_utils.check_remote_file(contentsFile)

    if stats_file:
        print(" The stats are already computed: ")
        with open(stats_file) as f:
            for line in f:
                print(line, end='')
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
    print(" Statistics are stored in "+ CONFIG["statistics"]["path"] + " folder")

    print("\n Here the 10 most used packages for the file: " + contentsFile.name \
          + "\n-----------------------------"\
          + "\n" + str(stats)
          + "-----------------------------")

    # plot_results(stats)
