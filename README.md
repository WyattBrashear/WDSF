# Wyatt's Data Storage Format (WDSF)
## What Is It?
WDSF is a data storage format that uses text:key pairs.
This is similar to JSON, but unlike JSON it is partially programmatic.
WDSF Files are internally converted to Dictionary objects so they can be easily used in a program.
Currently, it can be modified by using the official python library.
## How to write a WDSF file
A WDSF file is simple enough that it can be written by hand.
Heres how to write one:
All files must be started with a header:
```text
#WDSF1.0
```

This is the most simple data structure:
```text
key|value
```
That is it. But, there is also a list type:
```text
!LIST|LIST_NAME:
1
2
3
4
5
6
7
8
9
10
!LIST_END
```
There is also a programmatic way to use WDSF, similar to Flask's Template Rendering System:
```text
COOL_DATA|!#FUNC:x*y
```
These arguments will be passed and evaluated at time of reading:
```python
wdsf_file.read(args=[["x", 10], ["y", 20]])
```
For compatibility reasons, all data types (excluding lists) are treated as strings.
## Library Documentation
Reading a WDSF file and convert it to a Dictionary object:
```python
import wdsflib
wdsf_file = wdsflib.WDSFFile(file_name)
wdsf_data = wdsf_file.read() #Returns a dictionary that can be used in wdsf_data.get('key')
```
Transmutation of a file is a process that converts a WDSF file into a JSON file it can be used like this:
```python
import wdsflib
wdsf_file = wdsflib.WDSFFile(file_name)
wdsf_file.transmute("output.json")
```
And there is a function that can do the opposite:
```python
import wdsflib
dict_object = {
    "key": "value"
}
#Convert the dictionary to a WDSF file
wdsflib.convert_to_wdsf(dict_object, f"{file_name}.wdsf")
```
## Installation

```bash
pip install wdsf
```