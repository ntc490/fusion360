#!/usr/bin/python
"""
ttablev2.py, Copyright (C) 2016 Nathan Crapo
ttablev2.py comes with ABSOLUTELY NO WARRANTY; for details
see GPLv2 header within.  This is free software, and you
are welcome to redistribute it under certain conditions;
see header for details.

Usage:
  ttablev2.py [-o <output_file>] [-m | --metric] [-l | --linuxcnc-file <linuxcnc-file-name> ]  <file>
  ttablev2.py [-o <output_file>] [-i | --imperial] [-l | --linuxcnc-file <linuxcnc-file-name>] <file>

Options:
  -m, --metric                        Set machine units to metric (default)
  -i, --imperial                      Set machine units to imperial
  -l <file>, --linuxcnc-file <file>   Merge data with existing linuxcnc_file
  -o <file>, --output <file>          Specify an output file (defaults to stdout)
  --version                            Print program version
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
import re



# ----- Constants -----

VERSION = '1.0.0'



# ----- Classes -----

class ToolLibrary:
    """
    Manage a collection of tools.  Provide filtering and ordering of
    the list for clients.
    """
    ORDER_TOOL_NUM=1
    ORDER_TOOL_TYPE=2
    ORDER_VENDOR=3
    METRIC_UNITS = 'millimeters'
    IMPERIAL_UNITS = 'inches'
    DEFAULT_UNITS = METRIC_UNITS

    def __init__(self, filename, lcnc_filename):
        "Construct a tool library from a file in Fusion3D format."
        self.tools = []
        self.filter = Tool.TYPE_ALL
        self.machine_units = self.DEFAULT_UNITS
        self.order = self.ORDER_TOOL_NUM

        if len(lcnc_filename):
          try:
              lcnc_lineList = [re.sub('\s+', ' ', line).strip('\n').split(";")[0] for line in open(lcnc_filename[0], "r")]
          except IOError as e:
              sys.stderr.write("%s\n" % e)
              sys.exit(-1)

        file_handle = open(filename)
        jdata = json.load(file_handle)
        file_handle.close()
        for t in jdata['data']:
            new_tool=Tool(t)
            if len(lcnc_filename) and len(lcnc_lineList):
                toolnumberTag = "T"
                res = [line.split()[1:] for line in lcnc_lineList if (line.split()[0].lower().startswith(toolnumberTag.lower()) and line.split(" ")[0].lower() == "t%d"%new_tool.num())]
                if len(res)==1:
                    new_tool.set_lcnc_data(res[0])
                elif len(res)>1:
                    sys.stderr.write("More than one match for tool number %s in the linuxcnc file\n" % new_tool.num())
                    sys.exit(-1)
            self.tools.append(new_tool)

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
        "tools = [ t for t in self.tools if t.type() & self.filter ]"
        "tools = [ t for t in self.tools ]"
        tools = set()
        sys.stderr.write("Skipping duplicate tool numbers ...\n")
        tools = [tools.add(t.num()) or t for t in self.tools if t.num() == 0 or t.num() not in tools]
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
    TYPE_BALL_END_MILL = 2
    TYPE_FACE_END_MILL = 4
    TYPE_CHAMFER_MILL = 8
    TYPE_FLAT_END_MILL = 16
    TYPE_HOLE_MAKING = 32
    TYPE_TURNING = 64
    TYPE_HOLDERS = 128
    TYPE_PROBE = 256
    TYPE_ALL = (TYPE_MILLING | TYPE_BALL_END_MILL | TYPE_FACE_END_MILL | TYPE_CHAMFER_MILL | TYPE_FLAT_END_MILL | TYPE_HOLE_MAKING | TYPE_TURNING | TYPE_HOLDERS | TYPE_PROBE)

    def __init__(self, d):
        "Pass dictionary from Fusion 360 file."
        self.raw_dict = d
        self.calculated_type = Tool.__calc_type(d['type'])
        self.lcnc_length_in = self.length()
        self.lcnc_diameter_in = self.diameter()
        self.lcnc_pocket_in = 0

    def set_lcnc_data(self, lcnc_data_in):
        # validate if I and J are the same, if not ignore lcnc data
        try:
            lcnc_i = [item[1:] for item in lcnc_data_in if (item[0].lower() == "i")]
            if len(lcnc_i)==1:
                i = float(lcnc_i[0])
            lcnc_d = [item[1:] for item in lcnc_data_in if (item[0].lower() == "d")]
            if len(lcnc_d)==1:
                d = float(lcnc_d[0])
            else:
                d = 0
            lcnc_q = [item[1:] for item in lcnc_data_in if (item[0].lower() == "q")]
            if len(lcnc_q)==1:
                q = int(lcnc_q[0])
            else:
                q = 0

            if (isclose(i, self.length()) and isclose(d, self.diameter()) and q == self.type_lcnc()):
                lcnc_l = [item[1:] for item in lcnc_data_in if (item[0].lower() == "z")]
                if len(lcnc_l)==1:
                    self.lcnc_length_in = float(lcnc_l[0])
                lcnc_d = [item[1:] for item in lcnc_data_in if (item[0].lower() == "d")]
                if len(lcnc_d)==1:
                    self.lcnc_diameter_in = float(lcnc_d[0])
            else:
                sys.stderr.write("Tool %d, igoring LinuxCNC diameter and length data due to either I(%.6f/%.6f), D(%.6f/%.6f) or type(%d/%d) mismatch\n" % 
                           (self.num(), i, self.length(), d, self.diameter(), q, self.type_lcnc()))
                self.lcnc_length_in = 0
                self.lcnc_diameter_in = self.diameter()
                self.lcnc_pocket_in = 0
            # always take the lcnc pocket
            lcnc_p = [item[1:] for item in lcnc_data_in if (item[0].lower() == "p")]
            if len(lcnc_p)==1:
                self.lcnc_pocket_in = int(lcnc_p[0])
        except:
            sys.stderr.write("Tool %d, error trying to extract I/J from linuxcnc data [%s]\n" % 
                           (self.num(), lcnc_data_in))
            raise

    def diameter(self):
        "Return diameter of the tool.  Holders do not have a diameter, for example."
        try:
            d = float(self.raw_dict['geometry']['DC'])
        except:
            d = float(0.0)
        return d

    def corner_radius(self):
        "Return corner radius of the tool. Most tools dont have one, ball nose for example, do."
        try:
            d = float(self.raw_dict['geometry']['RE'])
        except:
            d = float(0.0)
        return d

    def lcnc_diameter(self):
        "Return lcnc diameter of the tool."
        return self.lcnc_diameter_in

    def num(self):
        "Return the tool number."
        try:
            n = self.raw_dict['post-process']['number']
        except:
            n = 0
        return n

    def lcnc_pocket(self):
        "Return the tool pocket number."
        return self.lcnc_pocket_in

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

    def type_lcnc(self):
        "Return tool type id in a linuxcnc friendly format for column Q. i.e instead of using the bitwize mask 1 2 .. 32 64, convert to linear 1..9"
        "Q - tool orientation (lathe only) - integer, 0-9"
        t=self.calculated_type
        lcnc_id=0
        while t>0:
            t=t>>1
            lcnc_id=lcnc_id+1
        return lcnc_id

    def units(self):
        "Get units of properties for tool."
        return self.raw_dict['unit']

    def length(self):
        "Get shoulder + holder lengh for tool."
        try:
            d = float(self.raw_dict['geometry']['LB'])
            for segment in self.raw_dict['holder']['segments']:
              d = d + float(segment['height'])
        except:
            d = float(0.0)
        return d

    def lcnc_length(self):
        return self.lcnc_length_in

    @staticmethod
    def __calc_type(type_str):
        """
        Convert string representation of tool type to an ID.  This is the Fusion360
        Language.
        """
        """ using type for probing, hence chamfer is does not require diameter measurfement and is therefore classified as a hole making tool"""
        if type_str == 'holder':
            return Tool.TYPE_HOLDERS
        elif type_str.find('drill') >= 0 or type_str.find('tap') >= 0 or type_str.find('chamfer') >= 0:
            return Tool.TYPE_HOLE_MAKING
        elif type_str.find('ball end mill') >= 0 or type_str.find('bull nose end mill') >= 0:
            return Tool.TYPE_BALL_END_MILL
        elif type_str.find('face mill') >= 0:
            return Tool.TYPE_FACE_END_MILL
        elif type_str.find('chamfer mill') >= 0:
            return Tool.TYPE_CHAMFER_MILL
        elif type_str.find('flat end mill') >= 0:
            return Tool.TYPE_FLAT_END_MILL
        elif type_str.find('mill') >= 0:
            return Tool.TYPE_MILLING
        elif type_str.find('turning') >= 0:
            return Tool.TYPE_TURNING
        elif type_str.find('probe') >= 0:
            return Tool.TYPE_PROBE
        else:
            return Tool.TYPE_UNKNOWN

    def __repr__(self):
        r = "tool#=%d, dia=%d %s, vendor=%s, desc=%s, shoulder-lenght=%d holder_length=%d %s[%d]\n" % (self.num(),
                                                                   self.diameter(),
                                                                   self.units(),
                                                                   self.vendor(),
                                                                   self.description(),
                                                                   self.length(),
                                                                   self.type_str(),
                                                                   self.type())
        return r



# ----- Helpers -----
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
  return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def print_linuxcnc_tool_table(out_file, tool_library):
    """
    Print tools in LinuxCNC table format.  The out_file may be stdout or a file
    object to a file on disk.
    """
    for tool in tool_library.get_tools():
        conv_unit = tool_library.get_unit_converter(tool)
        if tool.num() > 0:
          out_file.write("T%d P%d D%.6f Z%.6f I%.6f Q%d  ;%s\n" % (tool.num(), # tool num
                                                  tool.lcnc_pocket(), # pocket num
                                                  conv_unit(tool.lcnc_diameter()), # v offset, using it for aproximate diameter
                                                  conv_unit(tool.lcnc_length()), # z offset - manage in the LinuxCNC tool table
                                                  conv_unit(tool.length()), # u offset, using it for aproximate z height
                                                  tool.type_lcnc(), # tool orientation, using tool type here
                                                  tool.vendor().encode('utf-8') + " - " + tool.description().encode('utf-8') + " - " + tool.type_str().encode('utf-8')))
        #else:
        #  sys.stdout.write("Skipping ... t%d p%d z%d d%.3f ;%s\n" % (tool.num(), # tool num
        #                                          tool.num(), # pocket num
        #                                          0, # z offset - manage in the LinuxCNC tool table
        #                                          conv_unit(tool.diameter()),
        #                                          tool.vendor().encode('utf-8') + " - " + tool.description().encode('utf-8')))






# ----- Main Application -----

def main():
    "Program entry point."
    arguments = docopt(__doc__, version = VERSION)
    input_filename = arguments['<file>']
    output_filename = arguments['--output']
    lcnc_filename = arguments['--linuxcnc-file']
    
    if output_filename is None or output_filename == '-':
        output_file = sys.stdout 
    else:
        try:
            output_file = file(output_filename, 'w')
        except IOError as e:
            sys.stderr.write("%s\n" % e)
            sys.exit(-1)
    try:
        library = ToolLibrary(input_filename, lcnc_filename)
    except IOError as e:
        sys.stderr.write("%s\n" % e)
        sys.exit(-1)


    if arguments['--metric']: library.set_machine_units(ToolLibrary.METRIC_UNITS)
    elif arguments['--imperial']: library.set_machine_units(ToolLibrary.IMPERIAL_UNITS)

    library.show(Tool.TYPE_ALL)
    library.hide(Tool.TYPE_HOLDERS)
    
    print_linuxcnc_tool_table(output_file, library)



if __name__ == "__main__":
    main()

