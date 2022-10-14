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
    """Base calculator superclass for all calculator classes."""

    def __init__(self):
        self.space_conversion = 1.
        self.total_cost = 0

    def calculate_cost(self, *args, **kwargs):
        pass

    def get_cost(self):
        return self.total_cost

    @staticmethod
    def _get_next_even_int(n: float):
        """
        Method that returns the next even number based on a float input.

        @rtype: float
        """
        return float(int(n) + 1 if int(n) % 2 == 1 else int(n) + 2 if n != int(n) else n)


class Material(BaseCalculations):
    """Subclass pertaining to the calculations for material costs."""

    def __init__(self):
        # Internal volume calculations put in list that matches indexes of job types
        self._get_required_volume = (self._3pcddz, self._2pcfrz, self._2pcfrs, self._2pcfra)
        # Everything else is initialized to their default values
        self.dimensions = [0., 0., 0.]
        self.mod_dimensions = [0., 0., 0.]
        self.precision = 1
        self.required_volume = 0
        self.cost_density = 1
        self.combo = 1
        self.max_offset = .25
        self.basing_multiplier = 0.
        self.additional_cost = 0.
        self.config = {}
        super().__init__()

    def get_volume(self):
        return self.required_volume

    def get_block(self):
        # return self.mod_dimensions
        return [self.mod_dimensions[n] / self.space_conversion for n in range(3)]

    def calculate_cost(self, job, dimensions, conversion, precision, is_combo, config):
        """
        Overriden superclcass method that calculates the material costs based on above parameters.

        @param job: type of job (index)
        @param dimensions: the box_dimensions of the part as a tuple
        @param conversion: the space conversion rate
        @param precision: the difficulty offset
        @param is_combo: boolean determining whether the part is comboed
        @param config: the config.json file in dictionary format
        """
        self.precision = precision
        print("CONFIG IMPORT:", config)
        self.config = config
        self.dimensions, self.space_conversion = dimensions, conversion
        print('self.space_conversion', self.space_conversion)
        self.dimensions = [self.dimensions[n] * self.space_conversion for n in range(3)]

        print(self.dimensions)

        self.required_volume = self._get_required_volume[job](*self.dimensions)
        self.combo = 1. if not is_combo else self.combo
        print(">COMBO", self.combo)
        self.required_volume *= self.combo
        self.total_cost += self.required_volume * self.cost_density + self.additional_cost
        print("VOLUME: ", self.required_volume, "\nCOST: ", self.total_cost)

    def _get_offset(self):
        return self.max_offset * self.precision

    def _3pcddz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc'] * self.config["cost_per_pound_zinc"]
        self.combo = COMBO_MULTIPLIERS['Zinc']
        self.mod_dimensions = [(x + 2 * (z + ZINC_PADDING) + self._get_offset()),
                               (y + 2 * (z + ZINC_PADDING) + self._get_offset()),
                               round(z + 12, 0)]
        self.additional_cost = x * y * z / 4 * PATTERN_MULTIPLIER + x * y * BASING_MULTIPLIERS['3pc']
        return prod(self.mod_dimensions)

    def _2pcfrz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc'] * self.config["cost_per_pound_zinc"]
        self.mod_dimensions = [(x + 2 * z + self._get_offset()),
                               (y + 2 * z + self._get_offset()),
                               (z + 5)]
        self.additional_cost = x * y * z / 4 * PATTERN_MULTIPLIER + x * y * BASING_MULTIPLIERS['2pc']
        return prod(self.mod_dimensions)

    def _2pcfrs(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Steel'] * self.config["cost_per_pound_steel"]
        self.mod_dimensions = [(self._get_next_even_int(x + 8) + self._get_offset()),
                               (self._get_next_even_int(y + 6) + self._get_offset()),
                               (z + 2)]
        return prod(self.mod_dimensions)

    def _2pcfra(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Aluminum'] * self.config["cost_per_pound_aluminum"]
        self.mod_dimensions = [(self._get_next_even_int(x + 8) + self._get_offset()),
                               (self._get_next_even_int(y + 6) + self._get_offset()),
                               (z + 2)]
        return prod(self.mod_dimensions)


class Cutting(BaseCalculations):
    """Calculator class to execute all the calculations in order to determine remaining output data."""

    def __init__(self):
        self.total_time = 0.
        self.box_dimensions = [0., 0., 0.]
        self.precision = 1
        self.material = ''
        self.part_dimensions = [0., 0., 0.]
        # Dictionary defined to map each instruction to corresponding method
        # self.instructions = {'Volume To Remove': self._calculate_volume,
        #                      'Estimated FR Ratio': self._calculate_ratio,
        #                      'Percent Error': self._calculate_error,
        #                      'Cut Rate': self._calculate_rate,
        #                      'Time Required': self._calculate_time}
        self.cut_volume = self.cut_ratio = self.cut_error = self.cut_rate = 0
        self.m_tools = ToolManager()
        super().__init__()

    def get_time(self):
        return self.total_time

    def calculate_cost(self, mat, box, dim, precision, conversion, is_combo, config):
        self.material = 'zinc' if mat in (0, 1) else 'steel' if mat in (2,) else 'aluminum' if mat in (3,) else ''
        self.box_dimensions = box
        self.part_dimensions = dim
        self.space_conversion = conversion
        self.precision = precision
        self.config = config
        print('self.box_dimensions', self.box_dimensions)
        print('self.part_dimensions', self.part_dimensions)
        self.box_dimensions = [self.box_dimensions[n] / self.space_conversion for n in range(3)]
        self.part_dimensions = [self.part_dimensions[n] / self.space_conversion for n in range(3)]

        self.cut_volume = self._calculate_volume()
        print('self.cut_volume', self.cut_volume)
        self.cut_ratio = self._calculate_ratio()
        print('self.cut_ratio', self.cut_ratio)
        self.cut_error = self._calculate_error()
        print('self.cut_error', self.cut_error)
        self.cut_rate = self._calculate_rate()
        print('self.cut_rate', self.cut_rate)
        self.combo = 1. if not is_combo else COMBO_MULTIPLIERS[self.material.capitalize()]
        self.total_time += self._calculate_time() * self.combo / 2.4
        # self.total_time += self._legacy_method() * self.combo / 2.4
        self.total_cost += self.total_time * self.config['cost_per_hour_' + self.material]
        print('TOTAL COST IN HOURS: ', self.total_cost)
        # self.total_cost = 0

    def _legacy_method(self):
        return prod(self.box_dimensions) / 144

    @property
    def get_additional_values(self):
        return tuple([self.cut_volume, self.cut_ratio, self.cut_error, self.cut_rate])

    def _calculate_volume(self) -> float:
        """Internal method to calculate volume to material remove.

        Current formula is [r = xyz - v], where:

            r = volume to remove

            x = x-dimension value of box from cimatron

            y = y-dimension value of box from cimatron

            z = z-dimension value of box from cimatron

            v = total volume occupied by the part"""

        # r = numpy.prod(self.box_dimensions) - self.part_dimensions
        r = numpy.prod(self.box_dimensions) - numpy.prod(self.part_dimensions) * 0.025
        return round(r, 2)

    def _calculate_ratio(self) -> float:
        """Internal method to calculate percentage of time actually cutting
        the material as opposed to not cutting it.

        This formula involves taking an initial value and modifying that value
        by a certain amount depending on certain factors. In this case, the
        box_dimensions are taken into account.

        Current formula is [p = a(-e^(-0.00277x)+1)+b], where:

            p = ratio of feedrate to non-feedrate

            a = maximum deviation from original value (from ptt.constants)

            e = 2.7182818285... (constant)

            x = average dimension size of the job (calculated below)

            b = the original value to be modified (from ptt.constants)"""

        l, h, w = map(float, self.box_dimensions)
        a = FRATE_VAR
        b = FRATE_RATIO
        x = abs((l + w + h) / 3)
        p = a * (-e ** (-0.00277 * x) + 1) + b
        return round(p, 3)

    def _calculate_error(self) -> float:

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

        potency = 0.5

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
        tool in hours.

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
        mod = r * self.cut_ratio / 2.4
        t = (v / c) * p / r / 60 * mod
        print(v, r, p, c)
        return round(t, 3)


class MasterCalculations:
    """Class to handle the management of all calculators in the application"""

    def __init__(self):
        self.m_materials = Material()
        self.m_cutting = Cutting()
        self.m_base = BaseCalculations()

    def __call__(self, calculator=BaseCalculations):
        """
        Method that calls every time the class is called after initialization. Fetches the relevant calculator.

        @param calculator: the requested calculator
        @return: the corresponding calculator object
        """
        if calculator is Material:
            print("CALC MATCH FOUND")
            return self.m_materials
        elif calculator is Cutting:
            print("CALC MATCH FOUND")
            return self.m_cutting
        else:
            return self.m_base

    def get_cumulative_cost(self):
        """
        Method that retrieves the summation of all the costs derived from the calculators.

        @return: the cumulative cost derived from the calculators
        """
        cost = 0
        for calculator in [self.m_base, self.m_cutting, self.m_materials]:
            cost += calculator.get_cost()
        return cost
