# Random-Name-Generator

### Video Demo:  (https://youtu.be/u5JaREUvGig)

### Description:
This Python script generates a random full name. 
  
Generated full names can be configured to be a male name or a female name. Furthermore, you can specify what country you want the name to come from. You can set these configurations as arguments in the command line, for example:

```
% python3 random_name_generator.py --gender female --country Italy
  Ginevra Lucero
```

The script works by extracting data for the first name from https://en.wikipedia.org/wiki/List_of_most_popular_given_names and the last name from https://namecensus.com/last-names/.

The script has a caching system. On first run, it will extract and read the data from the above mentioned websites, and once output is done, create a Pickle file on disk. Additional runs of the script will then no longer extract data from the web, but from the Pickle files. Once the files are over 24 hours old, the next run of the script will run as if there were no Pickle files and extract data from the above mentioned websites, it will then override the old cache Pickle file with a new one.

The script uses a Pickle file to cache the data. I had thought of using a CSV file, however, after researching about the pros and cons of Pickle file format vs CSV I believed the pros outweighed the cons. To recap my research: 
Pros - The pickle format is faster at saving and faster at loading data compared to CSV. Furthermore, Pickle file format requires less disk space than a CSV.
Cons - Pickle format is stored as a byte stream, which means they are non-human readable and they can be generated via Python programming language only.

There is already a random name generator module for Python, https://github.com/treyhunner/names/blob/master/README.rst, however this module does not provide the configuration option of selecting country of name. Furthermore, the this module uses data from a static file on disk, meaning it doesn't fetch fresh name data from the web. For most purposes this module is fine, but if you want an over engineered version, you've come to the right place!
