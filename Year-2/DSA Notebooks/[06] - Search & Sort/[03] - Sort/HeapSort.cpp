//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │        H       e       a       p       │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Heap sort is a comparison-based sorting technique based on Binary Heap data structure.
* Similar to the selection sort, as it tries at first to find the minimum value to place
* at the beginning. Then repeat the same process for the remaining elements.

* Heap Sort is an in-place sorting algorithm. (Does not require additional memory space
* proportional to the input size) But it is not a stable algorithm. (The relative order
* of equal elements may not be preserved)

* Consider that:
*      A. The Last non-leaf node is at index [(size / 2) - 1].
*      B. The left  child of a node at index [i] is set at index [2i + 1].
*      C. The right child of a node at index [i] is set at index [2i + 2].

------ COMPLIXETY -----------------------------------------------------------------------

*                   ┌───────────────────────────────────────────────────────────────┐
*      ┌──────────┐ │                 C  o  m  p  l  e  x  i  t  y                  │ 
*      │ UnStable │ │───────────────────────────────────────────────────────────────│
*      └──────────┘ │            T i m e            │           S p a c e           │ 
*    ┌──────────────┘───────────────────────────────────────────────────────────────│
*    │  Best Case   │          O(n log(n))          │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │   Average    │          O(n log(n))          │             O(1)              │
*    │──────────────────────────────────────────────────────────────────────────────│
*    │    Worst     │          O(n log(n))          │             O(1)              │
*    └──────────────────────────────────────────────────────────────────────────────┘

------ STEPS ----------------------------------------------------------------------------

* 1. Building a max heap* from the given array of elements.
*    Starting from the last interval node and moving upwards.

* 2. The heap root (Max) is swapped with the last element of the array (Min).
*    The heap size is then reduced [-1], and the heap property is restored by heapifying
*        the heap root.

* Max Heap: The value of each node is greater than or equal to the values of its children.

------ MODEL ----------------------------------------------------------------------------

* ------------------------------------- Iteration 0 -------------------------------------

*                                                     ┌─────────────────────────────┐
*           ┌─────────────────────────────┐           │              1              │
*  Heapify  │  1  │  8  │  3  │  0  │  5  │           │         8         3         │
*           └─────────────────────────────┘           │      0     5                │
*                                                     └─────────────────────────────┘

*           ┌─────────────────────────────┐
*           │              1              │           ┌─────────────────────────────┐
*  maxHeap  │>        8         3         │           │  1  │  8  │  3  │  0  │  5  │
*           │>     0     5                │           └─────────────────────────────┘
*           └─────────────────────────────┘
*           ┌─────────────────────────────┐
*           │>             8              │           ┌─────────────────────────────┐
*  maxHeap  │>        1         3         │           │  8  │  1  │  3  │  0  │  5  │
*           │      0     5                │           └─────────────────────────────┘
*           └─────────────────────────────┘
*           ┌─────────────────────────────┐
*           │              8              │           ┌─────────────────────────────┐
*  maxHeap  │>        5         3         │           │  8  │  5  │  3  │  0  │  1  │
*           │>     0     1                │           └─────────────────────────────┘
*           └─────────────────────────────┘

*           ┌─────────────────────────────┐
*           │              1              │           ┌─────────────────────────────┐
*  .swap()  │         5         3         │           │  1  │  5  │  3  │  0  │  8  │
*           │      0     8                │           └─────────────────────────────┘
*           └─────────────────────────────┘
*           ┌─────────────────────────────┐
*           │              1              │           ┌───────────────────────┐── ──┐
* .remove() │         5         3         │           │  1  │  5  │  3  │  0  │  8   
*           │      0                      │           └───────────────────────┘── ──┘
*           └─────────────────────────────┘

* ------------------------------------- Iteration 1 -------------------------------------

*                                                     ┌─────────────────────────────┐
*           ┌───────────────────────┐── ──┐           │              1              │
*  Heapify  │  1  │  5  │  3  │  0  │  8              │         5         3         │
*           └───────────────────────┘── ──┘           │      0                      │
*                                                     └─────────────────────────────┘

*           ┌─────────────────────────────┐
*           │              1              │           ┌───────────────────────┐── ──┐
*  maxHeap  │>        5         3         │           │  1  │  5  │  3  │  0  │  8   
*           │>     0                      │           └───────────────────────┘── ──┘
*           └─────────────────────────────┘
*           ┌─────────────────────────────┐
*           │>             5              │           ┌───────────────────────┐── ──┐
*  maxHeap  │>        1         3         │           │  5  │  1  │  3  │  0  │  8   
*           │      0                      │           └───────────────────────┘── ──┘
*           └─────────────────────────────┘

*           ┌─────────────────────────────┐
*           │              0              │           ┌───────────────────────┐── ──┐
*  .swap()  │         1         3         │           │  0  │  1  │  3  │  5  │  8   
*           │      5                      │           └───────────────────────┘── ──┘
*           └─────────────────────────────┘
*           ┌─────────────────────────────┐
*           │              0              │           ┌─────────────────┐── ──┐── ──┐
* .remove() │         1         3         │           │  0  │  1  │  3  │  5     8   
*           │                             │           └─────────────────┘── ──┘── ──┘
*           └─────────────────────────────┘

* ------------------------------------- Iteration 2 -------------------------------------

*                                                     ┌─────────────────────────────┐
*           ┌───────────┐── ──┐── ──┐── ──┐           │              0              │
*  Heapify  │  0  │  1  │  3     5     8              │         1                   │
*           └───────────┘── ──┘── ──┘── ──┘           │                             │
*                                                     └─────────────────────────────┘

* ------------------------------------- Iteration 3 -------------------------------------

*                                                     ┌─────────────────────────────┐
*           ┌─────┐── ──┐── ──┐── ──┐── ──┐           │              0              │
*  Heapify  │  0  │  1     3     5     8              │                             │
*           └─────┘── ──┘── ──┘── ──┘── ──┘           │     //      END      \\     │
*                                                     └─────────────────────────────┘

----------------------------------------------------------------------------------------- */

void swap(int& a, int& b) {
    int *c = new int(a);
    a = b;
    b = *c;
    delete c;
}

void heapify(int array[], int size, int initialRoot) {
    int maxRoot = initialRoot;
    int Left = 2*initialRoot + 1, Right = 2*initialRoot + 2;

    if (Left  < size && array[Left]  > array[maxRoot])
        maxRoot = Left;

    if (Right < size && array[Right] > array[maxRoot])
        maxRoot = Right;

    if (maxRoot != initialRoot) {   // maxHeap
        swap(array[initialRoot], array[maxRoot]);
        heapify(array, size, maxRoot);
    }
}

void heapSort(int array[], int size) {

    for (int Roots = size / 2 - 1; Roots >= 0; Roots--) {
        heapify(array, size, Roots);    // Create Heap -> maxHeap
    }

    for (int i = size - 1; i >= 0; i--) {
        swap(array[0], array[i]);   // Swap (Min, Max)
        heapify(array, i, 0);       // Recursion (With Removing Max)
    }

    cout << "\n\nArray Is Sorted Successfully By Heap Sort Algorithm.\n\n";
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    heapSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}