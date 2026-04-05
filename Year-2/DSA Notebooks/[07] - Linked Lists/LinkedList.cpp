//* ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │   Data Structures And Algorithms   │       Author: Asem Al-Sharif       │         Topic: Linked List         │
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

* Linked Lists are linear data structures consisting of a sequence of elements, cosidering each element points to
* the next element in the sequence.

* Unlike arrays, linked lists do not require contiguous memory locations for their elements. Each element, known as
* a Node, contains two fields: [A. Data] and [B. Reference] (Links to the next node in the sequence).

* Unlike dynamic arrays either, linked lists are more efficient in inserting and deleting elements, as changeSize 
* function is not needed on each time an element is inserted or deleted in the list. Also it stems from the ability
* to modify the 'Next' pointer, contrasting with the array's need for shifting elements.

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                                H   E   A   P                                              │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │  [▼ Head]                                                                                                 │
*  │   │  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐      │
*  │   └──   Data  │ Pointer ->       Data  │ Pointer ->       Data  │ Pointer ->       Data  │ Nullptr │      │
*  │      └──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘      │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

* The Nodes (Data) in the linked list are considered as:
*     1. Head:
*        The Starting node of any linked list, serves as the entry for accessing the other nodes in the list.
*     2. Tail:
*        The last node in the linked list points to a null reference, indicating the end of the list. 
*     3. Node:
*        Each element in the linked list, it contains the current node data and next node reference.

* About The Head:
* - It's a pointer that holds the memory address (location) of the first node in the list sequence.
* - By following the pointers starting from the head, you can traverse through the entire linked list.

----------------------------------------------------------------------------------------------------------------

* Traverse:

* Traverse through the linked list is the one and only way to loop through it. It is a nessirey method for many
* functions and operations, such as: display(), getSize(), doesExist(), search(), getData(), getOrder(), and ..

* How To Traverse Through Linked Lists ? 
* - 1. Define Traverse Counter ('traverse' or 'current') And Copy The Head Pointer.
* - 2. Start (Loop) From The Head Until Counter.Next = Nullptr (Represents the end of the list).
*      - Change The Condition If There Is No Need To Reach The End Of The List.
* - 3. Do Whatever You Have Traversed For. (e.g. Display Current.Data, Count Nodes, Compare Value (For Search))
* - 4. Update / Move The Traverse Counter Forward (By: Counter = Counter.Next).

! - Do NOT traverse by the real head of the linked list, once it is updated, all the previous nodes are lost.

--------------------------------------------------------

* Order & reachOrder :

* - In general, Linked Lists nodes are typically devoid of indices are not indexed, so there is common practice
*   when there is a requisite to manage nodes in order, for functions such as: in-place insertion and deletion
*   or getOrder(data) or getData(order). By defining one or two counters representing the increcement with each
*   new traverse: 
*       1. Order: Assumes the role of signifying the positional significance of a targset node within the list.
*       2. reachOrder: Metric for the traversal steps or path undertaken from the head to the desired node.

----------------------------------------------------------------------------------------------------------------

* Linked Lists Types:

* Normal / Singly Linked List:
*           ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
*     Head -> Data │ Next ->    Data │ Next ->    Data │ Next ->    Data │ Next ->    Data │ NULL │
*           └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
* Each node points to the next node in the sequence.


* Circular Linked List: 
*           ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
*  ┌─ Head -> Data │ Next ->    Data │ Next ->    Data │ Next ->    Data │ Next ->    Data │ Next -> ─┐
*  │        └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   │
*  └──────────────────────────────────────────────────────────────────────────────────────────────────┘
* The last node (Tail) points back to the first node (Head), forming a loop.


* Doubly Linked List:
*                  ┌────────────────────┐ -> ┌────────────────────┐ -> ┌────────────────────┐
*                  │ Head │ Data │ Next        Pre. │ Data │ Next        Pre. │ Data │ NULL │
*                  └────────────────────┘ <- └────────────────────┘ <- └────────────────────┘
* Each node points to both (Next, Previous) nodes in sequence, allowing for traversal in both directions.

