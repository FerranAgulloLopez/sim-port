from src.Constants import Constants


class Auxiliary:

    def _binarySearch(self, arr, left, right, value):
        if left > right:
            return right
        m = (left + right) // 2
        if value > arr[m]:
            return self._binarySearch(arr, m + 1, right, value)
        elif value < arr[m]:
            return self._binarySearch(arr, left, m - 1, value)
        return m

    def binarySearch(self, arr, value):
        return self._binarySearch(arr, 0, len(arr) - 1, value)


def get_fitness(output_file):
    """ reads stats from the default output_file and determines the viability and benefits """
    total_idle_magnitude = 0
    with open(output_file + '.stats.csv', 'r') as ifs:
        headers = ifs.readline()[:-1].split(',')
        data = ifs.readline()[:-1].split(',')
        for idx in range(len(headers)):
            if headers[idx] == 'Shift_Type':
                duration = float(data[idx + 1])  # in h
                capacity_usage = float(data[idx + 2])  # in %
                if capacity_usage >= Constants.MAX_CAPACITY_USAGE:  # def 70%
                    return 0
                partial_idle_time = (100 - capacity_usage) * duration  # in h
                # Squared for prioritizing magnitude over dispersion of idle time through the shifts
                partial_magnitude = partial_idle_time * partial_idle_time
                total_idle_magnitude += partial_magnitude
    return total_idle_magnitude
