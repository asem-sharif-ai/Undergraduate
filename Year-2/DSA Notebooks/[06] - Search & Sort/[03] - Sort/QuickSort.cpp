//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │        Q     u     i     c     k       │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Quick Sort is an efficient sorting algorithm based on the divide-and-conquer strategy.

* The main idea behind Quick Sort is to select a Pivot element and partition the other
* elements into two sub-arrays, according to whether they are less than or greater than
* the pivot. Then recursively sort the sub-arrays.

* Key Points:
* - The recursion stops when the sub-arrays reach a size of 1 or 0. 
*   At this point, the array is considered sorted and combined to produce the final array.

------ COMPLIXETY -----------------------------------------------------------------------

*                   ┌───────────────────────────────────────────────────────────────┐
*      ┌──────────┐ │                 C  o  m  p  l  e  x  i  t  y                  │ 
*      │ UnStable │ │───────────────────────────────────────────────────────────────│
*      └──────────┘ │            T i m e            │           S p a c e           │ 
*    ┌──────────────┘───────────────────────────────────────────────────────────────│
*    │  Best Case   │          O(n log(n))          │             O(n)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │   Average    │          O(n log(n))          │             O(n)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │    Worst     │          O(n^2)               │             O(n)              │
*    └──────────────────────────────────────────────────────────────────────────────┘

------ STEPS ----------------------------------------------------------------------------

* 1. Choose a Pivot element to serve as the center value. This could be the first element,
*    the last element, a randomly chosen element, or the median of the array.

* 2. Place the Pivot in its correct position, ensuring that:
*    - All elements greater than the pivot are placed to its right.
*    - All elements smaller than the pivot are placed to its left.

* 3. Recursively apply the algorithm to sort the elements on the left side of the pivot,
*    and the elements on the right side of the pivot.

*                           ┌─────────────────────────────┐
*                           │  B  │  A  │  P  │  Y  │  X  │    [(B ? A) < P < (Y ? X)]
*                           └─────────────────────────────┘

*                           ┌───────────┐ 
*                           │  B  │  A  │    Sort (Left)
*                           └───────────┘ 
*                           ┌───────────┐ 
*                           │  Y  │  X  │    Sort (Right)
*                           └───────────┘ 

*                           ┌─────────────────────────────┐
*                           │  A  │  B  │  P  │  X  │  Y  │     [ A < B < P < X < Y ]
*                           └─────────────────────────────┘

------ MODEL ----------------------------------------------------------------------------

*                           ┌─────────────────────────────┐
*                           │  1  │  8  │  3  │  0  │  5  │ 
*                           └─────────────────────────────┘

* -------------------------------------  Partition  -------------------------------------