----------------------------------------------------------------------------------------------------------------

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                      Arrays                         V.S                    Linked Lists                   │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │ 1. Arrays (Usually) has a fixed size.                │ 1. Linked Lists has flexible size.                 │
*  │                                                      │                                                    │
*  │ 2. Elements require contiguous block of memory caus- │ 2. Nodes do not require contiguous locations and   │
*  │    -ing wastage in case of the size is larger than   │    memory is dynamically allocated, which makes it │
*  │    needed.                                           │    more memory-efficient.                          │
*  │                                                      │                                                    │
*  │ 3. Constant time O(1) to access elements (Indices).  │ 3. Linear time O(n) to access nodes (Traverse).    │
*  │                                                      │                                                    │
*  │ 4. Suitable for random accessing, displaying, mathe- │ 4. Better for insertion, deletion, and other oper- │
*  │    -matical and matrix operations.                   │    -ations.                                        │
*  │                                                      │                                                    │
*  │ 5. Inefficient for insertions and deletions, espec-  │ 5. Efficient for insertions and deletions, as it   │
*  │    -ially in the middle, as these operations require │    involves changing pointers without shifting any │
*  │    to shift some elements.                           │    elements.                                       │
*  │                                                      │                                                    │
*  │ 6. Simple implementation.                            │ 6. Complex implementation.                         │
*  │                                                      │                                                    │
*  │              [ Contiguous Locations ]                │            [ Not Contiguous Locations ]            │
*  │          ┌─────────────────────────────┐             │    ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐     │
*  │          │  V  │  V  │  V  │  V  │  V  │             │    │ D.P │  │ D.P │  │ D.P │  │ D.P │  │ D.P │     │
*  │          └─────────────────────────────┘             │    └─────┘  └─────┘  └─────┘  └─────┘  └─────┘     │
*  │        i=   0     1     2     3     4                │       -        -        -        -        -        │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

* Note (2): 
* Even though the linked lists are memory-efficient data structures, each node requires additional memory cost 
* (Compared with array elements) due to the storage requirements of the 'Next' pointer.

----------------------------------------------------------------------------------------------------------------  */

struct Node {
    int data;
    Node* next;
};

class LinkedList {
private:
    Node* head;
    Node* tail;

public:
    LinkedList() : head(nullptr) {}

/*  ------------------------------------------------------------------------------------------------------------  */

    bool isEmpty() {return head == nullptr;}

    /*
      If the head points to nothing, The list is empty (true).
    */

/*  ------------------------------------------------------  */

    bool doesExist(int data) {
        if (isEmpty()) return false;

        Node* traverse = head;
        while (traverse != nullptr) {
            if (traverse->data == data) return true;
            traverse = traverse->next;
        }

        return false;
        }

    /*
      A. If list is empty, Nothing exists.
      B. Else, Traverse and compare equality between (Current.Data & Search Key).
         B1. If Found, Return true.   //! (End)
         B2. Else, Continue traversing.

      C. If Traverse has ended, Was not broken by true state, Return false.
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    void display() {
        if (isEmpty()) {
            cerr << "List Is Empty." ;
            return;
        } else {
            Node* traverse = head;

            while (traverse != nullptr) {
                cout << traverse->data << " ";
                traverse = traverse->next;
            }
        }
    }

    /*
      A. If list is empty, tell so.
      B. Else, Traverse and display Current.data.
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    void reverse() {
        Node* traverse = head;
        Node* preNode = nullptr;
        Node* nextNode = nullptr;

        while (traverse != nullptr) {
            nextNode = traverse->next;
            traverse->next = preNode;
            preNode = traverse;
            traverse = nextNode;
        }

        head = preNode;
    }

    /*
      A. Initialize current, previous, and next nodes pointers.
      B. Else, Traverse and while sill in list range:
         B1. Save the next to avoid losing the rest of the list.
         B2. Make the current.next point to the previous (Reverse the pointers directions).
         B3. Move to the next node in the original order.

      C. Update the head to point to the new head (When the traversal is ended).
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    void empty() {
        Node* traverse = head;
        while (traverse != nullptr) {
            Node* lastTraverse = traverse;
            traverse = traverse->next;
            delete lastTraverse;
        }

        head = nullptr;
        cout << "Linked List Has Been Successfully Deleted." << endl;
    }

    /*
      A. If list is empty, tell so.
      B. Else, Traverse and while sill in list range:
         B1. Create a pointer to hold the current node.
         B2. Move forward to the next node.
         B3. Delete that previous node.

      C. Update the head to nullptr (When the traversal is ended).

      *  A pointer is set to hold the last node because if the current is the one to delete, all remaining nodes
      *  is unaccessible.
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    int getSize() {
        Node* traverse = head;

        int size = 0;
        while (traverse != nullptr) {
            size++;
            traverse = traverse->next;
        }
        return size;
    }

    /*
      A. Set Size counter = 0.
      B. Traverse and increase Size counter (+1 per traverse).
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    int getHead() { return head->data; }
    
    /*
      A. Return head.data if exists.
      B. Return -999 if list is empty (as an error).
    */

/*  ------------------------------------------------------  */

