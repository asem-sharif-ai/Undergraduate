//* ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │   Data Structures And Algorithms   │       Author: Asem Al-Sharif       │     Topic: Hash And Hash Table     │
//* ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
using namespace std;

/*  ----------------------------------------------------------------------------------------------------------------

* For the given array[]:                                                 Try to get 'CX' . .
*                ┌──────────────────────────────────────────────────────────────────────────┐
*                │ MR │ OT │ KP │ GT │ CX │ BY │ JQ │ NS │ DW │ EU │ AZ │ LQ │ HS │ FV │ IR │
*                └──────────────────────────────────────────────────────────────────────────┘
*       [index] =  00   01   02   03   04   05   06   07   06   09   10   11   12   13   14

* Finding the desired value, 'CX', necessitates iterating through all values in the array using a comparison loop.
* This sequential search is the only approach to pinpoint the specific value within the given array.

* However, what if, somehow, there could be a relationship between the index and the stored data? This is what
* 'Hashing' is.

* In simpler terms, hashing is calling a function that creates a connection between the data and its storage
* location, making it easier to find and retrieve, as the data itself serves as a reference for the index.

----------------------------------------------------------------------------------------------------------------

* Hashing is a process of converting any given input data into a fixed-size string of numerical values as an output.

* The primary objective of hashing is to expedite access within extensive collections and databases. 
*   - By utilizing hash functions, which initiate a relation between data and indices, the process of retrieving
*     specific values becomes much faster. This acceleration is crucial for optimizing the efficiency of operations
*     in cases of dealing with large datasets and extensive databases.

* Hashing process consists of:
*    1. Hash Input:
*       Any type of data used as an input to a hashing function (Usually a (Key, Value) pair).

*    2. Hash Output (Hash Code / Value):
*       Fixed-size string of numerical values (or characters) serves as a unique identifier for the input data.

*    3. Hash Function:
*       The critical component of the hashing process, it relies on complex mathematical formulas to transform
*       the input keys into the hash code.

*    4. Hash Table:
*       The structure that provides an associative array (or array of linked lists heads) abstraction, where data
*       values are mapped to unique indices.

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                               H   a   s   h                                               │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                                                                           │
*  │                                                 Function                                                  │
*  │            Input:                   ┌──────────────────────────────┐            Output:                   │
*  │                                     │       index = sum mod 3      │          ┌───────────────┐           │
*  │            ┌───────────┐            │ ┌──────────────────────────┐ │          │ ┌───────────┐ │           │
*  │            │ "SIMPLE " │            │ │ 83 73 77 80 76 69 32 = 1 │ │          │ │ "HASH "   │ │           │
*  │            └───────────┘            │ └──────────────────────────┘ │          │ └───────────┘ │           │
*  │            ┌───────────┐            │ ┌──────────────────────────┐ │          │ ┌───────────┐ │           │
*  │            │ "HASH "   │      ->    │ │ 72 65 83 72 32       = 0 │ │    ->    │ │ "SIMPLE " │ │           │
*  │            └───────────┘            │ └──────────────────────────┘ │          │ └───────────┘ │           │
*  │            ┌───────────┐            │ ┌──────────────────────────┐ │          │ ┌───────────┐ │           │
*  │            │ "EXAMPLE" │            │ │ 69 88 65 77 80 76 69 = 2 │ │          │ │ "EXAMPLE" │ │           │
*  │            └───────────┘            │ └──────────────────────────┘ │          │ └───────────┘ │           │
*  │                                     └──────────────────────────────┘          └───────────────┘           │
*  │                                                                                                           │
*  │                                                                                                           │
*  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│
*  │   ASCII:   │   'H'  │   'A'  │   'S'  │   'I'  │   'M'  │   'P'  │   'L'  │   'E'  │   'X'  │   'Space'   │
*  │   Codes:   │   #72  │   #65  │   #83  │   #73  │   #77  │   #80  │   #76  │   #69  │   #88  │     #32     │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------

* About Hashing Tables:

* Hash tables enable rapid data retrieval based on unique keys, providing constant-time complexity for operations
* such as: Insertion, search, and deletion.

* Commonly used as a valuable tool in enhancing database performance. As They facilitate quick lookup operations 
* based on unique identifiers (Keys), optimizing the retrieval of information from large datasets.

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                     Hash Table Operations Complexity:                                     │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                   Time Complexity:                   │                 Space Complexity:                  │
*  │                                                      │                                                    │
*  │  Insertion, Deletion, And Search:                    │  Hash Table Size:                                  │
*  │  Best And Average Case: Constant (O(1)).             │  For an Average Well-Designed Hash Table:  (O(n))  │
*  │   ..  But the collisions may degrade it to O(n).     │                                                    │
*  │                                                      │                                                    │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------

* About Hashing Functions (Algorithms):

* The simplest description of the hashing algorithms is:
*   - Calculations applied to a key value to transform it into an address, which represents its position in the
*     hash table.

* The good hash function ensures the uniform distribution of keys across the hash space, minimizing the
* probability of collisions. This uniform distribution is required for efficient retrieval.

* For numeric keys, devide the key value by the number of available addresses (Table Size), and consider the
* reminder:                         [ key_address = key_value mod table_size ]

* For the non-numeric keys, devide the sum of ASCII codes in the key instead of the value, and consider the
* reminder:                      [ key_address = sum(ASCII_Code) mod table_size ]

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                     Uniqueness                     V.S                     Collisions                     │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                     │                                                     │
*  │                                                     │  If, somehow, the hash function generated the same  │
*  │  Every and each key must have a unique, exclusive   │  hash code as an index for different inputs.        │
*  │  relationship with its corresponding index,         │                                                     │
*  │  represented by a unique hash code.                 │   ┌────────────────────────┐                        │
*  │                                                     │   │ -- │ i. │ -- │    │    │    (X, Y, Z) -> [i]    │
*  │                                                     │   └────────────────────────┘                        │
*  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│                                                     │
*  │                                                     │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│
*  │  A crucial attribute in the hash functions is its   │                                                     │
*  │  sensitivity to input changes.                      │ 1. Solve By Open Addressing:                        │
*  │                                                     │   ┌────────────────────────┐                        │
*  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│   │ -- │ X. │ -- │ Y. │ Z. │    (Linear Probing)    │
*  │                                                     │   └────────────────────────┘                        │
*  │  That even a minor alteration in the input data     │  Linear Search is used to find Y & Z, Start = [i]   │
*  │  should generate a markedly different hash code.    │                                                     │
*  │                                                     │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│
*  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│                                                     │
*  │                                                     │ 2. Solve By Closed Addressing (Chaining):           │
*  │                                                     │   ┌────────────────────────┐                        │
*  │                                                     │   │ -- │ X. │ -- │    │    │     (Linked Lists)     │
*  │  This property is known as Avalanche Effect:        │   └───── ▼ ────────────────┘                        │
*  │                                                     │        ┌─ ──┐                                       │
*  │  - Ensuring that a minor alteration in the input    │        │ Y. │  Standerd Traverse is used to find    │
*  │    leads to a significant and unpredictable change  │        └ ▼ ─┘  Y & Z, Start = [i]                   │
*  │    in the output hash code.                         │        ┌─ ──┐                                       │
*  │                                                     │        │ Z. │                                       │
*  │                                                     │        └────┘                                       │
*  │                                                     │                                                     │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

* Collision Resolution by Open Addressing:
*    1. Linear Probing:
*       When a collision occurs, the algorithm searches for the next available (empty) slot in a linear fashion
*       (sequentially) until an empty slot is found. (may cause primary clustering)

*    2. Quadratic Probing:
*       Uses a quadratic function to determine the next probe position by changing the collision hash function.

*    3. Double Hashing:
*       Does a secondary hash function to calculate the step size for probing. It provides a more diverse probing
*       sequence, as well as reducing clustering.

* Collision Resolution by Closed Addressing (Chaining):
*    - Each index in the hash table will be considered as a bucket, to contain a head and pointer to a linked list.
*      Values that were hashed to the same address are stored sequentially as nodes in this linked list.

---------------------------------------------------------------------------------------------------------------- */

