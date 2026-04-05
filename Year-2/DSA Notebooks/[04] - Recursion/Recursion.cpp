//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures and Algorithms        ╭─╮              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮│╰───────────────────────────────────────────────╮
//* │           R  e  c  u  r  s  i  o  n           ╰─╯                                               │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯


#include <iostream>
using namespace std;

/* --------------------------------------------------------------------------------------------------------

* Recursive functions are functions that work by calling themselves, creating a cascade of calls that break
* down the problem into smaller, identical versions of the main problem, until a base case is reached,
* leading to the final answer. 

* Recursion provides elegant solutions to seemingly complex problems by breaking them down into smaller
* instances of the same problem, either directly or indirectly calling itself.

* With each recursive call, a new activation record is created on the function call stack, this record
* stores variables and the return address, effectively keeping track of the various stages
* of the problem-solving process.

* ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
* │                                   R   e   c   u   r   s   i   o   n                                   │
* │───────────────────────────────────────────────────────────────────────────────────────────────────────│
* │                                                                                                       │
* │     ╭──────────────────────────────────────────────────────────────────────────────────  [Return 120] │
* │ - [5!] = 5 * [4!] <╮                                                                     [Return  24] │
* │              ╰> [4!] = 4 * [3!] <╮                                                       [Return   6] │
* │                            ╰> [3!] = 3 * [2!] <╮                                         [Return   2] │
* │                                          ╰> [2!] = 2 * [1!]     <╮                       [Return   1] │
* │                                                        ╰> [1!] = 1                                    │
* │                                                                                                       │
* │─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ─── ───│
* │                                                                                                       │
* │          │                                               │          │                                 │
* │     ╭────│> int factorial(1) {                           │          │                                 │
* │     │    │      if (1 || 0) {                            │          │                                 │
* │     │    │          return 1;                           >│╮         │                                 │
* │     │    │      }                                        ││         │                                 │
* │     │    │  }                                            ││         │                                 │
* │     │    │                                               ││         │                                 │
* │     │    │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──││         │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
* │     │    │                                               ││         │                                 │
* │     │ ╭──│> int factorial(2) {                           ││         │                                 │
* │     │ │  │      if (1 || 0) {                            ││         │                                 │
* │     │ │  │          return 1;                            ││         │                                 │
* │     │ │  │      } else {                                 ││         │                                 │
* │     ╰────│<         return 2 * factorial(1);            <│╯         │                                 │
* │       │  │  }                                           >│──╮       │                                 │
* │       │  │                                               │  │       │                                 │
* │       │  │── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│  │       │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
* │       │  │                                               │  │       │                                 │
* │       │ ╭│> int factorial(3) {                           │  │       │                                 │
* │       │ ││      if (1 || 0) {                            │  │       │                                 │
* │       │ ││          return 1;                            │  │       │                                 │
* │       │ ││      } else {                                 │  │       │                                 │
* │       ╰──│<         return 3 * factorial(2);            <│──╯       │                                 │
* │         ││  }                                           >│────╮     │                                 │
* │         ││                                               │    │     │                                 │
* │         ││── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──│    │     │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
* │         ││                                               │    │     │                                 │
* │         ││  int main() {                                 │    │     │ `main()` : Calling Function     │
* │         ││      . . .                                    │    │     │                                 │
* │         ╰│<     cout << factorial(3);                   <│────╯     │ `factorial()` : Called Function │
* │          │      . . .                                    │          │                                 │
* │          │      return 0;                                │          │                                 │
* │          │  }                                            │          │                                 │
* │          │                                               │          │                                 │
* │          └───────────────────────────────────────────────┘          │                                 │
* │                                                                     │                                 │
* └───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---------- COMPONENTS -------------------------------------------------------------------------------------

* - 0. Error Case (Optional): Ensure that the given data conforms to the function's recursive requirements,
*       preventing it from diverging from the sequential path to the base case.

* - 1. Base Case: Representing the most straightforward version of the problem solvable directly, without
*      additional recursion. It serves as the exit point from the nesting recursion chain.

* - 2. Recursive Case: In these states, the problem is deconstructed into smaller instances, and the
*      function calls itself with these reduced inputs. Analogously, it resembles opening the nesting
*      recursion to unveil another one.

---------- COMMON USES ------------------------------------------------------------------------------------

* - 1. Tree traversals (And similar self-referential structures):
*      - Pre-Order, In-Order, and Post-Order.

* - 2. Factorial Calculation:
*      - Multiplying positive integers down to 1.

* - 3. Fibonacci Sequence Generation:
*      - Representing each positive integers by the sum of the two preceding ones.

* - 4. Sorting Algorithms (e.g. Merge and Quick Sort):
*      - Generally, Recursion is employed in a "Divide and Conquer" approach for sorting lists, aiming to
*        achieve correct order through a systematic process of breaking down and solving smaller sub-lists.

---------- ITERATION VS RECURSION -------------------------------------------------------------------------

* Iterative solutions are often preferred over recursive solutions when iteration is possible,
* as the use of explicit loops eliminates the need for additional stack space, leading to more
* efficient memory usage and both both time and space complexity.

* Especially for those algorithms which are based on iterative strategies or dynamic programming,
* are more naturally expressed using loops rather than recursion.

* Recursive calls consume additional stack space for each function call. In the case of large
* datasets, or if the recursion goes too deep, it can lead to a stack overflow.

* Recursion has its merits and is suitable for certain problems, iterative solutions are generally
* prefered in cases where the iterative approach provides better performance, readability, and
* control over the resources usage.

---------- RECURSION NOTES --------------------------------------------------------------------------------

* To finite the recursion process, ensure that the base case is reachable, to prevent the function from
* calling itself infinitely and causing a stack overflow and program crash errors.

* This example underscores the necessity of defining a strong base case to prevent program crashes and
* avoid stack overflow. Without a proper base case, the program may encounter issues.

*/
int Bad_Recursive_Factorial(int n) { // Stop-Recursion Condition is Weak or Missing.
    if (n == 0 || n == 1) {                                            //! Incorrect Base Case
        return 1;
    } else {                                                                //? Recursive Case
        return n * Bad_Recursive_Factorial(n - 1);
    }
}
/*

* When the input integer is negative, the base case will never be met, as it is typically defined for
* non-negative integers, and negative integers do not have a valid factorial definition.
* Consequently, the recursive function will continue applying the factorial operation indefinitely, 
* leading to an infinite recursion as it descends into negative values.

-------------------------------------------------------------------------------------------------------- */

