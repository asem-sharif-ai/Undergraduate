//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │    S   e   l   e   c   t   i   o   n   │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Selection Sort is a simple comparison-based sorting algorithm. It works by dividing the
* input array into two parts: [A. Sorted] and [B. Unsorted]. (Like Insertion Sort)

* Then, repeatedly SELECTS the smallest (or largest, depending on the sorting order)
* element from the unsorted part and swap it with the frist element in the unsorted part.

* After each iteration, the sorted part is increased by 1 element, so the algorithm skips
* the last sorted element and continues to increase the sorted part until it reaches the
* penultimate element.

------ COMPLIXETY -----------------------------------------------------------------------

*                   ┌───────────────────────────────────────────────────────────────┐
*      ┌──────────┐ │                 C  o  m  p  l  e  x  i  t  y                  │ 
*      │ UnStable │ │───────────────────────────────────────────────────────────────│
*      └──────────┘ │            T i m e            │           S p a c e           │ 
*    ┌──────────────┘───────────────────────────────────────────────────────────────│
*    │  Best Case   │             O(n^2)            │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │   Average    │             O(n^2)            │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │    Worst     │             O(n^2)            │             O(1)              │
*    └──────────────────────────────────────────────────────────────────────────────┘

------ STEPS ----------------------------------------------------------------------------

* 1. Save the First Unsorted Value (it may be swapped if it isn't the lowest).

* 2. Assume that the First is the Lowest.

* 3. Loop and compare the lowest with all remaining elements (try to update the lowest).

* 4. Swap the First Element with the Lowest.
*    4.1. If it was the real Lowest -> No change.
*    4.2. Else, the Lowest is set in its correct order.

* 5. Repeat until the current iteration counter reaches the pre-last element.
*    (The last element never was selected as Lowest, so it has to be the largest)


* key : Represents the current iteration frist unsorted value.
*       - Necessary to avoid losing values while swapping.

* [i] : Represents the current iteration counter, it increases after each loop.
*       - Action: [[0 -> size-1]] ||| i++ after completing each iteration.

*        [ii] : Represents the current comparison forwarding counter in each loop.
*               - Action: [[i+1 -> size-1]] ||| ii++ after each comparison.

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐ 
*        1. │ S. │        UnSorted        │    ->   2. │ Sorted │      UnSorted      │
*           └─────────────────────────────┘            └─────────────────────────────┘

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐ 
*        3. │   Sorted   │    UnSorted    │    ->   4. │     Sorted     │  UnSorted  │
*           └─────────────────────────────┘            └─────────────────────────────┘

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐ 
*        5. │       Sorted       │  UnS.  │    ->   6. │         Sorted         │ Un │
*           └─────────────────────────────┘            └─────────────────────────────┘

------ MODEL ----------------------------------------------------------------------------

* -------------------- Iteration 0 [i, L = 0 | ii = 1:4 | Key = 1] : --------------------

*            L ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │                                     // Start
*           └─────────────────────────────┘
*                    ▲ ii

* Iteration 0.0 :
*            L ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │    //? 8 > 1 Skip
*           └─────────────────────────────┘
*                    ▲ ii

* Iteration 0.1 :
*            L ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │    //? 3 > 1 Skip
*           └─────────────────────────────┘
*                          ▲ ii

* Iteration 0.2 :
*              ▼ i               ▼ L
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │    //! 0 < 1 Hold (Update L)
*           └─────────────────────────────┘
*                                ▲ ii

* Iteration 0.3 :
*              ▼ i               ▼ L
*           ┌─────────────────────────────┐    
*           │  1  │  8  │  3  │  0  │  5  │    //? 5 > 0 Skip
*           └─────────────────────────────┘
*                                      ▲ ii (Stop)

ToDo: array[i] = array[L];
ToDo: array[L] = key;

*              ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  8  │  3  │  1  │  5  │
*           └─────────────────────────────┘
*                                      ▲ ii


* -------------------- Iteration 1 [i, L = 1 | ii = 2:4 | Key = 8] : --------------------

*                  L ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  8  │  3  │  1  │  5  │
*           └─────────────────────────────┘
*                          ▲ ii

* Iteration 1.0 :
*                    ▼ i   ▼ L
*           ┌─────────────────────────────┐
*           │  0  │  8  │  3  │  1  │  5  │    //! 3 < 8 Hold (Update L)
*           └─────────────────────────────┘
*                          ▲ ii

* Iteration 1.1 :
*                    ▼ i         ▼ L
*           ┌─────────────────────────────┐
*           │  0  │  8  │  3  │  1  │  5  │    //! 1 < 3 Hold (Update L)
*           └─────────────────────────────┘
*                                ▲ ii

* Iteration 1.2 :
*                    ▼ i         ▼ L
*           ┌─────────────────────────────┐
*           │  0  │  8  │  3  │  1  │  5  │    //? 5 > 1 Skip
*           └─────────────────────────────┘
*                                      ▲ ii (Stop)

ToDo: array[i] = array[L];
ToDo: array[L] = key;

*                    ▼ i         ▼ L
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │
*           └─────────────────────────────┘
*                                      ▲ ii


* -------------------- Iteration 2 [i, L = 2 | ii = 3:4 | Key = 3] : --------------------

*                        L ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │
*           └─────────────────────────────┘
*                                ▲ ii

* Iteration 2.0 :
*                        L ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │    //? 8 > 3 Skip
*           └─────────────────────────────┘
*                                ▲ ii

* Iteration 2.1 :
*                        L ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │    //? 5 > 3 Skip
*           └─────────────────────────────┘
*                                      ▲ ii (Stop)

* Initial [L] is set at [i] so if it is not updated to any of [ii], [i] is the lowest.

* Swapping ([i], [L]) will be executed, but it does not change anything when there is
* no such update from the loop.

* -------------------- Iteration 3 [i, L = 3 | ii = 4:4 | Key = 8] : --------------------

*                              L ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │
*           └─────────────────────────────┘
*                                      ▲ ii

* Iteration 3.0 :
*                                ▼ i   ▼ L
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │    //! 5 < 8 Hold (Update L)
*           └─────────────────────────────┘
*                                      ▲ ii (Stop)

ToDo: array[i] = array[L];
ToDo: array[L] = key;

*                                ▼ i (Stop)
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │                                        // End
*           └─────────────────────────────┘
*                                      ▲ ii (Stop)

----------------------------------------------------------------------------------------- */

void selectionSort(int array[], int size) {
    int key, i, ii;

    for (i = 0; i < size-1; i++) {
        key = array[i];
        int L = i;

        for (ii = i+1; ii < size; ii++) {
            if (array[ii] < array[L]) {
                L = ii;
            }
        }

        array[i] = array[L];
        array[L] = key;
    }

    cout << "\n\nArray Is Sorted Successfully By Selection Sort Algorithm.\n\n";
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    selectionSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";
        
    return 0;
}