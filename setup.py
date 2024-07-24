from setuptools import find_packages, setup
from typing import List

PATH = r'D:\udemy-ml-project\Udemy-ML-Project\requirements.txt'
# constant
HYPEN_E_DOT = "-e ."


def get_requirements(PATH:str)->List[str]:
    """
    this function will return the listv of required libraries

    """
    with open(PATH) as file:
        requirements = file.readlines()
        # replace \n 
        requirements = [req.replace("\n",'') for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements


    


setup(
    name= "ML Project",
    version= "0.1",
    author= "Yogesh",
    author_email= "yogeshsingh0286@gmail.com",
    packages= find_packages(),
    install_requires = get_requirements(PATH)
)
