# -*- coding: utf-8 -*-

#    SPIA, Simple Python Internationalization API

#    Copyright (C) 2013 Carlos Cesar Caballero Diaz <ccesar@linuxmail.org>
#   
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import re
import sys
import os



def _get_internationalized_chains(file, function_call = None):
    if function_call == None:
        function_call = '_'
    chains = []
    try:
        # open the file
        file = open(logfile, "r")           
        # read through the file
        for text in file.readlines():
           #strip off the \n
            text = text.rstrip()
           #this is probably not the best way, but it works for now
            regex = re.findall(function_call+'\((["\'])(.*?)(["\'])\)', text)
            # if the regex is not empty and is not already in ips list append
            if regex is not None and regex not in chains and not regex == []:
                chains.append(regex[0][1])
        file.close()
    except IOError, (errno, strerror):
        print ("I/O Error(%s) : %s" % (errno, strerror))

    return chains

def create_chains_file(input_file, output_dir, function_call = None, lang = None):
    chains = _get_internationalized_chains(input_file, function_call)

    if not lang == None:
        file_name = os.path.join(output_dir,lang+".py")
    else:
        file_name = os.path.basename(input_file)
        (name, ext) = os.path.splitext(file_name)
        file_name = os.path.join(output_dir,name+"_SPIA_lang"+ext)


    file = open(file_name, 'w+')
    print('# coding: utf8',file=file)
    print('',file=file)
    print('keys = {',file=file)
    for chain in chains:
        print('\''+chain+'\':\''+chain+'\',',file=file)
    print('}',file=file)
    file.close()

