//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures And Algorithms          │              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮ ╰───────────────────────────────────────────────╮
//* │               A   r   r   a   y               │               C    l    a    s    s             │
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

class Array {
private:
    int size, takenSize, *array;

public: 
    Array(int given_size) {    // Constructor 
        size = given_size;
        takenSize = 0;
        array = new int[size];
    }

    ~Array() {                 // Destructor
        delete[] array;
    }

    void fill(int number) {
        for (int i = 0; i < min(number, size); i++) {
            cout << "Enter Array's Item (" << i + 1 << "/" << min(number, size) << "): \t";
            cin >> array[i];
            takenSize++;
        }
    }

    void empty() {
        for (int i = 0; i < takenSize; i++) {
            array[i] = 0;
        }
        takenSize = 0;
    }

    void add(int item) {
        (takenSize < size) ? array[takenSize++] = item : array[takenSize];
    }

    void pop() {
        (takenSize > 0) ? array[--takenSize] = 0 : array[takenSize];
    }

    void display() {
        if (takenSize > 0) {
            cout << "Array: ";
            for (int i = 0; i < takenSize; i++) {
                cout << array[i] << " ";
            } cout << endl;
        } else {
            cout << "Array is empty.\n";
        }
    }

    int getSize()   { return size; }
    int getLength() { return takenSize; }
};

int main() {
    
    cout << "Enter the size of the array: ";
    int arraySize;   cin >> arraySize;

    Array myArray(arraySize);

    cout << "Enter the number of elements to fill: ";
    int fillCount;   cin >> fillCount;
    myArray.fill(fillCount);

    myArray.display();

    cout << "Enter an item to add: ";
    int newItem;  cin >> newItem;
    myArray.add(newItem);

    myArray.display();

    myArray.pop();
    myArray.display();

    myArray.empty();

    myArray.display();

    return 0;
}