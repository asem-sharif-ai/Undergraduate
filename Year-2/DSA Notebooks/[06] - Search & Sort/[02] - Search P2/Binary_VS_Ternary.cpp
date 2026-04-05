//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │         Author: ENG Asem Al-Sharif         │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         B    i    n    a    r    y         │           T   e   r   n   a   r   y          │
//* ╰───────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

class Section { // For The Display, IGNORE.
public:
    static void Start(string name = "Untiteled Section", int before = 0, int after = 1) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[4;91m" << name << ":\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
    static void End(char symbol = '-', int number = 50, int before = 1, int after = 0) {
        for (int i = 0; i <= before; i++) cout << endl;
        cout << "\033[91m" << string(number, symbol) << "\033[0m";
        for (int i = 0; i <= after;  i++) cout << endl;
    }
};

int binarySearch(int array[], int size, int key) {

    int Low = 0, High = size - 1;
    int iterations = 0, comparisons = 0;

    while (Low <= High) {

        iterations++;
        comparisons++;

        int Mid = (High + Low) / 2;

        if (array[Mid] == key) {
            comparisons+=1;
            cout << "\nKey [" << key << "] Is Found At Index [" << Mid << "] By Binary Search.\n";
            cout << "Total Comparisons: " << comparisons << endl
                 << "Total Iterations : " << iterations  << endl;
            return Mid;

        } else if (array[Mid] > key) {
            comparisons+=2;
            High = Mid - 1;
        } else { /* if (array[Mid] < key) */
            comparisons+=2;
            Low = Mid + 1;
        }
    } comparisons++; // loop over (Low > High)

    cout << "\nKey [" << key << "] Is Not Found By Binary Search.\n";
    cout << "Total Comparisons: " << comparisons << endl
         << "Total Iterations : " << iterations  << endl;
    return -1;
}

int ternarySearch(int array[], int size, int key) {

    int Low = 0, High = size - 1;
    int  iterations = 0, comparisons = 0;

    while (Low <= High) {

        iterations++;
        comparisons++;

        int Third = (High - Low) / 3;
        int lowThird  = Low + Third;
        int highThird = High - Third;

        if (array[lowThird] == key) {
            comparisons+=1;
            cout << "\nKey [" << key << "] Is Found At Index [" << lowThird << "] By Ternary Search.\n";
            cout << "Total Comparisons: " << comparisons << endl
                 << "Total Iterations : " << iterations  << endl;
            return lowThird;
            
        } else if (array[highThird] == key) {
            comparisons+=2;
            cout << "\nKey [" << key << "] Is Found At Index [" << highThird << "] By Ternary Search.\n";
            cout << "Total Comparisons: " << comparisons << endl
                 << "Total Iterations : " << iterations  << endl;
            return highThird;

        } else if (array[lowThird] > key) {
            comparisons+=3;
            High = lowThird - 1;

        } else if (array[highThird] < key) {
            comparisons+=4;
            Low = highThird + 1;

        } else {  /* if (array[lowThird] < key < array[highThird]) */
            comparisons+=4;
            Low = lowThird + 1;
            High = highThird - 1;
        }
    } comparisons++; // loop over (Low > High)

    cout << "\nKey [" << key << "] Is Not Found By Ternary Search.\n";
            cout << "Total Comparisons: " << comparisons << endl
                 << "Total Iterations : " << iterations  << endl;
    return -1;
}

int main() {

    int array_1[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25};
    int size_1 = sizeof(array_1) / sizeof(array_1[0]);

    cout << "Array : ";
    for (int element : array_1)
        cout << element << " ";

    while (true) {
        int key_1;
        cout << "\nEnter A Search Key: ";
        cin >> key_1;

        int index_1  = binarySearch(array_1, size_1, key_1);
        int index_1_ = ternarySearch(array_1, size_1, key_1);

        Section::End();
    }

    return 0;
}
