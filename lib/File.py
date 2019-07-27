import subprocess
import sys
from pathlib import Path

import yaml

from lib import statistcs_engine

with open(Path("config/config.yaml"), mode='r') as configFile:
    CONFIG = yaml.load(configFile, Loader=yaml.Loader)
    # print(CONFIG)


class File:
    """ class used to store attributes and methods of the downloaded archive
    @:var name will contain also the path of the extracted file
    """
    arch = None
    repo = None
    filename_path = None
    archive_name  = None
    statistics    = ""
    last_update_date = None
    creation_date = None
    plot_file = None

    def __init__(self, cmdargs):
        self.arch = cmdargs.arch
        self.repo = CONFIG["repo"]["url"]
        self.filename_path  = Path("Contents-" + self.arch)
        self.archive_name   = Path(self.filename_path.name + ".gz")
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

    def get_filename_path(self):
        return self.filename_path

    def set_archive_name(self, an):
        self.archive_name = an

    def set_name(self, n):
        if not isinstance(n, Path):
            raise TypeError(" Store only paths as objects. Tried to store "+ n + " of type "+ str(type(n)))

        self.filename_path = n

    def set_creation_date(self, cd):
        self.creation_date = cd

    def set_plot_file(self, csv_file):
        self.plot_file = csv_file

    def get_plot_file(self):
        return self.plot_file

    def compute_stats(self, engine):
        """ Based on the type of engine it will compute the stats for the file
            bash: will run a fast external script, located in the lib folder
            python: should elaborate in a more pythonic and modern way
        :return: the statistics as a string
        """
        file_path = CONFIG["downloadFolder"]+"/"+self.filename_path.name

        if engine == 'bash':
            command = [str(Path("bash ./lib/statistics_engine.sh")), file_path]
            bash_child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            line_count = 1
            for line in iter(bash_child.stdout.readline, b''):
                out_string = "{:<4}".format(str(line_count)+". ") + line.decode(sys.stdout.encoding)
                # sys.stdout.write(out_string)
                self.statistics += out_string
                line_count += 1
        else:
            self.statistics = statistcs_engine.compute_stats(file_path)
        return self.statistics

