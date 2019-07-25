import subprocess
import sys

import yaml

with open('config/config.yaml', mode='r') as configFile:
    CONFIG = yaml.load(configFile, Loader=yaml.Loader)
    # print(CONFIG)


class File:
    arch = None
    repo = None
    name = None
    archive_name = None
    statistics = ""
    last_update_date = None
    creation_date = None

    def __init__(self, cmdargs):
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

