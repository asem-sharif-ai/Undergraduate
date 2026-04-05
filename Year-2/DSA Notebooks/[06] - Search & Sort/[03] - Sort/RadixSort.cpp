//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │      R      a      d      i      x     │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Radix Sort is an efficient, non-comparative, linear sorting algorithm that works by
* distributing the elements by processing them digit by digit (based on their individual
* radix).

* The key idea behind Radix Sort is to exploit the concept of place value. as it assumes
* that sorting numbers digit by digit will eventually result in a fully sorted list.

* Radix Sort can be performed using different variations, such as Least Significant Digit
* (LSD) Radix Sort or Most Significant Digit (MSD) Radix Sort.

------ LSD VS MSD -----------------------------------------------------------------------

* LSD Radix Sort:
*     A. Stable and Simple to implement.
*     B. Performs well for fixed-length keys.
*     C. Performs well when the range of possible key values is limited.

* MSD Radix Sort:
*     A. More complex to implement.
*     B. Can handle variable-length keys efficiently.

* MSD Disadvantage: Stability is harder to achieve in the sorting process.

------ COMPLIXETY -----------------------------------------------------------------------

*       Time Complexity                   Space Complexity
*      ┌────────────────────────┐        ┌────────────────────────┐
*      │ All Cases │ O(d*(n+k)) │        │ All Cases │ O(d*(n+k)) │
*      └────────────────────────┘        └────────────────────────┘

* [n] : Number of keys to be sorted.
* [d] : Maximum number of digits in the keys.
* [k] : Range of possible values for each digit (e.g., 10 for decimal digits).

------ STEPS ----------------------------------------------------------------------------

* 0. Same basic steps as Count Sort.

* 1. Start with the rightmost (Least Significant) digit.                         [Pass i]
*    Sort the elements based on their digit value.

* 2. Move to the next digit to the left.                                       [Pass i+1]
*    Sort the elements based on their digit value with respect to the first sorted order.

* 3. Repeat until all digits are considered.
*    Continue this process until the most significant digit is reached.

------ MODEL ----------------------------------------------------------------------------

*            ┌───────────────────────────────────────────────────────────┐
*            │ 543 │ 187 │ 726 │ 320 │  45 │ 654 │ 881 │  92 │ 398 │ 789 │
*            └───────────────────────────────────────────────────────────┘
*                                       ▼                 ▼		          Zero-Padding
*            ┌───────────────────────────────────────────────────────────┐
*            │ 543 │ 187 │ 726 │ 320 │ 045 │ 654 │ 881 │ 092 │ 398 │ 789 │
*            └───────────────────────────────────────────────────────────┘

*             #1        ->            #2        ->            #3
*            ┌───────────┐           ┌───────────┐           ┌───────────┐
*            │ --0 │ 320 │           │ -2- │ 320 │           │ 0-- │ 045 │
*            │───────────│           │───────────│           │───────────│
*            │ --1 │ 881 │           │ -2- │ 726 │           │ 0-- │ 092 │
*            │───────────│           │───────────│           │───────────│
*            │ --2 │ 092 │           │ -4- │ 543 │           │ 1-- │ 178 │
*            │───────────│           │───────────│           │───────────│
*            │ --3 │ 543 │           │ -4- │ 045 │           │ 3-- │ 320 │
*            │───────────│           │───────────│           │───────────│
*            │ --4 │ 654 │           │ -5- │ 654 │           │ 3-- │ 398 │
*            │───────────│           │───────────│           │───────────│
*            │ --5 │ 045 │           │ -8- │ 881 │           │ 5-- │ 543 │
*            │───────────│           │───────────│           │───────────│
*            │ --6 │ 726 │           │ -8- │ 178 │           │ 6-- │ 654 │
*            │───────────│           │───────────│           │───────────│
*            │ --7 │ 187 │           │ -8- │ 789 │           │ 7-- │ 726 │
*            │───────────│           │───────────│           │───────────│
*            │ --8 │ 398 │           │ -9- │ 092 │           │ 7-- │ 789 │
*            │───────────│           │───────────│           │───────────│
*            │ --9 │ 789 │           │ -9- │ 398 │           │ 8-- │ 881 │
*            └───────────┘           └───────────┘           └───────────┘

----------------------------------------------------------------------------------------- */

int getMax(int array[], int size) {   // Returns The Maximum Value Of The Array
	int Max = array[0];
	for (int i = 1; i < size; i++)
		if (array[i] > Max)
			Max = array[i];

	return Max;
}

void countSort(int array[], int size, int digit) {

	int max = getMax(array, size);
    int *count = new int[max+1] {0}; // 882 .. TERRIBLE !
    int *final = new int[size]  {0}; // Output: Sorted Array.

	for (int i = 0; i < size; i++)
		count[(array[i] / digit) % size]++;

	for (int i = 1; i < size; i++)
		count[i] += count[i - 1];

	for (int i = size - 1; i >= 0; i--) {
		final[count[(array[i] / digit) % size] - 1] = array[i];
		count[(array[i] / digit) % size]--;
	}

	for (int i = 0; i < size; i++)
		array[i] = final[i];

    delete[] count;
    delete[] final;
}

void radixSort(int array[], int size) {
	int max = getMax(array, size);

	for (int digit = 1; max / digit > 0; digit *= 10) // Repeat The Process For Each Digit
		countSort(array, size, digit);

    cout << "\n\nArray Is Sorted Successfully By Radix Sort Algorithm.\n\n";
}

int main() {

    int array[] = {543, 187, 726, 320, 45, 654, 881, 92, 398, 789};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    radixSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}