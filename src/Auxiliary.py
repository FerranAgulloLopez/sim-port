class Auxiliary:

    def _binarySearch(self, arr, left, right, value):
        if left > right:
            return right
        m = (left + right)//2
        if value > arr[m]:
            return self._binarySearch(arr, m + 1, right, value)
        elif value < arr[m]:
            return self._binarySearch(arr, left, m - 1, value)
        return m

    def binarySearch(self, arr, value):
        return self._binarySearch(arr, 0, len(arr) - 1, value)
