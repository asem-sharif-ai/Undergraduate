//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │         Author: ENG Asem Al-Sharif         │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         B    i    n    a    r    y         │           S    e    a    r    c    h         │
//* ╰───────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
    static constexpr auto*color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";
    
    static void Start(string name = "Untitled Section", int before = 0, int after = 1) {
    cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n'); }
    
    static void End(char symbol = '-', int number = 50, int before = 1, int after = 0) {
    cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n'); }
    
};

/* ----------------------------------------------------------------------------------------------
---------- BRIEF --------------------------------------------------------------------------------

* Binary Search is an efficient search algorithm that defines a High, Low, and Middle values of
* the array assuming it is sorted, Then compares the Middle with the search key, and then, based
* on that, chooses which half will be used as the search space of the next iteration and drops the
* other half of the array. And repeat until:
*      A. The key is set at the Middle value.
*         -> Returns its index.
*      B. Low become greater than high (Search Space Is Empty).
*         -> Returns -1 (Key Not Found).

* Binary Search may fail to get the key index for some existing elements in the unsorted arrays,
* but the advantage is its time complexity for large, sorted elementa ollections.

---------- STEPS --------------------------------------------------------------------------------

* 1. Start from the Middle of the array.
* 2. Compare the Middle element with the search key.
*    3.1. If the Middle element is equal to the search key:                   [L-------K-------H]
*         4.1. Returns the frist Middle index. (Best Case)                     / / / /   \ \ \ \

*    3.2. If the Middle element is greater than the search key:               [L---K---M-------H]
*         4.2. Drop the elements from Middle to High.                         [L---K-H]  \ \ \ \
*              Consider --Middle as newHigh.
*              Calculate newMiddle.
*              Repeat from Step 2.

*    3.3. If the Middle element is smaller than the search key:               [L-------M---K---H]
*         4.3. Drop the elements from Middle to Low.                           / / / /  [L-K---H]
*              Consider ++Middle as newLow.
*              Calculate newMiddle.
*              Repeat from Step 2.

---------- PROPERTIES ---------------------------------------------------------------------------



---------- COMPLIXETY ---------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │  C o m p l e x i t y  │             T i m e              │            S p a c e             │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │               O(1)               │               O(1)               │
* │        B e s t        │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │          Key Is Found At Index [Mid] (At Frist Iteration).          │
* │                       │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │            O(log₂ n)             │               O(1)               │
* │       W o r s t       │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │            Key Is Found At Index [{Low, Mid ± 1, High}].            │
* │                       │                 Key Is Not Found In The Input Data.                 │
* │                       │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘
₂
---------- MODEL --------------------------------------------------------------------------------

* Key = [i] : (Best Case)
*               ▼ Low                           ▼ Mid                           ▼ High
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*             └───────────────────────────────────────────────────────────────────┘
* 3.1 The Middle element is equal to the search key.

 ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

* Key = [j] : (Worst Case)

* Search Space 0 :
*               ▼ Low                           ▼ Mid                           ▼ High
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*             └───────────────────────────────────────────────────────────────────┘
* 3.3 The Middle element is smaller than the search key.


* Search Space 1 :
*                                                  ▼ Low       ▼ Mid           ▼ High
*                                                ┌───────────────────────────────┐
*                                                │ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*                                                └───────────────────────────────┘
* 3.2 The Middle element is greater than the search key.


* Search Space 2 :
*                                                  ▼ L ▼ M ▼ H
*                                                ┌───────────┐
*                                                │ j ─ k ─ l │
*                                                └───────────┘
* 3.2 The Middle element is greater than the search key.


* Search Space 3 :
*                                                ► ▼ ◄
*                                                ┌───┐
*                                                │ j │
*                                                └───┘
* 3.1 The Middle element is equal to the search key.

/* ------------------------------------------------------------------------------------------- */

int binarySearch(int array[], int size, int key) {

    int Low = 0, High = size - 1;

    while (Low <= High) {
        int Mid = (High + Low) / 2;

        if (array[Mid] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << Mid << "] By Binary Search.\n";
            return Mid;

        } else if (array[Mid] > key) {
            High = Mid - 1;
        } else { /* if (array[Mid] < key) */
            Low = Mid + 1;
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Binary Search.\n";
    return -1;
}

int main() {

/* -------------------------------------------------------------------------------------- */

    Section::Start("Sorted Array");

    int array_1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

    cout << "Array : ";
    for (int element : array_1)
        cout << element << " ";

    int key_1;
    cout << "\nEnter A Search Key: ";
    cin >> key_1;

    int index_1 = binarySearch(array_1, size_1, key_1);

    Section::End();

/* -------------------------------------------------------------------------------------- */

    Section::Start("UnSorted Array");

    int array_2[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size_2 = sizeof(array_2) / sizeof(array_2[0]);

    cout << "Array : ";
    for (int element : array_2)
        cout << element << " ";

    int key_2;
    cout << "\nEnter A Search Key: ";
    cin >> key_2;   // Success: 1, 4, 7, 15

    int index_2 = binarySearch(array_2, size_2, key_2);

    int key_3;
    cout << "\nEnter A Search Key: ";
    cin >> key_3;   // Fail: All Remaining Keys.

    int index_3 = binarySearch(array_2, size_2, key_3);

    Section::End();

/* -------------------------------------------------------------------------------------- */

    return 0;
}