#!/home/notroot/.pyenv/shims/python
"""
Author: Joseph Edwards
"""
import os
import pybrat.installer as installer

# installer root is at this file
if __name__=="__main__":
    installer.main(os.path.dirname(os.path.abspath(__file__)))