// Fibonacci Function: F(n) = F(n - 1) + F(n - 2)

unsigned long long Recursive_Fibonacci(int n) {
    if (n < 0) {                                                                //! Error Case
        cerr << "Error: Fibonacci is undefined for negative numbers.\n";
        return 0;
    } else if (n == 0 || n == 1) {                                               //! Base Case
        return n;
    } else {                                                                //? Recursive Case
        return Recursive_Fibonacci(n - 1) + Recursive_Fibonacci(n - 2);
    }
}

/* ---------------------------------------------- */

unsigned long long Iterative_Fibonacci(int n) {
    if (n < 0) {
        cerr << "Error: Fibonacci is undefined for negative numbers.\n";
        return 0;
    } else if (n == 0 || n == 1) {
        return n;
    } else {
        unsigned long long Fibonacci, Minus_1 = 1, Minus_2 = 0;

        for (int i = n; i > 1; i--) {
            Fibonacci = Minus_1 + Minus_2;
            Minus_2 = Minus_1;
            Minus_1 = Fibonacci;
        }

        return Fibonacci;
    }
}

/* ------------------------------------------------------------------------------------------- */

// Factorial Function: F(n) = n * (n - 1) * (n - 2) * ... * 2 * 1

unsigned long long Recursive_Factorial(int n) {
    if (n < 0) {                                                                //! Error Case
        cerr << "Error: Factorial is undefined for negative numbers.\n";
        return 0;
    } else if (n == 0 || n == 1) {                                               //! Base Case
        return 1;
    } else {                                                                //? Recursive Case
        return static_cast <unsigned long long> (n) * Recursive_Factorial(n - 1);
    }
}

/* ---------------------------------------------- */

unsigned long long Iterative_Factorial(int n) {
    if (n < 0) {
        cerr << "Error: Factorial is undefined for negative numbers.\n";
        return 0;
    } else {
        unsigned long long Factorial = 1;
        while (n > 1) {
            Factorial *= static_cast<unsigned long long>(n);
            n--;
        }

        return Factorial;
    }
}

/* ----------------------------------------------------------------------------------------------

* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │       n       │   0   │    1    │    2    │    3    │    4    │    5    │    6    │    7    │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │   Fibonacci   │   0   │    1    │    1    │    2    │    3    │    5    │    8    │    13   │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │   Factorial   │   1   │    1    │    2    │    6    │    24   │   120   │   720   │   5040  │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘
* ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
* │       n       │        8        │         9         │        10         │         11        │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │   Fibonacci   │        21       │         34        │        55         │         89        │
* │─────────────────────────────────────────────────────────────────────────────────────────────│
* │   Factorial   │      40320      │       362880      │      3628800      │      39916800     │
* └─────────────────────────────────────────────────────────────────────────────────────────────┘

---------------------------------------------------------------------------------------------- */

int main() {

    cout << "Enter a number: ";
    int n; cin >> n;

    cout << "Factorial of [" << n << "] is [" << Recursive_Factorial(n) << "] - Using Recursive Function.\n";
    cout << "Factorial of [" << n << "] is [" << Iterative_Factorial(n) << "] - Using Iterative Function.\n";
    cout << "Fibonacci of [" << n << "] is [" << Recursive_Fibonacci(n) << "] - Using Recursive Function.\n";
    cout << "Fibonacci of [" << n << "] is [" << Iterative_Fibonacci(n) << "] - Using Iterative Function.\n";


    //! Error Warning
    // cout << "Factorial of [-1] is [" << Recursive_Factorial(-1) << "] - Using Recursive Function.\n";

    //! Stack OverFlow Warning
    // cout << "Factorial of [-1] is [" << Bad_Recursive_Factorial(-1) << "] - Using . . . Whatever.\n";

    return 0;
}