    int getTail() {
        if (isEmpty()) return -999;

        Node* traverse = head;

        while (traverse->next != nullptr)
            traverse = traverse->next;

        return traverse->data;
    }

    /*
      A. Traverse until pre-last node and return its data.
      B. Return -999 if list is empty (as an error).
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    int MinMax(int choice) {
        if (isEmpty()) return -999;

        Node* traverse = head;
        int min = traverse->data;
        int max = traverse->data;

        while (traverse != nullptr) {
            if (traverse->data < min) min = traverse->data;
            if (traverse->data > max) max = traverse->data;

            traverse = traverse->next;
        }

        if (choice == 1) return min;
        if (choice == 2) return max;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    int getOrder(int data) {
    Node* traverse = head;
    int reachOrder = 1;

    while (traverse != nullptr) {
        if (traverse->data == data) return reachOrder;
        traverse = traverse->next;
        reachOrder++;
    }
    
    return -1;
    }

    /*
      A. Set Increasing Order counter = 1.
      B. Traverse and compare equallities between (Current.Data & Search Key)
         B1. If Found, Return current Increasing Order counter.   //! (End)
         B2. Else, Increase the counter and continue traversing

      C. If Traverse has ended, And key is not found, return -1 (as an error).
    */

/*  ------------------------------------------------------  */

    int getData(int order) {
        if (order < 1 || order > getSize()) return -999;

        Node* traverse = head;
        int reachOrder = 1;

        while (traverse != nullptr && reachOrder <= order) {
            if (reachOrder == order) return traverse->data;
            traverse = traverse->next;
            reachOrder++;
        }

        return -999;
    }

    /*
      A. If Order is out of bounds, return -999 (as error)
      B. Else, Set Increasing Order counter, Traverse and compare between (Increasing Order & Given Order)
         B1. Once the counters are equal, Return current node data
         B2. Until that, Increase the counter and continue traversing

      C. By default, Return -999.
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    void insertStart(int data) {
        Node* newNode = new Node();
        newNode->data = data;

        if (isEmpty()) newNode->next = nullptr;
        else           newNode->next = head;
        
        head = newNode;
    }

    /*
      A. Create a new node and fill its data with the key value
         B1. If the list is empty, next should be nullptr
         B2. If not, next should be the old head of the list

      C. Update the head to point to the new node
    */

/*  ------------------------------------------------------  */

    void insertEnd(int data) {

        Node* newNode = new Node();
        newNode->data = data;
        newNode->next = nullptr;

        if (isEmpty()) {
            head = newNode;
        } else {
            Node* traverse = head;
            while (traverse->next != nullptr)
                traverse = traverse->next;

            traverse->next = newNode;
        }
    }

    /*
      A. Create a new node and fill its data with the key value and next pointer with nullptr (intended to set as tail)
         B1. If the list is empty, head should point to the one and only node
         B2. If not, Traverse until the last node, then change its next pointer from nullptr to the new node
    */

/*  ------------------------------------------------------  */

    void insertAt(int data, int order) {
        Node* newNode = new Node();
        if (newNode == nullptr) {
            cerr << "Memory Allocation Failed." << endl;
            return;
        }

        newNode->data = data;

        if (order < 1 || order > getSize()) {
            cerr << "Invalid Order (Out of Bounds)." << endl;
            delete newNode;
            return;
        } else if (order == 1 || isEmpty()) {
            insertStart(data);
            return;
        } else if (order == getSize() + 1) {
            insertEnd(data);
            return;
        } else {
            Node* traverse = head;
            int reachOrder = 1;

            while (traverse != nullptr && reachOrder < order - 1) {
                traverse = traverse->next;
                reachOrder++;
            }

            newNode->next = traverse->next;
            traverse->next = newNode;
        }
    }
    
    /*
      A. Advanced operation to insert at specific order, keep an eye on the Increasing Order counter and it will guide you.
    */

/*  ------------------------------------------------------  */
    
    void insertBefore(int existingData, int newData) {

        if (isEmpty()) {
            cerr << "List Is Empty." << endl;
            return;
        } else if (!doesExist(existingData)) {
            cerr << "Data Does Not Exist." << endl;
            return;
        }

        Node* newNode = new Node();
        newNode->data = newData;
        Node* traverse = head;

        while (traverse->next != nullptr && traverse->next->data != existingData)
            traverse = traverse->next;

        newNode->next = traverse->next;
        traverse->next = newNode;
    }

