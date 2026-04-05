//* ╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │   Data Structures And Algorithms   │       Author: Asem Al-Sharif       │     Topic: Binary Search Trees     │
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

* Trees are hierarchical data structures, consist of nodes (items) representing data, commencing at the root, and
* interconnected through pointers, serving as edges.

* The nodes (items) in the trees are considered as:
*     1. Root: The most top node, with no preceding edges (No parents), serves as the start for traversing the tree.
*     2. Leaf: The last node in the branch, with no outgoing edges (No children).
*     3. Internal Node: Neither a root nor a leaf.

* Trees Main Concepts And Characteristics:
*     01. Node: Block that stores data and holds a reference (pointer) to either other nodes or null.
*     02. Edge: Represents a relationship between the parent (preceding) and child (following) nodes.

*     03. Parent: A node that has one or more child nodes.
*     04. Child: A node that has a parent node (further, than the parent, to the root).
*     05. Siblings: Children nodes with the same parent.

*     06. Subtree: A portion of a tree (including nodes and edges) that forms a tree itself.

*     07. Depth:  The level or distance of a node from the root (Root is at depth 0, ++).
*     09. Height: The length of the longest path from a node to a leaf (max(∀ levels)).

*     10. Binary Tree: A tree in which each node has at most two children, referred to as Left and Right Child.
*     11. Binary Search Tree (BST): A binary tree, when: (Left_Child < Childs_Parent < Right_Chlid)

*     12. Balanced Tree: A tree in which the heights of the two child subtrees of any node differ by at most one.

----------------------------------------------------------------------------------------------------------------

* About The Binary Trees:
* 1. The tree must have only one root.
* 2. Each node can not have more than one parent.
* 3. Each node must either be a leaf (with 0 children) or a parent with 1 or 2 children.

----------------------------------------------------------------------------------------------------------------

* About The Binary Search Trees (BSTs):
* 1. The left  child must be smaller than the root node.
* 2. The right child must be greater than or equal to the root node.
* 3. Each node value must be unique.

* Unlike a heap, which is a complete binary tree with specific ordering properties, a Binary Search Tree can take
* any shape as long as it maintains the binary search property.

* Binary Search Trees excel in insertion and deletion operations, due to their structural efficiency, since each
* node maintains: A. Left  subtree with values smaller than itself.
*                 B. Right subtree with values greater than itself.

* The structure optimizes the search process by minimizing the search space through strategic comparisons,
* ensuring precise alignment for the desired operation.

