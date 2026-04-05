//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures and Algorithms        ╭─╮              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮│╰───────────────────────────────────────────────╮
//* │              P  o  i  n  t  e  r              ╰─╯           R  e  f  e  r  e  n  c  e           │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
static constexpr auto *color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";

static void Start(string name = "Untitled Section", int before = 0, int after = 1)
{cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n');}

static void End(char symbol = '-', int number = 50, int before = 1, int after = 0)
{cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n');}

};

/* ----------------------------------------------------------------------------------------------------

* ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
* │      [ & ]      │      Reference Operator      │     Means: "Address Of Value ( + Variable )"     │
* │─────────────────│──────────────────────────────│──────────────────────────────────────────────────│
* │      [ * ]      │     Dereference Operator     │     Means: "Value At Address ( + Pointer )"      │
* └───────────────────────────────────────────────────────────────────────────────────────────────────┘

* Pointers Are Variables That Store Memory Address Of Other Variable.

* ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
* │            Variable            │            Reference            │            *Pointer            │
* │───────────────────────────────────────────────────────────────────────────────────────────────────│
* │                                │                                 │                                │
* │ type variable = value;         │ type &reference = variable;     │ type *pointer = &variable;     │
* │                                │                                 │                                │
* │───────────────────────────────────────────────────────────────────────────────────────────────────│
* │                                │                                 │                                │
* │ Variable_Name  = variable      │ Name  = reference               │ Name  = pointer                │
* │ Variable_Value = value         │ Value = LinkFor(variable)       │ Value = AddressOf(variable)    │
* │                                │                                 │                                │
* │───────────────────────────────────────────────────────────────────────────────────────────────────│
* │                                │                                 │                                │
* │ Store Values.                  │ Another Name For Existing       │ Store Memory Addresses Of      │
* │                                │ Variables.                      │ Variables.                     │
* │                                │                                 │                                │
* └───────────────────────────────────────────────────────────────────────────────────────────────────┘

!  `type var  = val;`
!   -> Declaring A Variable [var] With Value [val].

!  `type &ref = val;`
!   -> Declaring A Reference [ref] With Value [link_to(var)].

!  `type *ptr = &var;`
!   -> Declaring A Pointer [ptr] With Value [address_of(var)].

-------------------------------------------------------------------------------------------------------

* Arrays Pointers:
*                                                 ╭───────────────────────────────────────────────────╮
*                                                 │   ┌───────────────────────────────────────────┐   │
*           [▼ P]       [▼ P+8]     [▼ P+16]      │   │         char / bool        │   1 Byte.    │  <╯
*         ┌─────────────────────────────┐         │   │───────────────────────────────────────────│
*         │  A  │  B  │  C  │  D  │  E  │         │   │          short int         │   2 Bytes.   │  <╯
*         └─────────────────────────────┘         │   │───────────────────────────────────────────│
*                 [▲ P+4]     [▲ P+12]            │   │   int / long int / float   │   4 Bytes.   │  <╯
*                                                 │   │───────────────────────────────────────────│
* Pointers Arithmetic Is Determined By The Data   │   │   long long int / double   │   8 Bytes.   │  <╯
*                                          Type  <╯   └───────────────────────────────────────────┘

* Note That:
* - When A Pointer Is Passed To An Array, It Points To The First Element Of The Array.
* - The Array Name Is Also A Pointer To The First Element.

?  Value  [i]  =   array[i]  =  *(array + i)  =  *(pointer + i)
? Address [i]  =  &array[i]  =   (array + i)  =   (pointer + i)

* Recall: 
* - Memory addresses based on index: &array[i] = &array[0] + (i * sizeof(array[0]))

---------------------------------------------------------------------------------------------------  */

int Function(int *pointer) {
    return *pointer += 1;   // Return The Value Increased By +1
}

/* ------------------------------------------------------------------------------------------------- */

int main() {

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("[&] = Get Memory Address");

    int Variable = 10;
    cout << "Variable.Value : " << Variable << endl << "Variable.Address : " << &Variable;

    Section::End(75);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("[*] = Declare A Pointer");

        //*  A. int *pointer;                              -> Pointer
        //*     int *pointer = &variable;                  -> Pointer

        //*  B. int *dynamicVariable = new int;            -> Dynamic Variable
        //*     int *dynamicVariable = new int(value);     -> Dynamic Variable

    int *random_pointer;
    cout << "Random Pointer : " << random_pointer << endl;

    int *null_pointer = nullptr;    // NULL
    cout << "Null Pointer : " << null_pointer;    // 0

    char   *char_ptr; 
    float  *integer_pointer;
    double *double_pointer;
    string *string_Pointer;    //* ... Other Data Types

    Section::End(75);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Create Pointer 'ptr' To Hold The Address Of Variable 'var_1'", 0);

    int var_1 = 100;
    int *ptr = &var_1;

    cout << "Value   (var_1 = *ptr) : " << var_1  << " = " << *ptr << endl
         << "Pointer (ptr = &var_1) : " << &var_1 << " = " << ptr  << endl << endl;

    var_1  = 250;   // *ptr = 250;

    cout << "New Value    : " << var_1 << " = " << *ptr  << endl
         << "Same Address : " << &var_1 << " = " << ptr << endl << endl;


    Section::Start("Create Reference 'ref' To Hold A Address For Variable 'var_2'", -1);

    int var_2 = 500;
    int &ref = var_2;

    cout << "Value (var_2 = ref) : " << var_2 << endl;
    cout << "By Reference        : " << ref    << endl << endl;   // Same As Value

    var_2 = 1000;   // ref = 1000;
    cout << "New Value     : " << var_2 << endl;
    cout << "New Reference : " << ref;

    Section::End(75);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Pointer As Function Parameter");

    int functionVariable = 5;
    int *functionPointer = &functionVariable;

    cout << "Pointer  Value     : " << *functionPointer << endl;
    cout << "Function Pointer 1 : " << Function(functionPointer) << endl;
    cout << "Function Pointer 2 : " << Function(functionPointer) << endl;
    cout << "Function Pointer 3 : " << Function(functionPointer) << endl;

    Section::End(75, 0);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Pointer To An Array");

    int array[] = {10, 20, 30, 40, 50};
    int* pointer = array; // OR ` = array[0] `

    cout << "Value At [i = 0] (By Index)                         : " << array[0]       << endl
         << "Value At [i = 1] (By Pointer Arithmetic On Array)   : " << *(array + 1)   << endl
         << "Value At [i = 2] (By Pointer Arithmetic On Pointer) : " << *(pointer + 2) << endl << endl;

    cout << "Address Of [i = 0] (By Reference)                   : " << &array[0]      << endl
         << "Address Of [i = 1] (Pointer Arithmetic On Array)    : " <<  (array + 1)   << endl
         << "Address Of [i = 2] (Pointer Arithmetic On Pointer)  : " <<  (pointer + 2) << endl;

    Section::End(75, 0);

/* ------------------------------------------------------------------------------------------------- */
/*
*                                    Pointer_0 ▼        _2 ▼        _4 ▼
*                                           ┌─────────────────────────────┐
*                                           │  0  │  1  │  2  │  3  │  4  │
*                                           └─────────────────────────────┘
*                                          Pointer_1 ▲        _3 ▲


        //*   Pointer++ : Means To Move Forward To The Next Pointer.

        //*   *Pointer++ : Value At Pointer_1 -> Value At Pointer_2 -> Value At Pointer_3
        //*   *Pointer-- : Value At Pointer_3 -> Value At Pointer_2 -> Value At Pointer_1


*       Pointer_2;  Pointer_2++;  Pointer_2++; 
*
*                 [ _2 ▼ ]                                                                              [ _4 ▼ ]
*       ┌─────────────────────────────┐      ┌─────────────────────────────┐      ┌─────────────────────────────┐
*       │  0  │  1  │  2  │  3  │  4  │  ->  │  0  │  1  │  2  │  3  │  4  │  ->  │  0  │  1  │  2  │  3  │  4  │ 
*       └─────────────────────────────┘      └─────────────────────────────┘      └─────────────────────────────┘
*                                                            [ _3 ▲ ]
*/

    Section::Start("Pointer++ & Pointer--");

    const int scrollSize = 5;
    int scrollArray[scrollSize] = {10, 20, 30, 40, 50};

    int *scrollPointer = &scrollArray[2]; // (30)

    cout << "Pointer 3 : " << scrollPointer << " [Value = " << *(scrollArray + 2) << "]\n"<< endl;

    scrollPointer++ ; // (40)
    cout << "++Pointer 3 : " << scrollPointer << " [Value = " << *(scrollArray + 2+1) << "]\n";
    cout << "  Pointer 4 : " << scrollPointer << " [Value = " << *(scrollArray + 3)   << "]\n";

    scrollPointer-- ; // Reset to (30)
    scrollPointer-- ; // (20)
    cout << "--Pointer 3 : " << scrollPointer << " [Value = " << *(scrollArray + 2-1) << "]\n";
    cout << "  Pointer 2 : " << scrollPointer << " [Value = " << *(scrollArray + 1)   << "]\n";

    Section::End(75, 0);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Array Of Pointers");

    const int valuesSize = 5;
    int valuesArray[valuesSize] = {10, 20, 30, 40, 50};

    int* pointersArray[valuesSize];

    for(int i = 0; i < valuesSize; i++)
        pointersArray[i] = &valuesArray[i];

    for(int i = 0; i < valuesSize; i++)
        cout << pointersArray[i] << " ";

    Section::End(75);

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Pointer-To-Pointer");

    int x = 50;
    int *pointerX = &x;
    int **p_pointerX = &pointerX;

    cout << "Value Through Double Pointer : " << **p_pointerX << endl;

    **p_pointerX = 100;
    cout << "Modified Value : " << x;

    Section::End(75);

/* ------------------------------------------------------------------------------------------------- */

    return 0;
}