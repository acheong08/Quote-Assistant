#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 13:19:03 2021

@author: jackhayley
"""

import json

try:
    from .constants import TOOLS, TOOL_TYPES, resource_path
except ValueError:
    from constants import TOOLS, TOOL_TYPES, resource_path


class Tool:

    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0:
            self.data = args[1]
            return
        else:
            self.data = {}
            self.init_data(*args, **kwargs)

    def init_data(self, *args, **kwargs):
        self.data['id'] = self.get_id(*args)
        for kw in kwargs:
            self.data[kw] = kwargs[kw]
        print(self.data)

    def get_id(self, *args):
        text = TOOL_TYPES[args[0]]
        if (args[1][text]) >= 9:
            text += '_' + str(args[1][text] + 1)
        else:
            text += '_0' + str(args[1][text] + 1)
        return text

    def _insert_dict(m_obj1, m_obj2=('Diameter', 'Stepover', 'FRATE')):
        """Generates job dictionary based on given values and keys. In this case the
        program utilizes its default case to give job dictionary based on cutting
        info for each material type"""
        x_1, y_1, z_1 = map(str, m_obj2)
        x_2, y_2, z_2 = map(float, m_obj1)
        return {x_1: x_2, y_1: y_2, z_1: z_2}


class _Standard(Tool):

    def __init__(self, *args, **kwargs):
        super().__init__('Tip-radius', *args, **kwargs)


class _Ball(Tool):

    def __init__(self, *args, **kwargs):
        super().__init__('Ball-nose', *args, **kwargs)


class _Drill(Tool):

    def __init__(self, *args, **kwargs):
        super().__init__('Drill', *args, **kwargs)


class ToolManager():
    toolTypes = {"tip": _Standard,
                 "bll": _Ball,
                 "djt": _Drill}

    def __init__(self):
        pass

    def add_tool(self):

        with open(TOOLS, 'r', encoding="utf-8", errors="replace") as file:
            current_tools = json.load(file)
        tool_info = input("Input tool info: ").split()
        tool_info[1:] = [float(info) for info in tool_info[1:]]

        tool = ToolManager.toolTypes[tool_info[0]](self.get_tool_types(
            current_tools),
            job='stamping',
            diameter=tool_info[1],
            radius=tool_info[2],
            stepdown=tool_info[3],
            stepover=tool_info[4],
            feedrate=tool_info[5],
            weight=tool_info[6])
        current_tools.append(tool.data)
        print(current_tools)
        file = open(TOOLS, 'w', encoding="utf-8", errors="replace")
        file.write(json.dumps(current_tools, sort_keys=False, indent=4))
        file.close()

    def get_tool_types(self, tools):
        types = {'tip': 0, 'bll': 0, 'djt': 0}
        for i_1, tool in enumerate(tools):
            for i_2, t_type in enumerate(list(types.keys())):
                if t_type in tool['id']:
                    types[t_type] += 1
        return types

    def get_job_tools(self, job_type):
        with open(resource_path(TOOLS), 'r', encoding="utf-8", errors="replace") as file:
            tools = json.load(file)
        return_tools = []
        for tool in tools:
            if tool['job'] == job_type:
                return_tools.append(ToolManager.toolTypes[tool['id'][:3]](tool))
                print('Tool added:', return_tools[-1].data)

        return return_tools


# =============================================================================
#         file = open(TOOLS, 'job',encoding="utf-8", errors="replace")
#         file.write(json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4))
#         file.close()
#         
#         file = open(TOOLS, 'r',encoding="utf-8", errors="replace")
#         print(file.read())
#         file.close()
# =============================================================================

# file = open(file_name, "r", encoding="utf-8", errors="replace")


if __name__ == '__main__':
    # ToolManager.add_tool()
    tm = ToolManager()
    # while True:
    #
    #     tm.add_tool()
    #     if input("Continue? ") != '0': continue
    #     break
    print(tm.get_job_tools('stamping'))
    pass
