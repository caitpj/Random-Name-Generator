# Random-Name-Generator

### Video Demo:  <URL HERE>

### Description:
This Python script generates a random full name. 
  
Generated full names can be configured to be a male name or a female name. Furthermore, you can specify what country you want the name to come from. You can set these configurations as arguments in the command line, for example:

```
% python3 random_name_generator.py --gender female --country Italy
  Ginevra Lucero
```

The script works by extracting data for the first name from https://en.wikipedia.org/wiki/List_of_most_popular_given_names and the last name from https://namecensus.com/last-names/.
  
The script has a caching system. On first run, it will extract the data from the above mentioned websites and create a Pickle file on disk. Additional runs of the script will then no longer extract data from the web, but from the Pickle files. Once the files are over 24 hours old, the next run of the script will run as if there were no Pickle files and extract data from the above mentioned websites, it will then overide the old cache Pickle file with a new one.
