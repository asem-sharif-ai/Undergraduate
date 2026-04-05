//* ╭─────────────────────────────────────────────────────────────────────────────────────────────────╮
//* │         Data Structures and Algorithms        ╭─╮              Author: Asem Sharif              │
//* ╰───────────────────────────────────────────────╮│╰───────────────────────────────────────────────╮
//* │           S  t  r  u  c  t  u  r  e           ╰─╯               U   n   i   o   n               │
//* ╰─────────────────────────────────────────────────────────────────────────────────────────────────╯

#include <iostream>
#include <cstring>   // memset
using namespace std;

/*

*  A struct gives EACH field its OWN separate slot in memory.
*  All fields exist simultaneously and independently.
*  Size = SUM of all fields (+ possible padding).

*  A union gives ALL fields the SAME single slot in memory.
*  Only ONE field is valid at a time, the one you wrote last.
*  Size = MAX of all fields.

* struct Person {
*      char   grade;    // 1 byte
*      short  age;      // 2 bytes
*      int    score;    // 4 bytes
*  };   // (total = 1 + 2 + 4 = 7 bytes, compiler may pad to 8):
*            ┌───────────┬─────────────┬─────────────────────┐
*            │   grade   │     age     │        score        │
*            │   char    │    short    │         int         │
*            │   1 B     │     2 B     │         4 B         │
*            └───────────┴─────────────┴─────────────────────┘
*             ↑ each field lives at its OWN address, never overlaps.
*  Writing to `grade` does NOT touch `age` or `score`.
*  Writing to `score` does NOT touch `grade` or `age`.
*  All three exist at the same time → you can read all of them freely.


*  union Data {
*      char   c;    * 1 byte
*      short  s;    * 2 bytes
*      int    i;    * 4 bytes
*  };   // (total = 4 bytes, the size of int, the largest):
*            ┌──────────────────────────────────────────────┐
*            │                    int i                     │  ← 4 bytes
*            ├────────────────────┐                         │
*            │      short s       │    (unused by short)    │  ← 2 bytes
*            ├──────────┐         │                         │
*            │  char c  │     (unused   by   char)          │  ← 1 byte
*            └──────────┴─────────┴─────────────────────────┘
*             ↑ ALL fields start at address 0 — they OVERLAP completely
*
*  Writing to `i` fills all 4 bytes.
*  Writing to `c` only changes byte 0 → bytes 1,2,3 still hold old `i` data.
*  Writing to `s` changes bytes 0 and 1 → bytes 2,3 still hold old `i` data.

*/

struct Person {
   char  grade; // 1 byte
   short age;     // 2 bytes
   int   score;   // 4 bytes
};

union Data {
   char  c;   // 1 byte
   short s;   // 2 bytes
   int   i;   // 4 bytes
};


/* 
* Tagged Union Pattern:
*  A "tagged union" (also called a discriminated union) combines:
*    • an integer TAG  → tells you WHICH field is currently valid
*    • a union PAYLOAD → holds the actual data
*
*  This is exactly what struct Object in your original code does.
*
*  ┌────────────────────────────────────────────────────────────────┐
*  │  struct TaggedValue                                            │
*  │  ┌──────────────┬────────────────────────────────────────────┐ │
*  │  │  int tag     │           union payload                    │ │
*  │  │  (4 bytes)   │  char / short / int / float / double /     │ │
*  │  │              │  long long / void*   →  all 8 bytes        │ │
*  │  └──────────────┴────────────────────────────────────────────┘ │
*  │  Total: 4 + 8 = 12 bytes (vs 8 separate variables!)            │
*  └────────────────────────────────────────────────────────────────┘
*
*  tag == 1 → read char_val
*  tag == 2 → read int_val
*  tag == 3 → read double_val
*  tag == 4 → read ptr_val
*  anything else → garbage (your bug, not the language's)
*/

struct TaggedValue {
   int tag;  // 1=char, 2=int, 3=double, 4=ptr
   union {
      char        char_val;
      int         int_val;
      double      double_val;
      void*       ptr_val;
   };
};

void printTagged(const TaggedValue& v) {
    switch (v.tag) {
        case 1: cout << "  char   → " << v.char_val   << "\n"; break;
        case 2: cout << "  int    → " << v.int_val     << "\n"; break;
        case 3: cout << "  double → " << v.double_val  << "\n"; break;
        case 4: cout << "  ptr    → " << v.ptr_val     << "\n"; break;
        default: cout << "  ??? unknown tag\n"; break;
    }
}

/*
* Union as a type punning tool:
*  Because all fields share the same bytes, you can write as one type
*  and read as another, this is called "type punning."

*  Classic trick: inspect the raw bytes of a float.

*  union FloatBits {
*      float    f;
*      uint32_t bits;   // same 4 bytes, read as unsigned int
*  };

*    Layout for f = 1.0f  (IEEE 754):
*    Bit pattern: 0 01111111 00000000000000000000000
*    Hex:         0x3F800000

*  byte[0] byte[1] byte[2] byte[3]
*  ┌──────┬──────┬──────┬──────┐
*  │ 0x00 │ 0x00 │ 0x80 │ 0x3F │   ← float stored little-endian
*  └──────┴──────┴──────┴──────┘
*    ↑ writing .f and reading .bits gives 0x3F800000

*/

