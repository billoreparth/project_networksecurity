from setuptools import find_packages,setup 
from typing import List

# this functions will be used to get all requirements 
def get_requirements()->List[str]:
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file :
            lines = file.readlines()
            for i in lines :
                requirement=i.strip()
                # ignoring -e . 
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    
    except FileNotFoundError:
        print("requiremets.txt not found")

    return requirement_list

print(get_requirements())

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Parth Billore',
    author_email='billoreparth80@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)