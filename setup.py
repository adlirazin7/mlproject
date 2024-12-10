from typing import List
from setuptools import find_packages, setup # type: ignore


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    with open('requirements.txt') as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements



setup(
    name='mlproject',
    version='0.0.1',
    author='Adli',
    author_email='adlirazin7@yahoo.com',
    description="A ML project",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    packages=find_packages(), # Automatically finds all packages and sub-packages
    install_requires= get_requirements('requirements.txt') # In case of too much packages, proceed with requirements.txt
)