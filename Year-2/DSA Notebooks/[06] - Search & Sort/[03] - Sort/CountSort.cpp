//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms       │         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮ ╰────────────────────────────────────────╮
//* │      C      o      u      n      t     │         S       o       r       t        │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Count Sort is an efficient, non-comparative, linear sorting sorting algorithm that sorts
* elements based on their keys' integer values. 

* This algorithm works by counting the occurrences of each unique key in the input array,
* then uses this count information to determine the position of each element in the final
* sorted output.

* Count Sort is a stable sort, so that the relative order of equal elements is preserved.

* Disadvantage: Becomes less practical when the key values have a large range compared to
*               the number of elements (size = Max+1).

------ COMPLIXETY -----------------------------------------------------------------------

*       Time Complexity                   Space Complexity
*      ┌────────────────────────┐        ┌────────────────────────┐
*      │ All Cases │   O(n+k)   │        │ All Cases │    O(k)    │
*      └────────────────────────┘        └────────────────────────┘

* [n] : Number of keys to be sorted.
* [k] : Range of possible keys values.

------ STEPS ----------------------------------------------------------------------------

* 1. Find the maximum key value, and create an count array of size [Max+1] with initial
*    values of zero.

* 2. Traverse and increase each key count in the count array.

* 3. Modify the count array to represent the cumulative count.

* 4. Create the final sorted array by placing elements in their correct positions based on
*    the count array.

------ MODEL ----------------------------------------------------------------------------

* Array:
*           ┌─────────────────────────────┐
*           │  1  │  8  │  3  │  0  │  5  │
*           └─────────────────────────────┘

-----------------------------------------------------------------------------------------

*   - 1. getMax Max = 8;

*   - 2. Create Count[8+1]:
*           ┌─────────────────────────────────────────────────────┐
*           │  0  │  0  │  0  │  0  │  0  │  0  │  0  │  0  │  0  │  ▶  Count
*           └─────────────────────────────────────────────────────┘
*      [i] =   0     1     2     3     4     5     6     7     8

-----------------------------------------------------------------------------------------

*   - 3. Calulate the count of each key:
*           ┌─────────────────────────────────────────────────────┐
*           │  1  │  1  │  0  │  1  │  0  │  1  │  0  │  0  │  1  │
*           └─────────────────────────────────────────────────────┘
*      [i] =   0     1     2     3     4     5     6     7     8


*   - 4. Calulate the cumulative count:
*           ┌─────────────────────────────────────────────────────┐
*           │  1  │  2  │  2  │  3  │  3  │  4  │  4  │  4  │  5  │
*           └─────────────────────────────────────────────────────┘
*      [i] =   0     1     2     3     4     5     6     7     8

-----------------------------------------------------------------------------------------

*   - 4. Create final array:

*                                                         ┌─────────────────────────────┐
* [▼ Count]                                               │  1  │  8  │  3  │  0  │  5  │
* ┌─────────────────────────────────────────────────────┐ └─────────────────────────────┘   
* │  1  │  2  │  2  │  3  │  3  │  4  │  4  │  4  │  5  │ [▲ Array]             [Final ▼]
* └─────────────────────────────────────────────────────┘ ┌─────────────────────────────┐   
*                                                         │  0  │  0  │  0  │  0  │  0  │
*                                                         └─────────────────────────────┘

for (int i = size - 1; i >= 0; i--) {         |  index.final = value.count[value.array] - 1
    final[count[array[i]] - 1] = array[i];    |  value.index.final = value.last.array
    count[array[i]]--;                        |  last--
}                                             |

* 1.  [i = size-1 = 4]  ->  [array[4] = 5]  ->  [count[5]-1 = 4-1 = 3]  ->  [final[3] = 5]
* 2.  [i = size-2 = 3]  ->  [array[3] = 0]  ->  [count[0]-1 = 1-1 = 0]  ->  [final[0] = 0]
* 3.  [i = size-3 = 2]  ->  [array[2] = 3]  ->  [count[3]-1 = 3-1 = 2]  ->  [final[2] = 3]
* 4.  [i = size-4 = 1]  ->  [array[1] = 8]  ->  [count[8]-1 = 5-1 = 4]  ->  [final[4] = 8]
* 5.  [i = size-5 = 0]  ->  [array[0] = 1]  ->  [count[1]-1 = 2-1 = 1]  ->  [final[1] = 1]

* Final:
*           ┌─────────────────────────────┐
*           │  0  │  1  │  3  │  5  │  8  │                                    Thank You!
*           └─────────────────────────────┘

----------------------------------------------------------------------------------------- */

int getMax(int array[], int size) {   // Returns The Maximum Value Of The Array
    int Max = array[0];
    for (int i = 1; i < size; i++)
        if (array[i] > Max)
            Max = array[i];

    return Max;
}

void countSort(int array[], int size) {

    int Max = getMax(array, size);
    int* count = new int[Max + 1] {0};
    int* final = new int[size] {0};

    for (int i = 0; i < size; i++)
        count[array[i]]++;

    for (int i = 1; i <= Max; i++)
        count[i] += count[i - 1];

    for (int i = size - 1; i >= 0; i--) {
        final[count[array[i]] - 1] = array[i];
        count[array[i]]--;
    }

    for (int i = 0; i < size; i++)
        array[i] = final[i];
    
    cout << "\n\nArray Is Sorted Successfully By Count Sort Algorithm.\n\n";

    delete[] count;
    delete[] final;
}


int main() {

    int array[] = {543, 187, 726, 320, 45, 654, 881, 92, 398, 789};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array Before Sorting : ";
    for (int element : array) 
        cout << element << " ";

    countSort(array, size);

    cout << "Array After Sorting : ";
    for (int element : array) 
        cout << element << " ";

    return 0;
}