----------------------------------------------------------------------------------------------------------------

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                             T   r   e   e   s                                             │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                   │                                   │                                   │
*  │ Binary Tree:                      │ Binary Search Tree:               │ Binary Unbalanced Tree:           │
*  │                                   │                                   │                                   │
*  │                 [10]              │                 [40]              │                 [20]              │
*  │               /      \            │               /      \            │               /      \            │
*  │           [20]        [30]        │           [25]        [65]        │           [10]        [30]        │
*  │          /    \      /    \       │          /    \      /    \       │          /    \                   │
*  │        [40]  [50]  [60]  [70]     │        [15]  [35]  [55]  [75]     │        [05]  [15]                 │
*  │      /    \                       │       /    \                      │      /    \                       │
*  │    [80]  [90]                     │     [10]  [20]                    │    [03]  [07]                     │
*  │                                   │                                   │                                   │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │  Level  │                                                                                                 │
*  │         │                                          ┌──────────┐                                           │
*  │    0    │                                          │  Node A  │                                           │
*  │         │                                          └──────────┘                                           │
*  │         │                                       /                \                                        │
*  │         │                            ┌──────────┐                 ┌──────────┐                            │
*  │    1    │                            │  Node B  │                 │  Node C  │                            │
*  │         │                            └──────────┘                 └──────────┘                            │
*  │         │                            /          \                 /          \                            │
*  │         │                     ┌──────────┐ ┌──────────┐    ┌──────────┐ ┌──────────┐                      │
*  │    2    │                     │  Node D  │ │  Node E  │    │  Node F  │ │  Node G  │                      │
*  │         │                     └──────────┘ └──────────┘    └──────────┘ └──────────┘                      │
*  │         │                     /          \                                         \                      │
*  │         │              ┌──────────┐ ┌──────────┐                              ┌──────────┐                │
*  │    3    │              │  Node H  │ │  Node I  │                              │  Node J  │                │
*  │         │              └──────────┘ └──────────┘                              └──────────┘                │
*  │  4 : 7  │                  ....                                                                           │
*  │         │              ┌──────────┐                                                                       │
*  │    8    │              │  Node O  │                                                                       │
*  │         │              └──────────┘                                                                       │
*  │         │                                                                                                 │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │           ┌─────────┐ │          ┌──────────┐      │              ┌──────────┐ ┌──────────┐ ┌──────────┐  │
*  │ 1. Nodes: │  A : O  │ │ 3. Root: │  Node A  │      │  5. Parents: │ B (D, E) │ │ C (F, G) │ │ D (H, I) │  │
*  │           └─────────┘ │          └──────────┘      │              └──────────┘ └──────────┘ └──────────┘  │
*  │                       │          ┌───────────────┐ │                                                      │
*  │ 2. Edges: ['/' & '\'] │ 4. Leaf: │ E, F, I, J, O │ │  Note (5.): (D, E) e.g. are siblings children.       │
*  │                       │          └───────────────┘ │                                                      │
*  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│
*  │                                    │                 ┌───────────────────┐   │                            │
*  │ 6. Sub-Tree:   \                   │   7. Intervals: │ B, C, D, G, [H:N] │   │   8. Depth or Height = 8   │
*  │                 ┌──────────┐       │                 └───────────────────┘   │                            │
*  │                 │  Node C  │       │ ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── │
*  │                 └──────────┘       │                                                                      │
*  │                 /          \       │ 9. Longest Path: [A -> B -> D -> H -> J -> K -> L -> M -> N -> O]    │
*  │          ┌──────────┐ ┌──────────┐ │                                                                      │
*  │          │  Node F  │ │  Node G  │ │ 10. Tree Is Binary. (Nodes Have Either 0, 1, or 2 children)          │
*  │          └──────────┘ └──────────┘ │ 11. Tree Is Not Balanced. (s.t. Leaves Level: [2 (F, G)], [9 (O)])   │
*  │                            ..      │                                                                      │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                      Binary Search Trees Traversals:                                      │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │   Pre  Order   │   Root -> Left -> Right   │  A.  B.  D.  H.  K.  L.  M.  N.  O.  I.  E.  C.  F.  G.  J.  │
*  │────────────────│───────────────────────────│──────────────────────────────────────────────────────────────│
*  │   In   Order   │   Left -> Root -> Right   │  O.  N.  M.  L.  K.  H.  D.  I.  B.  E.  A.  F.  C.  J.  G.  │
*  │────────────────│───────────────────────────│──────────────────────────────────────────────────────────────│
*  │   Post Order   │   Left -> Right -> Root   │  O.  N.  M.  L.  K.  H.  I.  D.  E.  B.  F.  J.  G.  C.  A.  │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------

* Recursion:
* Recursion is a powerful and efficient mathematical technique involves that defines a problem in relation to
* itself.

* Recursive functions leverage this concept by breaking down a complex problem into a series of simpler
* instances of the same problem, then each recursive call handles a smaller portion of the main problem
* until reaching a base case. At the point the recursion stops, the overall problem is solved by combining the
* results.

--------------------------------------------------------

* Recursion is applied in tree traversal applications, as the natural structure of trees lends itself to
* recursive solutions.

*  ┌───────────────────────────────────┐
*  │        [  R   o   o   t  ]        │
*  │                 |                 │
*  │ Max = Root - 1  | Min = Root + 1  │
*  │                 |                 │
*  │── ── ── ── ── ──|── ── ── ── ── ──|
*  │   [ R o o t ]   |   [ R o o t ]   │ -> Each subtree with a designated root is treated as
*  │        |        |        |        │    an independent tree in its own right.
*  │ X= R-1 | N= R+1 | X= R-1 | N= R+1 │
*  │        |        |        |        │
*  │── ── ── ── ── ──|── ── ── ── ── ──|
*  │    |   |   |    |    |   |   |    │ -> And as on . . . This is why recursion is used in BSTs.
*  └───────────────────────────────────┘

* The recursive functions handle subtrees, for operations such as:
*    - 1. Insertion:
*         Recursive insertion starts from the root, compares the value to be inserted with the current node,
*         and recursively inserts in the left or right subtree until an appropriate position is found.

*    - 2. Deletion:
*         Involves locating the node to delete, which can be a leaf node or a node with one or two children.
*         Subsequently, the correct value is chosen to replace it in place.

*    - 3. Search:
*         Involves comparing the target value with the current node's (root) value, and conducting a recursive
*         search in the left or right subtree based on the outcome of the comparison.

---------------------------------------------------------------------------------------------------------------

*  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────────┐
*  │                                       Linked Lists As Binary Trees:                                       │
*  │───────────────────────────────────────────────────────────────────────────────────────────────────────────│
*  │                                                  [ ▼ Root ]                                               │
*  │                                          ┌─────────────────────┐                                          │
*  │                            ┌─────────────│ Left │ Data │ Right │─────────────┐                            │
*  │                            │             └─────────────────────┘             │                            │
*  │                            ▼                                                 ▼                            │
*  │                 ┌─────────────────────┐                           ┌─────────────────────┐                 │
*  │                 │ Left │ Data │ Right │                           │ Left │ Data │ Right │                 │
*  │                 └─────────────────────┘                           └─────────────────────┘                 │
*  │                 ┌──┘               └──┐                           ┌──┘               └──┐                 │
*  │                 ▼                     ▼                           ▼                     ▼                 │
*  │     ┌─────────────────────┐ ┌─────────────────────┐   ┌─────────────────────┐ ┌─────────────────────┐     │
*  │     │ Left │ Data │ Right │ │ Left │ Data │ Right │   │ NULL │ Data │ Right │ │ NULL │ Data │ NULL* │     │
*  │     └─────────────────────┘ └─────────────────────┘   └─────────────────────┘ └─────────────────────┘     │
*  │       ┌─┘           ┌─┘         └─┐           └─┐                       │                                 │
*  │       ▼             ▼             ▼             ▼                       ▼                                 │
*  │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           ┌───────────┐                           │
*  │ │ N │ D │ N │ │ N │ D │ N │ │ N │ D │ N │ │ N │ D │ N │           │ N │ D │ N │                           │
*  │ └───────────┘ └───────────┘ └───────────┘ └───────────┘           └───────────┘                           │
*  │                                                                                                           │
*  └───────────────────────────────────────────────────────────────────────────────────────────────────────────┘

----------------------------------------------------------------------------------------------------------------  */

class Node {
public:
    int data;
    Node* left;
    Node* right;

    Node(int item) : data(item), left(nullptr), right(nullptr) {}
};

/*  ------------------------------------------------------------------------------------------------------------  */

class BinarySearchTree {
private:
    Node* root;

public:
    BinarySearchTree() : root(nullptr) {}

    Node* getRoot() {return root;}

    /*  ------------------------------------------------------  */

    Node* getMin(Node* root) {
        if (root == nullptr) return nullptr;

        while (root->left != nullptr) {
            root = root->left;
        }

        return root;
    }

    /*  ------------------------------------------------------  */

    Node* getMax(Node* root) {
        if (root == nullptr) return nullptr;

        while (root->right != nullptr) {
            root = root->right;
        }

        return root;
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    int getDepth(Node* root) {
        if (root == nullptr) {
            return -1;
        }

        int leftDepth = getDepth(root->left);
        int rightDepth = getDepth(root->right);

        return max(leftDepth, rightDepth) + 1;
    }

/*  ------------------------------------------------------  */

    int getDepth() {
        return getDepth(root);
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    int getLevel(Node* root, int item, int level = 0) {
        if (root == nullptr) {
            return -1;
        }

        if (root->data == item) {
            return level;

        } else if (item < root->data) {
            return getLevel(root->left, item, level + 1);

        } else if (item > root->data) {
            return getLevel(root->right, item, level + 1);

        }
    }

/*  ------------------------------------------------------  */

    int getLevel(int key) {
        return getLevel(root, key);
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    Node* RecursiveInsert(Node* root, int item) {
        if (root == nullptr) {
            Node* newNode = new Node(item);
            return newNode;
        } else if (item < root->data) {
            root->left = RecursiveInsert(root->left, item);
        } else if (item > root->data) {
            root->right = RecursiveInsert(root->right, item);
        }

        return root;
    }

/*  ------------------------------------------------------  */

    void Insert(int item) {
        root = RecursiveInsert(root, item);
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    Node* RecursiveDelete(Node* root, int item) {
        if (root == nullptr) {
            return nullptr;
        } else if (item < root->data) {
            root->left = RecursiveDelete(root->left, item);
        } else if (item > root->data) {
            root->right = RecursiveDelete(root->right, item);
        } else {

            if (root->left == nullptr) {
                Node* temp = root->right;
                delete root;
                return temp;

            } else if (root->right == nullptr) {
                Node* temp = root->left;
                delete root;
                return temp;

            } else {
                Node* maxLeft = getMax(root->left);
                root->data = maxLeft->data;
                root->left = RecursiveDelete(root->left, maxLeft->data);
            }
        }

        return root;
    }

/*  ------------------------------------------------------  */

    void Delete(int item) {
        root = RecursiveDelete(root, item);
    }

/*  ------------------------------------------------------------------------------------------------------------  */
    
    Node* RecursiveSearch(Node* root, int item) {
        if (root == nullptr) return nullptr;

        if (root->data == item) {
            return root;
        } else if (root->data > item) {
            return RecursiveSearch(root->left, item);
        } else {
            return RecursiveSearch(root->right, item);
        }
    }

/*  ------------------------------------------------------  */

    bool Search(int item) {
        Node* result = RecursiveSearch(root, item);

        return (result != nullptr);
    }

/*  ------------------------------------------------------------------------------------------------------------  */

    void preOrder(Node* root) { // Root -> Left -> Right
        if (root == nullptr) {
        return;
        }

        cout << root->data << " ";
        preOrder(root->left);
        preOrder(root->right);
    }

/*  ------------------------------------------------------  */

    void inOrder(Node* root) { // Left -> Root -> Right
        if (root == nullptr) {
        return;
        }

        inOrder(root->left);
        cout << root->data << " ";
        inOrder(root->right);
    }

/*  ------------------------------------------------------  */

    void postOrder(Node* root) { // Left -> Right -> Root
        if (root == nullptr) {
        return;
        }

        postOrder(root->left);
        postOrder(root->right);
        cout << root->data << " ";
    }

/*  ------------------------------------------------------------------------------------------------------------  */

};

int main() {

/*  ------------------------------------------------------------------------------------------------------------  */

    BinarySearchTree tree1, tree2;

    int array1[] = {50, 25, 10, 5, 15, 40, 75, 60, 55, 90, 100};
    for (int element : array1) tree1.Insert(element);

    /*
     *          50         
     *         /  \        
     *       25    75      
     *      / \    / \     
     *     10 40  60  90   
     *    / \     /    \   
     *   5  15   55    100 
     */

    /* ----- LTR ---------------
     * int array2[] = {30, 45, 50, 60, 70, 40, 35, 33, 15, 20, 10, 5};
     * for (int element : array2) tree2.Insert(element);
     *
     *          30          
     *         /  \         
     *       15    45       
     *      / \    / \      
     *     10 20  40  50    
     *    /           / \   
     *   5           35  60 
     *              /     \ 
     *             33     70
     * ------------------------- */

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Display The Tree");

    cout << "[Pre-Order]:  ";
    tree1.preOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "[In-Order]:   ";
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "[Post-Order]: ";
    tree1.postOrder(tree1.getRoot());

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Get Nodes' Level & Tree Depth");

    cout << "Node [50] is at Level: " << tree1.getLevel(50) << endl;
    cout << "Node [75] is at Level: " << tree1.getLevel(75) << endl;
    cout << "Node [10] is at Level: " << tree1.getLevel(15) << endl;
    cout << "Node [11] is at Level: " << tree1.getLevel(11) << endl << endl;

    cout << "Tree Depth: " << tree1.getDepth();

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Search In Tree");

    if (tree1.Search(50)) 
        cout << "Node [50] is in the tree at level " << tree1.getLevel(50) << endl << endl;
    else 
        cout << "Node [50] is not in the tree." << endl << endl;

    if (tree1.Search(5)) 
        cout << "Node [5]  is in the tree at level " << tree1.getLevel(5) << endl << endl;
    else 
        cout << "Node [5]  is not in the tree." << endl << endl;

    if (tree1.Search(30)) 
        cout << "Node [30] is in the tree at level " << tree1.getLevel(30) << endl << endl;
    else 
        cout << "Node [30] is not in the tree." << endl;

    Section::End(75, 0);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Delete Nodes");

    cout << "Tree [In-Order]:          ";
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "Deleting [15] [In-Order]: ";
    tree1.Delete(15);
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "Deleting [90] [In-Order]: ";
    tree1.Delete(90);
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "Deleting [80] [In-Order]: ";
    tree1.Delete(80);
    tree1.inOrder(tree1.getRoot());
    
    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    Section::Start("Insert Nodes");

    cout << "Inserting [45]  [In-Order]: ";
    tree1.Insert(45);
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "Inserting [0]   [In-Order]: ";
    tree1.Insert(0);
    tree1.inOrder(tree1.getRoot());
    cout << endl << endl;

    cout << "Inserting [200] [In-Order]: ";
    tree1.Insert(200);
    tree1.inOrder(tree1.getRoot());

    Section::End(75);

/*  ------------------------------------------------------------------------------------------------------------  */

    return 0;
}