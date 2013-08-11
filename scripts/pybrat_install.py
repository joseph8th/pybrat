#!/usr/bin/env python
"""
Author: Joseph Edwards
"""
import os
import installer

# installer root is at this file
if __name__=="__main__":
    installer.main(os.path.dirname(os.path.abspath(__file__)))
