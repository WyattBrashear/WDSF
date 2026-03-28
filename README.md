# Wyatt's Data Storage Format (WDSF)
## What Is It?
WDSF is a data storage format that uses text:key pairs.
This is similar to JSON, but unlike JSON it is partially programmatic.
WDSF Files are internally converted to Dictionary objects so they can be easily used in a program.
Currently, it can be modified by using the official python library.
## Library Documentation
Reading a WDSF file and convert it to a Dictionary object:
```python
import wdsflib
wdsf_file = wdsflib.WDSFFile(file_name)
wdsf_data = wdsf_file.read() #Returns a dictionary that can be used in wdsf_data.get('key')
```
