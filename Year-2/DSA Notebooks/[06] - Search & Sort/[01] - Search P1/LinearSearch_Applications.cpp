#include <iostream>
using namespace std;

//* Direction = (1 -> `LTR` -> {0; size-1; ++}) || (-1 -> `RTL` -> {size-1; 0; --})

int directed_linearSearch(int array[], int size, int key, int direction = 1) {

    int index = -1;
    direction = (direction != 0) ? max(min(direction, 1), -1) : 1; // {-ve = 1, +ve = 1, 0 = 1}

    for (int i = (direction == 1 ? 0 : size - 1); (direction == 1 ? (i < size) : (i >= 0)); i += direction) {
        if (array[i] == key) {
            index = i;
            break;
        }
    }

    (index != -1)
    ? cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By "
           << (direction == 1 ? "`LTR`" : "`RTL`") << " Linear Search.\n"

    : cout << "\nKey [" << key << "] Is Not Found By Linear Search.\n";

    return index;
}

/* ------------------------------------------------------------------------------------------- */

//* Simpler Implementation:
int directed_linearSearch_(int array[], int size, int key, int direction = 1) {
    
    direction = (direction != 0) ? max(min(direction, 1), -1) : 1;

    if (direction == 1) {
        for (int index = 0; index < size; index++) {
            if (array[index] == key) {
                cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By `LTR` Linear Search.\n";
                return index;
            }
        }
    } else {
        for (int index = size - 1; index >= 0; index--) {
            if (array[index] == key) {
                cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By `RTL` Linear Search.\n";
                return index;
            }
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Linear Search.\n";
    return -1;
}

/* ------------------------------------------------------------------------------------------- */

int countFrequency(int array[], int size, int key, int start = 0) {
    int count = 0;
    for (int index = start; index < size; index++) {
        (array[index] == key) ? count++ : count;
    }

    (count != 0)
    ? cout << "\nKey [" << key << "] Was Found [" << count << "] Times By Linear Search.\n"
    : cout << "\nKey [" << key << "] Was Not Found By Linear Search.\n";

    return count;
}

/* ------------------------------------------------------------------------------------------- */

int removeDuplicates(int array[], int size, int key, bool all = false) {

    for (int i = size - 1; i >= 0; i--) {
        if (array[i] == key) {
            if (all) {
                for (int ii = i; ii < size - 1; ii++) {
                    array[ii] = array[ii + 1];
                } size--;
            } else {
                all = true;
            }
        }
    }

    return size;
}

/* ------------------------------------------------------------------------------------------- */

int main() {

    int array[] = {1, 1, 2, 9, 8, 9, 8, 2, 2, 3, 4, 5, 4, 5, 8};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "\nArray: ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << (i < size-1 ? ", " : "\n");
    } cout << "Size: " << size << endl;

/* ------------------------------------------------------------------------------------------- */

    int search = directed_linearSearch (array, size, 2,  1); // 2
        search = directed_linearSearch (array, size, 2, -1); // 8
        search = directed_linearSearch_(array, size, 1,  1); // 0
        search = directed_linearSearch_(array, size, 1, -1); // 1

/* ------------------------------------------------------------------------------------------- */

    int Frequency = countFrequency(array, size, 2); // 3
        Frequency = countFrequency(array, size, 8); // 3

/* ------------------------------------------------------------------------------------------- */

    size = removeDuplicates(array, size, 2);    // 1, 1, 9, 8, 9, 8, 2, 3, 4, 5, 4, 5, 8

    cout << "\nRemove [2] (Let One): ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << (i < size-1 ? ", " : "\n");
    } cout << "Size: " << size << endl;

/* ------------------------------------------------------------------------------------------- */

    size = removeDuplicates(array, size, 9, 1); // 1, 1, 8, 8, 2, 3, 4, 5, 4, 5, 8
    size = removeDuplicates(array, size, 4, 1); // 1, 1, 8, 8, 2, 3, 5, 5, 8

    cout << "\nRemove [9] And [4] (All): ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << (i < size-1 ? ", " : "\n");
    } cout << "Size: " << size << endl;

/* ------------------------------------------------------------------------------------------- */

    size = removeDuplicates(array, size, 8);    // 1, 1, 2, 3, 5, 5, 8

    cout << "\nRemove [8] (Let One): ";
    for (int i = 0; i < size; i++) {
        cout << array[i] << (i < size-1 ? ", " : "\n");
    } cout << "Size: " << size << endl;

/* ------------------------------------------------------------------------------------------- */

    return 0;
}