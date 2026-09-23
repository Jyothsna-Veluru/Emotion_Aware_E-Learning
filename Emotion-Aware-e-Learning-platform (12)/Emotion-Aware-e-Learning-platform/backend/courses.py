"""
courses.py
==========
Full educational content for the two demo courses: Python and Java.

Each course has 5 modules. Each module carries:
  - title, explanation, examples (basic / advanced)
  - a practice task
  - a 5-question quiz with easy / medium / hard tiers
  - a coding challenge with a starter, hint and reference solution

All content is real teaching material - no placeholders.
"""

# ---------------------------------------------------------------------------
# PYTHON COURSE
# ---------------------------------------------------------------------------

PYTHON_COURSE = {
    "id": "python",
    "name": "Python Programming",
    "tagline": "From first variable to clean, idiomatic Python.",
    "color": "#3b82f6",
    "modules": [
        {
            "id": "py-1",
            "title": "Variables, Types & I/O",
            "explanation": (
                "A variable is a name bound to a value. Python is dynamically typed, "
                "so you never declare a type - the interpreter infers it from the value "
                "you assign. The core built-in types you will meet first are int, float, "
                "str and bool. Use input() to read text from the user (it always returns "
                "a str) and print() to display output. Convert between types explicitly "
                "with int(), float() and str() when needed."
            ),
            "examples": {
                "basic": "name = input('Your name: ')\nage = int(input('Your age: '))\nprint(f'Hi {name}, next year you will be {age + 1}.')",
                "advanced": "# Multiple assignment and type introspection\nx, y, z = 1, 2.5, 'three'\nfor v in (x, y, z):\n    print(f'{v!r} is a {type(v).__name__}')",
            },
            "practice_task": "Ask the user for two numbers and print their sum, difference, product and quotient.",
            "quiz": [
                {"q": "What type does input() always return?", "options": ["int", "str", "float", "bool"], "answer": 1, "difficulty": "easy"},
                {"q": "Which converts '42' to an integer?", "options": ["str(42)", "int('42')", "float('42')", "bool('42')"], "answer": 1, "difficulty": "easy"},
                {"q": "What is the result of type(3.0).__name__?", "options": ["int", "double", "float", "number"], "answer": 2, "difficulty": "medium"},
                {"q": "What does f'{2+3}' produce?", "options": ["'2+3'", "'5'", "5", "Error"], "answer": 1, "difficulty": "medium"},
                {"q": "Given x = y = z = []  then x.append(1); what is z?", "options": ["[]", "[1]", "Error", "None"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Calculator",
                "prompt": "Write a function calc(a, b, op) that returns the result of applying op ('+','-','*','/') to a and b. Guard against division by zero by returning None.",
                "starter": "def calc(a, b, op):\n    # your code here\n    pass",
                "hint": "Use a dictionary mapping the operator string to a lambda, and check op == '/' and b == 0.",
                "solution": "def calc(a, b, op):\n    if op == '/' and b == 0:\n        return None\n    ops = {'+': a + b, '-': a - b, '*': a * b, '/': a / b if b else None}\n    return ops.get(op)",
            },
        },
        {
            "id": "py-2",
            "title": "Control Flow",
            "explanation": (
                "Control flow decides which statements run. if / elif / else branch on "
                "boolean conditions. Python uses indentation (not braces) to define blocks. "
                "Comparison operators (==, !=, <, >, <=, >=) and boolean operators "
                "(and, or, not) build conditions. Remember that any non-empty object is "
                "truthy and 0, '', [], None are falsy."
            ),
            "examples": {
                "basic": "score = 72\nif score >= 90:\n    print('A')\nelif score >= 60:\n    print('Pass')\nelse:\n    print('Retake')",
                "advanced": "# Ternary + chained comparison\nn = 15\nlabel = 'teen' if 13 <= n <= 19 else 'not teen'\nprint(label)",
            },
            "practice_task": "Read a year and print whether it is a leap year (divisible by 4, but not by 100 unless also by 400).",
            "quiz": [
                {"q": "Which value is falsy?", "options": ["'0'", "[]", "1", "'False'"], "answer": 1, "difficulty": "easy"},
                {"q": "What defines a block in Python?", "options": ["Braces {}", "Indentation", "Semicolons", "Parentheses"], "answer": 1, "difficulty": "easy"},
                {"q": "What does (3 < 5 < 10) evaluate to?", "options": ["True", "False", "Error", "3"], "answer": 0, "difficulty": "medium"},
                {"q": "Result of: 'a' if 0 else 'b'", "options": ["'a'", "'b'", "0", "Error"], "answer": 1, "difficulty": "medium"},
                {"q": "What does `not (True and False)` return?", "options": ["True", "False", "None", "Error"], "answer": 0, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Prime Number",
                "prompt": "Write is_prime(n) returning True if n is a prime number, else False.",
                "starter": "def is_prime(n):\n    # your code here\n    pass",
                "hint": "Numbers < 2 are not prime. Test divisors up to int(n ** 0.5) + 1.",
                "solution": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
            },
        },
        {
            "id": "py-3",
            "title": "Loops & Iteration",
            "explanation": (
                "Loops repeat work. A for loop iterates over any iterable (lists, strings, "
                "ranges). A while loop repeats while a condition holds. range(start, stop, "
                "step) generates numbers lazily. Use break to exit early, continue to skip "
                "to the next iteration, and enumerate() when you need both the index and "
                "the value."
            ),
            "examples": {
                "basic": "for i in range(1, 6):\n    print(i, i ** 2)",
                "advanced": "words = ['sky', 'tree', 'sun']\nfor idx, w in enumerate(words, start=1):\n    print(f'{idx}. {w.title()}')",
            },
            "practice_task": "Print the multiplication table (1-10) for a number entered by the user.",
            "quiz": [
                {"q": "range(3) yields:", "options": ["1,2,3", "0,1,2", "0,1,2,3", "1,2"], "answer": 1, "difficulty": "easy"},
                {"q": "Which keyword skips to the next loop iteration?", "options": ["break", "skip", "continue", "pass"], "answer": 2, "difficulty": "easy"},
                {"q": "enumerate(['a','b']) gives pairs starting at:", "options": ["1", "0", "-1", "depends"], "answer": 1, "difficulty": "medium"},
                {"q": "How many times does `for _ in range(2,10,3)` loop?", "options": ["2", "3", "4", "8"], "answer": 1, "difficulty": "medium"},
                {"q": "What does a `for/else` else block run after?", "options": ["Each iteration", "Only on break", "Loop ends without break", "Never"], "answer": 2, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Fibonacci",
                "prompt": "Write fib(n) returning a list of the first n Fibonacci numbers, e.g. fib(5) -> [0,1,1,2,3].",
                "starter": "def fib(n):\n    # your code here\n    pass",
                "hint": "Track two variables a, b = 0, 1 and append a each step, then a, b = b, a + b.",
                "solution": "def fib(n):\n    seq, a, b = [], 0, 1\n    for _ in range(n):\n        seq.append(a)\n        a, b = b, a + b\n    return seq",
            },
        },
        {
            "id": "py-4",
            "title": "Functions & Scope",
            "explanation": (
                "Functions package reusable logic. Define them with def, pass arguments, "
                "and return values. Parameters can have default values and be passed by "
                "keyword. Variables created inside a function are local; the function can "
                "read outer (global) names but needs the global keyword to rebind them. "
                "Prefer returning values over mutating globals - it keeps code testable."
            ),
            "examples": {
                "basic": "def greet(name, greeting='Hello'):\n    return f'{greeting}, {name}!'\nprint(greet('Sai'))",
                "advanced": "# *args / **kwargs\ndef summarize(*nums, label='total'):\n    return f'{label}: {sum(nums)}'\nprint(summarize(1, 2, 3, label='sum'))",
            },
            "practice_task": "Write a function that takes a list of numbers and returns a dict with min, max and average.",
            "quiz": [
                {"q": "Which keyword returns a value from a function?", "options": ["yield", "return", "out", "send"], "answer": 1, "difficulty": "easy"},
                {"q": "A default parameter is written as:", "options": ["def f(x=1)", "def f(x:1)", "def f(x->1)", "def f(x==1)"], "answer": 0, "difficulty": "easy"},
                {"q": "*args collects extra positional args into a:", "options": ["dict", "tuple", "list", "set"], "answer": 1, "difficulty": "medium"},
                {"q": "To rebind a global inside a function you use:", "options": ["nonlocal", "global", "extern", "static"], "answer": 1, "difficulty": "medium"},
                {"q": "Default mutable arg `def f(x=[])` is risky because the list is:", "options": ["Copied each call", "Shared across calls", "Always empty", "Read-only"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Reverse String",
                "prompt": "Write reverse(s) that returns the string s reversed, without using s[::-1].",
                "starter": "def reverse(s):\n    # your code here\n    pass",
                "hint": "Build the result by prepending each character, or iterate reversed(range(len(s))).",
                "solution": "def reverse(s):\n    out = ''\n    for ch in s:\n        out = ch + out\n    return out",
            },
        },
        {
            "id": "py-5",
            "title": "Data Structures",
            "explanation": (
                "Python ships powerful built-in collections. Lists are ordered, mutable "
                "sequences. Tuples are immutable. Dictionaries map keys to values with "
                "O(1) lookup. Sets store unique items. Comprehensions build these "
                "concisely: [x*x for x in range(5)] or {k: v for k, v in pairs}. Choosing "
                "the right structure is often the biggest performance lever you have."
            ),
            "examples": {
                "basic": "fruit = {'apple': 3, 'pear': 5}\nfor name, qty in fruit.items():\n    print(name, qty)",
                "advanced": "# Comprehension + set dedup\nnums = [1, 2, 2, 3, 3, 3]\nsquares = {n * n for n in nums}\nprint(sorted(squares))",
            },
            "practice_task": "Count the frequency of each word in a sentence and print the most common one.",
            "quiz": [
                {"q": "Which is immutable?", "options": ["list", "dict", "tuple", "set"], "answer": 2, "difficulty": "easy"},
                {"q": "Dictionary lookup by key is on average:", "options": ["O(n)", "O(log n)", "O(1)", "O(n^2)"], "answer": 2, "difficulty": "easy"},
                {"q": "{1,2,2,3} has length:", "options": ["4", "3", "2", "Error"], "answer": 1, "difficulty": "medium"},
                {"q": "[x for x in range(6) if x%2] yields:", "options": ["[0,2,4]", "[1,3,5]", "[0,1,2]", "[2,4,6]"], "answer": 1, "difficulty": "medium"},
                {"q": "What does dict.get('k', 0) do if 'k' is missing?", "options": ["Raises KeyError", "Returns 0", "Returns None", "Adds 'k'"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Palindrome",
                "prompt": "Write is_palindrome(s) that ignores case and spaces and returns True if s reads the same forwards and backwards.",
                "starter": "def is_palindrome(s):\n    # your code here\n    pass",
                "hint": "Normalize: keep only alphanumerics, lowercase them, then compare to the reverse.",
                "solution": "def is_palindrome(s):\n    cleaned = [c.lower() for c in s if c.isalnum()]\n    return cleaned == cleaned[::-1]",
            },
        },
    ],
}

# ---------------------------------------------------------------------------
# JAVA COURSE
# ---------------------------------------------------------------------------

JAVA_COURSE = {
    "id": "java",
    "name": "Java Programming",
    "tagline": "Strong typing, the JVM, and object-oriented thinking.",
    "color": "#f97316",
    "modules": [
        {
            "id": "jv-1",
            "title": "Syntax, Types & main()",
            "explanation": (
                "Java is statically typed: every variable has a declared type checked at "
                "compile time. A program runs from public static void main(String[] args). "
                "Primitive types (int, double, char, boolean) hold raw values; reference "
                "types (String, arrays, objects) hold references. System.out.println "
                "prints a line. Every statement ends with a semicolon and code lives "
                "inside a class."
            ),
            "examples": {
                "basic": "public class Hello {\n    public static void main(String[] args) {\n        int year = 2026;\n        System.out.println(\"Year: \" + year);\n    }\n}",
                "advanced": "// Type inference with var (Java 10+)\nvar names = new String[]{\"Ann\", \"Bo\"};\nfor (var n : names) System.out.println(n.toUpperCase());",
            },
            "practice_task": "Declare an int, a double and a String, then print a sentence combining all three.",
            "quiz": [
                {"q": "Java's entry method signature is:", "options": ["void main()", "public static void main(String[] args)", "static main(args)", "def main()"], "answer": 1, "difficulty": "easy"},
                {"q": "Which is a primitive type?", "options": ["String", "Integer", "int", "List"], "answer": 2, "difficulty": "easy"},
                {"q": "What ends every Java statement?", "options": ["Newline", "Period", "Semicolon", "Comma"], "answer": 2, "difficulty": "medium"},
                {"q": "var x = 5; infers x as:", "options": ["double", "int", "Integer", "String"], "answer": 1, "difficulty": "medium"},
                {"q": "char in Java stores a value of how many bits?", "options": ["8", "16", "32", "64"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Calculator",
                "prompt": "Write a static method calc(double a, double b, char op) returning the result of +, -, *, /. Return Double.NaN on divide-by-zero.",
                "starter": "static double calc(double a, double b, char op) {\n    // your code here\n    return 0;\n}",
                "hint": "Use a switch on op; for '/' check b == 0 and return Double.NaN.",
                "solution": "static double calc(double a, double b, char op) {\n    switch (op) {\n        case '+': return a + b;\n        case '-': return a - b;\n        case '*': return a * b;\n        case '/': return b == 0 ? Double.NaN : a / b;\n        default: return Double.NaN;\n    }\n}",
            },
        },
        {
            "id": "jv-2",
            "title": "Conditionals & Operators",
            "explanation": (
                "Java decisions use if / else if / else and switch. Conditions are strict "
                "booleans - unlike some languages you cannot use an int as a condition. "
                "Relational operators (==, !=, <, >) and logical operators (&&, ||, !) "
                "with short-circuit evaluation build the conditions. The ternary operator "
                "cond ? a : b gives a compact alternative."
            ),
            "examples": {
                "basic": "int score = 72;\nif (score >= 90) System.out.println(\"A\");\nelse if (score >= 60) System.out.println(\"Pass\");\nelse System.out.println(\"Retake\");",
                "advanced": "// switch expression (Java 14+)\nint day = 3;\nString name = switch (day) {\n    case 1, 7 -> \"Weekend\";\n    default -> \"Weekday\";\n};\nSystem.out.println(name);",
            },
            "practice_task": "Read three integers and print the largest using only if statements.",
            "quiz": [
                {"q": "Logical AND in Java is:", "options": ["and", "&&", "&", "AND"], "answer": 1, "difficulty": "easy"},
                {"q": "A Java if condition must be of type:", "options": ["int", "boolean", "any", "String"], "answer": 1, "difficulty": "easy"},
                {"q": "Ternary syntax is:", "options": ["a ? b : c", "a : b ? c", "if a then b", "a => b : c"], "answer": 0, "difficulty": "medium"},
                {"q": "What does short-circuit && do if the left side is false?", "options": ["Evaluates right", "Skips right", "Throws", "Returns null"], "answer": 1, "difficulty": "medium"},
                {"q": "Comparing two Strings with == compares:", "options": ["Contents", "Length", "References", "Hashcodes"], "answer": 2, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Number Patterns",
                "prompt": "Write a static method that prints a right-angled triangle of stars of height n (row i has i stars).",
                "starter": "static void triangle(int n) {\n    // your code here\n}",
                "hint": "Outer loop i from 1..n, inner loop prints i stars, then a newline.",
                "solution": "static void triangle(int n) {\n    for (int i = 1; i <= n; i++) {\n        for (int j = 0; j < i; j++) System.out.print(\"*\");\n        System.out.println();\n    }\n}",
            },
        },
        {
            "id": "jv-3",
            "title": "Loops & Arrays",
            "explanation": (
                "Java offers for, while and do-while loops, plus the enhanced for-each "
                "loop for collections and arrays. Arrays are fixed-size, zero-indexed "
                "containers of one type, created with new int[5] or literal {1,2,3}. "
                "Access length with arr.length (a field, not a method). Out-of-bounds "
                "access throws ArrayIndexOutOfBoundsException at runtime."
            ),
            "examples": {
                "basic": "int[] nums = {4, 8, 15, 16};\nint sum = 0;\nfor (int n : nums) sum += n;\nSystem.out.println(sum);",
                "advanced": "// 2D array traversal\nint[][] grid = {{1,2},{3,4}};\nfor (int r = 0; r < grid.length; r++)\n    for (int c = 0; c < grid[r].length; c++)\n        System.out.print(grid[r][c] + \" \");",
            },
            "practice_task": "Create an array of 5 integers and print the maximum and the sum.",
            "quiz": [
                {"q": "Array length is accessed via:", "options": ["arr.size()", "arr.length", "len(arr)", "arr.count"], "answer": 1, "difficulty": "easy"},
                {"q": "Java arrays are indexed from:", "options": ["1", "0", "-1", "any"], "answer": 1, "difficulty": "easy"},
                {"q": "new int[3] initial values are:", "options": ["null", "0", "garbage", "1"], "answer": 1, "difficulty": "medium"},
                {"q": "for-each over int[] gives you each:", "options": ["index", "value", "pair", "pointer"], "answer": 1, "difficulty": "medium"},
                {"q": "Accessing arr[arr.length] throws:", "options": ["NullPointer", "ArrayIndexOutOfBounds", "ClassCast", "Nothing"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Arrays",
                "prompt": "Write static int secondMax(int[] a) returning the second-largest distinct value in a.",
                "starter": "static int secondMax(int[] a) {\n    // your code here\n    return 0;\n}",
                "hint": "Track first and second maxima in one pass; update second only when value < first.",
                "solution": "static int secondMax(int[] a) {\n    int first = Integer.MIN_VALUE, second = Integer.MIN_VALUE;\n    for (int v : a) {\n        if (v > first) { second = first; first = v; }\n        else if (v > second && v < first) second = v;\n    }\n    return second;\n}",
            },
        },
        {
            "id": "jv-4",
            "title": "Methods & OOP Basics",
            "explanation": (
                "Methods are named blocks with a return type, name and parameters. Java is "
                "object-oriented: a class is a blueprint, and objects are instances created "
                "with new. Fields hold state, methods define behavior, and a constructor "
                "initializes new objects. Access modifiers (public, private) control "
                "visibility - encapsulating fields as private with getters/setters is the "
                "norm."
            ),
            "examples": {
                "basic": "class Dog {\n    String name;\n    Dog(String n) { name = n; }\n    void bark() { System.out.println(name + \" says woof\"); }\n}\n// new Dog(\"Rex\").bark();",
                "advanced": "// Encapsulation\nclass Account {\n    private double balance;\n    public void deposit(double a) { if (a > 0) balance += a; }\n    public double getBalance() { return balance; }\n}",
            },
            "practice_task": "Create a Rectangle class with width and height fields and an area() method.",
            "quiz": [
                {"q": "Objects are created with which keyword?", "options": ["make", "create", "new", "alloc"], "answer": 2, "difficulty": "easy"},
                {"q": "A constructor's name must match the:", "options": ["package", "class", "method", "field"], "answer": 1, "difficulty": "easy"},
                {"q": "private fields are accessible from:", "options": ["Anywhere", "Same class only", "Subclasses", "Same package"], "answer": 1, "difficulty": "medium"},
                {"q": "A method with no return uses type:", "options": ["null", "void", "empty", "none"], "answer": 1, "difficulty": "medium"},
                {"q": "Two methods, same name, different params is called:", "options": ["Overriding", "Overloading", "Shadowing", "Hiding"], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "Student Management",
                "prompt": "Create a Student class (name, marks[]) with a method average() returning the mean of marks as a double.",
                "starter": "class Student {\n    String name;\n    int[] marks;\n    // constructor + average() here\n}",
                "hint": "Sum the marks in a loop, divide by marks.length (cast to double to avoid integer division).",
                "solution": "class Student {\n    String name; int[] marks;\n    Student(String n, int[] m) { name = n; marks = m; }\n    double average() {\n        int sum = 0;\n        for (int m : marks) sum += m;\n        return marks.length == 0 ? 0 : (double) sum / marks.length;\n    }\n}",
            },
        },
        {
            "id": "jv-5",
            "title": "Strings & Collections",
            "explanation": (
                "Strings in Java are immutable objects with a rich API: length(), "
                "charAt(), substring(), toUpperCase(), split() and more. Use StringBuilder "
                "when you need to build text in a loop - it avoids creating many "
                "intermediate strings. For dynamic collections, ArrayList<T> grows "
                "automatically and HashMap<K,V> stores key-value pairs, both from "
                "java.util."
            ),
            "examples": {
                "basic": "String s = \"hello world\";\nSystem.out.println(s.length());\nSystem.out.println(s.toUpperCase());\nSystem.out.println(s.split(\" \").length);",
                "advanced": "import java.util.*;\nMap<String,Integer> count = new HashMap<>();\nfor (String w : \"a b a c\".split(\" \"))\n    count.merge(w, 1, Integer::sum);\nSystem.out.println(count);",
            },
            "practice_task": "Count how many vowels appear in a String entered by the user.",
            "quiz": [
                {"q": "String length is obtained with:", "options": ["s.length", "s.length()", "len(s)", "s.size()"], "answer": 1, "difficulty": "easy"},
                {"q": "Java Strings are:", "options": ["Mutable", "Immutable", "Primitive", "Arrays of int"], "answer": 1, "difficulty": "easy"},
                {"q": "For heavy string concatenation in loops, prefer:", "options": ["String +", "StringBuilder", "char[]", "concat()"], "answer": 1, "difficulty": "medium"},
                {"q": "ArrayList and HashMap live in package:", "options": ["java.lang", "java.io", "java.util", "java.net"], "answer": 2, "difficulty": "medium"},
                {"q": "\"abc\".substring(1) returns:", "options": ["\"abc\"", "\"bc\"", "\"a\"", "\"ab\""], "answer": 1, "difficulty": "hard"},
            ],
            "challenge": {
                "title": "String Processing",
                "prompt": "Write static String reverseWords(String s) that reverses the order of words, e.g. 'I love Java' -> 'Java love I'.",
                "starter": "static String reverseWords(String s) {\n    // your code here\n    return \"\";\n}",
                "hint": "Split on spaces into an array, then join from the last index back to the first.",
                "solution": "static String reverseWords(String s) {\n    String[] w = s.trim().split(\"\\\\s+\");\n    StringBuilder sb = new StringBuilder();\n    for (int i = w.length - 1; i >= 0; i--) {\n        sb.append(w[i]);\n        if (i > 0) sb.append(' ');\n    }\n    return sb.toString();\n}",
            },
        },
    ],
}

COURSES = {"python": PYTHON_COURSE, "java": JAVA_COURSE}


def list_courses():
    """Lightweight catalog (no quiz answers) for the selection screen."""
    out = []
    for c in COURSES.values():
        out.append({
            "id": c["id"],
            "name": c["name"],
            "tagline": c["tagline"],
            "color": c["color"],
            "module_count": len(c["modules"]),
        })
    return out


def get_course(course_id, include_answers=False):
    """Return a full course. Quiz answers are stripped unless explicitly asked."""
    course = COURSES.get(course_id)
    if not course:
        return None
    if include_answers:
        return course
    # deep-ish copy that removes the 'answer' field from quizzes
    import copy
    safe = copy.deepcopy(course)
    for m in safe["modules"]:
        for q in m["quiz"]:
            q.pop("answer", None)
        m["challenge"].pop("solution", None)
    return safe
