//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │         Author: ENG Asem Al-Sharif         │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         T   e   r   n   a   r   y          │           S    e    a    r    c    h         │
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

* Ternary Search is an efficient search algorithm that defines a High, Low, and Third values of
* the array assuming it is sorted, then works by dividing the array into three parts instead of
* two, as done in Binary Search.

* This trisection approach enhances its ability to navigate through the array, potentially 
* accelerating the search process.

---------- STEPS --------------------------------------------------------------------------------

* Similar to Binary Search, but consider dividing the array into three parts instead of the two.

---------- COMPLIXETY ---------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │  C o m p l e x i t y  │             T i m e              │            S p a c e             │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │               O(1)               │               O(1)               │
* │        B e s t        │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │      Key Is Found At Index [{L_Th, H_Th}] (At Frist Iteration).     │
* │                       │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │            O(log₃ n)             │               O(1)               │
* │       W o r s t       │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │       Key Is Found At Index [{Low, L_Th ± 1, H_Th ± 1, High}].      │
* │                       │                 Key Is Not Found In The Input Data.                 │
* │                       │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------- MODEL --------------------------------------------------------------------------------

* Key = [f] OR [l] : (Best Case)
*               ▼ Low               ▼ L_Th                  ▼ R_Th              ▼ High
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*             └───────────────────────────────────────────────────────────────────┘

 ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

* Key = [j] : (Average Case)

* Search Space 0 :
*               ▼ Low               ▼ L_Th                  ▼ R_Th              ▼ High
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*             └───────────────────────────────────────────────────────────────────┘


* Search Space 1 :
*                                       ▼   ▼       ▼ h ▼
*                                     ┌───────────────────┐
*                                     │ g ─ h ─ i ─ j ─ k │
*                                     └───────────────────┘

/* ------------------------------------------------------------------------------------------- */

int ternarySearch(int array[], int size, int key) {

    int Low = 0, High = size - 1;

    while (Low <= High) {
        int Third = (High - Low) / 3;
        int lowThird  = Low + Third;    // One Third.
        int highThird = High - Third;   // Two Thirds.

        if (array[lowThird] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << lowThird << "] By Ternary Search.\n";
            return lowThird;
        } else if (array[highThird] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << highThird << "] By Ternary Search.\n";
            return highThird;
        } else if (array[lowThird] > key) {
            High = lowThird - 1;
        } else if (array[highThird] < key) {
            Low = highThird + 1;
        } else {  /* if (array[lowThird] < key < array[highThird]) */
            Low = lowThird + 1;
            High = highThird - 1;
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Ternary Search.\n";
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

    int index_1 = ternarySearch(array_1, size_1, key_1);

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("UnSorted Array");

    int array_2[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size_2 = sizeof(array_2) / sizeof(array_2[0]);

    cout << "Array : ";
    for (int element : array_2)
        cout << element << " ";

    int key_2;
    cout << "\nEnter A Search Key: ";
    cin >> key_2;   // Success: 3, 8, 13

    int index_2 = ternarySearch(array_2, size_2, key_2);

    int key_3;
    cout << "\nEnter A Search Key: ";
    cin >> key_3;   // Fail: All Remaining Keys.

    int index_3 = ternarySearch(array_2, size_2, key_3);

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    return 0;
}