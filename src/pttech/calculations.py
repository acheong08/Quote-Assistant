import numpy

try:
    from pttech.constants import *
    from pttech.tools import *
except ImportError:
    # PyCharm is stupid, I'm stupid, we're all stupid.
    from src.pttech.constants import *
    from src.pttech.tools import *
from math import *


class BaseCalculations:

    def __init__(self):
        self.space_conversion = 1.
        self.total_cost = 0

    def calculate_cost(self, *args, **kwargs):
        pass

    def get_cost(self):
        return self.total_cost

    @staticmethod
    def _get_next_even_number(n):
        return float(int(n) + 1 if int(n) % 2 == 1 else int(n) + 2 if n != int(n) else n)


class Material(BaseCalculations):

    def __init__(self):
        self._get_required_volume = (self._3pcddz, self._2pcfrz, self._2pcfrs, self._2pcfra)
        self.dimensions = [0., 0., 0.]
        self.precision = 1
        self.required_volume = 0
        self.cost_density = 1
        self.max_offset = 0.5
        self.basing_multiplier = 0.
        self.additional_cost = 0.
        self.config = {}
        super().__init__()

    def get_volume(self):
        return self.required_volume

    def calculate_cost(self, job, dimensions, conversion, precision, config):
        self.dimensions = [0., 0., 0.]
        self.precision = precision
        print("CONFIG IMPORT:", config)
        self.config = config
        self.dimensions, self.space_conversion = dimensions, conversion
        self.dimensions = [self.dimensions[n] * self.space_conversion for n in range(3)]

        print(self.dimensions)
        self.required_volume = self._get_required_volume[job](*self.dimensions)
        self.total_cost += self.required_volume * self.cost_density + self.additional_cost
        print("VOLUME: ", self.required_volume, "\nCOST: ", self.total_cost)

    def _get_offset(self):
        return self.max_offset / self.precision

    def _3pcddz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc'] * self.config["cost_per_pound_zinc"]
        self.additional_cost = x * y / 4 * PATTERN_MULTIPLIER + x * y * z * BASING_MULTIPLIERS['3pc']
        return (x + 2 * (z + ZINC_PADDING) + self._get_offset()) * \
               (y + 2 * (z + ZINC_PADDING) + self._get_offset()) * \
               round(z + 12, 0)

    def _2pcfrz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc'] * self.config["cost_per_pound_zinc"]
        self.additional_cost = x * y / 4 * PATTERN_MULTIPLIER + x * y * z * BASING_MULTIPLIERS['2pc']
        return (x + 2 * z + self._get_offset()) * \
               (y + 2 * z + self._get_offset()) * \
               (z + 5)

    def _2pcfrs(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Steel'] * self.config["cost_per_pound_steel"]
        return (self._get_next_even_number(x + 6) + self._get_offset()) * \
               (self._get_next_even_number(y + 6) + self._get_offset()) * \
               (z + 2)

    def _2pcfra(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Aluminum'] * self.config["cost_per_pound_aluminum"]
        return (self._get_next_even_number(x + 6) + self._get_offset()) * \
               (self._get_next_even_number(y + 6) + self._get_offset()) * \
               (z + 2)


class Cutting(BaseCalculations):
    """Calculator class to execute all the calculations in order to determine
        the remaining output data."""

    def __init__(self):
        # Dictionary defined to map each instruction to corresponding method
        self.dimensions = [0., 0., 0.]
        self.precision = 1
        self.instructions = {'Volume To Remove': self._calculate_volume,
                             'Estimated FR Ratio': self._calculate_ratio,
                             'Percent Error': self._calculate_error,
                             'Cut Rate': self._calculate_rate,
                             'Time Required': self._calculate_time}
        self.cut_volume = self.cut_ratio = self.cut_error = self.cut_rate = 0
        self.m_tools = ToolManager()
        super().__init__()

    # def __call__(self, operation,
    #              mapped_obj=None,
    #              initial_value=-1,
    #              padding_amount=0,
    #              additional_values=0) -> float:
    #     """ "__call__" runs every time the object is called after __init__
    #
    #     Parameters:
    #         operation: which instruction to run
    #         mapped_obj: map of the data values from DataIO
    #         initial_value: sometimes can be the initial constant
    #         padding_amount: sometimes can be the maximum modification amount
    #         additional_values: utilized if additional values required
    #
    #     Returns the internal calculation corresponding to the instruction"""
    #
    #     # Gets the placeholder values redefined (if necessary)
    #     self.mapped_obj = mapped_obj
    #     self.initial_value = initial_value
    #     self.padding_amount = padding_amount
    #     self.additional_values = additional_values
    #     # The internal calculation is run and returns the resultant value
    #     return self.instructions[operation]()

    def calculate_cost(self, material, dimensions, volume, precision, conversion):
        self.dimensions = dimensions
        self.part_volume = volume
        self.space_conversion = conversion
        self.precision = precision

        self.dimensions = [self.dimensions[n] / self.space_conversion for n in range(3)]

        self.cut_volume = self._calculate_volume()
        self.cut_ratio = self._calculate_ratio()
        self.cut_error = self._calculate_error()
        self.cut_rate = self._calculate_rate()
        self.total_cost += self._calculate_time()
        print("TOTAL COST IN HOURS: ", self.total_cost)

    @property
    def get_additional_values(self):
        return (self.cut_volume, self.cut_ratio, self.cut_error, self.cut_rate)

    def _calculate_volume(self) -> float:
        """Internal method to calculate volume to material remove.

        Current formula is [r = xyz - v], where:

            r = volume to remove

            x = x-dimension value of box from cimatron

            y = y-dimension value of box from cimatron

            z = z-dimension value of box from cimatron

            v = total volume occupied by the part"""

        r = numpy.prod(self.dimensions) - self.part_volume
        return round(r, 2)

    def _calculate_ratio(self) -> float:
        """Internal method to calculate percentage of time actually cutting
        the material as opposed to not cutting it.

        This formula involves taking an initial value and modifying that value
        by a certain amount depending on certain factors. In this case, the
        dimensions are taken into account.

        Current formula is [p = a(-e^(-0.00277x)+1)+b], where:

            p = ratio of feedrate to non-feedrate

            a = maximum deviation from original value (from ptt.constants)

            e = 2.7182818285... (constant)

            x = average dimension size of the job (calculated below)

            b = the original value to be modified (from ptt.constants)"""

        l, h, w = map(float, self.dimensions)
        a = FRATE_VAR
        b = FRATE_RATIO
        x = abs((l + w + h) / 3)
        p = a * (-e ** (-0.00277 * x) + 1) + b
        return round(p, 3)

    def _calculate_error(self) -> float:  # TODO: Add machine implementation

        """[WIP] Internal method to calculate predicted percentage error of
        the cutting time on the machines.

        This formula involves taking an initial value and modifying that value
        by a certain amount depending on certain factors. In this case, the
        difficulty is taken into account.

        Current formula is [p = 1+dx], where:

            p = percentage error (predicted)

            d = difficulty rating (inputted)

            x = initial error value (from ptt.constants)"""

        potency = 0.25

        d = self.precision
        d = float(d)
        x = PCT_ERROR
        p = 1 + d * x * potency
        return round(p, 3)

    def _calculate_rate(self) -> float:
        """[WIP] Internal method to calculate predicted rate of cutting the
        material on the machines.

        This formula involves taking an initial value and modifying that value
        by a certain amount depending on certain factors. In this case, the
        difficulty is taken into account.

        Current formula is [r = (t1+t2+...+tn)w], where:

            r = cut rate (predicted)

            f = material average feedrate (from ptt.constants)

            d = material average tool diameter (from ptt.constants)

            s = material average step over (from ptt.constants)"""

        # material, difficulty = self.mapped_obj

        # difficulty = float(difficulty)
        # d, f, s = map(float, list(self.padding_amount[material].values()))
        # print("values:", d, s, f)
        # d /= 0.039370078740157
        # r = f * (d - s)
        # return round(r, 3)
        s = 0.
        t = []

        potency = 0.25

        tools = self.m_tools.get_job_tools('stamping')

        for tool in tools:
            s += tool.data['weight']

        for tool in tools:
            d, o, f, w = map(float,
                             list(list(tool.data.values())[n]
                                  for n in range(4, 8)))
            # print(d, o, s, tools)
            a = -(-0.5 * self.precision + 1) * potency
            w += a * (d * o / s / len(tools)) ** 0.5 - a
            # w += 0.05 * (2 - difficulty) * ln(d * o / s / 10.12)
            t.append(d * o * f * w)
        print("AV WEIGHT----", s / len(tools))
        print("----CUT RATE:", sum(t) / s)
        r: float = sum(t) / s
        return round(r, 3)

    def _calculate_time(self) -> float:
        """[WIP] Internal method to calculate predicted machine time for a
        quote in hours.

        This formula involves taking the initial volume and rates and modifying
        the quotient by a certain amount depending on certain factors. In this
        case, the percent error and FRATE ratio are taken into account.

        Current formula is [t = (vp)/(60rc)], where:

            t = machine hours (predicted)

            v = volume to remove (calculated in a prior method)

            p = percentage error (calculated in a prior method)

            r = Feedrate ratio (calculated in a prior method)

            c = cut rate (calculated in a prior method)"""

        v, r, p, c = self.cut_volume, self.cut_ratio, self.cut_error, self.cut_rate
        t = (v / c) * p / r / 60
        print(v, r, p, c)
        return round(t, 3)


class MasterCalculations:

    def __init__(self):
        self.m_materials = Material()
        self.m_cutting = Cutting()
        self.m_base = BaseCalculations()

    def __call__(self, calculator=BaseCalculations):
        if calculator is Material:
            print("CALC MATCH FOUND")
            return self.m_materials
        elif calculator is Cutting:
            print("CALC MATCH FOUND")
            return self.m_cutting
        else:
            return self.m_base
