//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms      ╭╮         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮│╰────────────────────────────────────────╮
//* │        D        e        l        e    ╰╯   t        i        o        n          │
//* ╰───────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, ignore.
public:
    static void Start(string name = "Untiteled Section", int before = 0, int after = 1) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[4;91m" << name << ":\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
    static void End(int number = 50, int before = 1, int after = 0) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[91m" << string(number, '-') << "\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
};

/* --------------------------------------------------------------------------------------

------ BRIEF ----------------------------------------------------------------------------

* Deletion is a simple pop operation that removes a key from the array by shifting each
* following element one position back in index order, overwriting the unwanted element.
* After that, the array's logical size is reduced by 1 to eliminate the last duplicated
* element.

* Deleting an element from an array process essentially consists of two main stages:
*   1. Finding the element by checking either linear or binary search.
*   2. Removing it by overwriting (shifting) every and each element to the left.

* The previous guide is based on sorted array cases. However, in unsorted arrays, the
* process is simpler and more efficient. It is preferable to overwrite the unwanted
* element with the last element, avoiding linear time complexity and making the
* implementation simpler."

------ PRO TIP --------------------------------------------------------------------------

* The "physical size" of a static array refers to the fixed number of memory slots
* reserved for the array. This size doesn't change during the program's execution.

* The "logical state" refers to how the program views or interprets the array,
* which can be altered by marking elements as deleted.

* Logical deletion doesn't change the physical size of the array. The array size
* remains constant, only the logical state of the array is altered to indicate the
* absence of the last element.

* In summary, delete an element from a static array means to change how the program
* interprets that array (logical state), but not altering the actual memory reserved
* for the array (constant physical size).

------ STEPS ----------------------------------------------------------------------------

* 1. Checks whether the given key is in the array, if so then returns its index.
* 2. Shifts the elements (by -1 index) starting from the one right next to the key.
* 3. Reduces the taken size (capacity) of the array by -1.

------ COMPLIXETY -----------------------------------------------------------------------

* Time Complexity :
*   1. Get Index :
*      A. Linear Search :  O(1)  |  O(n)
*      B. Binary Search :  O(1)  |  O(log n)

*   2. Shift Elements   :  O(1)  |  O(n)

* Space Complexity : O(1)

* Overall Complexity : O(n)

------ MODEL ----------------------------------------------------------------------------

* Before Deletion :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*    Best Case    : delete(q)  ->  Index = [size-1]  ->  shift(none)
*    Average Case : delete(i)  ->  Index = [n]       ->  shift(some)
*    Worst Case   : delete(a)  ->  Index = [0]       ->  shift(all)

* Goal State :                        ▼ ⤺  ⤺  ⤺  ⤺  ⤺  ⤺  ⤺  ⤺  ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* Actual State :                      ▼
*   ┌───────────────────────────────────────────────────────────────┐─ ─┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │ q   ◄ Constant Physical Size
*   └───────────────────────────────────────────────────────────────┘─ ─┘
*                                                                 ▲ Updated Logical State

------------------------------------------------------

* Get Index By Search :               ▼
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* Satrted By Shifting The Last Element To The Left (Overwriting On The Key) :
*                                      ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* Continue Shifting To The Left, Forwarding :
*                                           ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* Continue Shifting All Elements Greater Than Key :
*                                               ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

*                                                   ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

*                                                       ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

*                                                           ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

*                                                               ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ p ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* Last Shift :
*                                                                   ⤺
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ p ─ q ─ q │
*   └───────────────────────────────────────────────────────────────────┘

* After Deletion :                    ▼
*   ┌───────────────────────────────────────────────────────────────┐─ ─┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │ q  
*   └───────────────────────────────────────────────────────────────┘─ ─┘
*                                                                 ▲ return size--;

----------------------------------------------------------------------------------------- */

int getIndex(int array[], int size, int key, int search) {
    if (search != 0) {   // Linear Search
        for (int index = 0; index < size; index++) {
            if (array[index] == key) {
                cout << endl << "Key Is Found At Index [" << index << "] By Linear Search." << endl;
                return index;
            }
        }
        cout << endl << "Key Is Not Found By Linear Search." << endl;
        return -1;

    } else {   // Binary Search
        int Low = 0, High = size - 1;

        while (Low <= High) {
            int Mid = (High + Low) / 2;

            if (array[Mid] > key) {
                High = Mid - 1;
            } else if (array[Mid] < key) {
                Low = Mid + 1;
            } else {
                int index = Mid; 
                cout << endl << "Key Is Found At Index [" << index << "] By Binary Search." << endl;
                return index;
            }
        }
        cout << endl << "Key Is Not Found By Binary Search." << endl;
        return -1;
    }
}

int deleteKey(int array[], int size, int key, int search=1, int method=1) {
    int index = getIndex(array, size, key, search);

    if (index != -1) {   // Key Exists

        if (method != 0) array[index] = array[size - 1];   // Swap

        else {   // Shift
            for (int i = index ; i < size - 1 ; i++)
                array[i] = array[i + 1];
        }
        
        cout << "Key Is Deleted Successfully." << endl;
        return --size;

    } else {   // Key Does Not Exist
        cout << "Key Is Not In The Array." << endl;
        return size;
    }
}

/*  -------------------------------------------------------------------------------------------------------------  */

/*
Parameters:
    -    1. Array
    -    2. Size
    -    3. Search Mode     [0 Binary, Else Linear (Default)]
    -    4. Deletion Method [0 Shift,  Else Swap   (Default)]
*/

int main() {

/* -------------------------------------------------------------------------------------- */

    Section::Start("Sorted Array");

    int array_1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

    cout << "Array Before Deletion: ";
    for (int i = 0; i < size_1; i++)
        cout << array_1[i] << " ";

    cout << "\nSize: " << size_1 << endl;    

    int key_1, search_1, method_1;

    cout << "\nEnter a Deletion Key: ";
    cin >> key_1;

    cout << "\nType [0] For Binary Search Algorithm, Else For Linear: ";
    cin >> search_1;
	
    cout << "\nType [0] For Shifting, Else For Swapping: ";
    cin >> method_1;

	size_1 = deleteKey(array_1, size_1, key_1, search_1, method_1);

    cout << "\nArray After Deletion: ";
    for (int i = 0; i < size_1; i++)
        cout << array_1[i] << " ";

    cout << "\nSize: " << size_1;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("UnSorted Array");

    int array_2[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};
    int size_2 = sizeof(array_2) / sizeof(array_2[0]);

    cout << "Array Before Deletion: ";
    for (int i = 0; i < size_2; i++)
        cout << array_2[i] << " ";

    cout << "\nSize: " << size_2 << endl;    

    int key_2, search_2, method_2;

    cout << "\nEnter a Deletion Key: ";
    cin >> key_2;

    cout << "\nType [0] For Binary Search Algorithm, Else For Linear: ";
    cin >> search_2;
	
    cout << "\nType [0] For Shifting, Else For Swapping: ";
    cin >> method_2;

	size_2 = deleteKey(array_2, size_2, key_2, search_2, method_2);

    cout << "\nArray After Deletion: ";
    for (int i = 0; i < size_2; i++)
        cout << array_2[i] << " ";

    cout << "\nSize: " << size_2;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

	return 0;
}