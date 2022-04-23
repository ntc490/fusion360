#!/usr/bin/env python3
"""
ttable.py, Copyright (C) 2016 Nathan Crapo
ttable.py comes with ABSOLUTELY NO WARRANTY; for details
see GPLv2 header within.  This is free software, and you
are welcome to redistribute it under certain conditions;
see header for details.

Usage:
  ttable.py [-o <output_file>] [-m | --metric]  <file>
  ttable.py [-o <output_file>] [-i | --imperial] <file>

Options:
  -m, --metric                 Set machine units to metric (default)
  -i, --imperial               Set machine units to imperial
  -o <file>, --output <file>   Specify an output file (defaults to stdout)
  --version                    Print program version
"""


# Utility to convert Fusion 360 Tool Library to LinuxCNC tool table
#
# Copyright (C) 2016  Nathan Crapo
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
#
import json
import zipfile
import sys
from docopt import docopt


# ----- Constants -----

VERSION = '1.0.0'


# ----- Classes -----

class ToolLibrary:
    """
    Manage a collection of tools.  Provide filtering and ordering of
    the list for clients.
    """
    ORDER_TOOL_NUM = 1
    ORDER_TOOL_TYPE = 2
    ORDER_VENDOR = 3
    METRIC_UNITS = 'millimeters'
    IMPERIAL_UNITS = 'inches'
    DEFAULT_UNITS = METRIC_UNITS

    def __init__(self, filename):
        "Construct a tool library from a file in Fusion3D format."
        self.tools = []
        self.filter = Tool.TYPE_ALL
        self.machine_units = self.DEFAULT_UNITS
        self.order = self.ORDER_TOOL_NUM

        zipped_file = zipfile.ZipFile(filename, 'r')
        file_handle = zipped_file.open('tools.json')
        jdata = json.load(file_handle)
        file_handle.close()
        for t in jdata['data']:
            self.tools.append(Tool(t))

    def show(self, bitmap):
        "Add something to the tool filter"
        self.filter = self.filter | bitmap

    def hide(self, bitmap):
        "Remove something from the tool filter"
        self.filter = self.filter & ~bitmap

    def get_filter(self):
        "Get the filter setting as a bitmap"
        return self.filter

    def set_machine_units(self, units):
        self.machine_units = units

    def get_machine_units(self):
        return self.machine_units

    def set_order(self, order):
        "Set order of tools for client queries.  See ORDER_* constants."
        self.order = order

    def get_tools(self):
        "Get ordered, filtered subset of tools from this library."
        sort_func = self.__get_sort_func()
        tools = [t for t in self.tools if t.type() & self.filter]
        return sorted(tools, key=sort_func)

    def get_unit_converter(self, tool):
        ratio = 1
        if (self.machine_units == self.METRIC_UNITS and
                tool.units() == self.IMPERIAL_UNITS):
            ratio = 25.4
        elif (self.machine_units == self.IMPERIAL_UNITS and
              tool.units() == self.METRIC_UNITS):
            ratio = 1 / 25.4

        def basic_converter(value):
            return value * ratio
        return basic_converter

    def __get_sort_func(self):
        if self.order == self.ORDER_TOOL_TYPE:
            return lambda x: x.type()
        elif self.order == self.ORDER_VENDOR:
            return lambda x: x.vendor()
        else:
            return lambda x: x.num()


class Tool:
    """
    Endmill, drill, holder, or other CNC tool.  Keep track of properties.
    """
    TYPE_UNKNOWN = 0
    TYPE_MILLING = 1
    TYPE_HOLE_MAKING = 2
    TYPE_TURNING = 4
    TYPE_HOLDERS = 8
    TYPE_ALL = (TYPE_MILLING | TYPE_HOLE_MAKING | TYPE_TURNING | TYPE_HOLDERS)

    def __init__(self, d):
        "Pass dictionary from Fusion 360 file."
        self.raw_dict = d
        self.calculated_type = Tool.__calc_type(d['type'])

    def diameter(self):
        "Return diameter of the tool.  Holders do not have a diameter, for example."
        try:
            d = self.raw_dict['geometry']['DC']

        except:
            d = 0
        return d

    def num(self):
        "Return the tool number."
        try:
            n = self.raw_dict['post-process']['number']
        except:
            n = 0
        return n

    def vendor(self):
        "Return the tool vendor."
        return self.raw_dict['vendor']

    def description(self):
        "Return the tool description."
        return self.raw_dict['description']

    def type_str(self):
        "Return Fusion 360 tool type string."
        return self.raw_dict['type']

    def type(self):
        "Return tool type ID."
        return self.calculated_type

    def units(self):
        "Get units of properties for tool."
        return self.raw_dict['unit']

    @staticmethod
    def __calc_type(type_str):
        """
        Convert string representation of tool type to an ID.  This is the Fusion360
        Language.
        """
        if type_str == 'holder':
            return Tool.TYPE_HOLDERS
        elif type_str.find('mill') >= 0 or type_str.find('counter sink') >= 0:
            return Tool.TYPE_MILLING
        elif type_str.find('drill') >= 0:
            return Tool.TYPE_HOLE_MAKING
        elif type_str.find('turning') >= 0:
            return Tool.TYPE_TURNING
        else:
            return Tool.TYPE_UNKNOWN

    def __str__(self):
        r = "tool#=%d, dia=%d %s, vendor=%s, desc=%s, %s[%d]\n" % (self.num(),
                                                                   self.diameter(),
                                                                   self.units(),
                                                                   self.vendor(),
                                                                   self.description(),
                                                                   self.type_str(),
                                                                   self.type())
        return r


# ----- Helpers -----

def print_linuxcnc_tool_table(out_file, tool_library):
    """
    Print tools in LinuxCNC table format.  The out_file may be stdout or a file
    object to a file on disk.
    """

    for tool in tool_library.get_tools():
        conv_unit = tool_library.get_unit_converter(tool)
        out_file.write(f'T{tool.num():<8} '
                       f'P{tool.num():<8} '
                       f'Z{0:<8} '
                       f'D{conv_unit(tool.diameter()):08.5f} '
                       f'; {tool.vendor() + " - " + tool.description()} \n')


# ----- Main Application -----

def main():
    "Program entry point."
    arguments = docopt(__doc__, version=VERSION)
    input_filename = arguments['<file>']
    output_filename = arguments['--output']

    if output_filename is None or output_filename == '-':
        output_file = sys.stdout
    else:
        try:
            output_file = open(output_filename, 'w')
        except IOError as e:
            sys.stderr.write("%s\n" % e)
            sys.exit(-1)

    try:
        library = ToolLibrary(input_filename)
    except IOError as e:
        sys.stderr.write("%s\n" % e)
        sys.exit(-1)

    if arguments['--metric']:
        library.set_machine_units(ToolLibrary.METRIC_UNITS)
    elif arguments['--imperial']:
        library.set_machine_units(ToolLibrary.IMPERIAL_UNITS)

    library.show(Tool.TYPE_ALL)
    library.hide(Tool.TYPE_HOLDERS)

    print_linuxcnc_tool_table(output_file, library)


if __name__ == "__main__":
    main()
