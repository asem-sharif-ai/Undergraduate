//* ╭───────────────────────────────────────────────────────────────────────────────────────────╮
//* │       Data Structures And Algorithms         │         Author: ENG Asem Al-Sharif         │
//* ╰────────────────────────────────────────────╮ ╰────────────────────────────────────────────╮
//* │         I n t e r p o l a t i o n          │           S    e    a    r    c    h         │
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

/* ------------------------------------------------------------------------------------------- */

int interpolationSearch(int array[], int size, int key) {
    int Low = 0, High = size - 1;
    int interpolations = 0;

    while (Low <= High && key >= array[Low] && key <= array[High]) {
        interpolations++;

        // Find the index by interpolation formula
        int index = Low + ((double)(High - Low) / (array[High] - array[Low])) * (key - array[Low]);

        index = max(Low, min(index, High));

        if (array[index] == key) {
            cout << "\nKey [" << key << "] Is Found At Index [" << index << "] By Interpolation Search.\n";
            cout << "Total Interpolations: " << interpolations;
            return index;
        } else if (array[index] > key) {
            High = index - 1;
        } else {
            Low = index + 1;
        }
    }

    cout << "\nKey [" << key << "] Is Not Found By Interpolation Search.\n";
    cout << "Total Interpolations: " << interpolations;
    return -1;
}

/* ------------------------------------------------------------------------------------------- */

int main() {

    Section::Start("Interpolation Search");

    int array[] = {1, 2, 4, 7, 11, 16, 22, 29, 37, 46, 56, 77, 89, 102, 116};
    int size = sizeof(array) / sizeof(array[0]); 

    cout << "Array : ";
    for (int element : array)
        cout << element << " ";

    while (true) {
        
        int key;
        cout << "\nEnter A Search Key: ";
        cin >> key;

        int index  = interpolationSearch(array, size, key);
        
        Section::End();

    }

    return 0;
}