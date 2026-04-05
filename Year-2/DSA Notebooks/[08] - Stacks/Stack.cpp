//* ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │   Data Structures And Algorithms   │       Author: Asem Al-Sharif       │            Topic: Stack            │
//* ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

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

/*  ----------------------------------------------------------------------------------------------------------------

* Stacks are a fundamental linear data structures following the "Last In, First Out" (LIFO) principle. Consist of
* collections of elements in a structural that support two primary operations: Push and Pop.

* Unlike arrays, stacks do not require contiguous memory locations. Elements are stacked on top of each other,
* and the last element added is the first one to be removed.

* Stacks, in general, are efficient for managing function calls and recursive algorithms, by offering a straight-
* forward approach to managing data with a predictable order of access.

----------------------------------------------------------------------------------------------------------------

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                             S   t   a   c   k                                             │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                   │                                   │                                   │
*  │               .pop()              │               Stack               │             .push(#5)             │
*  │                                   │                                   │                                   │
*  │          │             │          │          │             │          │          │ ┌─────────┐ │          │
*  │          │             │          │          │             │          │          │ │ Top. #5 │ │          │
*  │          │             │          │          │             │          │          │ └─────────┘ │          │
*  │          │             │          │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │
*  │          │             │          │          │ │ Top. #4 │ │          │          │ │ Item #4 │ │          │
*  │          │             │          │          │ └─────────┘ │          │          │ └─────────┘ │          │
*  │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │
*  │          │ │ Top. #3 │ │          │          │ │ Item #3 │ │          │          │ │ Item #3 │ │          │
*  │          │ └─────────┘ │          │          │ └─────────┘ │          │          │ └─────────┘ │          │
*  │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │
*  │          │ │ Item #2 │ │          │          │ │ Item #2 │ │          │          │ │ Item #2 │ │          │
*  │          │ └─────────┘ │          │          │ └─────────┘ │          │          │ └─────────┘ │          │
*  │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │          │ ┌─────────┐ │          │
*  │          │ │ Item #1 │ │          │          │ │ Item #1 │ │          │          │ │ Item #1 │ │          │
*  │          │ └─────────┘ │          │          │ └─────────┘ │          │          │ └─────────┘ │          │
*  │          └─────────────┘          │          └─────────────┘          │          └─────────────┘          │
*  │                                   │                                   │                                   │
*  │  Pop: Removes the element at the  │                                   │  Push: Adds an element to the     │
*  │       top of the stack.           │                                   │        top of the stack.          │
*  │                                   │                                   │                                   │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │            ┌─────────┐            │            ┌─────────┐            │            ┌─────────┐            │
*  │ .peek() =  │ Item #3 │            │            │ Item #4 │            │            │ Item #5 │            │
*  │            └─────────┘            │            └─────────┘            │            └─────────┘            │
*  │                                                                                                           │
*  │  Peek: Retrieves (Returns) the element at the top of the stack without removing it.                       │
*  │                                                                                                           │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------

* Stacks are Logical Data Structures (abstract data types define a particular behavior), so they are commonly
* implemented using different underlying data structures, such as: Arrays or Linked Lists.

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                   Stack As Array                    V.S               Stack As Linked List                │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                      │                                                    │
*  │ 1. Requires contiguous memory allocation (Fixed Size)│ 1. Allocates memory dynamically for each element.  │
*  │                                                      │                                                    │
*  │ 2. Suitable when the size is known in advance or co- │ 2. Suitable when frequent insertions and deletions │
*  │    -nstant size.                                     │    are expected.                                   │
*  │                                                      │                                                    │
*  │ 3. Minimal overhead; only the elements and the fixed │ 3. Additional memory required for pointers in each │
*  │    -size array.                                      │    node.                                           │
*  │                                                      │                                                    │
*  │ 4. Constant-time access to elements randomly through │ 4. Access time is proportional to the position in  │
*  │    indices.                                          │    the list (Requires Traversing).                 │
*  │                                                      │                                                    │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------  */

//! ---------- Linked Lists As Stacks --------------------------------------------------------------------------  !\\

class Node {
public:
    int data;
    Node* next;

    Node() : data(0), next(nullptr) {}
    Node(int item) : data(item), next(nullptr) {}
};

class Stack {
private:
    Node* top;

public:
    Stack() : top(nullptr) {}

/*  ------------------------------------------------------------------------------------------------------------  */

    bool isEmpty() {return top == nullptr;}

/*  ------------------------------------------------------  */

