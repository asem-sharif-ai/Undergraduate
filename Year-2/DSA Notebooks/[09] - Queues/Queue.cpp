//* ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │   Data Structures And Algorithms   │       Author: Asem Al-Sharif       │            Topic: Queue            │
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

* Queues are a fundamental linear data structures following the "First In, First Out" (FIFO) principle.

* Queue's items are added at the rear (enqueue), and removed from the front (dequeue). The oldest item is the first
* to be dequeued (removed), and new items are added to the rear (end).

* Just like stacks, queues are Logical Data Structures that use Arrays or Linked Lists as thair underlying structure

* Note that it is never efficient to create array-based queue, as FIFO principle dequeueing requires shifting all
* remaining elements to fill the gap, resulting an O(n) time complexity per operation.

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                             Q   u   e   u   e                                             │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                                                                           │
*  │     ┌─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┐     │
*  │      ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐      │
*  │      │ Tail #7 │   │ Item #6 │   │ Item #5 │   │ Item #4 │   │ Item #3 │   │ Item #2 │   │ Head #1 │      │
*  │      └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘      │
*  │     └─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┘     │
*  │                                                                                                           │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                                                                           │
*  │  Dequeue() (Delete): Removing the item from the FRONT (Head) of the queue.                                │
*  │                                                                                                           │
*  │     ┌─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┐     │
*  │                    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐      │
*  │                    │ Tail #7 │   │ Item #6 │   │ Item #5 │   │ Item #4 │   │ Item #3 │   │ Head #2 │      │
*  │                    └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘      │
*  │     └─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┘     │
*  │                                                                                                           │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                                                                           │
*  │  Enqueue(#8) (Insert): Adding an item to the REAR (End / Tail) of the queue.                              │
*  │                                                                                                           │
*  │     ┌─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┐     │
*  │      ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐      │
*  │      │ Tail #8 │   │ Item #7 │   │ Item #6 │   │ Item #5 │   │ Item #4 │   │ Item #3 │   │ Head #2 │      │
*  │      └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘      │
*  │     └─────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ────────── ➤ ───────────┘     │
*  │                                                                                                           │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

* About The Haed (Front) & Tail (Rear):
* Pointers indicating the beginning and ending items in the queue.

----------------------------------------------------------------------------------------------------------------

* Queues Types:

* - Linear / Simple Queue (Most basic and common type):
* Simply Follows the "First In, First Out" (FIFO) principle in enqueuing and dequeuing.

* - Doubly Queue / Deque (More flexibility):
* Supports enqueuing (insertion) and dequeuing (deletion) at both edges (front and rear).

* - Circular Queue (Better space utilization): Fixed-size queue with Rear-Front connection. 

* - Priority Queue: Queue that maintains its items order based on the priority assigned to each item.

---------------------------------------------------------------------------------------------------------------- */

//! ---------- Linked Lists As Queues --------------------------------------------------------------------------  !\\

class Node {
public:
    int data;
    Node* next;

    Node() : data(0), next(nullptr) {}
    Node(int item) : data(item), next(nullptr) {}
};

class Queue {
private:
    Node* front;
    Node* rear;

public:
    Queue() : front(nullptr), rear(nullptr) {}

/*  ------------------------------------------------------------------------------------------------------------  */

    bool isEmpty() {return (front == nullptr);}

/*  ------------------------------------------------------  */

    bool doesExist(int item) {
        if (isEmpty()) return false;

        Node* traverse = front;
        while (traverse != nullptr) {
            if (traverse->data == item) return true; 
            traverse = traverse->next;
        }

        return false;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void display() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items to display)";
            return;
        } else {
            Node* traverse = front;
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
        Node* traverse = front;
        while (traverse != nullptr) {
            size++;
            traverse = traverse->next;
        }

        return size;
    }

/*  ------------------------------------------------------  */

    int getFront() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items in the front)" << endl;
            return -999;
        }
        return front->data;
    }

/*  ------------------------------------------------------  */

    int getRear() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items in the rear)" << endl;
            return -999;
        }
        return rear->data;
    }

/*  ------------------------------------------------------  */

    int getOrder(int item) {
        if (isEmpty()) return 0;

        int reachOrder = 1;
        Node* traverse = front;

        while (traverse != nullptr) {
            if (traverse->data == item) return reachOrder;
            reachOrder++;
            traverse = traverse->next;
        }

        return 0;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void enQueue(int item) {
        Node* newNode = new Node();
        newNode->data = item;

        if (isEmpty()) {
            front = rear = newNode;
        } else {
            rear->next = newNode;
            rear = newNode;
        }
    }

/*  ------------------------------------------------------  */

    int deQueue() {
        if (isEmpty()) {
            cerr << "Queue Is Empty, De-Queue Failed." << endl;
            return 0;
        } else if (front == rear) {
            int dequeued = front->data;

            front = nullptr;
            front = rear = nullptr;         // Reset Queue
            
            return dequeued;
        } else {
            int dequeued = front->data;

            Node* holdFront = front;
            front = front->next;
            delete holdFront;

            return dequeued;               // Save dequeued items' data (Optional)
        }
    }

/*  ------------------------------------------------------  */

    void empty() {while (!isEmpty()) deQueue();}

};

