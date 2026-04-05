//* ╭───────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures & Algorithms      ╭╮         Author: Asem Al-Sharif         │
//* ╰────────────────────────────────────────╮│╰────────────────────────────────────────╮
//* │        S    o    r    t    e    d      ╰╯    I   n   s   e   r   t   i   o   n    │
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

* Sorted Instertion is a clever insertion algorithm that is designed to insert an element
* in a sorted array while maintaining the sort order.

------ STEPS ----------------------------------------------------------------------------

* 1. Checks if the array has enough size (capacity) to store the key. If True, then:
*    2. Selects all elements such as [e > Key] and shift them to the right by 1 step.
*    3. Inserts the key at its respecting-sort order.
*    4. Increases the taken size by +1.

* Note that the shifting starts from the last element index and moves backward. Otherwise,
* use a temporary variable to avoid data loss

------ COMPLIXETY -----------------------------------------------------------------------

* Time Complexity : 
*      Best Case  :           O(n)               -> Key > All_Elements (Only Compartions)
*      Average & Worst Case : O(n^2)                            -> Compartions & Shifting

* Time Complexity gets worse when resizing is required for dynamic arrays.

* Space Complexity : O(1)

------ MODEL ----------------------------------------------------------------------------

* Key = [i]
* Position = [ h < i > j ]

* Before Insertion :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q ─ _ │
*   └───────────────────────────────────────────────────────────────────┘

* Goal State :                        ▼
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ p ─ q ─ _ │
*   └───────────────────────────────────────────────────────────────────┘
*                                       ⤻  ⤻  ⤻  ⤻  ⤻  ⤻  ⤻  ⤻  ⤻

------------------------------------------------------

* Satrted By Shifting The Last Element To The Right (Requires Free Capacity) :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ p ─ q ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                                                   ⤻

* Continue Shifting To The Right, Backwarding :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ p ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                                               ⤻

* Continue Shifting All Elements Greater Than The Key :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ o ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                                           ⤻

*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ n ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                                       ⤻

*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ m ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                                   ⤻

*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ l ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                               ⤻

* Pre-Last Shift :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ k ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                           ⤻

* Last Shift :
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h | j ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘
*                                       ⤻

* After Insertion :                   ▼
*   ┌───────────────────────────────────────────────────────────────────┐
*   │ a ─ b ─ c ─ d ─ e ─ f ─ g ─ h ─ i ─ j ─ k ─ l ─ m ─ n ─ o ─ p ─ q │
*   └───────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------- */

int insertSorted_S(int array[], int takenSize,  int maxSize, int key) {
    if (takenSize >= maxSize) {
        cout << "Array Is Full, Insertion Failed." << endl;
        return takenSize;
    } else {
    int i = takenSize - 1;                    // Start By The Last Element
    while (i >= 0 && array[i] > key) {       // Select The Elements > Key
        array[i + 1] = array[i];            // Shift The Elements
        i--;                               // Backward
    }
        array[i + 1] = key;              // Insert The Key
        takenSize++;                    // Increase The Taked Size
        cout << "The Key [" << key << "] Is Inserted Successfully At Index [" << i + 1 << "]." << endl;
    }

    return takenSize;
}

int insertSorted_D(int*& array, int& takenSize, int& maxSize, int key, int freeSize=10) {
    if (takenSize >= maxSize) {
        int temp_maxSize = maxSize + freeSize;
        int* temp_array = new int[temp_maxSize];

        for (int i = 0; i < takenSize; i++)
            temp_array[i] = array[i];
        
        delete[] array;

        array = temp_array;
        maxSize = temp_maxSize;

        int i = takenSize - 1;
        while (i >= 0 && array[i] > key) {
            array[i + 1] = array[i];
            i--;
        }
        
        array[i + 1] = key;
        takenSize++;
        cout << "Array Was Resized, And The Key [" << key << "] Is Inserted Successfully At Index [" << i + 1 << "]." << endl;
    }
    else {
        int i = takenSize - 1;
        while (i >= 0 && array[i] > key) {
            array[i + 1] = array[i];
            i--;
        }

        array[i + 1] = key;
        takenSize++;
        
        cout << "The Key [" << key << "] Is Inserted Successfully At Index [" << i + 1 << "]. Without Resizing The Array." << endl;
    }

    return takenSize;
}

/*  -------------------------------------------------------------------------------------------------------------  */

int main() {

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 1: Static-Full Array");

    const int maxSize_S0 = 10;
    int array_S0[maxSize_S0] = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int takenSize_S0 = 10;

    cout << "Static-Full Array, Size = " << maxSize_S0 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_S0; i++)
        cout << array_S0[i] << " ";

    int key_S0;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_S0;

    takenSize_S0 = insertSorted_S(array_S0, takenSize_S0, maxSize_S0, key_S0);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_S0; i++)
        cout << array_S0[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_S0;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 2: Static-Free Array");

    const int maxSize_S1 = 15;
    int array_S1[maxSize_S1] = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int takenSize_S1 = 10;

    cout << "Static-Free Array, Size = " << maxSize_S1 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_S1; i++)
        cout << array_S1[i] << " ";

    int key_s1;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_s1;

    takenSize_S1 = insertSorted_S(array_S1, takenSize_S1, maxSize_S1, key_s1);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_S1; i++)
        cout << array_S1[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_S1;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 3: Dynamic-Full Array");

    int maxSize_D0 = 10;
    int* array_D0 = new int[maxSize_D0] {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int takenSize_D0 = 10;

    cout << "Dynamic-Full Array, Size = " << maxSize_D0 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_D0; i++)
        cout << array_D0[i] << " ";

    int key_D0;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_D0;

    takenSize_D0 = insertSorted_D(array_D0, takenSize_D0, maxSize_D0, key_D0);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_D0; i++)
        cout << array_D0[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_D0;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    Section::Start("Case 4: Dynamic-Free Array");

    int maxSize_D1 = 15;
    int* array_D1 = new int[maxSize_D1] {2, 4, 6, 8, 10, 12, 14, 16, 18, 20};
    int takenSize_D1 = 10;

    cout << "Dynamic-Free Array, Size = " << maxSize_D1 << "\nBefore Insertion: ";
    for (int i = 0; i < takenSize_D1; i++)
        cout << array_D1[i] << " ";

    int key_D1;
    cout << "\n\nEnter An Insertion Key: ";
    cin >> key_D1;

    takenSize_D1 = insertSorted_D(array_D1, takenSize_D1, maxSize_D1, key_D1);

    cout << "\nAfter Insertion: ";
    for (int i = 0; i < takenSize_D1; i++)
        cout << array_D1[i] << " ";

    cout << "\nSize After Insertion = " << maxSize_D1;

    Section::End(75);

/* -------------------------------------------------------------------------------------- */

    return 0;
}