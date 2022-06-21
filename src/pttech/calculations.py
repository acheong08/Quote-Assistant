from pttech.constants import *


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
        self._get_required_volume = (self._3pcddz, self._2pcfrz, self._2pcfrs)
        self.dimensions = [0., 0., 0.]
        self.required_volume = 0
        self.cost_density = 1
        super().__init__()

    def get_volume(self):
        return self.required_volume

    def calculate_cost(self, job, dimensions, conversion):
        self.dimensions = [0., 0., 0.]
        self.dimensions, self.space_conversion = dimensions, conversion
        self.dimensions = [self.dimensions[n] * self.space_conversion for n in range(3)]
        print(self.dimensions)
        self.required_volume = self._get_required_volume[job](*dimensions)

        self.total_cost += self.required_volume * self.cost_density
        print("VOLUME: ", self.required_volume, "\nCOST: ", self.total_cost)

    def _3pcddz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc']
        return (x + 2 * (z + 2)) * (y + 2 * (z + 2)) * int(z + 5)

    def _2pcfrz(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Zinc']
        return (x + 2 * z) * (y + 2 * z) * (z + 5)

    def _2pcfrs(self, x, y, z):
        self.cost_density = MATERIAL_DENSITIES['Steel']
        return (self._get_next_even_number(x + 6)) * (self._get_next_even_number(y + 6)) * (z + 2)


class MasterCalculations:

    def __init__(self):
        self.m_materials = Material()
        self.m_base = BaseCalculations()

    def __call__(self, calculator=BaseCalculations):
        if calculator is Material:
            print("CALC MATCH FOUND")
            return self.m_materials
        else:
            return self.m_base
