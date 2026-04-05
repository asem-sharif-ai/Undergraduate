#include <iostream>
using namespace std;

int recursive_binarySearch(int array[], int size, int key, int Low, int High) {
    if (Low <= High) {
        int Mid = (High + Low) / 2;

        if (array[Mid] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << Mid << "] By Recursive Binary Search.\n";
            return Mid;
        } else if (array[Mid] > key) {
            return recursive_binarySearch(array, size, key, Low, Mid - 1);
        } else {  // array[Mid] < key
            return recursive_binarySearch(array, size, key, Mid + 1, High);
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Recursive Binary Search.\n";
    return -1;
}

int recursive_binarySearch(int array[], int size, int key) {
    return recursive_binarySearch(array, size, key, 0, size - 1);
}
