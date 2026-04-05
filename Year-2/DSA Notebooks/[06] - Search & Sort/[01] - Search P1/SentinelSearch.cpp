//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │       S   e   n   t   i   n   e   l        │           S    e    a    r    c    h         │
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
---------- BRIEF --------------------------------------------------------------------------------

* Sentinel Search is a specialized form of the linear search algorithm that optimizes the search
* process by strategically placing the search key at the last index of the array, known as a
* sentinel element.

* This eliminates the need to repeatedly check for the end of the array (Range Bounds) during the
* algorithm runtime, consequently, reducing the overall number of comparisons.

---------- DETAILS ------------------------------------------------------------------------------

* Regular Linear Search involves `N` comparisons for the key and the elements comparisons, and an 
* additional `N + 1` comparisons to ensure the index is still within bounds, resulting in `2N + 1`
* comparisons in the worst case. 

?   for (int index = 0; `index < size`; index++) {                                        `N + 1`
?       if (`array[index] == key`) { ... }                                                `N`
?   }

* While Sentinel Search replaces the last element with the search key, ensuring that the algorithm
* will always finds the key within the array, eliminating the need for index range checks.

?   while (`array[index] != key`) { ... }                                                 `N`
?   . . . 
?   if ((`index < size - 1`) || (`array[size - 1] == key`)) { ... }                       `2`

* The approach reduces the number of comparisons by one comparison per step, overall to `N + 2` in
* the worst case, consequently, the time complexity is remarkably cut down.

* It can be slightly more efficient than a Regular Linear Search due to the reduced comparisons.
* However, it's important to note that its overall time complexity remains O(n), just like the
* Regular Linear Search.

* We can conclude that Sentinel Linear Search is regarded as a more efficient implementation of
* the Regular Linear Search algorithm.

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
* │                       │        O(n + 2)  =  O(n)         │               O(1)               │
* │       W o r s t       │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │                   Key Is Found At Index [size-1].                   │
* │                       │                 Key Is Not Found In The Input Data.                 │
* │                       │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------- MODEL --------------------------------------------------------------------------------

* Key = [x] : (Worst Case)

* Before: 
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ q │
*             └───────────────────────────────────────────────────────────────────┘

* While: 
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ x │
*             └───────────────────────────────────────────────────────────────────┘
*              ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴

* After: 
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ q │
*             └───────────────────────────────────────────────────────────────────┘
*                                                                               ⤴

*     `1. index < size - 1 ?`                          //! False.
*     `2. The element at index [size -1] == key ?`     //! False.
*         - Key does not exist.

---------- NOTES --------------------------------------------------------------------------------

* Another approach for defining the sentinel value involves appending a specific, known value at
* the end of the array and modifying the loop to terminate when the current value matches the
* sentinel.

* However, this approach is strongly discouraged due to the potential risk of unintentionally
* introducing the sentinel value in the middle of the array. This can result in unexpected
* logic errors. Furthermore, this approach does not reduce the number of comparisons made
* during the search process.

---------------------------------------------------------------------------------------------- */

int sentinelSearch(int array[], int size, int key) {

    int index = 0, lastElement = array[size - 1];
    array[size-1] = key;   // Sentinel

    while (array[index] != key) {
        index++;
    }

    array[size-1] = lastElement;

    if ((index < size - 1) || (array[size - 1] == key)) {
        cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Sentinel Search.\n";
        return index;
    } else {
        cout << "\nKey [" << key << "] Is Not Found By Sentinel Search.\n";
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

    int index_1 = sentinelSearch(array_1, size_1, key_1);

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

    int index_2 = sentinelSearch(array_2, size_2, key_2);

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    return 0;
}