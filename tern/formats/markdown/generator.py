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


# global logger
logger = logging.getLogger(constants.logger_name)


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
                    r = requests.get("https://raw.githubusercontent.com/spdx/license-list-data/master/text/"+package.pkg_license+".txt")
                    result += "```\n"+r.text+"\n```\n"
    return result


class Markdown(generator.Generate):
    def generate(self, image_obj_list):
        '''Generate a markdown report'''
        logger.debug('Creating a markdown report of components in image...')
        return print_licenses_only(image_obj_list)
