//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures And Algorithms          │              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮ ╰───────────────────────────────────────────────╮
//* │             S   t   a   t   i   c             │               A   r   r   a   y   s             │
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

* Arrays are fixed-size collections of elements stored in contiguous memory locations. Classified as a
* Fundamental Non-Primitive Data Structure of Linear List type.

* Arrays are utilized for storing and accessing homogeneous data types, in addition to thair role as
* essential building blocks for more intricate data structures, as they are often implemented as the
* underlying structure for other complex structures such as Stacks and Queues.

* Array elements offer the ability of sequential or random access, allowing modification through any
* determined index. Additionally, the structure of arrays supports various operations, making them
* suitable and efficient for algorithms, such as: Insertion, Deletion, Searching, and Sorting.

-------------------------------------------------------------------------------------------------------

* - A. Unspecified (Auto / Fit) Array Size `[]` :
*      - The size is determined once the elements' scope is closed `}`.
*      - The machine calculates the exact bytes requirement for the array by multiplying the number of
*        elements with the data type size.

!  `data_type array_name[] = {array_elements};`

? int array[] : {1, 2, 3, 4, 5, 6, 7};
?                    ┌─────────────────────────────────────────┐
?                    │  1  │  2  │  3  │  4  │  5  │  6  │  7  |  Out of Bounds (Uninitialized Values).
?                    └─────────────────────────────────────────┘
?         index [i] =   0     1     2     3     4     5     6   ◄ Last = [size - 1]

* - Get Array Size (Capacity / Number of Elements) by `sizeof()`:
*      - It is a compile-time operator, used to determine the size (in bytes) of an object.
*      - When applied to an array (`sizeof(array)`), it returns the total size of the entire array.
*      - When applied to an element (`sizeof(array[0])`), returns the size of the data type.

