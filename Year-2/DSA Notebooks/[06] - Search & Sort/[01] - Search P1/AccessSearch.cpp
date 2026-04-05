//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │    A c c e s s  ─  O r g a n i z i n g     │           S    e    a    r    c    h         │
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

//* Elements structure

struct Array { 
    int value;
    bool prime = false; // true -> no limit
    int access = 0;
    bool trash = false; // true -> deleted
};

/* ------------------------------------------------------------------------------------------- */

void printArray(Array array[], int size) {
    for (int i = 0; i < size; i++) {
        if (!array[i].trash) {
            cout << "(" << array[i].value << ", " << array[i].access << ")";
            if (array[i].prime) cout << "*";
        }

        if (!array[i+1].trash && i < size-1) cout << ", ";
    }
}

void trashElement(Array array[], int index) {
    array[index].value = array[index].access = array[index].prime = 0;
    array[index].trash = true;
}

/* ------------------------------------------------------------------------------------------- */

int accessSearch(Array array[], int size, int key, int andSort = 1, int limit = 10) {
    if (size == 0) {
        cerr << "\nArray Is Empty.\n";
        return -100; // [-100] array is empty.
    }

    for (int index = 0; index < size; index++) {
        if (array[index].value == key) {
            array[index].access++;

            if ((array[index].access > limit) && (array[index].prime == false)) {
                for (int current = index; current < size - 1; current++) {
                    array[current] = array[current + 1];
                } // Shifting Over Deleted Element

                trashElement(array, size-1); // Trash Last Element Duplication
                cerr << "\nKey [" << key << "] Was Deleted Due To Excessive Access.\n";
                return -10; // [-10] key was found and deleted.
            }

            if (andSort != 0) {
                while ((array[index].access > array[index-1].access) && (index > 0)) {
                    swap(array[index], array[index-1]);
                    index--;
                }
            }

            cout << "\nKey [" << key << "] Was Found At Index [" << index << "] By Access Organizing Search.\n";
            return index;
        }
    }

    cout << "\nKey [" << key << "] Was Not Found By Access Organizing Search.\n";
    return -1; // [-1] key was not found.
}

/* ------------------------------------------------------------------------------------------- */

int main() {

/* ------------------------------------------------------------------------------------------- */

    Section::Start("Access Organizing Search");

    Array array[] = {{10}, {20}, {30, true}, {40}, {50, true, 3}, {60}, {70, true}, {80}, {90}, {100, 0, 3}};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array: ";
    printArray(array, size);
    cout << endl;

    while (true) {

        int key;
        cout << "\nEnter A Search Key: ";
        cin >> key;

        int index = accessSearch(array, size, key);

        cout << "\nCurrent Array: ";
        printArray(array, size);

        Section::End();
    }

/* ------------------------------------------------------------------------------------------- */

    return 0;
}