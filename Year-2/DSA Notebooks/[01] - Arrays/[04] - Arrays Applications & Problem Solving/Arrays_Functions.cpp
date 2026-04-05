//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures And Algorithms          │              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮ ╰───────────────────────────────────────────────╮
//* │               A   r   r   a   y               │             F  u  n  c  t  i  o  n  s           │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
static constexpr auto *color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";

static void Start(string name = "Untitled Section", int before = 0, int after = 1)
{cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n');}

static void End(char symbol = '-', int number = 50, int before = 1, int after = 0)
{ cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n');}

};

/* ------------------------------------------------------------------------------------------------- */

void display(int array[], int size, int slice = 0, int before = 1, int after = 1) {

        slice = min(max(slice, 0), size);

        cout << string(++before, '\n');

        for (int i = 0; i < slice; i++) {
            cout << ((i == 0) ? "[ " : "") << array[i] << " " << ((i == slice-1) ? "]" : "");
        }

        cout << string(++after, '\n');
}

/* ------------------------------------------------------------------------------------------------- */

void reverse(int array[], int size) {
    int i = 0, ii = size - 1;

    while (i < ii) {
        int temporary = array[i];
        array[i] = array[ii];
        array[ii] = temporary;

        i++; ii--;
    }
}

/* ------------------------------------------------------------------------------------------------- */

int *merge(int array_1[], int size_1, int array_2[], int size_2) {
    int* array_3 = new int[size_1 + size_2];

    for (int i = 0; i < size_1; i++)
        array_3[i] = array_1[i];
    for (int i = 0; i < size_2; i++)
        array_3[size_1 + i] = array_2[i];

    return array_3;
}

/* ------------------------------------------------------------------------------------------------- */

int *split(int array[], int size, int index = 0, int choice = 0) {

    (index == 0) ? index = size / 2 : index;
    
    int *array_1 = new int[index], *array_2 = new int[size - index], i = 0;

    while (i < index) {
        array_1[i] = array[i];
        i++;
    }

    while (i < size) {
        array_2[i - index] = array[i];
        i++;
    }

    if      (choice == 1) return array_1;
    else if (choice == 2) return array_2;
    else return array;
}

/* ------------------------------------------------------------------------------------------------- */

void showInfo(int array[], int size) {

    int Sum = 0, Min = array[0], Max = array[0];
    for (int i = 0; i < size; i++) {
        Sum += array[i];
        if (array[i] > Min) Min = array[i];
        if (array[i] < Max) Max = array[i];
    }

    double Avg = (double) 1.0 * Sum / size;

    cout << "\nSum     = " << Sum
         << "\nAverage = " << Avg
         << "\nMin     = " << Min
         << "\nMax     = " << Max << endl;
}

/* ------------------------------------------------------------------------------------------------- */

void isSorted(int array[], int size) {
    bool ascending = true, descending = true;

    for (int i = 1; i < size; ++i) {
        if (array[i] < array[i - 1]) {
            ascending = false;
        } else if (array[i] > array[i - 1]) {
            descending = false;
        }

        if (!ascending && !descending) {
            break;
        }
    }

    if (ascending) {
        cout << "\nThe array is sorted in ascending order.\n";
    } else if (descending) {
        cout << "\nThe array is sorted in descending order.\n";
    } else {
        cout << "\nThe array is not sorted.\n";
    }
}

/* ------------------------------------------------------------------------------------------------- */

int main() {

    // Static-Sorted
    int array_SS[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int size_SS = sizeof(array_SS) / sizeof(array_SS[0]);

    // Static-UnSorted
    int array_SU[] = {5, 7, 2, 3, 6, 1, 9, 4, 10, 8};
    int size_SU = sizeof(array_SU) / sizeof(array_SU[0]);

    // Dynamic-Sorted
    int* array_DS = new int[15]{11, 12, 13, 14, 15, 16, 17, 18, 19, 20};
    int size_DS = 10;
    
    // Dynamic-UnSorted
    int* array_DU = new int[15]{15, 17, 12, 13, 16, 11, 19, 14, 20, 18};
    int size_DU = 10;

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    display(array_SS, size_SS);
    reverse(array_SS, size_SS);
    display(array_SS, size_SS);

    cout << "\n──────────────────────────────────\n" ;

    display(array_SU, size_SU);
    reverse(array_SU, size_SU);
    display(array_SU, size_SU);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    display(array_DS, size_DS);
    reverse(array_DS, size_DS);
    display(array_DS, size_DS);

    cout << "\n──────────────────────────────────\n" ;

    display(array_DU, size_DU);
    reverse(array_DU, size_DU);
    display(array_DU, size_DU);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    reverse(array_SS, size_SS); reverse(array_DS, size_DS);  // Reset

    int* array_m = merge(array_SS, size_SS, array_DS, size_DS);
    int size_m = size_SS + size_DS;
    display(array_m, size_m);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    int* array_s1 = split(array_m, size_m, 5, 1);
    int size_s1 = 5;
    display(array_s1, size_s1);

    cout << "\n──────────────────────────────────\n" ;

    int* array_s2 = split(array_m, size_m, 5, 2);
    int size_s2 = size_m - 5;
    display(array_s2, size_s2);

    cout << "\n──────────────────────────────────\n" ;

    int* array_s3 = split(array_m, size_m, -1, 1);
    int size_s3 = size_m / 2;
    display(array_s3, size_s3);

    cout << "\n──────────────────────────────────\n" ;

    int* array_s4 = split(array_m, size_m, -1, 2);
    int size_s4 = size_m / 2;
    display(array_s4, size_s4);

    // cout << "\n──────────────────────────────────\n" ;

    // int* array_s0 = split(array_m, size_m);
    // int size_s0 = 5;
    // display(array_s0, size_s0);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    isSorted(array_SS, size_SS);
    isSorted(array_DS, size_DS);

    cout << "\n──────────────────────────────────\n" ;

    reverse(array_SS, size_SS); reverse(array_DS, size_DS);

    isSorted(array_SS, size_SS);
    isSorted(array_DS, size_DS);

    cout << "\n──────────────────────────────────\n" ;

    isSorted(array_SU, size_SU);
    isSorted(array_DU, size_DU);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    showInfo(array_SS, size_SS);

    cout << "\n──────────────────────────────────\n" ;

    showInfo(array_SU, size_SU);

    cout << "\n──────────────────────────────────\n" ;

    showInfo(array_DS, size_DS);

    cout << "\n──────────────────────────────────\n" ;

    showInfo(array_DU, size_DU);

    cout << "\n────────────────────────────────────────────────────────────────────\n" ;

    return 0;
}