    /*
      A. Traverse until being in correct position, insert, modify the pointers.
    */

/*  ------------------------------------------------------  */

    void insertAfter(int existingData, int newData) {

        if (isEmpty()) {
            cerr << "List Is Empty." << endl;
            return;
        } else if (!doesExist(existingData)) {
            cerr << "Data Does Not Exist." << endl;
            return;
        }

        Node* newNode = new Node();
        newNode->data = newData;
        Node* traverse = head;

        while (traverse != nullptr && traverse->data != existingData)
            traverse = traverse->next;

        newNode->next = traverse->next;
        traverse->next = newNode;
    }

    /*
      A. You can take the wheel from now on . . . <3
    */

/*  ------------------------------------------------------------------------------------------------------------  */

    void deleteStart() {
        if (isEmpty()) {
            cerr << "List Is Empty, Deletion Failed." << endl;
            return;
        }

        Node* holdHead = head;
        head = head->next;
        delete holdHead;
    }

/*  ------------------------------------------------------  */

    void deleteEnd() {
        if (isEmpty()) {
            cerr << "List Is Empty, Deletion Failed." << endl;
            return;
        } else if (getSize() == 1) {
            deleteStart();
            return;
        }

        Node* traverse = head;
        Node* pre_Traverse = nullptr;

        while (traverse->next != nullptr) {
            pre_Traverse = traverse;
            traverse = traverse->next;
        }

        delete traverse;
        pre_Traverse->next = nullptr;
    }

/*  ------------------------------------------------------  */

    void deleteAt(int order) {
        if (isEmpty()) {
            cerr << "List Is Empty, Deletion Failed." << endl;
            return;
        } else if (order < 1 || order > getSize()) {
            cerr << "Invalid Order, Deletion Failed." << endl;
            return;
        } else if (order == 1) {
            deleteStart();
            return;
        } else if (order == getSize()) {
            deleteEnd();
            return;
        }

        Node* traverse = head;
        Node* pre_Traverse = nullptr;
        int reachOrder = 1;

        while (traverse != nullptr && reachOrder < order) {
            pre_Traverse = traverse;
            traverse = traverse->next;
            reachOrder++;
        }

        if (traverse != nullptr) {
            pre_Traverse->next = traverse->next;
            delete traverse;
        }
    }

/*  ------------------------------------------------------  */

    void deleteNode(int data) {
        if (head == nullptr) {
            cerr << "List is empty. Deletion Failed." << endl;
            return;
        }

        Node* traverse = head;
        Node* pre_Traverse = nullptr;

        while (traverse != nullptr && traverse->data != data) {
            pre_Traverse = traverse;
            traverse = traverse->next;
        }

        if (traverse == nullptr) {
            cerr << "Node (" << data << ") is not found. Deletion Failed." << endl;
            return;
        }

        if (pre_Traverse == nullptr) head = traverse->next;
        else                         pre_Traverse->next = traverse->next;

        delete traverse;
        // cout << "Node (" << data << ") has been deleted successfully." << endl;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void mergeWith(LinkedList* list_2) {
        if (list_2 == nullptr || list_2->head == nullptr) return;   // Something is wrong

        if (head == nullptr) {
            head = list_2->head;
            tail = list_2->tail;
        } else {
            Node* traverse_1 = head;
            while (traverse_1->next != nullptr) {
                traverse_1 = traverse_1->next;
            }

            traverse_1->next = list_2->head;

            tail = list_2->tail;
        }

        list_2->head = nullptr;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void merge(Node* &head, Node* left, Node* right) {
        Node* dummy = new Node{0, nullptr};
        Node* current = dummy;

        while (left != nullptr && right != nullptr) {
            if (left->data < right->data) {
                current->next = left;
                left = left->next;
            } else {
                current->next = right;
                right = right->next;
            }
            current = current->next;
        }

        current->next = (left != nullptr) ? left : right;
        head = dummy->next;
        delete dummy;
    }

    void mergeSort(Node* &head) {
        if (head == nullptr || head->next == nullptr) {
            return;
        }

        Node* slow = head;
        Node* fast = head->next;

        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;
        }

        Node* left = head;
        Node* right = slow->next;
        slow->next = nullptr;

        mergeSort(left);
        mergeSort(right);
        merge(head, left, right);
    }

