import os

class WDSFFile:
    def __init__(self, file):
        self.file = file
    def read(self, args=None):
        with open(self.file, 'r') as f:
            returning_dict = {}
            reading_list = False
            list_data = []
            for line in f:
                #Handle comments
                if line.startswith('#'):
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
                        list_data = []
                #Handle Data
                else:
                    key, value = line.split('|')
                    #Handle Functions
                    if value.startswith('!#'):
                        #Special Statement Handler
                        if args is None:
                            raise Exception('No arguments provided for function!')
                        if value.startswith('!#FUNC'):
                            function_name = str(value.split(':')[1]).replace('\n', '')
                            rules_dict = {}
                            for arg, arg_value in args:
                                rules_dict.update({arg: arg_value})
                            rules_dict.update({'__builtins__': {}})
                            exec(f"__result__ = {function_name}", rules_dict)
                            result = rules_dict['__result__']
                            value = result
                    returning_dict.update({key: str(value).replace('\n', '')})
            return returning_dict

def convert_to_wdsf(data, output_file):
    with (open(output_file, 'w') as f):
        for key, value in data.items():
            if type(value) is list:
                f.write(f'!LIST|{key}\n')
                for item in value:
                    f.write(f"{item}\n")
                f.write('!LIST_END\n')
            else:
                f.write(f'{key}|{value}\n')




