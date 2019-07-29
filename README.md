## Readme

Please install some dependecies if missing in your system:
`pip install numpy pyyaml matplotlib requests`

This app is intended to be used with Python 3.

I used PyCharm Community 2019.2 as IDE on Ubuntu 19.04.

### Statistics Calculation
The core of the application is a script to compute the 10 most used 
packages per architecture.  
The output will be of the format: 
```
$ python package_statistics.py udeb-i386 --engine=bash

----------------------------------------
1.  debian-installer/brltty-udeb        351
2.  debian-installer/xkb-data-udeb      291
```
In addition to that a file with the results will be stored in statistics folder
and possibly a plot and csv file in the plot folder.

You can use two core engines using `--engine=python` or `--engine=bash`,
otherwise the python one will be used as default.

The architecture argument is mandatory and must be one of the
ones in the config file.

The `-h` argument will show a help menu.

### Download
A HTTP request will invoke the [Debian repo](http://ftp.uk.debian.org/debian/dists/stable/main/)
searching for the Contents-ARCH.gz file bsaed on the given argument.
The acceptable archs are set in the config file.

It uses a streming connection to deal with big files. 

### Caching
> “If you love life, don’t waste time, for time is what life is made up of.” 

Using a web scraper, the datetime of file creation is taken and saved
with the file name. In this way in the next run the script can detect
if computing power and user time can be saved. 

### Double engine
As default the engine will be the Python one, otherwise you can choose 
the bash script.
```
$ python package_statistics.py udeb-i386
```
```
$ python package_statistics.py udeb-i386 --engine=bash
```

### Plotting
```
$ python package_statistics.py udeb-i386 --showPlot
```

After statistics has been computed or found in cache a plot will be 
elaborated and stored in the plot dir.
If the `--showPlot` is given it will be also shown.
 
### Clean run
```
$ python package_statistics.py --clear i386git
```
Using the `--clear` argument you can be sure to not use ant cached
file and to download the online repo.
 
## Known Issues
- no unit tests
- The bash engine doesn't work on Windows
- Bash output is ugly
- Sometimes [a warning](https://gitlab.gnome.org/GNOME/glib/commit/a919be3d39150328874ff647fb2c2be7af3df996) is shown from glib



