//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         L    i    n    e    a    r         │           S    e    a    r    c    h         │
//* ╰───────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
static constexpr auto *color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";

static void Start(string name = "Untitled Section", int before = 0, int after = 1) {
cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n'); }

static void End(char symbol = '-', int number = 50, int before = 1, int after = 0) {
cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n'); }

};

/* ----------------------------------------------------------------------------------------------------
---------- BRIEF --------------------------------------------------------------------------------------

* Linear Search (Also known as Sequential Search) is a simple straightforward searching algorithm
* that examines each element in the size range of the input data one by one until:
*      A. Discovers an element matching the search key.
*         -> Returns (Outputs) its index.
*      B. Reaches the conclusion of the search space (e.g. array or list).
*         -> Returns (Outputs) [-1] (Key Not Found).

* Linear Search NEVER fails to get a key index for any and all of the existing elements in both
* sorted and unsorted collections. However, its time complexity is a limiting factor, making it
* more advisable for use when involving smaller elements collections.

---------- STEPS --------------------------------------------------------------------------------------

* 1. Starts at the first element of the array.
* 2. Compares the current element with the search key.
*    2.1. If The current element is equal to the search key,
*         3.1. Returns its index.
*    2.2. Otherwise,
*         3.2. Progresses to the next element and repeats the search method.
* 4. If the search reaches the limit of the array size without finding any matching elements,
*    4.1. Returns [-1] as an indication of an error.

---------- PROPERTIES ---------------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │    P r o p e r t y    │                L  i  n  e  a  r     S  e  a  r  c  h                │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 01 │ - Input          │ 1. Search space (Elements collection, e.g. array or list).          │
* │    │                  │ 2. Search range (Size of the search space).                         │
* │    │                  │ 3. Search key.                                                      │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 02 │ - Output         │ A. [index] of the search key if it exists in the input data.        │
* │    │                  │ B. [-1] otherwise .                                                 │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 03 │ - Finiteness     │ The search process terminates after a finite number of steps, so it │
* │    │                  │ is a finite algorithm.                                              │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 04 │ - Definiteness   │ The search process has a well-defined and clear set of steps, so it │
* │    │                  │ is a definite algorithm.                                            │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 05 │ - Generality     │ Linear Search is highly considered as a general-purpose algorithm,  │
* │    │                  │ across various cases, and with diverse data types.                  │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 06 │ - Adaptivity     │ Linear Search follows a straightforward, uniform strategy without   │
* │    │                  │ adjusting its approach based on the input data. So it is typically  │
* │    │                  │ not an adaptive algorithm.                                          │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 07 │ - Independence   │ The current iteration does not depend on the outcomes of previous   │
* │    │                  │ iterations, so it is typically an independent algorithm.            │
* │    │                  │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │    │                  │                                                                     │
* │ 09 │ - Simplicity     │                                                                     │
* │    │                  │ Linear Search is known for its simplicity, determinism, and         │
* │ 10 │ - Determinism    │                                                                     │
* │    │                  │ completeness.                                                       │
* │ 11 │ - Completeness   │                                                                     │
* │    │                  │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------- COMPLIXETY ---------------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │  C o m p l e x i t y  │             T i m e              │            S p a c e             │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │               O(1)               │               O(1)               │
* │        B e s t        │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │                      Key Is Found At Index [0]                      │
* │                       │                                                                     │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │                       │        O(2n + 1)  =  O(n)        │               O(1)               │
* │       W o r s t       │─────────────────────────────────────────────────────────────────────│
* │                       │                                                                     │
* │                       │                   Key Is Found At Index [size-1].                   │
* │                       │                 Key Is Not Found In The Input Data.                 │
* │                       │                                                                     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------- MODEL --------------------------------------------------------------------------------------

* Key = [o] : (Best Case)
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ q │
*             └───────────────────────────────────────────────────────────────────┘
*              ⤴

    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

* Key = [e] : (Average Case)
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ q │
*             └───────────────────────────────────────────────────────────────────┘
*              ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴

    ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

* Key = [q] : (Worst Case)
*             ┌───────────────────────────────────────────────────────────────────┐
*             │ o ─ n ─ d ─ m ─ j ─ i ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ q │
*             └───────────────────────────────────────────────────────────────────┘
*              ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴  ⤴

---------- APPLICATIONS -------------------------------------------------------------------------------

* Many functions rely on the concept of linear performance, determined by their used operations
* and compartions, these functions are constructed with linear performance due to its high
* efficiency in accessing any and all of the existing elements. Such as:

* 01. sum(collection)                                 02. average(collection)
* 03. getMin(collection)                              04. getMax(collection)
* 05. doesExist(collection, key)                      06. exclusiveAppend(collection, key)
* 07. countFrequency(collection, key)                 08. removeDuplicates(collection, key)
* 09. concatenate(collection_1, collection_2)         10. replace(collection, key_1, key_2)

* Also, some search algorithms incorporate linear search as a final step in the search process.
* For example, in jump search, the objective is to bypass certain undesired blocks of elements
* once it is determined, especially in sorted cases, that the key is not within their range.

---------------------------------------------------------------------------------------------------- */

int linearSearch(int array[], int size, int key) {
    for (int index = 0; index < size; index++) {
        if (array[index] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Linear Search.\n";
            return index;
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Linear Search.\n";
    return -1;
}

int main() {

/* ------------------------------------------------------------------------------------------- */

    Section::Start("Sorted Array");

    int array_1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

    cout << "Array: ";
    for (int element : array_1)
        cout << element << " ";

    int key_1;
    cout << "\n\nEnter A Search Key: ";
    cin >> key_1;

    int index_1 = linearSearch(array_1, size_1, key_1);

    // if (index_1 != -1) {
        // Key Exists.
    // } else {
        // Key Does Not Exist.
    // }

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    Section::Start("UnSorted Array");

    int array_2[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size_2 = sizeof(array_2) / sizeof(array_2[0]);

    cout << "Array: ";
    for (int element : array_2)
        cout << element << " ";

    int key_2;
    cout << "\n\nEnter A Search Key: ";
    cin >> key_2;

    int index_2 = linearSearch(array_2, size_2, key_2);

    Section::End();

/* ------------------------------------------------------------------------------------------- */

    return 0;
}