union FloatBits {
   float    f;
   unsigned int bits;
};


int main() {
    // ── 1. Struct: all fields independent ────────────────────────────────────
    cout << "━━━  STRUCT  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

    Person p;
    p.grade = 'A';
    p.age   = 20;
    p.score = 95;

    cout << "  p.grade = 'A',  p.age = 20,  p.score = 95\n";
    cout << "  All written → all readable independently:\n";
    cout << "  grade = " << p.grade
         << "   age = " << p.age
         << "   score = " << p.score << "\n";
    cout << "  sizeof(Person) = " << sizeof(Person) << " bytes\n\n";

    //
    //  Because each field owns its address, none of them interfere.
    //  This is safe — you can write in any order and read freely.
    //

    // ── 2. Union: shared memory, only last write is valid ────────────────────
    cout << "━━━  UNION  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

    Data d;
    d.i = 1000;
    cout << "  d.i = 1000\n";
    cout << "  → d.i = " << d.i
         << "   d.s = " << d.s
         << "   d.c = " << (int)d.c << "\n";

    //  Memory right now (little-endian):
    //  byte[0]=0xE8  byte[1]=0x03  byte[2]=0x00  byte[3]=0x00

    d.c = 'A';   // 'A' = 0x41 — overwrites byte 0 only!
    cout << "\n  d.c = 'A'  (0x41) — byte 0 overwritten!\n";
    cout << "  → d.i = " << d.i
         << "   (was 1000, now byte 0 is 0x41 = 65 → "
         << "0x41 + 0x03<<8 = " << d.i << ")\n";

    //  Memory now:
    //  byte[0]=0x41  byte[1]=0x03  byte[2]=0x00  byte[3]=0x00
    //  Reading d.i gives: 0x00000341 = 833  ← not 1000!

    cout << "  sizeof(Data) = " << sizeof(Data) << " bytes\n\n";


    // ── 3. Tagged union: the safe pattern ────────────────────────────────────
    cout << "━━━  TAGGED UNION  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

    TaggedValue v1, v2, v3;

    v1.tag = 1;  v1.char_val   = 'Z';
    v2.tag = 2;  v2.int_val    = 42000;
    v3.tag = 3;  v3.double_val = 3.14159;

    cout << "  v1 (tag=1, char):   "; printTagged(v1);
    cout << "  v2 (tag=2, int):    "; printTagged(v2);
    cout << "  v3 (tag=3, double): "; printTagged(v3);
    cout << "  sizeof(TaggedValue) = " << sizeof(TaggedValue) << " bytes\n\n";

    //  The tag is the contract. If you set tag=2 but read char_val,
    //  you're breaking the contract — undefined behavior territory.


    // ── 4. Type punning: inspect float bits ──────────────────────────────────
    cout << "━━━  TYPE PUNNING  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

    FloatBits fb;
    fb.f = 1.0f;

    cout << "  fb.f = 1.0f\n";
    cout << "  fb.bits (hex) = 0x" << hex << fb.bits << dec << "\n";
    cout << "  Expected:       0x3f800000  (IEEE 754 representation of 1.0)\n\n";

    fb.f = -0.5f;
    cout << "  fb.f = -0.5f\n";
    cout << "  fb.bits (hex) = 0x" << hex << fb.bits << dec << "\n";
    cout << "  Expected:       0xbf000000\n\n";


    // ── 5. Final cheat-sheet ──────────────────────────────────────────────────
    cout << "━━━  CHEAT SHEET  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";
    cout << "  ┌───────────────┬────────────────┬──────────────────────────┐\n";
    cout << "  │               │     STRUCT     │         UNION            │\n";
    cout << "  ├───────────────┼────────────────┼──────────────────────────┤\n";
    cout << "  │ Memory        │ sum of fields  │ max field size           │\n";
    cout << "  │ Fields coexist│ YES            │ NO — one at a time       │\n";
    cout << "  │ Writing one   │ safe           │ corrupts others          │\n";
    cout << "  │ Use case      │ group data     │ save memory, type-pun    │\n";
    cout << "  │ Modern alt    │  —             │ std::variant<>           │\n";
    cout << "  └───────────────┴────────────────┴──────────────────────────┘\n\n";

    cout << "  sizeof(Person)      = " << sizeof(Person)      << " bytes  (struct)\n";
    cout << "  sizeof(Data)        = " << sizeof(Data)        << " bytes  (union)\n";
    cout << "  sizeof(TaggedValue) = " << sizeof(TaggedValue) << " bytes  (tagged union)\n";
    cout << "  sizeof(FloatBits)   = " << sizeof(FloatBits)   << " bytes  (type-pun union)\n";

    return 0;
}

// ╔══════════════════════════════════════════════════════════════════════════════╗
// ║  QUICK RULES TO REMEMBER                                                     ║
// ║                                                                              ║
// ║  1. sizeof(struct) = sum of fields + alignment padding                       ║
// ║  2. sizeof(union)  = sizeof(largest field)                                   ║
// ║  3. In a union: only the LAST WRITTEN field is valid to read                 ║
// ║  4. Use a 'tag' integer to track which field is live (tagged union)          ║
// ║  5. Prefer std::variant<> in modern C++ — it enforces the tag for you        ║
// ╚══════════════════════════════════════════════════════════════════════════════╝
