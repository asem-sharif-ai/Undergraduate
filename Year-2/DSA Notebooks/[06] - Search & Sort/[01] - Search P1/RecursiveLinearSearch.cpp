//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │      R e c u r s i v e    L i n e a r      │           S    e    a    r    c    h         │
//* ╰───────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
    static constexpr auto *color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";
    
    static void Start(string name = "Untitled Section", int before = 0, int after = 1) {
    cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n'); }
    
    static void End(char symbol = '-', int number = 50, int before = 1, int after = 0) {
    cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n'); }
    
};

/* ----------------------------------------------------------------------------------------------
---------- DISADVANTAGES ------------------------------------------------------------------------

* Recursive Linear Search has some disadvantages compared to its iterative counterpart, and these
* factors contribute to its classification as a less optimal solution.

* The overhead of function calls and the additional memory requirements for the call stack make
* Recursive Linear Search less efficient in practice, especially for large datasets.

---------- NOTES --------------------------------------------------------------------------------

* Iterative solutions are often preferred over recursive solutions when iteration is possible,
* especially for those algorithms which are based on iterative strategies or dynamic programming,
* are more naturally expressed using loops rather than recursion.

* Iterative solutions usually involve fewer function calls and overhead, which making them more
* efficient in terms of both time and space complexity.

* In iterative solutions, the use of explicit loops eliminates the need for additional stack
* space, leading to more efficient memory usage.

* Recursive calls consume additional stack space for each function call. In the case of large
* datasets, or if the recursion goes too deep, it can lead to a stack overflow.

* While recursion has its merits and is suitable for certain problems, iterative solutions are
* generally prefered in scenarios where the iterative approach provides better performance,
* readability, and control over resource usage.

---------------------------------------------------------------------------------------------- */

int recursive_linearSearch(int array[], int size, int key, int start = 0) {
    if (start < size) {
        if (array[start] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << start << "] By Recursive Linear Search.\n";
            return start;
        } else {
            return recursive_linearSearch(array, size, key, start + 1);
        }

    } else {
        cout << "\nKey [" << key << "] Is Not Found By Recursive Linear Search.\n";
        return -1;
    }
}

int main() {

/* ------------------------------------------------------------------------------------------- */

    Section::Start("Sorted Array");

    int array_1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

    cout << "Array: ";
    for (int element : array_1)
        cout << element << " ";

    int key_1;
    cout << "\n\nEnter A Search Key: ";
    cin >> key_1;

    int index_1 = recursive_linearSearch(array_1, size_1, key_1);

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    Section::Start("UnSorted Array");

    int array_2[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size_2 = sizeof(array_2) / sizeof(array_2[0]);

    cout << "Array: ";
    for (int element : array_2)
        cout << element << " ";

    int key_2;
    cout << "\n\nEnter A Search Key: ";
    cin >> key_2;

    int index_2 = recursive_linearSearch(array_2, size_2, key_2);

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    return 0;
}