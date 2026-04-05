//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │        M     e     r     g     e       │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Merge Sort is an efficient sorting algorithm that follows the divide-and-conquer strategy.

* The main idea behind merge sort is to divide the unsorted list into sublists, such that
* sublist each containing ony one element, and then repeatedly merging them back together
* in sorted order to produce new sorted sublists until there is only one list remaining.

* Key Points:

* - Divide:  Divide the unsorted list into sublists, each containing one element.
*            This is the base case for the recursion.

* - Conquer: Recursively merge adjacent sublists to produce new sorted sublists until
*               there is only one sublist remaining.
*            This is done by comparing elements from the two sublists and merging them
*               in sorted order.

* - The Divide-and-Conquer approach can be viewed as three steps:
*   - 1. Divide:  Dividing the problem into sub-problems.
*   - 2. Conquer: 1. Solving the sub-problems
*                 2. Combining the solutions to determine solution for the main problem.

------ COMPLIXETY -----------------------------------------------------------------------

*                   ┌───────────────────────────────────────────────────────────────┐
*      ┌──────────┐ │                 C  o  m  p  l  e  x  i  t  y                  │ 
*      │  Stable  │ │───────────────────────────────────────────────────────────────│
*      └──────────┘ │            T i m e            │           S p a c e           │ 
*    ┌──────────────┘───────────────────────────────────────────────────────────────│
*    │  Best Case   │          O(n log(n))          │             O(n)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │   Average    │          O(n log(n))          │             O(n)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │    Worst     │          O(n log(n))          │             O(n)              │
*    └──────────────────────────────────────────────────────────────────────────────┘

------ STEPS ----------------------------------------------------------------------------

* 1. Divide the unsorted list into two halves,
*    2. Recursively apply the algorithm on each of the two generated halves.

* 3. Merge the two sorted sublists created in the conquer step to produce a sorted list:
*    4. Start with an empty result array.
*    5. Compare the first elements of the two sublists, and append the smaller element to
*       the result array, and move to the next element.
*    6. Repeat the comparison and selection process until one of the sublists is exhausted.
*    7. Append the remaining elements of the non-empty sublist
*    8. Repeat recursively for each pair of sublists until there is only one sorted list.

------ MODEL ----------------------------------------------------------------------------

*                           ┌─────────────────────────────┐
*                           │  1  │  8  │  3  │  0  │  5  │ 
*                           └─────────────────────────────┘

* 1. Dividing the array until each sub-array contains only one element :

*               ┌─────────────────┐                   ┌───────────┐
*               │  1  │  8  │  3  │                   │  0  │  5  │ 
*               └─────────────────┘                   └───────────┘
*             ┌───────────┐   ┌─────┐               ┌─────┐   ┌─────┐
*             │  1  │  8  │   │  3  │               │  0  │   │  5  │ 
*             └───────────┘   └─────┘               └─────┘   └─────┘
*           ┌─────┐ ┌─────┐   ┌─────┐               ┌─────┐   ┌─────┐
*           │  1  │ │  8  │   │  3  │               │  0  │   │  8  │
*           └─────┘ └─────┘   └─────┘               └─────┘   └─────┘

─────────────────────────────────────────────────────────────────────────────────────────

* 2. Merging adjacent pairs in a sorted manner :

* ------------------------------------  Iteration 0  ------------------------------------

* - Input :
*           ┌─────┐ ┌─────┐
*           │  1  │ │  8  │
*           └─────┘ └─────┘

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Action :
*             ┌───────────┐
*             │  A  │  B  │ 
*             └───────────┘

*              - A = min(1, 8) 
*              - B = Remaining_Element

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Output :
*             ┌───────────┐
*             │  1  │  8  │ 
*             └───────────┘

─────────────────────────────────────────────────────────────────────────────────────────

* ------------------------------------  Iteration 1  ------------------------------------

* - Input :
*             ┌───────────┐   ┌─────┐               ┌─────┐   ┌─────┐
*             │  1  │  8  │   │  3  │               │  0  │   │  5  │ 
*             └───────────┘   └─────┘               └─────┘   └─────┘

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Action :
*               ┌─────────────────┐                   ┌───────────┐
*               │  A  │  B  │  C  │                   │  D  │  E  │ 
*               └─────────────────┘                   └───────────┘

*              - A = min(1, 3)                       - D = min(0, 5)
*              - B = min(max(1, 3), 8)               - E = Remaining_Element
*              - C = Remaining_Element

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Output :
*               ┌─────────────────┐                   ┌───────────┐
*               │  1  │  3  │  8  │                   │  0  │  5  │
*               └─────────────────┘                   └───────────┘

─────────────────────────────────────────────────────────────────────────────────────────

* ------------------------------------  Iteration 2  ------------------------------------

* - Input :
*               ┌─────────────────┐                   ┌───────────┐
*               │  1  │  3  │  8  │                   │  0  │  5  │ 
*               └─────────────────┘                   └───────────┘

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Action :
*                           ┌─────────────────────────────┐
*                           │  A  │  B  │  C  │  D  │  E  │ 
*                           └─────────────────────────────┘

*              - A = min(1, 0)
*              - B = min(max(1, 0), 5)
*              - C = min(3, max(max(1, 0), 5))
*              - D = min(8, max(3, max(max(1, 0), 5)))
*              - E = Remaining_Element

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

* - Output :
*                           ┌─────────────────────────────┐
*                           │  0  │  1  │  3  │  5  │  8  │ 
*                           └─────────────────────────────┘

─────────────────────────────────────────────────────────────────────────────────────────
----------------------------------------------------------------------------------------- */

void merge(int array[], int Left, int Mid, int Right) {

    int i, ii, iii;     // Counters
    int size_L = Mid - Left + 1;
    int size_R = Right - Mid;
    int* array_L = new int[size_L];
    int* array_R = new int[size_R];

    for (i = 0 ; i < size_L ; i++)
        array_L[i] = array[Left + i];
    for (ii = 0 ; ii < size_R ; ii++)
        array_R[ii] = array[Mid + ii + 1];

    i = ii = 0;
    iii = Left;

    while (i < size_L  &&  ii < size_R) {
        if (array_L[i] <= array_R[ii]) {
            array[iii] = array_L[i];
            i++;
        } else {
            array[iii] = array_R[ii];
            ii++;
        }
        iii++;

    } while (i < size_L) {
        array[iii] = array_L[i];
        i++;
        iii++;
    } while (ii < size_R) {
        array[iii] = array_R[ii];
        ii++;
        iii++;
    }

    delete[] array_L;
    delete[] array_R;
}

void mergeSort(int array[], int Left, int Right) {
    if (Left < Right) {
        int Mid = (Left + Right) / 2;

        mergeSort(array, Left, Mid);
        mergeSort(array, Mid+1, Right);

        merge(array, Left, Mid, Right);
    }
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    int Left = 0;
    int Right = size - 1; 

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    mergeSort(array, Left, Right);
    cout << "\n\nArray Is Sorted Successfully By Merge Sort Algorithm.\n\n";

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}