    bool doesExist(int item) {
        if (isEmpty()) return false;

        Node* traverse = top;
        while (traverse != nullptr) {
            if (traverse->data == item) return true; 
            traverse = traverse->next;
        }

        return false;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void display() {
        if (isEmpty()) {
            cerr << "Stack Is Empty is empty. (No items to display)";
            return;
        } else {
            Node* traverse = top;
            while (traverse != nullptr) {
                cout << traverse->data << " ";
                traverse = traverse->next;
            }
        }

        cout << endl;
    }

/*  ------------------------------------------------------  */

    int getSize() {
        if (isEmpty()) {return 0;}

        int size = 0;
        Node* traverse = top;
        while (traverse != nullptr) {
            size++;
            traverse = traverse->next;
        }

        return size;
    }

/*  ------------------------------------------------------  */

    int getOrder(int item) {
        if (isEmpty()) return 0;

        int reachOrder = 1;
        Node* traverse = top;

        while (traverse != nullptr) {
            if (traverse->data == item) return reachOrder;
            reachOrder++;
            traverse = traverse->next;
        }

        return 0;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    int peek() {
        if (!isEmpty()) {
            return top->data;
        } else {
            cerr << "Stack Is Empty, Peek Failed." << endl;
            return -999;
        }
    }

/*  ------------------------------------------------------  */

    void push(int item) {
        Node* newNode = new Node();
        newNode->data= item;
        
        if (isEmpty()) newNode->next = nullptr;
        else           newNode->next = top;

        top = newNode;
    }

/*  ------------------------------------------------------  */

    int pop() {
        if (isEmpty()) {
            cerr << "Stack Is Empty, Deletion Failed." << endl;
            return 0;
        }

        int popped = top->data;

        Node* holdTop = top;
        top = top->next;
        delete holdTop;

        return popped;
    }

/*  ------------------------------------------------------  */

    void empty() {while (!isEmpty()) pop();}
    
};

//! ---------- Arrays As Stacks --------------------------------------------------------------------------------  !\\

#define maxSize 5 /* 1000 */     // const int maxSize = 5; 

class ArrayStack {
private:
    int array[maxSize];
    int top;

public:
    ArrayStack() : top(-1) {}

/*  ------------------------------------------------------------------------------------------------------------  */

    bool isEmpty() {return top == -1;}

/*  ------------------------------------------------------  */

    bool isFull() {return top == maxSize - 1;}

/*  ------------------------------------------------------  */

    bool doesExist(int item) {
        for (int i = 0; i <= top; i++) {
            if (array[i] == item)
                return true;
        }
        return false;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void display() {
        if (isEmpty()) {
            cerr << "Stack Is Empty." ;
            return;
        } else {
            for (int i = top; i >= 0; i--) {
                cout << array[i] << " ";
            }
        }
    }

/*  ------------------------------------------------------  */

    int getSize() {return top + 1;}

/*  ------------------------------------------------------  */

    int getOrder(int item) {
        for (int i = 0; i <= top; i++) {
            if (array[i] == item)
                return i + 1;
        }
        return -1;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    int peek() {
        if (!isEmpty()) {
            return array[top];
        } else {
            cerr << "Stack Is Empty, Peek Failed." << endl;
            return -1;
        }
    }

/*  ------------------------------------------------------  */

    void push(int item) {
        if (!isFull()) {
            top++;
            array[top] = item;
        } else {
            cerr << "Stack Overflow, Push Failed." << endl;
        }
    }

/*  ------------------------------------------------------  */

    int pop() {
        if (isEmpty()) {
            cerr << "Stack Is Empty, Deletion Failed." << endl;
            return 0;
        }

        int pop = array[top--];
        return pop; // Optional
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void empty() { top = -1; }

};

//! ---------- Main --------------------------------------------------------------------------------------------  !\\

    // Class_Name Object_Name;               Declaration
    // Object_Name.Function(Parameters);     Usage . . .

int main() {
    
/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Display Empty Stack");

    Stack UserStack; // Change To ArrayStack

    if (UserStack.isEmpty())
        cout << "Stack Is Empty.";
    else
        cout << "Stack Is Not Empty.";

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Create User Stack");

    int UserKeys;
    for (int i = 1; i <= 7; i++) {
        cout << "Enter Stack Element (" << i << "/7): ";
        cin >> UserKeys;
        cout << endl;
        UserStack.push(UserKeys);
        cout << "Curent Stack : ";
        UserStack.display();
        cout << endl;
    }

    Section::End(75, -1, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("User Final Stack");

    cout << "Final Stack : ";
    UserStack.display();

    cout << "\nStack Size : " << UserStack.getSize();

    cout << "\n\nStack Peek : " << UserStack.peek();

    Section::End(75);
    
/*  ------------------------------------------------------------------------------------------------------------  */

    // Section::Start("Array isFull Stack");

    // if (UserStack.isFull())
    //     cout << "Stack Is Full." << endl;
    // else
    //     cout << "Stack Is Not Full." << endl;

    // Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Pop Top Key");

    cout << "Stack Update (Pop) : ";
    UserStack.pop();
    UserStack.display();

    Section::Start("Pop 3 More Keys");

    cout << "Stack Update (Pop x3) : ";
    UserStack.pop();
    UserStack.pop();
    UserStack.pop();
    UserStack.display();

    Section::End(75, 0, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Push New Key");
    
    cout << "Enter Push Key : ";
    cin >> UserKeys;
    UserStack.push(UserKeys);

    cout << endl << "Stack Update (Push) : ";
    UserStack.display();

    Section::End(75, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Current Stack");

    cout << "Stack Current Size : " << UserStack.getSize() << endl;

    cout << "Stack Current Top : " << UserStack.peek() << endl;

    Section::End(75, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Search Keys (Try Existing & Not Existing Keys)");

    for (int i = 1; i <= 3; i++) {
        cout << "Enter Search Key : ";
        cin >> UserKeys;
        if (UserStack.doesExist(UserKeys)) {
            cout << "Given Key (" << UserKeys << ") Is In The Stack At Order " << UserStack.getOrder(UserKeys) << "\n\n";
        } else {
            cout << "Given Key (" << UserKeys << ") Is Not In The Stack." << "\n\n";
        }
    }

    Section::End(75, -1);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Clear (Empty) Stack ");

    UserStack.empty();
    cout << "Stack after deletion:" << endl;
    UserStack.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    return 0;
}