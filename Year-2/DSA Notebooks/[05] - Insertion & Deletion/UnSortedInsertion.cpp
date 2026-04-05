//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms      ╭╮         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮│╰────────────────────────────────────────╮
//* │   U  n    S    o    r    t    e    d   ╰╯    I   n   s   e   r   t   i   o   n    │
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

* Unsorted insertion is a simple algorithm that inserts an element at the end of the array
* if and only if the array is static and has free size (capacity) or if it is dynamic and
* resizable.

------ STEPS ----------------------------------------------------------------------------

* For Static or Dynamic Arrays:
*     1. Checks if there is enough size (capacity) to store the element. If True, then:
*        2. Drops the element at the end of the array.
*        3. Increases the taken size (capacity) of the array by +1.

* For Dynamic Arrays (Resizing):
*     1-2. Create temporary larger array, and copy the main array elements to it.
*     3-4. Delete main array, and rename the temporary by the main name.
*     5-6. Add the key, and increase the taken size by +1.

------ COMPLIXETY -----------------------------------------------------------------------

* Time & Space Complexity : O(1)                          -> In Static or Dynamic Arrays.

* Time & Space Complexity : O(n)                          -> For Dynamic Arrays Resizing.

------ MODEL ----------------------------------------------------------------------------

* Key = [i]

* Before Insertion :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ o ─ n ─ d ─ m ─ j ─ q ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ _ │
*   └───────────────────────────────────────────────────────────────────┘

* After Insertion :                                                   ▼
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ o ─ n ─ d ─ m ─ j ─ q ─ k ─ a ─ e ─ c ─ h ─ g ─ p ─ l ─ f ─ b ─ i │
*   └───────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------- */

int insertUnSorted_S(int array[], int takenSize,  int maxSize, int key) {
    if (takenSize >= maxSize) {
        cout << "Array Is Full, Insertion Failed." << endl;
        return takenSize;
    } else {
        array[takenSize] = key; // Mentions the frist unfilled index.
        takenSize++;
        cout << "The Key [" << key << "] Is Inserted Successfully." << endl;
    }

    return takenSize;
}

int insertUnSorted_D(int*& array, int& takenSize, int& maxSize, int key, int freeSize=10) {
    if (takenSize >= maxSize) {

        // Create temporary, Copy main, Delete main, Rename temporary, Add key, Increase size.
        int temp_maxSize = maxSize + freeSize;
        int* temp_array = new int[temp_maxSize];

        for (int i = 0; i < takenSize; i++)
            temp_array[i] = array[i];
        
        delete[] array;

        array = temp_array;
        maxSize = temp_maxSize;

        temp_array[takenSize] = key;
        takenSize++;
        
        cout << "Array Was Resized, And The Key [" << key << "] Is Inserted Successfully." << endl;

    } else {
        array[takenSize] = key;
        takenSize++;
        cout << "The Key [" << key << "] Is Inserted Successfully. Without Resizing The Array." << endl;

    }

    return takenSize;
}

/*  -------------------------------------------------------------------------------------------------------------  */

int main() {

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 1: Static-Full Array");

    const int maxSize_S0 = 10;
    int array_S0[maxSize_S0] = {2, 4, 3, 1, 0, 9, 7, 6, 8, 0};
    int takenSize_S0 = 10;

    cout << "Static-Full Array, Size = " << maxSize_S0 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_S0; i++)
        cout << array_S0[i] << " ";

    int key_S0;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_S0;

    takenSize_S0 = insertUnSorted_S(array_S0, takenSize_S0, maxSize_S0, key_S0);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_S0; i++)
        cout << array_S0[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_S0;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 2: Static-Free Array");

    const int maxSize_S1 = 15;
    int array_S1[maxSize_S1] = {2, 4, 3, 1, 0, 9, 7, 6, 8, 0};
    int takenSize_S1 = 10;

    cout << "Static-Free Array, Size = " << maxSize_S1 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_S1; i++)
        cout << array_S1[i] << " ";

    int key_s1;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_s1;

    takenSize_S1 = insertUnSorted_S(array_S1, takenSize_S1, maxSize_S1, key_s1);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_S1; i++)
        cout << array_S1[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_S1;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 3: Dynamic-Full Array");

    int maxSize_D0 = 10;
    int* array_D0 = new int[maxSize_D0] {2, 4, 3, 1, 0, 9, 7, 6, 8, 0};
    int takenSize_D0 = 10;

    cout << "Dynamic-Full Array, Size = " << maxSize_D0 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_D0; i++)
        cout << array_D0[i] << " ";

    int key_D0;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_D0;

    takenSize_D0 = insertUnSorted_D(array_D0, takenSize_D0, maxSize_D0, key_D0);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_D0; i++)
        cout << array_D0[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_D0;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 4: Dynamic-Free Array");

    int maxSize_D1 = 15;
    int* array_D1 = new int[maxSize_D1] {2, 4, 3, 1, 0, 9, 7, 6, 8, 0};
    int takenSize_D1 = 10;

    cout << "Dynamic-Free Array, Size = " << maxSize_D1 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_D1; i++)
        cout << array_D1[i] << " ";

    int key_D1;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_D1;

    takenSize_D1 = insertUnSorted_D(array_D1, takenSize_D1, maxSize_D1, key_D1);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_D1; i++)
        cout << array_D1[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_D1;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    return 0;
}