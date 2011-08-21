'''
@author: nomemory (Andrei Ciobanu)
@version: 0.1
'''

'''
@license: 
Copyright 2011 Andrei N. Ciobanu

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import abc
import argparse
import random
import re
import string
import sys
import textwrap

from xml.etree.ElementTree import ElementTree


#------------------------------------------------------------------------------
class AbstractDataSet(object):
    '''
    Abstract class base for data sets .
    Classes based on AbstractDataSet are dynamic and must implement 
    next_value() method .
    '''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, ds_dict):
        '''
        Subclasses will have a dynamic structure based on the 
        ds_dict dictionary .  
        '''
        for (k, v) in ds_dict.items():
            self.__dict__[k] = v
    
    @abc.abstractmethod
    def next_value(self):
        return
#------------------------------------------------------------------------------
class Number(AbstractDataSet):
    '''
    ds_dict will contain the following:
            { 
                "floating" : "<boolean value>" ,
                "min": "<integer value>",
                "max": "<integer value>"
            }
    '''
    def next_value(self):
        '''
        Returns a random value based on in the ds_dict properties .
        '''
        func = random.uniform if self.floating == 'True' else random.randint
        return func(int(self.min), int(self.max))
#------------------------------------------------------------------------------
class LoremIpsum(AbstractDataSet):
    
    lorem_impsum = textwrap.dedent('''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut quis justo leo. 
    Quisque congue elit eu ante euismod ut aliquam nisi bibendum. Donec mollis 
    ipsum nec sapien auctor ut blandit ante aliquet. Fusce eget ante nunc. 
    Praesent ullamcorper neque sit amet diam scelerisque condimentum. Nulla 
    faucibus, justo non pretium consequat, tortor ligula consequat elit, vitae 
    dapibus orci metus eget nisl. Fusce ante ante, placerat et gravida ac, 
    fermentum eu nisl. Aenean posuere, orci vel dapibus adipiscing, ipsum dui 
    imperdiet dolor, eu rutrum lorem dolor id felis. Curabitur accumsan enim et 
    ipsum volutpat feugiat. Vivamus eget diam eros, in volutpat justo. 
    Curabitur bibendum, velit ac fermentum tincidunt, dui nulla volutpat nulla, 
    in ornare dui turpis ultrices dolor. Sed gravida suscipit arcu, ut 
    scelerisque augue aliquet non. Sed sagittis, turpis id ullamcorper rhoncus, 
    lorem nisi fringilla leo, et tristique odio augue id tortor. Integer 
    vehicula imperdiet nisl, eu ultrices neque condimentum eu. Ut sed purus 
    diam, eu euismod diam. Fusce eget venenatis arcu. Mauris porta, enim vel 
    pretium sagittis, ligula elit rutrum magna, sed pulvinar orci elit sit amet
    leo. Pellentesque habitant morbi tristique senectus et netus et malesuada 
    fames ac turpis egestas.
    ''').strip().replace('\n','')
    
    '''
    ds_dict will contain the following :
    {
        "length" : "<integer value>"
    }
    ''' 
    def next_value(self):
        '''
        Returns a lorem ipsum text .
        '''
        div = int(int(self.length) / len(LoremIpsum.lorem_impsum))
        mod = int(self.length) % len(LoremIpsum.lorem_impsum)
        return div * LoremIpsum.lorem_impsum + LoremIpsum.lorem_impsum[:mod]
#------------------------------------------------------------------------------
class Name(AbstractDataSet):
    '''
    ds_dict will contain the following :
        {
            "firstname" : "<boolean value>",
            "lastname" : "<boolean value>"
        }
    '''
    
    ''' Popular first names in 2010 '''
    fname = ['Ava', 'Aaron', 'Agathe', 'Agnes', 'Alba', 'Alexander', 'Alexis',
    'Alvaro', 'Andrew', 'Andrei', 'Angelina', 'Anthony', 'Anna', 'Ariana',
    'Brian', 'Bogdan', 'Carmen', 'Cristopher', 'Connor', 'Daan',
    'Daniel', 'David', 'Diego', 'Ella', 'Elizabeth', 'Elsa',
    'Emma', 'Enzo', 'Ethan', 'Gabriel', 'Grace', 'Gustav',
    'Isaac', 'Jacob', 'Javier', 'Jayden', 'John', 'Juliette',
    'Kacper', 'Lars', 'Leah', 'Levi', 'Logan', 'Lotte', 'Lucas',
    'Lieke', 'Linus', 'Lucia', 'Mateusz', 'Maxime', 'Melvin',
    'Mia', 'Michael', 'Mikolaj', 'Milan', 'Natalie', 'Natalia',
    'Olivia', 'Oscar', 'Pablo', 'Paul', 'Paula', 'Piotr', 'Quentin',
    'Sarah', 'Samuel', 'Sophia', 'Sem', 'Szymon', 'Thijs', 'Teodore',
    'Valeria', 'Valter', 'William', 'Wilma' ]
    
    ''' Last names '''
    lname = ['Abbott', 'Alcott', 'Antonescu', 'Bartok', 'Bayard', 'Banciu',
    'Bethmann', 'Bergen', 'Botev', 'Brown', 'Bush', 'Corvinus',
    'Chehachkov', 'Dimitrof', 'Dinev', 'Delano', 'Eisenhower',  'Enescu',
    'Frels', 'Fugger', 'Gilman', 'Hancock', 'Hoza', 'Ionescu', 'Iordache',
    'Kalish', 'Kafka', 'Krasniki', 'Lukasewicz', 'McCormick', 'Medici',
    'Menier', 'Morgan', 'Palagyi', 'Parrocel', 'Romanov', 'Rozycki',
    'Rufus', 'Olaru', 'Otis', 'Schoenberger', 'Strauss', 'Somoza',
    'Sowinski', 'Szigete', 'Tessedik', 'Tisch', 'Vajda', 'Vlas',
    'Walker', 'Warhola', 'Varchol', 'Wojnar', 'Zelenjcik']
            
    def next_value(self):
        '''
        Returns a random string based on ds_dict properties 
        '''
        ret = ''
        if self.firstname == 'True':
            fname_idx = random.randint(0, 1000) % len(self.fname) 
            ret = ret + self.fname[fname_idx]
        if self.lastname == 'True':
            lname_idx = random.randint(0, 1000) % len(self.lname)
            if len(ret) > 0:
                ret = ' ' + ret
            ret = ret + self.lname[lname_idx]
        return ret
#------------------------------------------------------------------------------
class Sequence(AbstractDataSet):
    '''
     ds_dict will contain the following:
        {
            "start" : "<integer value>",
            "increment" : "<integer value>"
        }
    '''
    def __init__(self, ds_dict):
        ''' 
        We will need to @override the constructor in order to add 
        the _cval property (current value in sequence) .
        '''
        super(Sequence, self).__init__(ds_dict)
        self.__cval = int(self.start) - int(self.increment)
        
    def next_value(self):
        '''
        Returns the next value in the sequence by adding the increment to
        the current value
        '''
        self.__cval += int(self.increment)
        return self.__cval
#------------------------------------------------------------------------------
class DataSetBuilder(object):
    ''' 
    Returns a new instance of a data set based on 
    subclass name (see @get_name function) 
    '''
    def __init__(self):
        '''
        __classes will be a dictionary of AbstractDataSet subclasses 
        in the following form:
        {
            <__classname__1>:<__class_object__1>,
            <__classname__2>:<__class_object__2>,
            ...
        }
        '''
        #@PydevCodeAnalysisIgnore
        self.__classes = { c.__name__ : c for c in \
                        AbstractDataSet.__subclasses__()}
        
    def instantiate(self, name, ds_dict):
        ''' 
        Returns the instance of the class based on class name .
        Every object instantiated with this method will be instances
        of AbstractDataSet subclasses .
        '''
        return self.__classes[name](ds_dict)
#------------------------------------------------------------------------------
class DataSetEvaluator(object):
    def __init__(self, xml_filename):
        #Build element tree        
        self.__elem_tree = ElementTree()
        self.__elem_tree.parse(xml_filename)
        
        #Initialize class attributes
        self.instances = self.init_instances()
        self.instances_values = self.update_iterations_values()
        self.iterations = int(self.init_iterations())
        self.template = self.init_template()
    
    def init_instances(self):
        '''
        Parse __elem_tree to determine and instantiate the data
        set objects present in the XML file . 
        '''
        #Obtain all the <dataset> elements from the XML file
        instances = {}
        dsb = DataSetBuilder()
        dataset_list = list(self.__elem_tree.iter("dataset"))
        for dataset in dataset_list:
            dataset_name = dataset.attrib['name']
            dataset_type = dataset.attrib['type']
            # Create the ds_dict for the Abstract Data Set subclasses
            ds_dict = {key:value for (key,value) in dataset.attrib.items() if \
                        key != 'name' and key != 'type'}
            #Build instances of Data Sets  
            instances[dataset_name] = dsb.instantiate(dataset_type, ds_dict)
        return instances
    
    def init_iterations(self):
        '''
        Returns the number of iterations (how many subsequent lines
        to generate)
        '''
        return int(self.__elem_tree.getroot().attrib['iterations'])
    
    def init_template(self):
        '''
        Retrieves the template string from the XML file 
        '''
        return self.__elem_tree.findall('template')[0].text
    
    def update_iterations_values(self):
        '''
        Keep a dictionary with instances values to preserve next_value()
        across iteration . 
        '''
        return {key : instance.next_value() for (key, instance) in \
                self.instances.items()}
    
    def write_output(self, output=sys.stdout):
        '''
        Parse the template and write the output to a stream .
        The default stream is sys.stdout . 
        '''
        # Find all #{data_set_names} and replace them with
        # self.instances[data_set_name].next_value()
        regex = '(?:^|(?<=[^#]))#{\w+}'
        def inner_subst(matchobj):
            #Removing unneeded characters from key
            key = matchobj.group(0)
            for c in ['{','#','}']:
                key = key.replace(c,'')
            #replace #{word} with instance values .
            return str(self.instances_values[key])
        for i in range(self.iterations):
            output.write(re.sub(regex, inner_subst, self.template) + '\n')
            self.instances_values = self.update_iterations_values()
        
#------------------------------------------------------------------------------

if __name__ == '__main__':
#    ap = argparse.ArgumentParser(description='Generate test data.')
#    ap.add_argument('-i','--input', dest='ifile', help='the input file (XML)')
#    ap.add_argument('-o','--output', dest='ofile',
#                     help='the output file (TEXT)')
#    
#    results = ap.parse_args()
#    if results.ifile is None:
#        ap.error('Input file (IFILE) cannot be empty')
#        sys.exit(-1)
#    
#    dsv = DataSetEvaluator(results.ifile)
#    
#    if results.ofile is None:
#        dsv.write_output()
#    else:
#        out = open(results.ofile, mode='w')
#        dsv.write_output(output=out)
#        out.close()
    t = LoremIpsum({'length' : '5'})
    print(t.next_value())