    void sort() {
        mergeSort(head);
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    static LinkedList convertArray(int* array, int size) {
        LinkedList arrayList;

        for (int i = 0; i < size; ++i) {
            arrayList.insertEnd(array[i]);
        }

        return arrayList;
    }

/*  ------------------------------------------------------  */

    int* convertToArray() {
        int size = getSize();
        if (size == 0) {
            cerr << "List is empty. Conversion Failed." << endl;
            return nullptr;
        }

        int* array = new int[size];
        Node* traverse = head;

        for (int i = 0; i < size; ++i) {
            array[i] = traverse->data;
            traverse = traverse->next;
        }

        return array;
    }

};

/*  ------------------------------------------------------------------------------------------------------------  */

    // Class_Name Object_Name;               Declaration
    // Object_Name.Function(Parameters);     Usage . . .

int main() {

/*  ------------------------------------------------------------------------------------------------------------  */

    LinkedList list1, list2, list3, list4;


    Section::Start("Display While Empty");

    cout << "List 1: ";
    list1.display();

    cout << "\nList 2: ";
    list2.display();

    if (list3.isEmpty()) 
        cout << "\nList 4 is empty.";

    if (list3.isEmpty()) 
        cout << "\nList 4 is empty.";

    Section::End(75);
    
/*  ------------------------------------------------------------------------------------------------------------  */

    for (int i = 10; i < 21; i++) list1.insertEnd(i);

    for (int i = 20; i < 31; i++) list2.insertEnd(i);

    for (int i = 30; i < 41; i++) list3.insertEnd(i);

    for (int i = 40; i < 51; i++) list4.insertEnd(i);

    Section::Start("Display After Insertion");

    cout << "List 1: ";
    list1.display();

    cout << "\nList 2: ";
    list2.display();

    cout << "\nList 3: ";
    list3.display();

    cout << "\nList 4: ";
    list4.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Merge Lists");

    list3.mergeWith(&list4);
    cout << "List 3 Merged With List 4: \n";
    list3.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Clear List");

    list4.empty();
    if (list4.isEmpty()) 
        cout << "List 4 is empty.";
    else 
        cout << "List 4 still has elements.";

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Search In List");

    if (list3.doesExist(15))
        cout << "15 Exists is list 3 at order (" << list3.getOrder(15) << ")." << endl;
    else 
        cout << "15 Does not exist is list 3." << endl;

    if (list3.doesExist(35))
        cout << "35 Exists is list 3 at order (" << list3.getOrder(35) << ")." << endl;
    else 
        cout << "35 Does not exist is list 3." << endl;

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Reverse List");

    list3.reverse();
    list3.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Other Functions");

    cout << "List 3 Info: " << endl <<
            "1. Head : " << list3.getHead() << endl <<
            "2. Tail : " << list3.getTail() << endl << 
            "3. Size : " << list3.getSize() << endl << 
            "4. Min  : " << list3.MinMax(1) << endl << 
            "5. Max  : " << list3.MinMax(2) << endl << 
            "6. Data at order (5) is (" << list3.getData(5) << ")" << endl <<
            "7. Order of data (33) is (" << list3.getOrder(33) << ")";

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Convert List To Array");

    int* array1 = list1.convertToArray();
    cout << "List 1 as an Array: ";
    for (int i = 0; i < list1.getSize(); ++i)
        cout << array1[i] << " ";

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Convert Array To List");
    
    int array2[] = {99, 98, 97, 96, 95, 94, 93, 92, 91, 90};
    int array2_Size = sizeof(array2) / sizeof(array2[0]);
    LinkedList list5 = LinkedList::convertArray(array2, array2_Size);

    cout << "[99'] Array As Linked List: ";
    list5.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Delete Functions");

    cout << "List 2: \n";
    list2.display();

    list2.deleteStart();
    cout << "\n\nDelete Head: \n";
    list2.display();

    list2.deleteEnd();
    cout << "\n\nDelete Tail: \n";
    list2.display();

    list2.deleteAt(5);
    cout << "\n\nDelete Data At Order = 5: \n";
    list2.display();

    list2.deleteNode(28);
    cout << "\n\nDelete Data = 28: \n";
    list2.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Insert Functions");

    cout << "Insert Head = 1: \n";
    list2.insertStart(1);
    list2.display();

    cout << "\n\nInsert Tail = 9: \n";
    list2.insertEnd(9);
    list2.display();

    cout << "\n\nInsert Node = 10 At Order = 5: \n";
    list2.insertAt(10, 5);
    list2.display();

    cout << "\n\nInsert -1 after 10: \n";
    list2.insertAfter(10, -1);
    list2.display();

    cout << "\n\nInsert -9 Before 10: \n";
    list2.insertBefore(10, -9);
    list2.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Sort List");

    list2.sort();
    list2.display();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    return 0;
}