//! ---------- Structure Class ------------------------------------------------------------------------------  !\\

class Key {
public:
    string key;
    int value;
    Key* next;

    Key(const string& k, int v) : key(k), value(v), next(nullptr) {}
};

class LinkedList {
public:
    Key* head;

    LinkedList() : head(nullptr) {}

/*  ---------------------------------------------------------------------------------------------------------  */

    void insert(const string& key, int value) { // Chaining
        Key* newNode = new Key(key, value);

        if (head == nullptr) {
            head = newNode;
        } else {
            Key* traverse = head;
            while (traverse->next != nullptr) traverse = traverse->next;
            traverse->next = newNode;
        }
    }

/*  ----------------------------------------------------  */

    void insert_L(const string& key, int value) { // Linear Probing (Not working well)
        Key* newNode = new Key(key, value);
        newNode->next = head;
        head = newNode;
    }

/*  ---------------------------------------------------------------------------------------------------------  */

};

//! ---------- Hash Table Class -----------------------------------------------------------------------------  !\\

class HashTable {
private:
    int size;
    LinkedList* table;

public:
    HashTable(int size) : size(size) {
        table = new LinkedList[size];
    }

    ~HashTable() {
        delete[] table;
    }

/*  ---------------------------------------------------------------------------------------------------------  */

