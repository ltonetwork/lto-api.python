import configparser
import os

config = configparser.ConfigParser()


# Just a small function to write the file
def writeFile(fileName):
    config.write(open(fileName, 'w'))


if not os.path.exists('config.ini'):
    config['testing'] = {'test': '45', 'test2': 'yes'}
    writeFile("config.ini")
else:
    config.read('config.ini')
    print(config.sections())
    #print(config.options('testing'))
    x = config.getboolean('testing_2','a')
    '''config.add_section('testing_2')
    config.set('testing_2', 'A', 'True')
    config.set('testing_2','B', '10')
    writeFile('config.ini')'''
    print(x)
    print(type(x))
'''# parse existing file
config.read('test.ini')

# read values from a section
string_val = config.get('section_a', 'string_val')
bool_val = config.getboolean('section_a', 'bool_val')
int_val = config.getint('section_a', 'int_val')
float_val = config.getfloat('section_a', 'pi_val')

# update existing value
config.set('section_a', 'string_val', 'world')

# add a new section and some values
config.add_section('section_b')
config.set('section_b', 'meal_val', 'spam')
config.set('section_b', 'not_found_val', '404')

#config.remove_section('testing')
#config.remove_option('testing', 'test2')'''
