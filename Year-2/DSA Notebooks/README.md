# Data Structures & Algorithms - Year 2

> Part of [`ai-undergraduate`](https://github.com/asemsharif/ai-undergraduate) · Faculty of Artificial Intelligence, Menoufia University
>
> A full semester of DSA implemented in C++ - every file contains working code, inline explanations, and ASCII memory/structure diagrams drawn directly in the source.

---

## Structure

| # | Topic | Files |
|---|-------|-------|
| 01 | [Static Arrays](#01--static-arrays) | 1 |
| 02 | [Dynamic Arrays](#02--dynamic-arrays) | 1 |
| 03 | [Multidimensional Arrays](#03--multidimensional-arrays) | 1 |
| 04 | [Arrays - Applications & Problem Solving](#04--arrays--applications--problem-solving) | 1 |
| 05 | [Array Class](#05--array-class) | 1 |
| 02 | [Pointer & Reference](#02--pointer--reference) | 1 |
| 03 | [Structure & Union](#03--structure--union) | 1 |
| 04 | [Recursion](#04--recursion) | 1 |
| 05 | [Insertion & Deletion](#05--insertion--deletion) | 3 |
| 01 | [Search - Part 1 (Linear)](#01--search-part-1--linear) | 6 |
| 02 | [Search - Part 2 (Binary & Beyond)](#02--search-part-2--binary--beyond) | 5 |
| 03 | [Sorting](#03--sorting) | 8 |
| 07 | [Linked Lists](#07--linked-lists) | 1 |
| 08 | [Stacks](#08--stacks) | 1 |
| 09 | [Queues](#09--queues) | 1 |
| 10 | [Trees](#10--trees) | 1 |
| 14 | [Hash Tables](#14--hash-tables) | 1 |

---

## 01 · Static Arrays

### `Static_Arrays.cpp`
The foundation. Covers how arrays map to contiguous memory blocks, index-to-address arithmetic, and the cost model of random access vs insertion vs deletion.

**Concepts:** memory layout, base address + offset formula, cache locality, bounds - and why indexing is O(1) while shifting is O(n).

```
addr(i) = base + i × sizeof(element)

[0x100][0x104][0x108][0x10C]
  A[0]   A[1]   A[2]   A[3]
```

---

## 02 · Dynamic Arrays

### `DynamicArray.cpp`
Manual implementation of a resizable array - the mechanism behind `std::vector`. Covers heap allocation, growth strategy (doubling), and amortized O(1) push.

**Concepts:** `new[]` / `delete[]`, capacity vs size, realloc + copy, amortized analysis, iterator invalidation on resize.

---

## 03 · Multidimensional Arrays

### `Multidimensional_Arrays.cpp`
2D and 3D arrays - both stack-allocated and heap-allocated (pointer-to-pointer). Includes row-major vs column-major layout and how that affects cache performance.

**Concepts:** row-major storage, `arr[i][j]` → `base + (i×cols + j) × size`, jagged arrays, pointer arithmetic for 2D heap arrays.

---

## 04 · Arrays - Applications & Problem Solving

### `Arrays_Applications.cpp`
Practical problems built on top of arrays: sliding window, prefix sums, two-pointer, frequency counting. Bridges raw array knowledge into algorithm design.

**Concepts:** sliding window O(n), prefix sum arrays, two-pointer technique, in-place transformations.

### `Arrays_Functions.cpp`
Arrays passed to functions - decay to pointers, passing size explicitly, returning heap arrays, `const` correctness.

**Concepts:** array-to-pointer decay, `sizeof` gotcha inside functions, pass-by-pointer vs pass-by-reference for arrays.

---

## 05 · Array Class

### `Array_Class.cpp`
Wraps a raw array in a C++ class with operator overloading, bounds checking, copy semantics (Rule of Three), and iterator support.

**Concepts:** `operator[]` with bounds check, copy constructor, copy assignment, destructor, `const` member functions, range-for compatibility.

---

## 02 · Pointer & Reference

### `Pointer_Reference.cpp`
Deep dive into pointers and references - the machinery that makes everything else in C++ possible. Covers raw pointer arithmetic, `const` qualifiers, references as aliases, and `nullptr`.

**Concepts:** pointer arithmetic, `*` / `&` operators, `const T*` vs `T* const`, double pointers, references vs pointers, function pointers, pointer-to-member.

```
int x = 42;
int* p = &x;

  p        *p
[0x200] → [42]   at address 0x200
```

---

## 03 · Structure & Union

### `Structure_Union.cpp`
Side-by-side study of `struct` and `union` - memory layout, field alignment, and the tagged-union pattern. Includes ASCII byte diagrams and live corruption examples.

**Concepts:** struct padding & alignment, `sizeof` rules, union overlapping fields (size = max field), tagged union pattern, type punning, `std::variant<>` as the modern alternative.

```
struct → each field owns its address
[grade][  age  ][    score    ]   ← sum of fields

union  → all fields share address 0
[         int         ]
[  short  ]
[ char ]                          ← size = largest field
```

---

## 04 · Recursion

### `Recursion.cpp`
Recursion from first principles - the call stack visualised, base cases, tail vs non-tail forms, and memoization. Classic problems: factorial, Fibonacci, tower of Hanoi, binary search recursive form.

**Concepts:** call stack frames, base case / recursive case, tree of calls, stack overflow risk, tail call, memoization with arrays, divide-and-conquer intuition.

```
factorial(4)
  └─ 4 × factorial(3)
         └─ 3 × factorial(2)
                └─ 2 × factorial(1)
                       └─ 1  ← base case, unwinds back up
```

---

## 05 · Insertion & Deletion

### `UnSortedInsertion.cpp`
Insert into an unsorted array - front, back, and arbitrary position. Covers element shifting and the true cost of maintaining order during insert.

**Concepts:** O(1) append, O(n) insertion at position, shifting direction (right-to-left to avoid overwrite).

### `SortedInsertion.cpp`
Maintain sorted order on every insert - binary search to find position, shift, place. The building block for insertion sort and sorted-array-backed sets.

**Concepts:** binary search for insertion point, in-place shift, maintaining invariant across operations.

### `Deletion.cpp`
Remove by value and by index from both sorted and unsorted arrays. Compares the shift-and-shrink approach vs swap-with-last (O(1) delete for unsorted).

**Concepts:** swap-with-last O(1) trick for unsorted delete, O(n) shift for sorted delete, handling duplicates, shrinking logical size.

---

## 01 · Search - Part 1: Linear

### `LinearSearch.cpp`
The baseline. Scans every element until found or exhausted. O(n) worst case - the unavoidable cost when data is unsorted.

**Concepts:** sequential scan, early exit, worst/average/best case, unsorted data requirement.

### `SentinelSearch.cpp`
Optimises linear search by placing a sentinel (the target) at the end of the array, eliminating the bounds check inside the loop - one comparison per iteration instead of two.

**Concepts:** sentinel value trick, loop invariant, branch reduction, cache-friendly loop.

### `Linear_VS_Sentineal.cpp`
Head-to-head benchmark and analysis - standard linear vs sentinel. Measures the real-world impact of removing one comparison per iteration across large arrays.

### `SelfOrganizingSearch.cpp`
Adaptive search: every successful find moves the element closer to the front. Exploits temporal locality - frequently accessed elements migrate to O(1) reach over time.

**Concepts:** move-to-front heuristic, transpose heuristic, frequency ordering, amortised analysis.

### `RecursiveLinearSearch.cpp`
Recursive formulation of linear search - base cases for empty array and found, recursive step. Demonstrates how iteration maps to tail recursion.

**Concepts:** recursive base/step, stack depth O(n), tail-recursive form.

### `LinearSearch_Applications.cpp`
Real problems that reduce to linear search: finding min/max, counting occurrences, searching in 2D arrays, first/last occurrence.

---

## 02 · Search - Part 2: Binary & Beyond

### `BinarySearch.cpp`
The classic O(log n) search on sorted arrays. Covers iterative form, the midpoint overflow fix (`lo + (hi - lo) / 2`), and equal-range variants (first / last occurrence).

**Concepts:** sorted precondition, halving search space, O(log n) proof, integer overflow in midpoint, lower\_bound / upper\_bound variants.

```
target = 23, array = [5, 11, 17, 23, 38, 44, 62]
              lo=0          mid=3          hi=6
                    arr[3]=23 → found at index 3
```

### `RecursiveBinarySearch.cpp`
Binary search expressed recursively - same logic, explicit call stack instead of a loop. Includes analysis of why iteration is preferred (no stack overhead).

### `TernarySearch.cpp`
Divides the search space into three parts instead of two. O(log₃ n) comparisons but more comparisons per step - often slower than binary in practice.

**Concepts:** two midpoints, three-way split, comparison count analysis, unimodal function search application.

### `Binary_VS_Ternary.cpp`
Direct comparison - binary vs ternary search. Analyses total comparisons, cache behaviour, and the counter-intuitive result that ternary is rarely faster.

### `RotatedBinarySearch.cpp`
Binary search on a sorted array that has been rotated at an unknown pivot - the classic interview problem. Identifies the sorted half at each step.

**Concepts:** rotation detection, which half is sorted, O(log n) still achievable, finding the pivot.

### `InterpolationSearch.cpp`
Beats binary search on uniformly distributed data by estimating position proportionally rather than always splitting in half. O(log log n) average, O(n) worst.

**Concepts:** probe formula `lo + (target - arr[lo]) × (hi - lo) / (arr[hi] - arr[lo])`, uniform distribution assumption, degradation on skewed data.

### `JumpSearch.cpp`
Jump forward in blocks of √n, then linear search backward. A middle ground - better than linear, no sorted-random-access requirement of binary.

**Concepts:** block size √n, forward jump + backward scan, O(√n) complexity, suitability for sequential storage (tape, disk).

### `AccessSearch.cpp`
Access patterns and their costs - sequential, random, sorted vs unsorted. Ties search algorithm choice to data structure and storage characteristics.

---

## 03 · Sorting

### `BubbleSort.cpp`
The entry point. Repeatedly swaps adjacent out-of-order elements. Includes the early-exit optimisation (already sorted → O(n)). O(n²) worst/average.

**Concepts:** adjacent swap, passes, stability, early-exit flag, O(n) best case.

### `SelectionSort.cpp`
Finds the minimum of the unsorted portion and places it. Minimises swaps (exactly n−1) - useful when swap is expensive. Unstable, always O(n²).

**Concepts:** selection, in-place, minimum swaps, instability, comparison vs swap cost.

### `InsertionSort.cpp`
Builds the sorted array one element at a time by inserting each into its correct position. O(n) on nearly sorted data - the best simple sort for small or nearly sorted inputs.

**Concepts:** shifting vs swapping, online algorithm, stability, adaptive (O(n) best), shell sort as extension.

### `MergeSort.cpp`
Divide, conquer, merge. Guaranteed O(n log n) always. Stable. Requires O(n) extra space - the classic tradeoff for predictable performance.

**Concepts:** divide and conquer, merge step, stability, O(n) auxiliary space, external sort application.

```
[38, 27, 43, 3]
 ├─ [38, 27] → [27, 38]
 └─ [43,  3] → [ 3, 43]
 merge → [3, 27, 38, 43]
```

### `QuickSort.cpp`
Partition around a pivot, recurse on both halves. O(n log n) average, O(n²) worst (avoided with good pivot choice). In-place, cache-friendly - the fastest sort in practice.

**Concepts:** partition (Lomuto / Hoare), pivot selection (median-of-three, random), worst case, tail recursion optimisation, introsort.

### `HeapSort.cpp`
Build a max-heap, repeatedly extract the maximum. O(n log n) always, O(1) auxiliary space. Slower than quicksort in practice due to poor cache behaviour.

**Concepts:** heapify, sift-down, in-place heap, O(n) build-heap proof, cache miss analysis.

### `CountSort.cpp`
Non-comparison sort for integer keys in a known range. O(n + k) - linear when k = O(n). The basis for radix sort.

**Concepts:** frequency array, prefix sum for stability, O(n + k) time and space, range limitation.

### `RadixSort.cpp`
Sort integers digit by digit using counting sort as a stable subroutine. O(d × n) - effectively O(n) for fixed-width integers.

**Concepts:** LSD vs MSD radix, stable sort requirement, digit extraction, O(n) for fixed-width keys.

---

## 07 · Linked Lists

### `LinkedList.cpp`
Full implementation of singly and doubly linked lists from scratch - node allocation, insert/delete at head/tail/position, reversal, cycle detection (Floyd's algorithm), and merge of two sorted lists.

**Concepts:** node + pointer structure, O(1) insert at head, O(n) traversal cost, sentinel/dummy nodes, slow/fast pointer for cycle detection, memory ownership.

```
head
 │
[data|next] → [data|next] → [data|next] → nullptr
```

---

## 08 · Stacks

### `Stack.cpp`
Stack implemented over both array and linked list. Covers push/pop/peek with overflow/underflow handling, and applications: balanced parentheses, infix→postfix conversion, function call simulation.

**Concepts:** LIFO discipline, O(1) push/pop, call stack analogy, postfix evaluation, monotonic stack pattern.

---

## 09 · Queues

### `Queue.cpp`
Queue over circular array and linked list. Covers standard queue, deque, and priority queue. Applications: BFS skeleton, task scheduling, sliding window maximum.

**Concepts:** FIFO discipline, circular buffer (head/tail mod capacity), O(1) enqueue/dequeue, deque operations, priority queue via heap.

---

## 10 · Trees

### `Tree.cpp`
Binary search tree from scratch - insert, search, delete (all three cases), traversals (in/pre/post/level-order), height, and balance check. Includes AVL rotation intuition.

**Concepts:** BST invariant, recursive insert/search, three delete cases (leaf, one child, two children), in-order = sorted output, tree height, balance factor, AVL rotations.

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

---

## 14 · Hash Tables

### `Hash.cpp`
Hash table with separate chaining and open addressing (linear probing, quadratic probing, double hashing). Covers load factor, rehashing, and collision analysis.

**Concepts:** hash function design, collision resolution, load factor α, rehashing trigger, O(1) average insert/search/delete, worst case O(n) with bad hash, universal hashing idea.

```
key → hash(key) % capacity → bucket index

bucket[0] → [k1|v1] → [k5|v5] → null   (chaining)
bucket[1] → [k2|v2] → null
bucket[2] → null
bucket[3] → [k3|v3] → [k7|v7] → null
```

---

## Notes

- Every file is self-contained - compile any single `.cpp` with `g++ file.cpp -o out && ./out`.
- ASCII memory/structure diagrams are embedded in the source as comments, not external assets.
- Complexity annotations (time + space) are included inline with each algorithm.
- Files are ordered to follow the teaching progression - each topic builds on the previous.