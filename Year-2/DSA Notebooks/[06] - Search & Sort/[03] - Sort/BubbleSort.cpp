//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │     B     u     b     b     l     e    │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Bubble Sort is a simple comparison-based sorting algorithm that iterates through the 
* array multiple times, and repeatedly compares adjacent elements, and swaps them
* if they are in the wrong order (the element on the left > the element on the right).

------ COMPLIXETY -----------------------------------------------------------------------

*                   ┌───────────────────────────────────────────────────────────────┐
*      ┌──────────┐ │                 C  o  m  p  l  e  x  i  t  y                  │ 
*      │  Stable  │ │───────────────────────────────────────────────────────────────│
*      └──────────┘ │            T i m e            │           S p a c e           │ 
*    ┌──────────────┘───────────────────────────────────────────────────────────────│
*    │  Best Case   │             O(n)              │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │   Average    │             O(n^2)            │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │    Worst     │             O(n^2)            │             O(1)              │
*    └──────────────────────────────────────────────────────────────────────────────┘

------ STEPS ----------------------------------------------------------------------------

* 1. Start with the first element in the array.
* 2. Compare the current element with the next element.
* 3. Swap (Current, Next) for all elements such Current [i] > Next [i+1].
* 3. Move to the next pair of elements and repeat the comparison and swap process.
* 4. Repeat until the current iteration counter reaches the pre-last element.


* Key Points:

* key : Represents the current iteration frist unsorted value.
*       - Necessary to avoid losing values while swapping.

* [i] : Represents the current iteration counter, it increases after each loop.
*       - Action: [[0 -> size-2]] ||| i++ after completing each iteration.

*        [ii] : Represents the current comparison forwarding counter in each loop.
*               - Action: [[0 -> size-i-1]] ||| ii++ after each comparison.

* The algorithm action is based on very simple condition, which is:
* If Value_At_Current > Value_At_Next, Swap.

* The sorted part of the array shows from the end, as the algorithm keeps swapping each 
* pair to set the smaller value at the first order. Consequently, the bigger values are 
* left at the end of the array after each iteration. This is the main concept of limiting 
* [ii] to [size - i - 1], where [i] increases by 1, and the 1 value (biggest of the current 
* iteration values) is moved to the last order.

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐
*        1. │       U n S o r t e d       │    ->   2. │      UnSorted      │ Sorted │
*           └─────────────────────────────┘            └─────────────────────────────┘

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐
*        3. │   UnSorted   │    Sorted    │    ->   4. │ UnSorted │      Sorted      │
*           └─────────────────────────────┘            └─────────────────────────────┘

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐
*        5. │  Un  │        Sorted        │    ->   6. │         S o r t e d         │
*           └─────────────────────────────┘            └─────────────────────────────┘

* In other words, it BUBBLES each pair of elements, and every iteration ends by placing
* the max value at the end.

*           ┌─────────────────────────────┐            ┌─────────────────────────────┐
*        1. │  Z  │  1  │  2  │  3  │  A  │    ->   2. │  1  │  2  │  3  │  A  │  Z  │
*           └─────────────────────────────┘            └─────────────────────────────┘
*              ▲ Max Value                     ..        All in one, frist iteration.

* 1. swap(Z, 1) -> [1, Z, 2, 3, A]   ->   2. swap(Z, 2) -> [1, 2, Z, 3, A]
* 3. swap(Z, 3) -> [1, 2, 3, Z, A]   ->   4. swap(Z, A) -> [1, 2, 3, A, Z]

------ MODEL ----------------------------------------------------------------------------

* --------------------- Iteration 0 [i = 0 | ii = 0:3 | Key = 1] : ----------------------

*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │                                     // Start
*           └─────────────────────────────┘
*              ▲ ii                 │ -> Stop


* Iteration 0.0 :
*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │    //? 1 < 8 Skip
*           └─────────────────────────────┘
*              ▲ ii

* Iteration 0.1 :
*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │    //! 8 > 3 Swap -> [1, 3, 8, 0, 5]
*           └─────────────────────────────┘
*                    ▲ ii

* Iteration 0.2 :
*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  8  │  0  │  5  │    //! 8 > 0 Swap -> [1, 3, 0, 8, 5]
*           └─────────────────────────────┘
*                          ▲ ii

* Iteration 0.3 :
*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  0  │  8  │  5  │    //! 8 > 5 Swap -> [1, 3, 0, 5, 8]
*           └─────────────────────────────┘
*                                ▲ ii

*              ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  0  │  5  │  8  │
*           └─────────────────────────────┘
*                                ▲ ii (Stop)


* --------------------- Iteration 1 [i = 1 | ii = 0:2 | Key = 3] : ----------------------

*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  0  │  5  │  8  │
*           └─────────────────────────────┘
*              ▲ ii           │ -> Stop

* Iteration 1.0 :
*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  0  │  5  │  8  │    //? 1 < 3 Skip
*           └─────────────────────────────┘
*              ▲ ii

* Iteration 1.1 :
*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  0  │  5  │  8  │    //! 3 > 0 Swap -> [1, 0, 3, 5, 8]
*           └─────────────────────────────┘
*                    ▲ ii

* Iteration 1.2 :
*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  0  │  3  │  5  │  8  │    //? 3 < 5 Skip
*           └─────────────────────────────┘
*                          ▲ ii

*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  0  │  3  │  5  │  8  │
*           └─────────────────────────────┘
*                          ▲ ii (Stop)


* --------------------- Iteration 2 [i = 2 | ii = 0:1 | Key = 3] : ----------------------

*                          ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  0  │  3  │  5  │  8  │
*           └─────────────────────────────┘
*              ▲ ii     │ -> Stop

* Iteration 2.0 :
*                          ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  0  │  3  │  5  │  8  │    //! 1 > 0 Swap -> [0, 1, 3, 5, 8]
*           └─────────────────────────────┘
*              ▲ ii

* Iteration 2.1 :
*                          ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │    //? 1 < 3 Skip
*           └─────────────────────────────┘
*                    ▲ ii

*                          ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │
*           └─────────────────────────────┘
*                    ▲ ii (Stop)


* --------------------- Iteration 3 [i = 3 | ii = 0:0 | Key = 5] : ----------------------

*                                ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │
*           └─────────────────────────────┘
*           ii ▲  │ -> Stop

* Iteration 3.0 :
*                                ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │    //? 0 < 1 Skip
*           └─────────────────────────────┘
*              ▲ ii

*                                ▼ i (Stop)
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │                                        // End
*           └─────────────────────────────┘
*              ▲ ii (Stop)

----------------------------------------------------------------------------------------- */

void bubbleSort(int array[], int size) {
    int key, i, ii;

    for (i = 0; i < size - 1; i++) {

        for (ii = 0; ii < size - i - 1; ii++) {

            if (array[ii] > array[ii + 1]) {
                key = array[ii];
                array[ii] = array[ii + 1];
                array[ii + 1] = key;
            }
        }
    }

    cout << "\n\nArray Is Sorted Successfully By Bubble Sort Algorithm.\n\n";
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    bubbleSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}