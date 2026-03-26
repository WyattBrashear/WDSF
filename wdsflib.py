import os

class WDSFFile:
    def __init__(self, file):
        self.file = file
    def read(self):
        with open(self.file, 'r') as f:
            returning_dict = {}
            reading_list = False
            list_data = []
            for line in f:
                print(reading_list)
                #Handle comments
                if line.startswith('#'):
                    continue
                if "{" or "}" in line:
                    continue
                if reading_list and not line.startswith('!'):
                    list_data.append(line.replace('\n', ''))
                    continue
                #If line starts with !, treat it as a special statement
                if line.startswith('!'):
                    #Handle List Objects
                    if line.startswith('!LIST|'):
                        reading_list = True
                        list_name = line.split('|')[1].replace('\n', '').replace(':', '')
                    #Terminate list readings.
                    if line.startswith('!LIST_END'):
                        returning_dict.update({list_name: list_data})
                        reading_list = False
                        list_data = [
                #Handle Data
                else:
                    key, value = line.split('|')
                    returning_dict.update({key: value.replace('\n', '')})
            return returning_dict
    def execute(self, args, output):
        with open(output, 'w') as f:
            with open(self.file, 'r') as file:
                line_numbers = []
                for line in file:
                    if '|' in line:
                        if line.split('|')[1].startswith('{'):
                            '''
                            Yes I understand this is extremely insecure, but i think it may be the best option for what
                            This project is aiming to accomplish.
                            '''
                            rules_dict = {}
                            for arg, value in args:
                                rules_dict.update({arg: value})
                            rules_dict.update({'__builtins__': {}})
                            exec(line.split('|')[1].replace('{', '').replace('}', '').replace('\n', ''), rules_dict)
                            result = rules_dict['__result__']
                            data_name = line.split('|')[0]
                            lines = file.readlines()  # Convert to list first
                            line_numbers.append(lines.index(line))


