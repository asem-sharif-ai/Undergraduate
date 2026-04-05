//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │         Author: ENG Asem Al-Sharif         │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │           J      u      m      p           │           S    e    a    r    c    h         │
//* ╰───────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
    static void Start(string name = "Untiteled Section", int before = 0, int after = 1) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[4;91m" << name << ":\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
    static void End(char symbol = '-', int number = 50, int before = 1, int after = 0) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[91m" << string(number, symbol) << "\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
};

/* ----------------------------------------------------------------------------------------------
---------- BRIEF --------------------------------------------------------------------------------

* Jump Search is a searching algorithm for sorted arrays. The main idea is to check fewer elements
* (than linear search) by jumping ahead by fixed step size or skipping some elements in place of
* searching all elements.

* Jump Search is Better than a linear search for arrays where the elements are uniformly
* distributed, as the number of steps taken in jump search is proportional to the square root of
* the size of the array, making it more efficient for large arrays.

* Jump search works well only for with sorted and very almost sorted arrays., as it jumps to a
* closer position in the array with each iteration.

---------- STEPS --------------------------------------------------------------------------------

* 1. Set a block size equal to sqrt(size), and start from the beginning of the array.

* 2. Compare the pre last element of the current iteration block (Assumed to be the biggest in 
*    sorted arrays) with the key:

*    2.1 If that last element is greater than or equal to the key.
*        3.1. Perform a linear search in the current block.
*             4.1. Return the matching element index.
*             4.2. Return [-1] if no matching element was found.

*    2.2. If that last element is smaller than the key.
*         3.2. Skip the current block.

*    2.3. If it reaches the end of the array without finding a suitable block for the key.
*         3.3 Return [-1].

---------- PROPERTIES ---------------------------------------------------------------------------

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

---------- COMPLIXETY ---------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │  C o m p l e x i t y  │             T i m e              │            S p a c e             │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │               O(1)               │               O(1)               │
* │        B e s t        │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │                      Key Is Found At Index [0]                      │
* │                       │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │              O(√n)               │               O(1)               │
* │       W o r s t       │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │                   Key Is Found At Index [size-1].                   │
* │                       │                 Key Is Not Found In The Input Data.                 │
* │                       │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------- MODEL --------------------------------------------------------------------------------

* Key = [i] (Average Case), ∵ Size = 17, ∴ Block Size = sqrt(17) = 4.

* 1. Create Blocks And Compare The Last Element With the Key:
*     ▼           ▼
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
* [array[min(jump, size) - 1] < key] -> [c < i] True, Skip Block.

*                 ▼           ▼
*               ┌───────────────────────────────────────────────────────┐
*               │ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*               └───────────────────────────────────────────────────────┘
* [array[min(jump, size) - 1] < key] -> [f < i] True, Skip Block.

*                             ▼           ▼
*                           ┌───────────────────────────────────────────┐
*                           │ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*                           └───────────────────────────────────────────┘
* [array[min(jump, size) - 1] < key] -> [i < i] False, Stop.


* 2. Do Linear Search Within The Key's Block:
*                           ┌───────────────┐
*                           │ g ─ h ─ i ─ j │
*                           └───────────────┘
*                            ⤴  ⤴  ⤴

---------------------------------------------------------------------------------------------- */

#include <cmath>

int jumpSearch(int array[], int size, int key) {

    int start = 0, jump = sqrt(size);
    
    while (array[min(jump, size) - 1] < key) {
        start = jump;
        jump += sqrt(size);

        if (start >= size) {
            cout << "\nKey [" << key << "] Is Not Found By Jump Search.\n";
            return -1;
        } 
    }

    // Do Linear Search Within The Key's Range Block
    for (int index = start; index < min(jump, size); index++) {
        if (array[index] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Jump Search.\n";
            return index;
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Jump Search.\n";
    return -1;
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

    int index_1 = jumpSearch(array_1, size_1, key_1);

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

    int index_2 = jumpSearch(array_2, size_2, key_2);

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    return 0;
}