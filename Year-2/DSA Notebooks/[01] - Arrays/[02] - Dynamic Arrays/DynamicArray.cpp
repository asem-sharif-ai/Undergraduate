//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures And Algorithms          │              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮ ╰───────────────────────────────────────────────╮
//* │              D  y  n  a  m  i  c              │               A   r   r   a   y   s             │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, ignore.
public:
    static void Start(string name = "Untiteled Section", int before = 0, int after = 1) {
        for (int i = 0; i <= before; i++)
            cout << endl;

        cout << "\033[4;91m" << name << ":\033[0m";

        for (int i = 0; i <= after; i++)
            cout << endl;
    }

    static void End(int number = 50, int before = 1, int after = 0) {
        for (int i = 0; i <= before; i++)
            cout << endl;

        cout << "\033[91m" << string(number, '-') << "\033[0m";
        
        for (int i = 0; i <= after; i++)
            cout << endl;
    }
};

/*  ---------------------------------------------------------------------------------------------------------------

* - Stack Memory:
*   The stack is a region of a computer's memory space that operates on a "Last-In, First-Out" (LIFO) basis.
*   It is used to store local variables and function call information.

* - Heap Memory:
*   The heap is a region of a computer's memory space where dynamic memory allocation and deallocation occurs.
*   It is separate from the stack.

* - Dynamic Memory:
*   Dynamic memory refers to memory that is allocated at runtime and can be resized or freed as needed.
*   It allows for flexibility in managing memory during program execution, but requires careful management
*      to avoid memory leaks or other issues.

* - Dynamic Arrays:
*   Dynamic arrays (Also known as resizable arrays), are arrays whose size does not require to be const and can
*      be changed during runtime.
*   Unlike static arrays, whose size is fixed at compile time, dynamic arrays are created on the heap,
*      and their size can be adjusted using dynamic memory allocation functions.

* - new-Operator:
*   The new operator in is used for dynamic memory allocation, allowing to allocate memory on the heap during
*      program execution. 
*   It returns a pointer to the allocated memory, and it is often paired with the delete operator to deallocate
*      the memory when it is no longer needed, preventing memory leaks.

---------------------------------------------------------------------------------------------------------------  */

int main() {
    
/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("new-Operator");

    int* dynamicInteger = new int;    // new int(100)
    *dynamicInteger = 100;

        //*  1. Allocates memory.
        //*  2. Constructs an object in allocated memory.

        //*  Or Use `unique_ptr<int> dynamicInteger = make_unique<int>(100);` for smart dynamic allocation, as it
        //*  automatically deallocate the dynamic variable once it goes out of scope.

    cout << "Dynamically Allocated Integer: " << *dynamicInteger << endl;

    delete dynamicInteger;            // Avoid memory leaks

    Section::End(75, 0);

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Dynamic Array");

    // //? data_type* array_name = new data_type[array_size] {array_elements};

    int dynamicSize = 5;
    int* dynamicArray = new int[dynamicSize];

    for (int i = 0; i < 5; i++)
        dynamicArray[i] = i * 10;

    cout << "Dynamically Allocated Array: ";
    for (int i = 0; i < 5; i++)
        cout << dynamicArray[i] << " ";

    delete[] dynamicArray;

    Section::End(75);

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Dynamic Size");

    int userSize;
    cout << "Enter Any Size : ";
    cin >> userSize;

    int* userArray = new int[userSize];      // Return Error in Static Array Case.

    for (int i = 0; i < userSize; i++) {
        dynamicArray[i] = i * 5;
        cout << dynamicArray[i] << " " ;
    }

    delete[] userArray;

    Section::End(75);

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Applications - Sign-Filtered Array");

    int unfiltered[] = {0, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 0, 6, 7, 8, 9, 10};
    int un_size = sizeof(unfiltered) / sizeof(unfiltered[0]);

    int Pve_Count = 0, Nve_Count = 0, zero_Count = 0;

    for (int i = 0; i < un_size; i++) {
        if (unfiltered[i] > 0) {
            Pve_Count += 1;
        } else if (unfiltered[i] < 0) {
            Nve_Count += 1;
        } else {
            zero_Count += 1;
        }
    }

    int *Pve_Array = new int[Pve_Count], *Nve_Array = new int[Nve_Count], *zero_Array = new int[zero_Count];

    int Pve_Index = 0, Nve_Index = 0, zero_Index = 0;

    for (int i = 0 ; i < un_size ; i++) {
        if      (unfiltered[i] > 0)  Pve_Array[Pve_Index++] = unfiltered[i];
        else if (unfiltered[i] < 0)  Nve_Array[Nve_Index++] = unfiltered[i];
        else                         zero_Array[zero_Index++] = i; // Return Zeros Index
    }

    cout << "Unfiltered Array : ";
    for (int i = 0; i < un_size; i++)
        cout << unfiltered[i] << " " ;
    cout << endl;
    
    cout << "\n+ve Array : ";
    for (int i = 0; i < Pve_Count; i++)
        cout << Pve_Array[i] << " " ;
    cout << endl;
    
    cout << "\n-ve Array : ";
    for (int i = 0; i < Nve_Count; i++)
        cout << Nve_Array[i] << " " ;
    cout << endl;

    cout << "\nZeros Index : ";
    for (int i = 0; i < zero_Count; i++)
        cout << zero_Array[i] << " " ;

    delete[] Pve_Array;
    delete[] Nve_Array;
    delete[] zero_Array;

    Section::End(75);

/*  -------------------------------------------------------------------------------------------------------------  */

/*
* Assume you have a full array of size n, expanding it means to copy each element to a new dynamic array of size m
* such as (m > n).

* Dynamic Array :                             Array 'Main'
                                    ┌─────────────────────────────┐
                                    │  1  │  2  │  3  │  4  │  5  │ 
                                    └─────────────────────────────┘

* Dynamic Array :                             Array 'Temporary'
                                    ┌───────────────────────────────────────────────────────────┐*
                                    │  _  │  _  │  _  │  _  │  _  │  _  │  _  │  _  │  _  │  _  │ 
                                    └───────────────────────────────────────────────────────────┘

* After Copying and Renaming :                Array 'Main'
                                    ┌───────────────────────────────────────────────────────────┐*
                                    │  1  │  2  │  3  │  4  │  5  │  _  │  _  │  _  │  _  │  _  │ 
                                    └───────────────────────────────────────────────────────────┘
* Steps : 
*   1. Create a temporary, dynamic array of x2 size of the dynamic, full array.
*   2. Copy each element to the temporary array.
*   3. Delete the old array (To free name & memory).
*   4. Rename the temporary array to the main one name.
*/

    Section::Start("Applications - Array Expanation");

    int *mainSize = new int(5);
    int *mainArray = new int[*mainSize] {1, 2, 3, 4, 5};

    cout << "Main Array - Before : ";
    for (int i = 0; i < *mainSize; i++)
        cout << mainArray[i] << " " ;
    cout << endl << "Size : " << *mainSize << endl;

    int *temporarySize = new int(*mainSize * 2);
    int *temporaryArray = new int[*temporarySize] {0};

    for (int i = 0; i < *mainSize; i++)
        temporaryArray[i] = mainArray[i];
    cout << endl;

    delete[] mainArray;
    delete mainSize;

    mainArray = temporaryArray;
    mainSize = temporarySize;

    cout << "Main Array - After : ";
    for (int i = 0; i < *mainSize; i++)
        cout << mainArray[i] << " ";

    cout << endl << "Size : " << *mainSize << endl;

    Section::End(75, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    return 0;
}