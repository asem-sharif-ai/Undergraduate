//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │    I   n   s   e   r   t   i   o   n   │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Insertion Sort is a simple comparison-based sorting algorithm. It works by dividing the
* input array into two parts: [A. Sorted] and [B. Unsorted]. (Like Selection Sort)

* It repeatedly INSERTS each iteration key at its correct order and continues to build
* the final sorted array one element per iteration.

* It is much less efficient on large sets than other advanced algorithms.

* It starts by comparing the first elements pair, if it is not sorted (ii+1 > ii),
* then overwrites the bigger element over the smaller one (ii+1 = ii),
* then backward (ii--) to find the correct order for the key (ii < key < ii+1).

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

* 1. Save the First Unsorted Value (it may be overwritten if it isn't in the correct order).

* 2. Compare the value at the Comparison Counter [ii] with the next value [ii+1].

* 3. If value at [ii] is smaller than the one at [ii+1], it means there exists a value
* followed by a smaller value, which represents a wrong order, so:
*    3.1 Overwrite the bigger value over the smaller one (Key).
*    3.2 Backward loop and compare to find the correct order for the smaller value. 

* 4. Once the loop breaks, it means either:
*    4.1 The counter reaches an order less than 0.
*    4.2 The counter reaches an order where a value smaller than the smaller value exists.
* - In both cases, [ii+1] is the correct order for the Key (smaller value).

* 4. Insert the key at [ii+1] as it represents its correct order.

* 5. Repeat until the current iteration counter reaches the last element.


* DO    [Key = X]                               ┌─────────────────────────────┐
* IF    [Z > X] DO [X = Z] AND [ <-<- X ]       │ ... │  Z  │  X  │  Y  │ ... │
* UNTIL [(I < 0)  OR  (Pre < Key < Next)]       └─────────────────────────────┘


* Key Points:

* key : Represents the current iteration frist unsorted value.
*        - Necessary to avoid losing values while swapping.

* [i] : Represents the current iteration counter, it increases after each loop.
*       - Action: [1 -> size-1] ||| i++ after completing each iteration.

*        [ii] : Represents the current comparison backwarding counter in each loop.
*               - Action: [i-1 -> 0 OR Until Value At Key <= Value_At [ii]]
*                          ii-- after each comparison.

* - while (`ii >= 0` && ...)
*   This will break the loop in case of Key is the lowest value.

* - while (... && `array[ii] > key`)
*   This will break the loop at the Key's correct order.

* - `array[ii+1] = array[ii];`
*   This will move the larger element ONLY 1 STEP to its fit / correct order.

* - array[`ii`+1] = key;
*   Note that [ii] after the loop backwarding represents the index where the current
*   value is smaller than the key.

------ MODEL ----------------------------------------------------------------------------

* ----------------------- Iteration 0 [i = 1 | ii = 0 | Key = 8] : ----------------------

*                    ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │                                      // Start
*           └─────────────────────────────┘
*              ▲ ii

* ii >= 0 && [array[ii] > key]   //! False = Skip Loop

* Swapping ([ii+1], key) will be executed, but it does not change anything when there is
* no such update from the loop.

* ----------------------- Iteration 1 [i = 2 | ii = 1 | Key = 3] : ----------------------

*                          ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │
*           └─────────────────────────────┘
*                    ▲ ii

* ii >= 0 && array[ii] > key     //? True = Do Loop

* Iteration 1.0 :
ToDo: array[ii+1] = array[ii];
ToDo:                       ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  8  │  8  │  0  │  5  │
ToDo:        └─────────────────────────────┘
ToDo:                 ▲ ii

ToDo: ii--;
ToDo:                       ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  8  │  8  │  0  │  5  │
ToDo:        └─────────────────────────────┘
ToDo:           ▲ ii

* ii >= 0 && [array[ii] > key]   //! False = End Loop

* array[ii+1] = key;
*                           ▼ i
*            ┌─────────────────────────────┐
*            │  1  │  3  │  8  │  0  │  5  │
*            └─────────────────────────────┘
*               ▲ ii

* ----------------------- Iteration 2 [i = 3 | ii = 2 | Key = 0] : ----------------------

*                                ▼ i
*           ┌─────────────────────────────┐
*           │  1  │  3  │  8  │  0  │  5  │
*           └─────────────────────────────┘
*                          ▲ ii

* ii >= 0 && array[ii] > key     //? True = Do Loop

* Iteration 2.0 :
ToDo: array[ii+1] = array[ii];
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  3  │  8  │  8  │  5  │ 
ToDo:        └─────────────────────────────┘
ToDo:                       ▲ ii

ToDo: ii--;
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  3  │  8  │  8  │  5  │
ToDo:        └─────────────────────────────┘
ToDo:                 ▲ ii

* ii >= 0 && array[ii] > key     //? True = Continue

* Iteration 2.1 :
ToDo: array[ii+1] = array[ii];
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  3  │  3  │  8  │  5  │ 
ToDo:        └─────────────────────────────┘
ToDo:                 ▲ ii

ToDo: ii--;
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  3  │  8  │  0  │  5  │
ToDo:        └─────────────────────────────┘
ToDo:           ▲ ii

* ii >= 0 && array[ii] > key     //? True = Continue

* Iteration 2.2 :
ToDo: array[ii+1] = array[ii];
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  1  │  3  │  8  │  5  │ 
ToDo:        └─────────────────────────────┘
ToDo:           ▲ ii

ToDo: ii--;
ToDo:                             ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  1  │  1  │  3  │  8  │  5  │ 
ToDo:        └─────────────────────────────┘
ToDo:      ▲ ii

* [ii >= 0] && array[ii] > key   //! False = End Loop

* array[ii+1] = key;
*                           ▼ i
*            ┌─────────────────────────────┐
*            │  0  │  1  │  3  │  8  │  5  │
*            └─────────────────────────────┘
*          ▲ ii

* ----------------------- Iteration 3 [i = 4 | ii = 3 | Key = 5] : ----------------------

*                                      ▼ i
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  8  │  5  │
*           └─────────────────────────────┘
*                                ▲ ii

* ii >= 0 && array[ii] > key     //? True = Do Loop

* Iteration 3.0 :
ToDo: array[ii+1] = array[ii];
ToDo:                                   ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  0  │  1  │  3  │  8  │  8  │
ToDo:        └─────────────────────────────┘
ToDo:                             ▲ ii

ToDo: ii--;
ToDo:                                   ▼ i
ToDo:        ┌─────────────────────────────┐
ToDo:        │  0  │  1  │  3  │  8  │  8  │
ToDo:        └─────────────────────────────┘
ToDo:                       ▲ ii

* ii >= 0 && [array[ii] > key]   //! False = End Loop

* array[ii+1] = key;
*                                       ▼ i (Stop)
*            ┌─────────────────────────────┐
*            │  0  │  1  │  3  │  5  │  8  │                                       // End
*            └─────────────────────────────┘
*                           ▲ ii

----------------------------------------------------------------------------------------- */

void insertionSort(int array[], int size) {
	int key, i, ii;

	for (i = 1; i < size; i++) {
		key = array[i];
		ii = i-1;

		while (ii >= 0 && array[ii] > key) {
			array[ii+1] = array[ii];
			ii--;
		}

		array[ii+1] = key;
	}

    cout << "\n\nArray Is Sorted Successfully By Insertion Sort Algorithm.\n\n";
}

int main() {

    int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    insertionSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}