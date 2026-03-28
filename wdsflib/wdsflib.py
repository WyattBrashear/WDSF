import json

class WDSFFile:
    """
    WDSFFile Class: Handles core WDSF file operations and parsing including: reading and transmutation
    """
    #Intialize the class
    def __init__(self, file):
        self.file = file
    def read(self, execute=True, args=None):
        """
        Reads a WDSF file and returns the results as a Dictionary object.
        Arg Info:
            execute: A boolean flag (By default set to True) on whether to execute function data inside a WDSF file
            args: a list object (Specifically a nested list) that contains the arguments to be passed to the functions inside the WDSF file
        :param execute:
        :param args:
        :return:
        """
        with open(self.file, 'r') as f:
            #Prepare the variables
            returning_dict = {}
            reading_list = False
            list_data = []
            is_wdsf_file = False
            # Verify that the file is a WDSF file
            if f.readline().startswith('#WDSF') and not is_wdsf_file:
                is_wdsf_file = True
            else:
                raise Exception('File is not a valid WDSF file!')
            f.seek(0)
            for line in f:
                if not is_wdsf_file:
                    break
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
                        if not execute:
                            continue
                        #Special Statement Handler
                        if args is None:
                            raise Exception('No arguments provided for function!')
                        if value.startswith('!#FUNC'):
                            function_name = str(value.split(':')[1]).replace('\n', '')
                            rules_dict = {}
                            for arg, arg_value in args:
                                rules_dict.update({arg: arg_value})
                            #Ensure the rules do not allow builtins
                            rules_dict.update({'__builtins__': {}})
                            exec(f"__result__ = {function_name}", rules_dict)
                            result = rules_dict['__result__']
                            value = result
                    #Update the returning dictionary
                    returning_dict.update({key: str(value).replace('\n', '')})
            #Return the dicitonary
            return returning_dict

    def transmute_file(self, output_file, reading_args=None):
        """
        Convert a WDSF file to a JSON file
        :param output_file:
        :param reading_args:
        :return:
        """
        writing_dict = self.read(args=reading_args)
        with open(output_file, 'w') as f:
            json.dump(writing_dict, f, indent=4)


def convert_to_wdsf(data, output_file):
    """
    Convert a Dictionary object to a WDSF file.
    :param data:
    :param output_file:
    :return:
    """
    with open(output_file, 'w') as f:
        f.write("#WDSF1.0")
        for key, value in data.items():
            if type(value) is list:
                f.write(f'!LIST|{key}\n')
                for item in value:
                    f.write(f"{item}\n")
                f.write('!LIST_END\n')
            else:
                f.write(f'{key}|{value}\n')
