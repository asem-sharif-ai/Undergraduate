//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures And Algorithms          │              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮ ╰───────────────────────────────────────────────╮
//* │               A   r   r   a   y               │         A  p  p  l  i  c  a  t  i  o  n  s      │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
static constexpr auto *color = "\033[91m", *color_ = "\033[4;91m", *reset = "\033[0m";

static void Start(string name = "Untitled Section", int before = 0, int after = 1)
{cout << string(++before, '\n') << color_ << name << ':' << reset << string(++after, '\n');}

static void End(char symbol = '-', int number = 50, int before = 1, int after = 0)
{ cout << string(++before, '\n') << color << string(number, symbol) << reset << string(++after, '\n');}

};

/* ------------------------------------------------------------------------------------------------- */

int main() {
    
/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Get Swm, Average, Highest, Lowest");

    int array_3[] = {0, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 0, 6, 7, 8, 9, 10};
    const int size_3 = sizeof(array_3) / sizeof(array_3[0]); // Used as copyArray Size

    cout << "Array .3 : ";
    for (int i = 0; i < size_3; i++) {
        cout << array_3[i] << " " ;
    }

    int sum = 0, highest = array_3[0], lowest  = array_3[0];

    for (int i = 0; i < size_3; ++i) {
        sum += array_3[i];

        if (array_3[i] > highest) {
            highest = array_3[i];
        } else if (array_3[i] < lowest) {
            lowest = array_3[i];
        }
    }

    double avg = (double) 1.0 * sum / size_3;

    cout << "\nSum     = " << sum
         << "\nAverage = " << avg
         << "\nMin     = " << lowest
         << "\nMax     = " << highest;

    Section::End();

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Copy An Array");

    int copyArray_3[size_3];
    for (int i = 0; i < size_3; i++) {
        copyArray_3[i] = array_3[i];
    }

    cout << "Copy-Array .3 : ";
    for (int element : copyArray_3)
        cout << element << " ";

    cout << endl;

    Section::Start("Application - Slice An Array");

    int sliceArray_3[10];
    for (int i = 0 ; i < 10 ; i++) {
        sliceArray_3[i] = array_3[i];
    }

    cout << "Slice-Array .3 (10) : ";
    for (int element : sliceArray_3)
        cout << element << " ";

    /* //* Sign-Filtered Array :
    How can array .3 be filtered into three separate arrays based on the zeros and the sign of each
    non-zero element?
      - For such operations, using dynamic arrays is recommended over static arrays. The limitation of
        static arrays lies in their fixed size known at compile-time, making them less suitable for 
        tasks where the size is not predetermined.
    */

    Section::End();

/* ------------------------------------------------------------------------------------------------- */

    Section::Start("Compare Arrays");

    const int AB_size = 5 ;
    int array_A[AB_size] = {1, 4, 3, 2, 5};
    int array_B[AB_size] = {1, 8, 3, 6, 5};

    bool isEqual = true;
    int i = 0;

    while (isEqual && i < AB_size) { // End once there exists a non-equal element
        if (array_A[i] != array_B[i]) isEqual = false;
        i++;
    }

    cout << (isEqual)
    ? "Both Arrays [A, B] Are Equal.\n"
    : "Arrays [A, B] Are Not Equal.\n";

    Section::Start("Application - Equallity Report");

    int binaryEquallityArray[AB_size];

    for (int i = 0 ; i < AB_size ; i++) {
        if (array_A[i] == array_B[i]) {
            cout<< "Element No." << i+1 << " Is Equal In Both Arrays" << endl;
            binaryEquallityArray[i] = 1;
        }
        else {
            cout<< "Element No." << i+1 << " Is Not Equal In Both Arrays" << endl;
            binaryEquallityArray[i] = 0;
        }
    }

    cout << endl << "Equallity Report As Binary Array : ";
    for (int element : binaryEquallityArray)
        cout << element << " ";

    Section::End();

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("Paralles Arrays");

    const int parallel_size = 3;
    string array_x[parallel_size] = {"One", "Two", "Three"};
    float  array_y[parallel_size] = {1.1  ,  2.2 ,  3.3   };
    int    array_z[parallel_size] = {1    ,  2   ,  3     };

    for (int i = 0 ; i < parallel_size ; i++)
        cout << array_x[i] << " = " << array_y[i] << " = " << array_z[i] << endl;

    Section::End();

/*  -------------------------------------------------------------------------------------------------------------  */

    Section::Start("User-Input Fixed-Size Array");

    const int user_size = 5;
    int user_array[user_size];

    for (int i = 0; i < user_size; ++i) {
        cout << "Enter Your Array Elements : " << i+1 << "/" << user_size << endl;
        cin >> user_array[i];
    }

    cout << "Your Array : ";
    for (int element : user_array)
        cout << element << " ";
    
    Section::End();

    return 0;
}