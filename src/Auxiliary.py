class Auxiliary:

    def _binarySearch(self, arr, left, right, value):
        if left > right:
            return right
        m = (left + right)//2
        if m >= len(arr):
            return len(arr) - 1
        elif value > arr[m]:
            return self._binarySearch(arr, m + 1, right, value)
        elif value < arr[m]:
            return self._binarySearch(arr, left, m - 1, value)
        return m

    def binarySearch(self, arr, value):
        print("Entrada en binary search", value, arr[0], arr[-1], len(arr))
        # Check boundaries
        if value < arr[0]:
            return 0
        if value > arr[-1]:
            return len(arr) - 1
        return self._binarySearch(arr, 0, len(arr) - 1, value)
