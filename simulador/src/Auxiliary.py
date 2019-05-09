class Auxiliary:
    def binarySearch(self, arr, left, right, value):
        if left > right:
            return right
        m = (left + right)//2
        if m >= len(arr):
            return len(arr) - 1
        elif value > arr[m]:
            return self.binarySearch(arr, m + 1, right, value)
        elif value < arr[m]:
            return self.binarySearch(arr, left, m - 1, value)
        return m
