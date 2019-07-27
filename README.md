## Readme
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

### Caching
> “If you love life, don’t waste time, for time is what life is made up of.” 

Using a web scraper, the datetime of file creation is taken and saved
with the file name. In this way in the next run the script can detect
if computing power and user time can be saved. 

### Plotting
```
$ python package_statistics.py udeb-i386 --engine=bash --showPlot
```

After statistics has been computed or found in cache a plot will be 
elaborated and stored in the plot dir.
If the `--showPlot` is given it will be also shown.
 
### Clean run
```
$ python package_statistics.py --clear --engine=python i386
```
Using the `--clear` argument you can be sure to not use ant cached
file and to download the online repo.
 
## Known Issues
- Try/catches on https connections and I/O streams
- Hardcoded strings
- Bash output is ugly

## Development Timing
I started searching a one line bash solution the evening of the 
same day, I spent an hour before to understand I misunderstood 
specifications coming to a solution like this `$ awk 'BEGIN{ FS="," } { if (NF > max) {max=NF; line=$0}} END{ print line }' Contents-amd64_small`

**3h**: When at home I cleaned up a little the new bash solution coming to this
```
# DON’T FORGET THE DOT
awk '{print $2}' $1 | egrep -o "[/.a-zA-Z0-9_-]+" | sort | uniq -cdi | sort -nr | awk 'BEGIN{i=0} { if (i<10){ print $2 " " $1; i++;} }'
```  

**~ 3h**: In the second evening I woked on the interface, argument parsing, modules
creation like an external config file and a cleaner skeleton.

**~ 5h**: On Thursday I was already in the flow and I continued adding features
and debugging early in the morning before work and in the evening after
that.
 Here I started to work on the caching feature and to merge some 
 duplicated code.
 
**~ 5h**: On Friday I had the idea to add graphs of the statistics. I've already used
them for a data mining project long ago and I'd loved them.

**~ 5h**: On saturday I added the Python engine not being sure of the 
jury reaction to a bash engine for a python homework.
Another reason is that I wanted to use some of the most modern python
features like Collections Counter, lambda functions and so on.

So I would say I spent around 20 hours for all the application, it is hard
to say since I worked on it also during my job hours between tasks. 

I used PyCharm Community 2019.2 as IDE on Ubuntu 19.04.
