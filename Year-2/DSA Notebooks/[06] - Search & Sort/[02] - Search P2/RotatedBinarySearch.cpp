#include <iostream>
using namespace std;

int rotated_binarySearch(int array[], int size, int key) {
    int Low = 0, High = size - 1;

    while (Low <= High) {
        int Mid = Low + (High - Low) / 2;

        if (array[Mid] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << Mid << "] By Rotated Binary Search Search.\n";
            return Mid;
        }

        if (array[Low] <= array[Mid]) { // Normal Half
            if (key >= array[Low] && key < array[Mid]) {
                High = Mid - 1;
            } else {
                Low = Mid + 1;
            }

        } else { // array[Mid] < array[Low] (e.g. [6, 7, 1, 2, 3, 4, 5])
            if (key > array[Mid] && key <= array[High]) {
                Low = Mid + 1;
            } else {
                High = Mid - 1;
            }
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Rotated Binary Search Search.\n";
    return -1;
}

/* ------------------------------------------------------------------------------------------- */

bool isRotated(int array[], int size) {
    int Low = 0, High = size - 1;
    return (array[Low] > array[High]);
}

/* ------------------------------------------------------------------------------------------- */

int getPivot(int array[], int size) { // Returns the pivot index
    int Low = 0, High = size - 1;

    if (array[Low] <= array[High]) return -1; // No rotation
    
    while (Low <= High) {
        int Mid = (Low + High) / 2;

        if (array[Mid] <= array[Mid + 1] && array[Mid] <= array[Mid - 1]) {
            return Mid; // Pivot index
        } else if (array[Mid] <= array[High]) {
            High = Mid - 1;
        } else if (array[Mid] >= array[Low]) {
            Low = Mid + 1;
        }
    }

    return -1;
}

/* ------------------------------------------------------------------------------------------- */

int countRotations(int array[], int size) {
    int index = getPivot(array, size);
    return (index != -1) ? index : 0;
}

/* ------------------------------------------------------------------------------------------- */

int main() {

    int Normal[]  = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int Rotated[] = {4, 5, 6, 7, 8, 9, 1, 2, 3};

    int size = sizeof(Normal) / sizeof(Normal[0]);

/* --------------------------------------------- */

    (isRotated(Normal, size)) ?
    cout << "\nNormal is rotated.\n" : cout << "\nNormal is not rotated.\n";

    (isRotated(Rotated, size)) ?
    cout << "\nRotated is rotated.\n" : cout << "\nRotated is not rotated.\n";

/* --------------------------------------------- */

    int pI = getPivot(Normal, size);
    int rot = countRotations(Normal, size);

    cout << "\nFor the normal array:\n"
         << "Pivot Index : [" << pI << "] , Value : [" << Normal[pI] << "]\n"
         << "Number of rotations : " << rot << ".\n";

    int pI_ = getPivot(Rotated, size);
    int rot_ = countRotations(Rotated, size);

    cout << "\nFor the rotated array:\n"
         << "Pivot Index : [" << pI_ << "] , Value : [" << Rotated[pI_] << "]\n"
         << "Number of rotations : " << rot_ << ".\n";

/* --------------------------------------------- */

    // {4, 5, 6, 7, 8, 9, 1, 2, 3};
    int search = rotated_binarySearch(Rotated, size, 8);  // Mid
        search = rotated_binarySearch(Rotated, size, 2);  // Normal
        search = rotated_binarySearch(Rotated, size, 5);  // Rotated
        search = rotated_binarySearch(Rotated, size, 10); // Not Exist

    return 0;
}