* 1. Choose a Pivot (I'd prefer to choose the first element) :
* 2. Loop and count the smaller elements (represents elements in wrong order) :

*                            L ▼ P                     ▼ R
*                           ┌─────────────────────────────┐
*                           │  1  │  8  │  3  │  0  │  5  │ 
*                           └─────────────────────────────┘
*                       checkOrder  ⤴    ⤴     ⤴    ⤴    wrongOrder = 1 (At 0)


* 3. Move the pivot by the number of the smaller elements :
* 4. Swap the left element with the pivot :

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  1  │  8  │  3  │  0  │  5  │
*                           └─────────────────────────────┘
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │ 
*                           └─────────────────────────────┘


* 5. Set counters (i = Left, ii = Right) such that:
* [i] : - Increasing counter,
*       - Will stop at the first value greater than the pivot in the range (Left, Pivot).

* [ii]: - Decreasing counter,
*       - Will stop at the first value smaller than the pivot in the range (Pivot, Right).

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │ 
*                           └─────────────────────────────┘
*                            i ▲  │     │              ▲ ii

* Now, Lets define the loops and actions that will functionalize the algorithm:

*   (A) = Check that any or both of (i, ii) in its range.

*       (B) = WHILE ([i]  in range), AND (Element <= Pivot) DO `i++;`
    
*       (C) = WHILE ([ii] in range), AND (Element >  Pivot) DO `ii--;`
    
*       (D) = IF BOTH [i] AND [ii] in range, DO { `Swap(at_i, at_ii)`, `i++;`, `ii--;` }


*   (E) = Return Pivot index as `pivot_i`



*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │     (A) Verified, DO (B)
*                           └─────────────────────────────┘
*                            i ▲  │     │              ▲ ii

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │     (B) Not Verified, DO (C)
*                           └─────────────────────────────┘
*                            i ▲  │     │              ▲ ii


*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │     (C) Verified, DO (C)
*                           └─────────────────────────────┘
*                            i ▲  │     │              ▲ ii


*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │     (C) Not Verified, DO (D)
*                           └─────────────────────────────┘
*                            i ▲  │     │       ▲ ii


*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  8  │  1  │  3  │  0  │  5  │     (D) Verified, DO AND LOOP
*                           └─────────────────────────────┘
*                            i ▲  │     │       ▲ ii


*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (A) Verified, DO (B)
*                           └─────────────────────────────┘
*                                 │i ▲  │  ▲ ii


*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (B) Not Verified, DO (C)
*                           └─────────────────────────────┘
*                                 │i ▲  │  ▲ ii

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (C) Verified, DO (C)
*                           └─────────────────────────────┘
*                                 │i ▲  │  ▲ ii

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (C) Not Verified, DO (D)
*                           └─────────────────────────────┘
*                                 │i ▲ii│

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (D) Not Verified, LOOP
*                           └─────────────────────────────┘
*                                 │i ▲ii│

*                            L ▼     ▼ P               ▼ R
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  8  │  5  │     (A) Not Verified, Return.
*                           └─────────────────────────────┘
*                                 │i ▲ii│

? Partition Returns `pivot_i = 1`.

─────────────────────────────────────────────────────────────────────────────────────────
* -------------------------------------  Sort Left  -------------------------------------

*   - `quickSort(array, Left, pivot_i - 1);`

*   - [ Left  = Left = (0)
*       Right = pivot_i - 1 = 1 - 1 = (0) ]

*                           ┌─────┐
*                           │  0  │
*                           └─────┘

*   - `if (Left >= Right) return;`                                              Base Case

─────────────────────────────────────────────────────────────────────────────────────────
* -------------------------------------  Sort Right  ------------------------------------

*   - `quickSort(array, pivot_i + 1, Right);`

*   - [ Left  = pivot_i + 1 = 1 + 1 = (2)
*   -   Right = Right = Size - 1 = 5 - 1 = (4) ]

*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │
*                                       └─────────────────┘

─────────────────────────────────────────────────────────────────────────────────────────
* - - - - - - - - - - - - - - - - - - -  Partition  - - - - - - - - - - - - - - - - - - -

*      - 1-2. Set a Pivot, Count wrongOrder

*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │
*                                       └─────────────────┘
*                                   checkOrder  ⤴    ⤴    wrongOrder = 0


*      - 3-4. Move the Pivot, Swap (No Change Becase Pivot Is In Correct Order).
*      - 5-6. Set The Counters, Loop

*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (A) Verified, DO (B)
*                                       └─────────────────┘
*                                       │i ▲  │        ▲ ii


*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (B) Not Verified, DO (C)
*                                       └─────────────────┘
*                                       │i ▲  │        ▲ ii


*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (C) Not Verified, DO (C)
*                                       └─────────────────┘
*                                       │i ▲  │        ▲ ii

*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (C) Not Verified, DO (C)
*                                       └─────────────────┘
*                                       │i ▲  │  ▲ ii


*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (C) Not Verified, DO (D)
*                                       └─────────────────┘
*                                       │i ▲ii│


*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (D) Not Verified, LOOP
*                                       └─────────────────┘
*                                       │i ▲ii│


*                                        L ▼ P         ▼ R
*                                       ┌─────────────────┐
*                                       │  3  │  8  │  5  │     (A) Not Verified, Return.
*                                       └─────────────────┘
*                                       │i ▲ii│

? Partition Returns `pivot_i = 0`.

─────────────────────────────────────────────────────────────────────────────────────────
* - - - - - - - - - - - - - - - - - - -  Sort Left  - - - - - - - - - - - - - - - - - - -

*   - `quickSort(array, Left, pivot_i - 1);`

*   - [ Left  = Left = (0)
*       Right = pivot_i - 1 = 0 - 1 = (-1) ]

*                           ┌─────┐
*                           │     │
*                           └─────┘

*   - `if (Left >= Right) return;`                                              Base Case

─────────────────────────────────────────────────────────────────────────────────────────
* - - - - - - - - - - - - - - - - - - -  Sort Right - - - - - - - - - - - - - - - - - - -

*   - `quickSort(array, pivot_i + 1, Right);`

*   - [ Left  = pivot_i + 1 = 0 + 1 = (1)
*   -   Right = Right = Size - 1 = 5 - 1 = (4) ]

*                                             ┌───────────┐
*                                             │  8  │  5  │
*                                             └───────────┘
─────────────────────────────────────────────────────────────────────────────────────────
* -   -   -   -   -   -   -   -   -   -  Partition  -   -   -   -   -   -   -   -   -   -



*      - 1-2. Set a Pivot, Count wrongOrder

*                                              L ▼ P   ▼ R
*                                             ┌───────────┐
*                                             │  8  │  5  │
*                                             └───────────┘
*                                         checkOrder  ⤴    wrongOrder = 1 (At 5)


*      - 3-4. Move the Pivot, Swap (No Change Becase Pivot Is In Correct Order).

*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  8  │  5  │
*                                             └───────────┘
*                                             ┌───────────┐
*                                             │  5  │  8  │
*                                             └───────────┘

*      - 5-6. Set The Counters, Loop

*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  8  │  5  │     (A) Verified, DO (B)
*                                             └───────────┘
*                                             │i ▲  │  ▲ ii


*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  5  │  8  │     (B) Not Verified, DO (C)
*                                             └───────────┘
*                                             │i ▲  │  ▲ ii


*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  5  │  8  │     (C) Verified, DO (C)
*                                             └───────────┘
*                                             │i ▲  │  ▲ ii


*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  5  │  8  │     (C) Not Verified, DO (D)
*                                             └───────────┘
*                                             │i ▲ii│


*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  5  │  8  │     (D) Not Verified, LOOP
*                                             └───────────┘
*                                             │i ▲ii│


*                                              L ▼   P ▼ R
*                                             ┌───────────┐
*                                             │  5  │  8  │    (A) Not Verified, Return.
*                                             └───────────┘
*                                             │i ▲ii│

? Partition Returns `pivot_i = 1`.

─────────────────────────────────────────────────────────────────────────────────────────
* -   -   -   -   -   -   -   -   -   -  Sort Left  -   -   -   -   -   -   -   -   -   -

*   - `quickSort(array, Left, pivot_i - 1);`

*   - [ Left  = Left = (0)
*       Right = pivot_i - 1 = 1 - 1 = (0) ]

*                           ┌─────┐
*                           │  5  │
*                           └─────┘

*   - `if (Left >= Right) return;`                                              Base Case

─────────────────────────────────────────────────────────────────────────────────────────
* -   -   -   -   -   -   -   -   -   -  Sort Right -   -   -   -   -   -   -   -   -   -

*   - `quickSort(array, Left, pivot_i - 1);`

*   - [ Left  = pivot_i + 1 = 1 + 1 = (2)
*       Right = Right = Size - 1 = 2 - 1 = (1) ]

*                           ┌─────┐
*                           │     │
*                           └─────┘

*   - `if (Left >= Right) return;`                                              Base Case

─────────────────────────────────────────────────────────────────────────────────────────

* After Combining the subarrays :

*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  5  │  8  │ 
*                           └─────────────────────────────┘

----------------------------------------------------------------------------------------- */

void swap(int& a, int& b) {
    int *c = new int(a);
    a = b;
    b = *c;
    delete c;
}

int partition(int array[], int Left, int Right) {
 
    int pivot_i = Left, pivot = array[pivot_i];
    int wrongOrder = 0;   // The number of smaller elements

    for (int checkOrder = Left + 1; checkOrder <= Right; checkOrder++) {
        if (array[checkOrder] <= pivot)
            wrongOrder++;
    }

    pivot_i = pivot_i + wrongOrder;
    swap(array[pivot_i], array[Left]);

    int i = Left, ii = Right;
    while (i < pivot_i || ii > pivot_i) {

        while (array[i]  <= pivot && i  < pivot_i)
            i++;

        while (array[ii] >  pivot && ii > pivot_i)
            ii--;

        if (i < pivot_i && ii > pivot_i) {
            swap(array[i], array[ii]);
            i++; ii--;
        }
    
    }

    return pivot_i;
}

void quickSort(int array[], int Left, int Right) {
 
    if (Left >= Right) return;   // Base Case
 
    int pivot_i = partition(array, Left, Right);   // Partition The Array
 
    quickSort(array, Left, pivot_i - 1);           // Sort Left
    quickSort(array, pivot_i + 1, Right);          // Sort Right
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    int Left = 0;
    int Right = size - 1;

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    quickSort(array, Left, Right);
    cout << endl << "\nArray Is Successfully Sorted By Quick Sort Algorithm.\n" << endl;

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}