    void display() {
        for (int i = 0; i < size; ++i) {
            cout << "[" << i << "] : ";
            Key* current = table[i].head;
            while (current != nullptr) {
                cout << "(" << current->key << ", " << current->value << ") ";
                current = current->next;
            }
            cout << endl;
        }
    }

/*  ---------------------------------------------------------------------------------------------------------  */

    int hash(const string& key) {
        int ASCII = 0;
        for (char c : key) ASCII += static_cast<int>(c);

        return ASCII % size; // Hash Code
    }

/*  ---------------------------------------------------------------------------------------------------------  */

    void insert(const string& key, int value) { // Chaining
        int index = hash(key);
        table[index].insert(key, value);
    }

/*  ----------------------------------------------------  */

    void insert_L(const string& key, int value) { // Linear Probing
        int index = hash(key);

        if (table[index].head == nullptr) {
            table[index].insert_L(key, value);
        } else {
            int mainIndex = index;
            
            do { index = (index + 1) % size;
            } while (index != mainIndex && table[index].head != nullptr);

            if (index != mainIndex) {
                table[index].insert_L(key, value);
            } else {
                cerr << "Hash Overflow. Insertion Failed." << endl;
            }
        }
    }

/*  ---------------------------------------------------------------------------------------------------------  */

};

//! ---------- Main -----------------------------------------------------------------------------------------  !\\

int main() {

    HashTable ChainingTable(3), LinearTable(5);

    ChainingTable.insert("SIMPLE ", 1);
    ChainingTable.insert("HASH ", 1);
    ChainingTable.insert("EXAMPLE", 1);
    ChainingTable.insert("HASH ", 2);
    ChainingTable.insert("EXAMPLE", 2);
    ChainingTable.insert("HASH ", 3);

    cout << "Chaining Table:" << endl;
    ChainingTable.display();

    cout  << endl << "---------------------------------------" << endl << endl;

    // cout << "Get value of key (\"EXAMPLE\") from Chaining Table: " << ChainingTable.get("EXAMPLE") << endl;

    // cout << "Chaining Table after removal (\"HASH\"):" << endl;
    // ChainingTable.remove("HASH");
    // ChainingTable.display();

    cout  << endl << "-------------------------------------------------------------------------------" << endl << endl;

    LinearTable.insert_L("SIMPLE ", 1);     // 490 mod 5 = 0 [0]
    LinearTable.insert_L("HASH ", 1);       // 324 mod 5 = 4 [4]
    LinearTable.insert_L("EXAMPLE", 1);     // 524 mod 5 = 4 [1]   //? Circular 
    LinearTable.insert_L("HASH ", 2);       // 324 mod 5 = 4 [2]
    LinearTable.insert_L("EXAMPLE", 2);     // 524 mod 5 = 4 [3]

    cout << "Linear Table:" << endl;
    LinearTable.display();

    LinearTable.insert_L("EXAMPLE", 3);     // 524 mod 5 = 4 [5]   //! Hash OverFlow

    cout  << endl << "---------------------------------------" << endl << endl;

    // cout << "Get value of key (\"EXAMPLE\") from Linear Table: " << LinearTable.get("EXAMPLE") << endl;

    // cout << "Linear Table after removal:" << endl;
    // LinearTable.remove("HASH");
    // LinearTable.display();

    cout  << endl << "-------------------------------------------------------------------------------" << endl << endl;

    return 0;
}