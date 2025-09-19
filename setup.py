'''
The setup.py file is an essential part of packaging and distributing Python Projects. It is used by setuptools
(or disutils in older Python versions) to define the configuration of your project, such as its metadata, dependencies, and more
'''

from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT='-e.'

def get_requirements()-> List[str]:
    '''
        This function will return list of requirements
    '''
    requirement_lst: List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                ## ignore empty lines
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
            return requirement_lst
                    
    except FileNotFoundError:
        print("requirements.txt file not found")
setup(
    name='NETWORKSECURITYMLOPS',
    version='0.0.1',
    author='Niranjana Subramanian',
    author_email='subramanianniranjana@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)