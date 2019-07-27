from collections import Counter
from pathlib import Path


def compute_stats(file_path):
    packages = []
    with open(file_path, encoding="utf8") as f:
        for line in f:
            pkg_tmp = line.split()[1]
            if ',' in pkg_tmp:
                pkg_tmp = pkg_tmp.split(",")
            if isinstance(pkg_tmp, str):
                packages.append(pkg_tmp)
            else:
                packages += pkg_tmp

    ''' --- solution 1 ---
    pkg_stats = dict(Counter(packages))
    pkg_stats_sort = sorted(pkg_stats, key=pkg_stats.__getitem__, reverse=True)
    count = 0
    for k in pkg_stats_sort:
        count += 1
        print(str(count) + ".\t" + k +"\t"+ str(pkg_stats[k]))
        if count == 10:
            break
    '''
    # --- solution 2 ---
    pkg_stats = Counter(packages)
    most_common = pkg_stats.most_common(10)
    stats_tmp = list(
        map(
            lambda x: "{:<4}".format(str(most_common.index(x) + 1) + ". ") +
                      "{:<60}".format(x[0]) +
                      str(x[1]) + "\n",
            most_common
        ))
    stats = ''.join(stats_tmp)
    return stats


# --- For testing
if __name__ == '__main__':
    compute_stats(Path("../download/Contents-udeb-i386_23-Jun-2019_0758"))
