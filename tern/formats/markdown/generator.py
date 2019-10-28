# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Michael Seidel. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

"""
markdown report generator
"""

import logging
import json
import requests
from tern.report import formats
from tern.formats import generator
from tern.report import content
from tern.utils import constants
import os.path
from os import path
import argparse

# global logger
logger = logging.getLogger(constants.logger_name)

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--local-licenses-folder', default=os.getcwd(),
                               help="Local Folder with additional license files"
                               "if spdx database does miss a license. ")
args = parser.parse_known_args()

def print_licenses_only(image_obj_list):
    '''Print a complete list of licenses for all images'''
    result = "--- \n"
    for image in image_obj_list:
        for layer in image.layers:
            for package in layer.packages:
                if (package.pkg_license):
                    result += "#" + package.name + "\n"
                    result += "**Version:** "+package.version+"\n"
                    result += "**License:** "+package.pkg_license+"\n"

                    if(path.exists(args[0].local_licenses_folder + "/" + package.version + ".txt")):
                        with open(args[0].local_licenses_folder + "/" + package.version + ".txt") as f:
                            result += "```\n"+f.read()+"\n```\n"
                    elif (path.exists(args[0].local_licenses_folder + "/" + package.pkg_license + ".txt")):
                        with open(args[0].local_licenses_folder + "/" + package.pkg_license + ".txt") as f:
                            result += "```\n"+f.read()+"\n```\n"
                    else:
                        r = requests.get("https://raw.githubusercontent.com/spdx/license-list-data/master/text/"+package.pkg_license+".txt")
                        if r.status_code == 200:
                            result += "```\n"+r.text+"\n```\n"
                        else:
                            result += "```\nNo license file for " + package.version + " " +package.pkg_license+" found!\n```\n"
                            logger.error("No license file for " + package.version + " " +package.pkg_license+" found!")
    return result


class Markdown(generator.Generate):
    def generate(self, image_obj_list):
        '''Generate a markdown report'''
        logger.debug('Creating a markdown report of components in image...')
        return print_licenses_only(image_obj_list)