//! ---------- Arrays As Queues --------------------------------------------------------------------------------  !\\

#define maxSize 5 /* 1000 */     // const int maxSize = 5; 

class ArrayQueue {
private:
    int array[maxSize];
    int front, rear;

public:
    ArrayQueue() : front(-1), rear(-1) {}

/*  ------------------------------------------------------------------------------------------------------------  */

    bool isEmpty() {return front == -1;}

/*  ------------------------------------------------------  */

    bool isFull() {return rear == maxSize - 1;}

/*  ------------------------------------------------------  */

    bool doesExist(int item) {
        if (isEmpty()) return false;

        for (int i = front; i <= rear; ++i) {
            if (array[i] == item) return true;
        }

        return false;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void display() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items to display)";
            return;
        } else {
            for (int i = front; i <= rear; ++i)
                cout << array[i] << " ";
        }

        cout << endl;
    }

/*  ------------------------------------------------------  */

    int getSize() {
        if (isEmpty()) return 0;
        return rear - front + 1;
    }

/*  ------------------------------------------------------  */

    int getFront() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items in the front)" << endl;
            return -999;
        }

        return array[front];
    }

/*  ------------------------------------------------------  */

    int getRear() {
        if (isEmpty()) {
            cerr << "Queue is empty. (No items in the rear)" << endl;
            return -999;
        }

        return array[rear];
    }

/*  ------------------------------------------------------  */

    int getOrder(int item) {
        if (isEmpty()) return 0;

        int reachOrder = 1;
        for (int i = front; i <= rear; ++i) {
            if (array[i] == item) return reachOrder;
            reachOrder++;
        }

        return 0;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void enQueue(int item) {
        if (rear == maxSize - 1) {
            cerr << "Queue overflow, En-Queue Failed." << endl;
            return;
        }

        if (isEmpty()) front = 0;

        array[++rear] = item;
    }

/*  ------------------------------------------------------  */

    int deQueue() {
        if (isEmpty()) {
            cerr << "Queue is empty, De-Queue Failed." << endl;
            return 0;
        } else {
            int dequeued = array[front];

            if (front == rear) front = rear = -1; // Reset Queue (Was Only 1 Item)
            else front++;

            return dequeued;
        }
    }

/*  ------------------------------------------------------  */

    void empty() {while (!isEmpty()) deQueue();}

};

//! ---------- Main --------------------------------------------------------------------------------------------  !\\

    // Class_Name Object_Name;               Declaration
    // Object_Name.Function(Parameters);     Usage . . .

int main() {

/*  ------------------------------------------------------------------------------------------------------------  */

    Queue userQueue; // Change To ArrayQueue

    Section::Start("Display Empty Queue");

    if (userQueue.isEmpty())
        cout << "Queue Is Empty.";
    else
        cout << "Queue Is Not Empty.";

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Create User Queue");

    int userKeys;
    for (int i = 1; i <= 7; i++) {
        cout << "Enter Queue Element (" << i << "/7): ";
        cin >> userKeys;
        cout << endl;
        userQueue.enQueue(userKeys);
        cout << "Current Queue : ";
        userQueue.display();
        cout << endl;
    }

    Section::End(75, -1, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("User Final Queue");

    cout << "Final Queue : ";
    userQueue.display();

    cout << "\nQueue Current Front : " << userQueue.getFront() << endl;
    cout << "\nQueue Current Rear  : " << userQueue.getRear()  << endl;
    cout << "\nQueue Current Size  : " << userQueue.getSize();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    // Section::Start("Array isFull Queue");

    // if (userQueue.isFull())
    //     cout << "Queue Is Full." << endl;
    // else
    //     cout << "Queue Is Not Full." << endl;

    // Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Dequeue Front Key");

    cout << "Queue Update (Dequeue) : ";
    userQueue.deQueue();
    userQueue.display();

    Section::Start("Dequeue 3 More Keys");

    cout << "Queue Update (Dequeue x3) : ";
    userQueue.deQueue();
    userQueue.deQueue();
    userQueue.deQueue();
    userQueue.display();

    Section::End(75, 0, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Enqueue New Key");

    cout << "Enter Enqueue Key : ";
    cin >> userKeys;
    userQueue.enQueue(userKeys);

    cout << endl << "Queue Update (Enqueue) : ";
    userQueue.display();

    Section::End(75, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Current Queue");

    cout << "Queue Current Front : " << userQueue.getFront() << endl;
    cout << "\nQueue Current Rear  : " << userQueue.getRear()  << endl;
    cout << "\nQueue Current Size  : " << userQueue.getSize();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Search Some Keys (Try Existing & Not Existing Keys)");

    for (int i = 1; i <= 3; i++) {
        cout << "Enter Search Key : ";
        cin >> userKeys;
        if (userQueue.doesExist(userKeys)) {
            cout << "Given Key (" << userKeys << ") Is In The Queue At Order " << userQueue.getOrder(userKeys) << endl << endl;
        } else {
            cout << "Given Key (" << userKeys << ") Is Not In The Queue." << endl << endl;
        }
    }

    Section::End(75, -1);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Clear (Empty) Queue ");
    userQueue.empty();

    cout << "Queue After Deletion:" << endl;
    userQueue.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    return 0;
}