import gzip
import os
import re

import numpy as np
import requests
import yaml
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

with open('config/config.yaml', mode='r') as configFile:
    CONFIG = yaml.load(configFile, Loader=yaml.Loader)


def plot_results(contentsFile, showPlot):
    """ plot the results in a shiny bar chart

    :param contentsFile: file object
    :return:
    """
    csv_file = os.path.join(CONFIG["statistics"]["plot_folder"], CONFIG["statistics"]["prefix"]
                            + contentsFile.get_name() +"_"
                            + contentsFile.get_creation_date()
                            + ".csv")
    # print(" Searching for plot data in "+ csv_file)

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
    packages  = [''] + packages
    # 0 needs to be added
    files_num = list(reversed([t[1] for t in data]))
    files_num = ['0'] + files_num
    # preparing the horizontal bar chart
    figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
    plt.barh(np.arange(len(packages)), files_num, align='center')
    plt.yticks(np.arange(len(packages)), packages)
    plt.subplots_adjust(left=0.3)
    plt.title(" Most used packages")
    plt.savefig(csv_file[:-3]+"png", bbox_inches='tight', dpi=100)
    print(" Plot saved")
    # maybe is too annoying to show the plot without asking, let's just save it
    if showPlot:
        plt.show()


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


def download_file(contentsFile):
    """
    Streaming is needed to download big files
    :param the file object instance
    :return:
    """
    url = CONFIG["repo"]["url"] + contentsFile.get_archive_name()
    creation_date = contentsFile.get_creation_date()

    local_archive_name = os.path.join("download", url.split('/')[-1])[:-3] +"_"+ creation_date + ".gz"

    contentsFile.set_creation_date(creation_date)
    contentsFile.set_archive_name(local_archive_name)
    contentsFile.set_name(local_archive_name)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_archive_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    return local_archive_name


def check_remote_file(contentsFile):
    """ Website scraper: using the following structure
        it extracts the creation date of the file.

        If the stats for that file are already present locally
        it returns them

        <a href="Contents-amd64.gz">Contents-amd64.gz</a>
            03-Jul-2019 14:16 = "%d-%b-%Y %H:%M"
    :param contentsFile: the file object
    :return: stats file or None
    """
    archive_name = contentsFile.get_archive_name()

    http_response = requests.get("http://ftp.uk.debian.org/debian/dists/stable/main/")
    resp_text = http_response.text

    right_string  = resp_text.split(archive_name+"</a>", 1)[1]
    creation_date = str(right_string).strip().split("  ")[0]

    creation_date_clean = creation_date.replace(" ","_").replace(":","")

    # This will be used by the download function for naming the file uniquely
    contentsFile.set_creation_date(creation_date_clean)

    # stats_filename = os.path.join(CONFIG["statistics"]["path"], archive_name +"_"+ creation_date_clean)
    stats_filename = os.path.join(
        CONFIG["statistics"]["path"],
        CONFIG["statistics"]["prefix"] +
        archive_name[:-3] + "_" +
        creation_date_clean)

    if os.path.isfile(stats_filename):
        return stats_filename
    else:
        return None


def extract_archive(contentsFile):
    """
    Extract the gzipped archive in a file with same name without extension
    :param archive_name:
    :return:
    """
    archive_path  = contentsFile.get_archive_name()
    creation_date = contentsFile.get_creation_date()

    # archive_path  = os.path.join(CONFIG["downloadFolder"], archive_name +"_"+ creation_date)
    out_file_name = archive_path[:-3]
    contentsFile.set_name(out_file_name)

    with gzip.open(archive_path, 'rb') as infile:
            with open(out_file_name, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)
    return True