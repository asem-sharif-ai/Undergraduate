//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │           Author: Asem Al-Sharif           │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │     S e l f   ─   O r g a n i z i n g      │           S    e    a    r    c    h         │
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

// Move to Front (MTF) & Transposition (T)

int organizingSearch(int array[], int size, int key, string method) {
    for (int index = 0; index < size; index++) { // Linear Search
        if (array[index] == key) { // Key Exists

            while (method != "MTF" && method != "mtf" && method != "T" && method != "t") {
                cerr << "\nInvalid Organization Method; choose either [`MTF` or `T`]: ";
                cin >> method;
            }

            if ((method == "MTF" || method == "mtf") && index > 0) { // Move to Front
                swap(array[index], array[0]);

                cout << "\nKey [" << key << "] Was Found At Index [" << index << "]" <<
                        "By Move-To-Front Organizing Search, And Moved To Index [" << 0 << "]\n";
                return 0;

            } else if ((method == "T"  || method == "t") && index > 0) { // Transposition
                swap(array[index], array[index - 1]);

                cout << "\nKey [" << key << "] Was Found At Index [" << index << "]" <<
                        "By Transposition Organizing Search, And Moved To Index [" << index-1 << "]\n";
                return --index;
            
            } else { // index = 0
                cout << "\nKey [" << key << "] Represents The Header Of The Array, " <<
                        "Detected By Self-Organizing Linear Search.\n";
                return index;
            }
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Self-Organizing Linear Search.\n";
    return -1;
}

int main() {

/* ------------------------------------------------------------------------------------------- */

    Section::Start("Self-Organizing Search");

    int array[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25};
    int size = sizeof(array) / sizeof(array[0]);

    cout << "Array: ";
    for (int element : array)
        cout << element << " ";
    cout << endl;

    while (true) {

        int key;
        cout << "\nEnter A Search Key: ";
        cin >> key;

        string form;
        cout << "Choose An Organization Form [`MTF` or `T`]: ";
        cin >> form;

        int index = organizingSearch(array, size, key, form);

        cout << "\nCurrent Index: [" << index << "]";

        cout << "\nCurrent Array: ";
        for (int element : array)
            cout << element << " ";

        Section::End();
    }

/* ------------------------------------------------------------------------------------------- */

    return 0;
}