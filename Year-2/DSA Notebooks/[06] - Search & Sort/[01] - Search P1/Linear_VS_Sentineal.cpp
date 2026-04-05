//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         L    i    n    e    a    r         │          S   e   n   t   i   n   e   l       │
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

/* ------------------------------------------------------------------------------------------- */

int linearSearch(int array[], int size, int key) {
    int comparisons = 0;
    for (int index = 0; index < size; index++) {
        comparisons++;
        if (array[index] == key) {
            comparisons++;
            cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Linear Search.\n";
            cout << "Total Comparisons: " << comparisons << endl;
            return index;
        }
        comparisons++;
    } comparisons++;   // index = size

    cout << "\nKey [" << key << "] Is Not Found By Linear Search.\n";
    cout << "Total Comparisons: " << comparisons << endl;
    return -1;
}

/* ------------------------------------------------------------------------------------------- */

int sentinelSearch(int array[], int size, int key) {

    int index = 0, lastElement = array[size - 1];
    array[size-1] = key;

    int comparisons = 0;

    while (array[index] != key) {
        comparisons++;
        index++;
    } comparisons++;   // array[index] == key

    array[size-1] = lastElement;

    if ((index < size - 1)) {
        comparisons+=1;
        cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Sentinel Search.\n";
        cout << "Total Comparisons: " << comparisons << endl;
        return index;

    } else if (array[size - 1] == key) {
        comparisons+=2;
        cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Sentinel Search.\n";
        cout << "Total Comparisons: " << comparisons << endl;
        return index;

    } else {
        comparisons+=2;
        cout << "\nKey [" << key << "] Is Not Found By Sentinel Search.\n";
        cout << "Total Comparisons: " << comparisons << endl;
        return -1;
    }
}

/* ------------------------------------------------------------------------------------------- */

int main() {

/* ------------------------------------------------------------------------------------------- */

    Section::Start("Linear VS Sentinel Search");

    int array[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
    // int array[] = {10, 3, 8, 1, 9, 4, 7, 15, 2, 14, 12, 11, 5, 6, 13};

    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array: ";
    for (int element : array)
        cout << element << " ";

    while (true) {

        int key;
        cout << "\n\nEnter A Search Key: ";
        cin >> key;

        int index_L = linearSearch(array, size, key);
        int index_S = sentinelSearch(array, size, key);

        Section::End();
    }

/* ------------------------------------------------------------------------------------------- */

    return 0;
}