? int size = sizeof(array) / sizeof(array[0]);`
?                  ╰> #28 Bytes    ╰> #4       = 7 -> Number of Elements

   --------------------------------------------------

* - B. Specified Array Size `[array_size]` :
*      - The size of static arrays must be a numeric constant (Number or Constant Integer `const int`).
*      - If the specified size is larger than the number of elements, the array will store the provided
*        values and fill the remaining gap with zeros.

!  `data_type array_name[array_size] = {array_elements};`

? const int size = 10;
? int array[size] = {1, 2, 3, 4, 5, 6, 7};   // [10]
?                    ┌───────────────────────────────────────────────────────────┐
?                    │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  0  │  0  |  0  |  R  |  R  |  . . .
?                    └───────────────────────────────────────────────────────────┘
?         index [i] =   0     1     2     3     4     5     6     7     8     9   ◄ Last = [size - 1]

-------------------------------------------------------------------------------------------------------

* - C. Accessing and Modifying Elements by Index :
*      - Note: Consider that arrays are zero-indexed.

!  `array_name[element_index];`
!  `array_name[element_index] = new_value;`

* Arrays offer constant time O(1) access to any of their elements, regardless of the array's size, by
* utilizing an index-based retrieval system.

* This efficiency is achieved because of how arrays are organized in memory (contiguous locations).

* Memory addresses based on indices formula:
!  `element_address = array_address + (index * sizeof(data_type))`

   --------------------------------------------------

* - D. Loop Over All or Some Elements :

!  `for (int i = 0; i < array_size; i++) {...}`
!  `for (data_type element : array_name) {...}`

---------------------------------------------------------------------------------------------------  */

int main() {

    int array_1[] = {0, 2, 4, 6, 8};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

/* 
*                    ┌─────────────────────────────┐
*                    │  0  │  2  │  4  │  6  │  8  │  ->  Size = 5
*                    └─────────────────────────────┘
*/

    const int size_2 = 10;
    int array_2[size_2] = {1, 3, 5, 7, 9};

/*
*                    ┌───────────────────────────────────────────────────────────┐
*                    │  1  │  3  │  5  │  7  │  9  │  0  │  0  │  0  │  0  |  0  |  ->  Size = 10
*                    └───────────────────────────────────────────────────────────┘
*/

    Section::Start("Access Elements");

    cout << "Frist Element At Array .1 (0) : " << array_1[0] << endl;
    cout << "Frist Element At Array .2 (1) : " << array_2[0] << endl << endl;

    cout << "Last Element At Array .1 (8) : " << array_1[size_1-1] << endl;
    cout << "Last Element At Array .2 (0) : " << array_2[size_2-1] << endl << endl;

    cout << "Eighth Element At Array .1 (?) : " << array_1[7] << endl;        /* Uninitialized, Unexpectable Value */
    cout << "Eighth Element At Array .2 (0) : " << array_2[7] << endl;        /* Free Size Gap -> Empty Value = 0  */

    // cout << array[0:5] << endl ;                            /* Syntax Error, This Is Not How To Slice An Array. */

    Section::End();

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Display An Array - [By Loop]");

    cout << "Array .1 Elements : " << endl;
    for (int i = 0 ; i < size_1 ; i++) {                                       /* Array Elements Sperated By Space */
        cout << array_1[i] << " ";                                             /* 0 2 4 6 8             | Fit Size */
    }
    cout << endl << endl; 

    cout << "Array .2 Elements : " << endl;
    for (int i = 0 ; i < size_2 ; i++) {
        cout << array_2[i] << " ";                                             /* 1 3 5 7 9 0 0 0 0 0 | '0'? Size. */ 
    }
    cout << endl;

    Section::Start("Display An Array - [By Elements]");
    
    cout << "Array .1 Elements : " << endl;
    for (int element : array_1) {
        cout << element << " ";
    }
    cout << endl << endl;

    cout << "Array .2 Elements : " << endl;
    for (int element : array_2) {
        cout << element << " ";
    }
    cout << endl;

    //! Note: The second method works only within the scope where the array is initially declared. 
    //!       Does not extend to functions passed as parameters.

    Section::End();

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Display An Array Memory Address");
    
    cout << "Array .1 Memory Address : " << array_2 << endl;                /* Memory Address - NOT Array Elements */
    cout << "Array .2 Memory Address : " << array_1 << endl;                /* But . . . . . In Case Of charArray? */

    Section::Start("Display Char Array Elements [No Loop]");

    char charArray[] = "Simple Characters Array.";
    cout << "charArray : " << charArray;                                    /* Characters Array Elements Displayed */

    Section::End();

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("OverWrite / Update Elements");

    array_2[0] = 10;
    array_2[1] += 10;
    array_2[2] ++;
    array_2[3] = array_2[3] + array_2[4];

    array_1[0] = array_2[0];

    cout << "Array .1 1St (1 -> 10)   : " << array_2[0] << endl <<
            "Array .1 2Nd (3 -> 3+10) : " << array_2[1] << endl <<
            "Array .1 3Rd (5 -> 5+1)  : " << array_2[2] << endl <<
            "Array .1 3Rd (7 -> 7+9)  : " << array_2[3] << endl;

    cout << "Array .2 1St (0 -> 1.1St) : " << array_2[0]; 

    Section::End(75);

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("2D Array");

    // //! data_type array_name[array_rows][array_columns] = {{row_1}, {row_2}, {row_3}, . . .};
    // //!           Note : each row has n elements [n = array_columns]

    const int R = 3 , C = 5 ;
    int array_2D[R][C] = {{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}, {11, 12, 13, 14, 15}};

    cout << "2D Array (3 x 5): " << endl;
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++)
            cout << array_2D[i][j] << " ";
        cout << endl;
    }

    Section::Start("rowSum, columnSum, & Sum");

    int sumArray = 0;
    for (int i = 0; i < R; i++) {
        for (int j = 0; j < C; j++) {
            sumArray += array_2D[i][j];
        }
    }
    cout << "Array Elements Sum : " << sumArray << endl << endl;

    for (int i = 0; i < R; i++) {
        int sumRows = 0;
        for (int j = 0; j < C; j++) {
            sumRows += array_2D[i][j];
        }
        cout << "Row No." << i+1 << " Sum : " << sumRows << endl;
    }
    cout << endl;

    for (int j = 0; j < C; j++) {
        int sumColumns = 0;
        for (int i = 0; i < R; i++) {
            sumColumns += array_2D[i][j];
        }
        cout << "Column No." << j+1 << " Sum : " << sumColumns << endl;
    }

    Section::End(75, 0);

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("3D Array");

    /*   type name =    */

    // //! data_type array_name[x_axis][y_axis][z_axis] = {X.{Y.{Z.}}};
    // //!           Steps : 
    // //!                1. { } -> Array,                            INSIDE {} :
    // //!                2.  { }, { }, { } -> x_axis,                      INSIDE EACH X {} :
    // //!                3.   { }, { }, { }, { }, { } -> y_axis,                  INSIDE EACH Y {} :
    // //!                4.    {z, z, z, z, z} -> z_axis

    const int X = 3 , Y = 5 , Z = 5 ;
    int array_3D[X][Y][Z] = {
    { {1,  2,  3,  4,  5 }, {6,  7,  8,  9,  10}, {11, 12, 13, 14, 15}, {16, 17, 18, 19, 20}, {21, 22, 23, 24, 25} },
    { {26, 27, 28, 29, 30}, {31, 32, 33, 34, 35}, {36, 37, 38, 39, 40}, {41, 42, 43, 44, 45}, {46, 47, 48, 49, 50} },
    { {51, 52, 53, 54, 55}, {56, 57, 58, 59, 60}, {61, 62, 63, 64, 65}, {66, 67, 68, 69, 70}, {71, 72, 73, 74, 75} } };

    cout << "3D Array (3 x 5 x 5): " << endl;
    for (int x = 0; x < X; x++) {
        for (int y = 0; y < Y; y++) {
            for (int z = 0; z < Z; z++) {
                cout << array_3D[x][y][z] << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
    
    Section::End(75, 0);

/*  -------------------------------------------------------------------------------------------------------------  */

    return 0;
}