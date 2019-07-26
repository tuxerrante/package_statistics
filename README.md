## Readme
### Stats Calculation
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

### Download
A HTTP request will invoke the [Debian repo](http://ftp.uk.debian.org/debian/dists/stable/main/)
searching for the Contents-ARCH.gz file bsaed on the given argument.
The acceptable archs are set in the config file.

### Caching
> “If you love life, don’t waste time, for time is what life is made up of.” 

Using a web scraper, the datetime of file creation is taken and saved
with the file name. In this way in the next run the script can detect
if computing power and user time can be saved. 

### Plotting
After statistics has been computed or found in cache a plot will be 
elaborated and stored in the plot dir.
 
## Known Issues
- try/catches on https connections and I/O streams
- hardcoded strings

## TODO
- double engine: Python and Bash
- a lot of ugly hardcoded code should be cleaned