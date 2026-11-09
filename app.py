import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from supabase import create_client

# ------------------------------------------------------------
# LearnWise AI - Personalized Learning Recommendation System
# Existing features preserved + revision and progress features
# ------------------------------------------------------------

st.set_page_config(
    page_title="LearnWise AI | Personalized Learning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if (
    "access_token" in st.session_state
    and "refresh_token" in st.session_state
):
    supabase.auth.set_session(
        st.session_state.access_token,
        st.session_state.refresh_token
    )
   # -------------------- Login and Signup --------------------

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🧠 LearnWise AI")
    st.subheader("Login or Create an Account")

    auth_option = st.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        horizontal=True
    )

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if auth_option == "Sign Up":
        if st.button("Create Account"):
            try:
                response = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.success("Account created! Please check your email.")
            except Exception as e:
                st.error(str(e))

    else:
        if st.button("Login"):
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if response.session is not None:
                    st.session_state.user = response.user
                    st.session_state.access_token = response.session.access_token
                    st.session_state.refresh_token = response.session.refresh_token
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.info("Please check your email for confirmation.")

            except Exception:
                st.error("Login failed. Check your email and password.")

    st.stop() 
    

# -------------------- Theme --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #FFFFFF; color: #334155; }
[data-testid="stHeader"] { background: #FFFFFF; }
[data-testid="stSidebar"] {
    background: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}
.block-container { padding-top: 1.8rem; padding-bottom: 2.5rem; max-width: 1300px; }
h1, h2, h3, h4 { color: #1E293B !important; letter-spacing: -.025em; }
p, label, li, .stMarkdown { color: #334155; }
div[data-testid="stMetric"] {
    background: #F8FAFC; border: 1px solid #E2E8F0;
    padding: 18px 20px; border-radius: 16px;
}
div[data-testid="stMetric"] label { color: #64748B !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #1E293B !important; }
.glass-card {
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 18px; padding: 20px; margin-bottom: 14px;
}
.hero {
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 22px; padding: 26px; margin-bottom: 20px;
}
.hero h1 { font-size: 2.35rem; margin: 0; }
.hero p { color: #334155; font-size: 1.02rem; margin-top: 10px; }
.small-muted { color: #64748B; font-size: .9rem; }
.pill {
    display: inline-block; border-radius: 999px; padding: 5px 11px;
    background: #EFF6FF; border: 1px solid #DBEAFE;
    color: #1D4ED8; font-size: .78rem; margin: 2px;
}
div.stButton > button, div.stFormSubmitButton > button {
    border-radius: 11px; border: 1px solid #2563EB;
    background: #2563EB; color: #FFFFFF; font-weight: 650;
    padding: .58rem 1rem;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    background: #1D4ED8; border-color: #1D4ED8; color: #FFFFFF;
}
div[data-testid="stProgress"] > div > div { background: #2563EB; }
hr { border-color: #E2E8F0; }
a { color: #2563EB !important; }
[data-testid="stRadio"] label { color: #334155 !important; }
.stAlert { border-radius: 13px; }
</style>
""", unsafe_allow_html=True)
# -------------------- Quiz bank --------------------
QUIZZES = {
    "Python": [
        ("Which function displays output in Python?", ["input()", "print()", "show()", "write()"], 1, "print() displays output."),
        ("Which data type stores whole numbers?", ["str", "float", "int", "list"], 2, "int stores integer values."),
        ("What is the result of 7 // 2?", ["3.5", "4", "3", "2"], 2, "// performs floor division."),
        ("Which symbol checks equality?", ["=", "==", "!=", ":"], 1, "== compares two values."),
        ("Which collection is mutable?", ["tuple", "str", "list", "int"], 2, "Lists can be changed after creation."),
        ("What does len('AI') return?", ["1", "2", "3", "AI"], 1, "The string has two characters."),
        ("Which keyword starts a condition?", ["for", "if", "def", "return"], 1, "if begins a conditional statement."),
        ("What does range(3) produce?", ["1,2,3", "0,1,2", "0,1,2,3", "3"], 1, "range(3) starts at zero and stops before three."),
        ("Which method adds an item to a list?", ["add()", "push()", "append()", "insertend()"], 2, "append() adds an item to the end."),
        ("Which value represents no value?", ["None", "null", "zero", "False"], 0, "Python uses None."),
    ],
    "Java": [
        ("Which keyword defines a class in Java?", ["class", "define", "struct", "object"], 0, "class is used to declare a class."),
        ("Which method is the usual Java entry point?", ["start()", "main()", "run()", "init()"], 1, "Java applications begin at main()."),
        ("Which type stores true or false?", ["int", "char", "boolean", "String"], 2, "boolean stores true or false."),
        ("Which symbol ends most Java statements?", [".", ":", ";", ","], 2, "A semicolon ends most statements."),
        ("Which keyword creates an object?", ["make", "new", "create", "this"], 1, "new creates an object."),
        ("Which is a single-line comment?", ["<!-- -->", "**", "//", "##"], 2, "// starts a single-line comment."),
        ("Which type stores a single character?", ["String", "char", "Character[]", "text"], 1, "char stores one character."),
        ("Java source files typically use which extension?", [".class", ".jav", ".java", ".js"], 2, "Java source code files end in .java."),
        ("Which keyword inherits a class?", ["implements", "extends", "inherits", "super"], 1, "extends is used for class inheritance."),
        ("Which access level is most restrictive?", ["public", "protected", "private", "default"], 2, "private members are accessible within their class."),
    ],
    "Data Structures": [
        ("Which structure follows LIFO?", ["Queue", "Stack", "Tree", "Graph"], 1, "A stack follows Last In, First Out."),
        ("Which structure follows FIFO?", ["Stack", "Queue", "Heap", "Tree"], 1, "A queue follows First In, First Out."),
        ("What is the first index of a Python list?", ["1", "-1", "0", "Depends"], 2, "Python sequences are zero-indexed."),
        ("Which is a linear data structure?", ["Graph", "Tree", "Array", "Network"], 2, "An array stores elements in a linear order."),
        ("Which operation adds to a stack?", ["enqueue", "push", "dequeue", "poll"], 1, "push adds an item to a stack."),
        ("Which operation removes from a queue front?", ["push", "pop", "dequeue", "insert"], 2, "dequeue removes the front item."),
        ("A linked list node commonly contains data and…", ["a pointer/link", "a loop", "a class name", "a file"], 0, "A node stores data and a link to another node."),
        ("Which traversal visits left, root, right?", ["Preorder", "Inorder", "Postorder", "Level order"], 1, "Inorder traversal is left, root, right."),
        ("Which structure represents relationships as vertices and edges?", ["Stack", "Queue", "Graph", "Array"], 2, "Graphs model vertices connected by edges."),
        ("Binary search requires data to be…", ["random", "sorted", "unique", "reversed"], 1, "Binary search relies on sorted order."),
    ],
    "DBMS": [
        ("What does DBMS stand for?", ["Data Backup Management System", "Database Management System", "Digital Base Management System", "Data Building Machine System"], 1, "DBMS stands for Database Management System."),
        ("Which language is commonly used to query relational databases?", ["HTML", "CSS", "SQL", "Python"], 2, "SQL is used to query and manage relational databases."),
        ("Which key uniquely identifies each row in a table?", ["Foreign key", "Primary key", "Candidate value", "Duplicate key"], 1, "A primary key uniquely identifies each row."),
        ("What does a foreign key do?", ["Deletes a table", "Links tables", "Sorts rows", "Creates a database"], 1, "A foreign key references a key in another table."),
        ("Which command retrieves data from a table?", ["GET", "OPEN", "SELECT", "FETCHTABLE"], 2, "SELECT retrieves data from a table."),
        ("Which command removes all rows but keeps the table structure?", ["DROP", "TRUNCATE", "ALTER", "CREATE"], 1, "TRUNCATE removes all rows while keeping the table structure."),
        ("What is normalization mainly used for?", ["Increasing duplicates", "Reducing data redundancy", "Deleting databases", "Encrypting passwords"], 1, "Normalization organizes data to reduce redundancy and update problems."),
        ("Which ACID property means a transaction is all-or-nothing?", ["Consistency", "Isolation", "Atomicity", "Durability"], 2, "Atomicity means a transaction completes fully or not at all."),
        ("Which clause filters rows?", ["ORDER BY", "WHERE", "GROUP BY", "SELECT"], 1, "WHERE filters rows based on a condition."),
        ("Which command changes the structure of an existing table?", ["ALTER", "INSERT", "SELECT", "COMMIT"], 0, "ALTER changes a table's structure."),
    ],
    "DLD": [
        ("What does DLD stand for?", ["Digital Logic Design", "Data Link Design", "Digital Language Development", "Direct Logic Data"], 0, "DLD stands for Digital Logic Design."),
        ("Which number system uses only 0 and 1?", ["Decimal", "Octal", "Binary", "Hexadecimal"], 2, "The binary number system uses 0 and 1."),
        ("How many inputs does a NOT gate have?", ["One", "Two", "Three", "Four"], 0, "A NOT gate has one input and produces its complement."),
        ("What is the output of an AND gate when both inputs are 1?", ["0", "1", "Undefined", "High impedance"], 1, "An AND gate outputs 1 only when both inputs are 1."),
        ("Which gate gives the complement of an OR operation?", ["AND", "XOR", "NOR", "NAND"], 2, "A NOR gate is the complement of an OR gate."),
        ("How many select lines are needed for a 4-to-1 multiplexer?", ["1", "2", "3", "4"], 1, "A 4-to-1 multiplexer needs 2 select lines."),
        ("Which circuit converts binary information into one of many output lines?", ["Encoder", "Decoder", "Adder", "Flip-flop"], 1, "A decoder activates an output based on its binary input."),
        ("Which flip-flop is commonly used to store one bit?", ["D flip-flop", "Half adder", "Multiplexer", "Decoder"], 0, "A flip-flop stores one bit of information."),
        ("A half adder adds how many single-bit inputs?", ["One", "Two", "Three", "Four"], 1, "A half adder adds two single-bit inputs."),
        ("Which circuit is used to remember a state?", ["Combinational circuit", "Sequential circuit", "Encoder only", "Comparator only"], 1, "Sequential circuits use memory elements and depend on previous state."),
    ],
    "DMS": [
        ("What does DMS commonly stand for in computer science courses?", ["Discrete Mathematical Structures", "Digital Memory System", "Data Management Software", "Direct Mathematical Science"], 0, "DMS stands for Discrete Mathematical Structures."),
        ("A statement in logic is a sentence that is…", ["Always a question", "Either true or false", "Always true", "Always false"], 1, "A proposition has a truth value: true or false."),
        ("What is the negation of a true proposition?", ["True", "False", "Unknown", "Both"], 1, "Negation reverses the truth value."),
        ("Which symbol commonly represents logical AND?", ["∨", "¬", "∧", "→"], 2, "The symbol ∧ represents logical AND."),
        ("A set is a collection of…", ["Ordered instructions", "Distinct objects", "Only numbers", "Repeated values only"], 1, "A set is a well-defined collection of distinct elements."),
        ("If A = {1, 2} and B = {2, 3}, what is A ∩ B?", ["{1, 3}", "{1, 2, 3}", "{2}", "∅"], 2, "The intersection contains elements common to both sets."),
        ("A relation from set A to set B is a subset of…", ["A ∪ B", "A × B", "A ∩ B", "B × B only"], 1, "A relation from A to B is a subset of the Cartesian product A × B."),
        ("Which property means a relation relates every element to itself?", ["Symmetric", "Transitive", "Reflexive", "Antisymmetric"], 2, "A reflexive relation contains (a, a) for every element a."),
        ("How many subsets does a set with 3 elements have?", ["3", "6", "8", "9"], 2, "A set with n elements has 2ⁿ subsets; 2³ = 8."),
        ("In a simple graph, an edge connects…", ["Two vertices", "Two matrices", "Two sets only", "Two functions"], 0, "An edge connects vertices in a graph."),
    ],
    "Data Wrangling": [
        ("What is data wrangling?", ["Deleting all data", "Cleaning and transforming data for analysis", "Designing a website", "Installing an operating system"], 1, "Data wrangling prepares raw data for analysis."),
        ("Which Python library is commonly used for tabular data manipulation?", ["Pandas", "Turtle", "Pygame", "Tkinter"], 0, "Pandas provides tools for working with tabular data."),
        ("In Pandas, which function reads a CSV file?", ["read_text()", "open_csv()", "read_csv()", "load_table()"], 2, "pandas.read_csv() loads a CSV file into a DataFrame."),
        ("What is a missing value?", ["A value that is not present", "A duplicate row", "A column heading", "A sorted value"], 0, "A missing value is data that has not been recorded or is unavailable."),
        ("Which Pandas method identifies missing values?", ["isnull()", "sort_values()", "rename()", "head()"], 0, "isnull() identifies missing values."),
        ("Which method removes duplicate rows in Pandas?", ["dropna()", "drop_duplicates()", "remove_all()", "unique_rows()"], 1, "drop_duplicates() removes duplicate rows."),
        ("What does DataFrame.head() display by default?", ["Last five rows", "First five rows", "Only column names", "All rows"], 1, "head() displays the first five rows by default."),
        ("Why is data type conversion used?", ["To change a column's data type", "To delete a file", "To create a chart only", "To rename Python"], 0, "Type conversion changes values to an appropriate data type."),
        ("What does merging datasets usually do?", ["Combines data using matching keys", "Deletes every column", "Sorts a single list", "Changes a file extension"], 0, "Merging combines datasets using one or more common keys."),
        ("Why should data be validated after cleaning?", ["To make the file larger", "To check that the data is accurate and consistent", "To remove all columns", "To hide missing values"], 1, "Validation checks that cleaning produced reliable, consistent data."),
    ],
    "Artificial Intelligence": [
        ("AI stands for…", ["Automated Internet", "Artificial Intelligence", "Advanced Interface", "Applied Input"], 1, "AI means Artificial Intelligence."),
        ("Which is a machine learning type?", ["Supervised learning", "Manual typing", "Formatting", "Compilation"], 0, "Supervised learning uses labeled examples."),
        ("What is a dataset?", ["A collection of data", "A coding error", "A CPU", "A browser"], 0, "A dataset is an organized collection of data."),
        ("Which task is NLP associated with?", ["Understanding text", "Cooling a CPU", "Drawing circuits", "File compression"], 0, "NLP focuses on human language."),
        ("Which is commonly used for image generation?", ["Stable Diffusion", "SQL", "Git", "Excel formulas"], 0, "Stable Diffusion is a generative image model."),
        ("Training data is used to…", ["Teach a model patterns", "Turn off a model", "Delete code", "Format a disk"], 0, "Models learn patterns from training data."),
        ("Which is an example of classification?", ["Predicting spam/not spam", "Adding numbers", "Sorting files manually", "Drawing a line"], 0, "Classification predicts a category."),
        ("A chatbot is designed to…", ["Interact using conversation", "Only store images", "Replace a keyboard", "Compile Java"], 0, "Chatbots communicate with users conversationally."),
        ("Which metric measures correct predictions among all predictions?", ["Accuracy", "Latency", "File size", "Brightness"], 0, "Accuracy is the fraction of correct predictions."),
        ("Generative AI can…", ["Create new content", "Only copy files", "Only calculate sums", "Only sort lists"], 0, "Generative AI produces content such as text or images."),
    ],
}
TOPICS = {
    "Python": {
        "Beginner": ["Variables & data types", "Input and output", "Operators", "Conditions", "Loops", "Strings", "Lists and tuples", "Sets and dictionaries"],
        "Intermediate": ["Functions", "File handling", "Exception handling", "Modules", "Comprehensions", "OOP fundamentals"],
        "Advanced": ["Decorators", "Generators", "Iterators", "Concurrency", "Testing", "Performance and packaging"],
    },
    "Java": {
        "Beginner": ["Java syntax", "Variables and data types", "Operators", "Conditions and loops", "Arrays", "Methods"],
        "Intermediate": ["Classes and objects", "Inheritance", "Interfaces", "Exception handling", "Collections", "File I/O"],
        "Advanced": ["Generics", "Streams", "Concurrency", "JVM basics", "Design patterns", "Testing"],
    },
    "Data Structures": {
        "Beginner": ["Arrays", "Strings", "Linked lists", "Stacks", "Queues", "Searching"],
        "Intermediate": ["Trees", "Binary search trees", "Hash tables", "Recursion", "Sorting", "Graphs"],
        "Advanced": ["Heaps", "Tries", "Balanced trees", "Graph algorithms", "Complexity analysis", "Dynamic programming"],
    },
    "DBMS": {
        "Beginner": ["Introduction to DBMS", "Database concepts and schemas", "Relational model and tables", "Keys and constraints", "Basic SQL queries", "SQL filtering and sorting", "SQL aggregate functions", "Joins basics"],
        "Intermediate": ["ER diagrams", "Relational algebra", "Normalization (1NF–3NF)", "Subqueries", "Advanced joins", "Views and indexes", "Transactions and ACID properties", "Concurrency control"],
        "Advanced": ["Query processing and optimization", "Indexing structures", "Transaction recovery", "Database security", "Distributed databases", "NoSQL fundamentals"],
    },
    "DLD": {
        "Beginner": ["Number systems", "Binary conversions", "Logic gates", "Boolean algebra basics", "Boolean expressions", "Truth tables", "K-map basics", "Combinational circuit basics"],
        "Intermediate": ["K-map simplification", "Half and full adders", "Subtractors", "Multiplexers and demultiplexers", "Encoders and decoders", "Comparators", "Latches and flip-flops", "Counters and registers"],
        "Advanced": ["Sequential circuit design", "Finite state machines", "Register transfer concepts", "Synchronous and asynchronous counters", "Memory basics", "Programmable logic devices"],
    },
    "DMS": {
        "Beginner": ["Introduction to discrete mathematics", "Propositions and logical connectives", "Truth tables", "Logical equivalence", "Predicates and quantifiers", "Set theory", "Set operations", "Cartesian products"],
        "Intermediate": ["Relations and their properties", "Equivalence relations", "Partial orders", "Functions and types", "Mathematical induction", "Counting principles", "Permutations and combinations", "Pigeonhole principle"],
        "Advanced": ["Recurrence relations", "Generating functions", "Graph theory basics", "Trees and spanning trees", "Boolean algebra", "Algebraic structures"],
    },
    "Data Wrangling": {
        "Beginner": ["Introduction to data wrangling", "Understanding datasets", "Python and Pandas basics", "Loading CSV and Excel files", "Inspecting rows and columns", "Selecting and filtering data", "Handling missing values", "Finding duplicate records"],
        "Intermediate": ["Data type conversion", "Renaming columns", "String cleaning", "Combining datasets", "Merging and joining DataFrames", "Grouping and aggregation", "Reshaping data", "Date and time cleaning"],
        "Advanced": ["Outlier detection and treatment", "Data validation", "Complex transformation pipelines", "Working with large datasets", "Data quality checks", "Preparing data for machine learning"],
    },
    "Artificial Intelligence": {
        "Beginner": ["What is AI?", "Data and datasets", "Machine learning basics", "Supervised learning", "Unsupervised learning", "AI applications"],
        "Intermediate": ["Model training", "Classification", "Regression", "Neural networks", "NLP basics", "Model evaluation"],
        "Advanced": ["Deep learning", "Transformers", "Computer vision", "Reinforcement learning", "Ethical AI", "Deployment"],
    },
}

RESOURCES = {
    "Python": [
        ("Python official tutorial", "https://docs.python.org/3/tutorial/"),
        ("W3Schools Python", "https://www.w3schools.com/python/"),
        ("Programiz Python", "https://www.programiz.com/python-programming"),
    ],
    "Java": [
        ("Oracle Java tutorials", "https://docs.oracle.com/javase/tutorial/"),
        ("W3Schools Java", "https://www.w3schools.com/java/"),
        ("Programiz Java", "https://www.programiz.com/java-programming"),
    ],
    "Data Structures": [
        ("GeeksforGeeks Data Structures", "https://www.geeksforgeeks.org/data-structures/"),
        ("VisuAlgo", "https://visualgo.net/en"),
        ("Programiz Data Structures", "https://www.programiz.com/dsa"),
    ],
    "DBMS": [
        ("W3Schools SQL Tutorial", "https://www.w3schools.com/sql/"),
        ("SQLBolt interactive lessons", "https://sqlbolt.com/"),
        ("GeeksforGeeks DBMS", "https://www.geeksforgeeks.org/dbms/"),
    ],
    "DLD": [
        ("All About Circuits – Digital", "https://www.allaboutcircuits.com/textbook/digital/"),
        ("Electronics Tutorials – Digital Circuits", "https://www.electronics-tutorials.ws/"),
        ("GeeksforGeeks Digital Electronics", "https://www.geeksforgeeks.org/digital-electronics-logic-design/"),
    ],
    "DMS": [
        ("OpenStax – Discrete Mathematics resources", "https://openstax.org/subjects/math"),
        ("MIT OpenCourseWare – Mathematics", "https://ocw.mit.edu/search/?q=discrete%20mathematics"),
        ("GeeksforGeeks Discrete Mathematics", "https://www.geeksforgeeks.org/discrete-mathematics/"),
    ],
    "Data Wrangling": [
        ("Pandas getting started", "https://pandas.pydata.org/docs/getting_started/"),
        ("Kaggle Pandas course", "https://www.kaggle.com/learn/pandas"),
        ("Real Python – Pandas", "https://realpython.com/learning-paths/pandas-data-science/"),
    ],
    "Artificial Intelligence": [
        ("Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course"),
        ("IBM AI resources", "https://www.ibm.com/think/topics/artificial-intelligence"),
        ("Elements of AI", "https://www.elementsofai.com/"),
    ],
}

# Flashcards are lightweight study prompts; they can be extended for every subject.
FLASHCARDS = {
    "Python": [
        ("What does print() do?", "Displays output."),
        ("What does int() do?", "Converts a value to an integer when possible."),
        ("What does == mean?", "Checks whether two values are equal."),
        ("What does // do?", "Performs floor division."),
        ("What is a list?", "An ordered, mutable collection."),
        ("What is a tuple?", "An ordered, immutable collection."),
        ("What does append() do?", "Adds an item to the end of a list."),
        ("What does a dictionary store?", "Key-value pairs."),
    ],
    "Java": [
        ("What does class declare?", "A class blueprint."),
        ("What is main()?", "The usual entry point of a Java application."),
        ("What does new do?", "Creates an object."),
        ("What type stores true or false?", "boolean."),
        ("What does extends mean?", "A class inherits from another class."),
        ("What is an array?", "A fixed-length collection of same-type elements."),
    ],
    "Data Structures": [
        ("What does LIFO mean?", "Last In, First Out; used by a stack."),
        ("What does FIFO mean?", "First In, First Out; used by a queue."),
        ("What is a linked list node?", "A data element with a link to another node."),
        ("What is a graph?", "A structure of vertices connected by edges."),
        ("What does binary search require?", "Sorted data."),
        ("What is a tree root?", "The topmost node."),
    ],
    "DBMS": [
        ("What is a DBMS?", "Software used to create, manage, and access databases."),
        ("What is a primary key?", "A column or set of columns that uniquely identifies a row."),
        ("What is a foreign key?", "A field that references a key in another table."),
        ("What does SELECT do?", "Retrieves data from a table."),
        ("What is normalization?", "Organizing tables to reduce redundancy and anomalies."),
        ("What does ACID stand for?", "Atomicity, Consistency, Isolation, and Durability."),
    ],
    "DLD": [
        ("What is a logic gate?", "An electronic circuit that performs a logical operation."),
        ("What is a truth table?", "A table showing outputs for every possible input combination."),
        ("What does a NOT gate do?", "It produces the complement of its input."),
        ("What is a multiplexer?", "A circuit that selects one of several inputs."),
        ("What is a flip-flop?", "A sequential circuit that stores one bit."),
        ("What does a half adder produce?", "Sum and carry outputs for two input bits."),
    ],
    "DMS": [
        ("What is a proposition?", "A statement that is either true or false."),
        ("What is a set?", "A well-defined collection of distinct elements."),
        ("What is a union?", "The set of elements that belong to either of the sets."),
        ("What is an intersection?", "The set of elements common to the sets."),
        ("What is a reflexive relation?", "A relation containing (a, a) for every element a."),
        ("How many subsets does an n-element set have?", "2 to the power n subsets."),
    ],
    "Data Wrangling": [
        ("What is data wrangling?", "Cleaning and transforming raw data into a useful format."),
        ("What is a DataFrame?", "A two-dimensional labeled data structure in Pandas."),
        ("Which Pandas function reads CSV files?", "pd.read_csv()."),
        ("What does isnull() do?", "Identifies missing values."),
        ("What does drop_duplicates() do?", "Removes duplicate rows."),
        ("Why validate cleaned data?", "To check its accuracy, consistency, and quality."),
    ],
    "Artificial Intelligence": [
        ("What does AI stand for?", "Artificial Intelligence."),
        ("What is a dataset?", "An organized collection of data."),
        ("What is supervised learning?", "Learning from labeled examples."),
        ("What is classification?", "Predicting a category."),
        ("What is NLP?", "Natural Language Processing."),
        ("What is generative AI?", "AI that creates new content."),
    ],
}
# -------------------- Session state --------------------
defaults = {
    "student_name": "Learner", "subject": "Python", "level": "Beginner",
    "goal": "Coding Practice", "planner_checks": {}, "completed_topics": set(),
    "quiz_results": {}, "quiz_submissions": {}, "quiz_answers": {},
    "topic_attempts": {}, "quiz_history": [], "flashcard_index": 0,
    "flashcard_revealed": False, "daily_goal_minutes": 30,
    "daily_logs": {}, "study_assistant_question": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
# -------------------- Load saved learning progress --------------------

if st.session_state.user is not None:
    user_id = st.session_state.user.id

    try:
        result = supabase.table("learning_progress") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        if result.data:
            saved_progress = result.data[0]

            st.session_state.planner_checks = saved_progress.get("planner_checks") or {}
            st.session_state.daily_goal_minutes = saved_progress.get("daily_goal_minutes") or 30
            st.session_state.daily_logs = saved_progress.get("daily_logs") or {}
            st.session_state.completed_topics = set(saved_progress.get("completed_topics") or [])
            st.session_state.quiz_results = saved_progress.get("quiz_results") or {}
            st.session_state.quiz_history = saved_progress.get("quiz_history") or []
            st.session_state.topic_attempts = saved_progress.get("topic_attempts") or {}

    except Exception as e:
        st.error(f"Could not load saved progress: {e}")

# -------------------- Sidebar --------------------
with st.sidebar:
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.pop("access_token", None)
        st.session_state.pop("refresh_token", None)
        st.rerun()

    st.markdown("## 🧠 LearnWise AI")
    st.caption("Your personalized learning companion")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Learning Recommendations", "Study Planner", "Learning Resources",
         "Practice Quiz", "Flashcards", "Study Assistant", "My Progress"],
        label_visibility="visible",
    )
    st.markdown("---")
    st.markdown("### 👤 Student profile")
    st.session_state.student_name = st.text_input("Your name", st.session_state.student_name)
    st.session_state.subject = st.selectbox("Learning subject", list(TOPICS.keys()), index=list(TOPICS.keys()).index(st.session_state.subject))
    st.session_state.level = st.selectbox("Current level", ["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.level))
    st.session_state.goal = st.selectbox("Learning goal", ["Theory", "Coding Practice", "Projects"], index=["Theory", "Coding Practice", "Projects"].index(st.session_state.goal))
    st.markdown("<div class='small-muted'>Prototype • Session-based progress</div>", unsafe_allow_html=True)

name = st.session_state.student_name.strip() or "Learner"
subject, level, goal = st.session_state.subject, st.session_state.level, st.session_state.goal

# -------------------- Helpers --------------------
def heading(title, subtitle=None):
    st.markdown(f"<h1 style='margin-bottom:0'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='small-muted' style='margin-top:7px'>{subtitle}</p>", unsafe_allow_html=True)

def topic_key(topic):
    return f"{subject}::{level}::{topic}"

def show_topic_progress():
    topics = TOPICS[subject][level]
    done = sum(1 for topic in topics if topic_key(topic) in st.session_state.completed_topics)
    return done, len(topics)

def planner_key(day_number, task):
    return f"{subject}-{level}-{day_number}-{task}"

def get_streak():
    """Count consecutive days with a logged study session, ending today or yesterday."""
    logs = st.session_state.daily_logs
    check_day = date.today()
    if check_day.isoformat() not in logs:
        check_day -= timedelta(days=1)
    streak = 0
    while check_day.isoformat() in logs:
        streak += 1
        check_day -= timedelta(days=1)
    return streak

def next_recommendation():
    current_topics = TOPICS[subject][level]
    for topic in current_topics:
        if topic_key(topic) not in st.session_state.completed_topics:
            attempt_key = f"{subject}::{level}::{topic}"
            attempts = st.session_state.topic_attempts.get(attempt_key, [])
            if attempts and attempts[-1] < 5:
                return topic, "Revise this topic first: your latest check-in was below 50%."
            if attempts and attempts[-1] >= 8:
                return topic, "Your check-in is strong. Mark this topic complete and continue."
            return topic, "Start here, then complete a short practice session."
    return "Review your completed topics", "You have completed this level's roadmap. Try a challenge or review."

# -------------------- Dashboard --------------------
if page == "Dashboard":
    st.markdown(f"""
    <div class="hero">
      <div class="pill">✨ YOUR PERSONAL LEARNING SPACE</div>
      <h1>Welcome back, {name} 👋</h1>
      <p>Build skills one focused session at a time. Your next learning steps are ready.</p>
    </div>
    """, unsafe_allow_html=True)
    done, total = show_topic_progress()
    quiz_score = st.session_state.quiz_results.get(subject)
    quiz_text = f"{quiz_score}/10" if quiz_score is not None else "Not taken"
    planner_done = sum(bool(st.session_state.planner_checks.get(planner_key(i, "done"), False)) for i in range(1, 8))
    today_log = st.session_state.daily_logs.get(date.today().isoformat(), 0)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Topics completed", f"{done}/{total}")
    c2.metric("Current subject", subject)
    c3.metric("Latest quiz score", quiz_text)
    c4.metric("Study streak", f"{get_streak()} 🔥")
    st.markdown("### 🚀 Your learning snapshot")
    left, right = st.columns([1.25, 1])
    next_topic, recommendation = next_recommendation()
    with left:
        st.markdown("<div class='glass-card'><h3>Recommended next step</h3>", unsafe_allow_html=True)
        st.markdown(f"**{next_topic}**")
        st.write(recommendation)
        st.write(f"Your selected goal is **{goal}** at **{level}** level.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='glass-card'><h3>Learning progress</h3>", unsafe_allow_html=True)
        st.progress(done / total if total else 0)
        st.write(f"{round(done / total * 100) if total else 0}% of your {subject} topics completed.")
        st.write(f"Today's logged study time: **{today_log} / {st.session_state.daily_goal_minutes} minutes**")
        st.progress(min(today_log / max(st.session_state.daily_goal_minutes, 1), 1.0))
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("### 🧭 Quick access")
    q1, q2, q3 = st.columns(3)
    q1.markdown("<div class='glass-card'><h3>📖 Learn</h3><p>Explore your personalized roadmap.</p></div>", unsafe_allow_html=True)
    q2.markdown("<div class='glass-card'><h3>📝 Practice</h3><p>Take a quiz and review explanations.</p></div>", unsafe_allow_html=True)
    q3.markdown("<div class='glass-card'><h3>📊 Track</h3><p>Review scores and study consistency.</p></div>", unsafe_allow_html=True)

    for index, topic in enumerate(topics, start=1):
        is_done = topic_key(topic) in st.session_state.completed_topics
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{index:02d} · {topic}**")
            advice = {
                "Theory": "Read the concept, write a short summary, and review an example.",
                "Coding Practice": "Understand the concept, then solve 2–3 small exercises.",
                "Projects": "Connect this topic to a small feature in a mini project.",
            }[goal]
            st.caption(advice)
        with col2:
            checked = st.checkbox("Done", value=is_done, key=f"topic_check_{subject}_{level}_{index}")
            if checked:
                st.session_state.completed_topics.add(topic_key(topic))
            else:
                st.session_state.completed_topics.discard(topic_key(topic))
        st.markdown("</div>", unsafe_allow_html=True)
    done, total = show_topic_progress()
    st.progress(done / total if total else 0)
    st.caption(f"{done} of {total} topics completed for {subject} ({level}).")

    st.markdown("### 🎯 Adaptive topic check-in")
    st.write("Record your score to receive a personalized next step. Repeated low scores trigger extra practice advice.")
    with st.form("topic_score_form"):
        assessed_topic = st.selectbox("Topic you practiced", topics, key="assessed_topic")
        assessed_score = st.slider("Your score (out of 10)", 0, 10, 6, key="assessed_score")
        record_score = st.form_submit_button("Get my recommendation")
    if record_score:
        attempt_key = f"{subject}::{level}::{assessed_topic}"
        st.session_state.topic_attempts.setdefault(attempt_key, []).append(int(assessed_score))
        st.session_state.latest_topic_assessment = {
            "key": attempt_key, "topic": assessed_topic, "score": int(assessed_score),
            "subject": subject, "level": level,
        }
    assessment = st.session_state.get("latest_topic_assessment")
    if assessment and assessment.get("subject") == subject and assessment.get("level") == level:
        attempts = st.session_state.topic_attempts.get(assessment["key"], [])
        score = assessment["score"]
        st.markdown("#### Your personalized next step")
        if score < 5:
            st.warning(f"You scored {score}/10 in **{assessment['topic']}**. Review this topic before moving ahead.")
            st.markdown("- Re-read concept notes and examples.\n- Practice 3–5 simpler questions, then retry.")
            if sum(value < 5 for value in attempts) >= 2:
                st.info("Repeated low scores detected. Break the topic into smaller parts, review a worked example, and retry a short practice set.")
        elif score >= 8:
            upcoming = next((t for t in topics if t != assessment["topic"] and topic_key(t) not in st.session_state.completed_topics), None)
            st.success(f"Strong result: {score}/10. " + (f"Next, consider **{upcoming}**." if upcoming else "Try an advanced challenge or mark this topic complete."))
        else:
            st.info(f"You scored {score}/10 in **{assessment['topic']}**. Review key points and practice a little more.")
        if level == "Beginner":
            st.markdown("**Beginner-friendly resources:**")
            for resource_title, resource_url in RESOURCES[subject][:2]:
                st.markdown(f"- [{resource_title}]({resource_url})")
                st.caption(f"Recorded check-ins for this topic: {len(attempts)}")
                # -------------------- Learning Recommendations --------------------
elif page == "Learning Recommendations":

    heading("🧠 Learning Recommendations", "A roadmap tailored to your subject, level, goal, and recent check-ins.")
    st.markdown(f"<div class='hero'><div class='pill'>{subject.upper()} • {level.upper()}</div><h2>Your personalized roadmap</h2><p>Goal: {goal}. Complete each topic to update your progress.</p></div>", unsafe_allow_html=True)
    topics = TOPICS[subject][level]

    for index, topic in enumerate(topics, start=1):
        is_done = topic_key(topic) in st.session_state.completed_topics
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**{index:02d} · {topic}**")
        with col2:
            checked = st.checkbox("Done", value=is_done, key=f"topic_check_{subject}_{level}_{index}")
            if checked:
                st.session_state.completed_topics.add(topic_key(topic))
            else:
                st.session_state.completed_topics.discard(topic_key(topic))
        st.markdown("</div>", unsafe_allow_html=True)

    try:
        supabase.table("learning_progress").upsert({
            "user_id": st.session_state.user.id,
            "planner_checks": st.session_state.planner_checks,
            "daily_goal_minutes": int(st.session_state.daily_goal_minutes),
            "daily_logs": st.session_state.daily_logs,
            "completed_topics": list(st.session_state.completed_topics),
            "quiz_results": st.session_state.quiz_results,
            "quiz_history": st.session_state.quiz_history,
            "topic_attempts": st.session_state.topic_attempts
        }, on_conflict="user_id").execute()

    except Exception as e:
        st.error(f"Could not save progress: {e}")


        # -------------------- Study Planner --------------------
elif page == "Study Planner":
    heading("📅 7-Day Study Planner", "Check off each day after your study session.")
    daily_topics = TOPICS[subject][level]
    for day_num in range(1, 8):
        topic = daily_topics[(day_num - 1) % len(daily_topics)]
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"**Day {day_num} · {topic}**")
            st.caption("Suggested session: 25 minutes learning + 15 minutes practice + 5 minutes recap.")
        with col2:
            st.checkbox(
                "Complete",
                value=st.session_state.planner_checks.get(
                    planner_key(day_num, "done"), False
                ),
                key=planner_key(day_num, "done")
            )

        st.markdown("</div>", unsafe_allow_html=True)
    completed_days = sum(bool(st.session_state.get(planner_key(i, "done"), False)) for i in range(1, 8))
    st.progress(completed_days / 7)
    st.caption(f"Weekly plan progress: {completed_days}/7 days.")
    for day_num in range(1, 8):
        st.session_state.planner_checks[planner_key(day_num, "done")] = st.session_state.get(planner_key(day_num, "done"), False)

    st.markdown("### ⏱️ Daily study goal")
    st.session_state.daily_goal_minutes = st.slider("Daily goal (minutes)", 10, 180, int(st.session_state.daily_goal_minutes), 5)
    today_key = date.today().isoformat()
    current_minutes = int(st.session_state.daily_logs.get(today_key, 0))
    logged_minutes = st.number_input("Minutes studied today", min_value=0, max_value=600, value=current_minutes, step=5)

    if st.button("Save today's study time"):
        st.session_state.daily_logs[today_key] = int(logged_minutes)
        st.success("Today's study time saved!")
        st.rerun()

    st.caption(f"Current streak: {get_streak()} day(s) 🔥. Your study time is saved.")

    try:
        supabase.table("learning_progress").upsert({
            "user_id": st.session_state.user.id,
            "planner_checks": st.session_state.planner_checks,
            "daily_goal_minutes": int(st.session_state.daily_goal_minutes),
            "daily_logs": st.session_state.daily_logs,
            "completed_topics": list(st.session_state.completed_topics),
            "quiz_results": st.session_state.quiz_results,
            "quiz_history": st.session_state.quiz_history,
            "topic_attempts": st.session_state.topic_attempts
        }, on_conflict="user_id").execute()

    except Exception as e:
        st.error(f"Could not save progress: {e}")
    


# -------------------- Learning Resources --------------------
elif page == "Learning Resources":
    heading("📚 Learning Resources", "Curated resources for each subject.")
    selected_resource_subject = st.selectbox("Choose a subject", list(RESOURCES.keys()), index=list(RESOURCES.keys()).index(subject))
    st.markdown(f"<div class='hero'><div class='pill'>RESOURCE LIBRARY</div><h2>{selected_resource_subject}</h2><p>Learn concepts and practice at your own pace.</p></div>", unsafe_allow_html=True)
    for title, url in RESOURCES[selected_resource_subject]:
        st.markdown(f"<div class='glass-card'><h3>🔗 {title}</h3><p><a href='{url}' target='_blank'>{url}</a></p></div>", unsafe_allow_html=True)

# -------------------- Practice Quiz --------------------
elif page == "Practice Quiz":
    heading("📝 Practice Quiz", "Answer 10 questions, submit, and review the explanations.")
    quiz_subject = st.selectbox("Quiz subject", list(QUIZZES.keys()), index=list(QUIZZES.keys()).index(subject))
    questions = QUIZZES[quiz_subject]
    st.markdown(f"<div class='hero'><div class='pill'>10 QUESTIONS • 10 POINTS</div><h2>{quiz_subject} Knowledge Check</h2><p>Choose one answer for every question.</p></div>", unsafe_allow_html=True)
    with st.form(key=f"quiz_form_{quiz_subject}"):
        answers = []
        for i, (question, options, correct, explanation) in enumerate(questions):
            st.markdown(f"<div class='glass-card'><b>Question {i+1} of 10</b><br>{question}</div>", unsafe_allow_html=True)
            answer = st.radio(f"Select an answer for question {i+1}", options, index=None,
                              key=f"{quiz_subject}_answer_{i}", label_visibility="collapsed")
            answers.append(answer)
            st.write("DEBUG ANSWERS:",answers)
        submit = st.form_submit_button("🚀 Submit Quiz")
    if submit:
        score, chosen_indices = 0, []
        for i, answer in enumerate(answers):
            options = questions[i][1]
            selected_index = options.index(answer) if answer in options else None
            chosen_indices.append(selected_index)
            if selected_index == questions[i][2]:
                score += 1
        st.session_state.quiz_results[quiz_subject] = score
        st.session_state.quiz_answers[quiz_subject] = chosen_indices
        st.session_state.quiz_submissions[quiz_subject] = True
        st.session_state.quiz_history.append({
            "date": date.today().isoformat(), "subject": quiz_subject,
            "score": score, "out_of": 10,
        })
        st.rerun()
    if st.session_state.quiz_submissions.get(quiz_subject, False):
        score = st.session_state.quiz_results.get(quiz_subject, 0)
        chosen = st.session_state.quiz_answers.get(quiz_subject, [])
        st.markdown("---")
        st.markdown(f"<div class='hero'><div class='pill'>QUIZ RESULT</div><h2>Your score: {score}/10</h2><p>{'Excellent work! 🌟' if score >= 9 else 'Great effort! Keep practicing. 💪' if score >= 7 else 'Good start. Review the explanations and try again. 📘'}</p></div>", unsafe_allow_html=True)
        st.progress(score / 10)
        if score < 5:
            st.warning("📘 Recommendation: Revise the basics and try again.")
        elif score < 8:
            st.info("📝 Recommendation: Practice more questions on this subject.")
        else:
            st.success("🚀 Recommendation: You are ready to learn the next topic!")
        for i, (question, options, correct, explanation) in enumerate(questions):
            selected = chosen[i] if i < len(chosen) else None
            if selected == correct:
                st.success(f"Q{i+1}: Correct — {explanation}")
            else:
                selected_text = options[selected] if selected is not None else "Not answered"
                st.error(f"Q{i+1}: Your answer: {selected_text}. Correct answer: {options[correct]}. {explanation}")
        if st.button("🔄 Retake this quiz", key=f"retake_{quiz_subject}"):
            st.session_state.quiz_submissions[quiz_subject] = False
            st.session_state.quiz_results.pop(quiz_subject, None)
            st.session_state.quiz_answers.pop(quiz_subject, None)
            for i in range(10):
                st.session_state.pop(f"{quiz_subject}_answer_{i}", None)
            st.rerun()
            # -------------------- Flashcards --------------------
elif page == "Flashcards":
    heading("🗂️ Flashcards", "Review key concepts. Reveal the answer, then move to another card.")
    cards = FLASHCARDS[subject]
    if cards:
        idx = st.session_state.flashcard_index % len(cards)
        prompt, answer = cards[idx]
        st.markdown(f"<div class='hero'><div class='pill'>CARD {idx + 1} OF {len(cards)}</div><h2>{prompt}</h2><p>Try to recall the answer before revealing it.</p></div>", unsafe_allow_html=True)
        if st.button("👀 Reveal answer", key="reveal_flashcard"):
            st.session_state.flashcard_revealed = True
        if st.session_state.flashcard_revealed:
            st.success(answer)
        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.button("⬅️ Previous card"):
                st.session_state.flashcard_index = (idx - 1) % len(cards)
                st.session_state.flashcard_revealed = False
                st.rerun()
        with next_col:
            if st.button("Next card ➡️"):
                st.session_state.flashcard_index = (idx + 1) % len(cards)
                st.session_state.flashcard_revealed = False
                st.rerun()

# -------------------- Study Assistant --------------------
elif page == "Study Assistant":
    heading("🤖 Study Assistant", "A built-in study guide using your selected subject, level, goal, and recorded progress.")
    question = st.text_area("What would you like help with?", placeholder="For example: What should I study next? How can I improve my quiz score?")
    if st.button("Get study guidance"):
        st.session_state.study_assistant_question = question.strip()
    if st.session_state.study_assistant_question:
        q = st.session_state.study_assistant_question.lower()
        next_topic, advice = next_recommendation()
        latest_score = st.session_state.quiz_results.get(subject)
        st.markdown("### Your study guidance")
        if any(word in q for word in ["next", "recommend", "study", "topic"]):
            st.info(f"**Suggested next topic: {next_topic}**\n\n{advice}\n\nYour goal is **{goal}**, so use the matching approach: " +
                    ("summarize the concept and examples." if goal == "Theory" else
                     "solve a few focused exercises." if goal == "Coding Practice" else
                     "build a small project feature."))
        elif any(word in q for word in ["score", "quiz", "improve", "weak"]):
            if latest_score is None:
                st.info("Take a quiz first. Your score and explanations will help personalize the next recommendation.")
            elif latest_score < 5:
                st.warning(f"Your latest {subject} score is {latest_score}/10. Revisit foundational topics, review each explanation, and retry after practice.")
            elif latest_score < 8:
                st.info(f"Your latest {subject} score is {latest_score}/10. Review missed answers and complete a short practice session.")
            else:
                st.success(f"Your latest {subject} score is {latest_score}/10. Try the next roadmap topic or a small challenge.")
        elif any(word in q for word in ["resource", "link", "learn"]):
            st.write("Here are resources for your selected subject:")
            for title, url in RESOURCES[subject]:
                st.markdown(f"- [{title}]({url})")
        else:
            st.write(f"For **{subject} ({level})**, start with **{next_topic}**. {advice}")
            st.caption("This built-in assistant uses simple rules; it is not connected to a live generative AI model.")

# -------------------- My Progress --------------------
elif page == "My Progress":
    heading("📊 My Progress", "Review completion, quiz performance, study consistency, and achievements.")
    done, total = show_topic_progress()
    attempts_count = len(st.session_state.quiz_history)
    scores = [item["score"] for item in st.session_state.quiz_history]
    average = sum(scores) / len(scores) if scores else 0
    planner_done = sum(bool(st.session_state.planner_checks.get(planner_key(i, "done"), False)) for i in range(1, 8))
    a, b, c, d = st.columns(4)
    a.metric("Topics completed", f"{done}/{total}")
    b.metric("Quiz attempts", attempts_count)
    c.metric("Average quiz score", f"{average:.1f}/10" if scores else "—")
    d.metric("Study streak", f"{get_streak()} 🔥")
    st.markdown("### 📈 Quiz performance")
    if st.session_state.quiz_history:
        score_df = pd.DataFrame(st.session_state.quiz_history)
        fig = px.line(score_df, x=score_df.index + 1, y="score", color="subject",
                      markers=True, range_y=[0, 10], title="Quiz score history")
        fig.update_layout(
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            font_color="#334155", title_font_color="#1E293B",
            xaxis_title="Attempt", yaxis_title="Score (out of 10)",
            xaxis=dict(gridcolor="#E2E8F0"), yaxis=dict(gridcolor="#E2E8F0"),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("#### Recent quiz attempts")
        st.dataframe(score_df.sort_index(ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("Take a quiz to see your score history here.")
    st.markdown("### 🏆 Achievements")
    badges = [
        ("🌱 First Steps", len(st.session_state.completed_topics) >= 1, "Complete your first learning topic."),
        ("📚 Topic Explorer", len(st.session_state.completed_topics) >= 5, "Complete five topics."),
        ("📝 Quiz Starter", attempts_count >= 1, "Submit your first quiz."),
        ("🎯 High Scorer", any(score >= 8 for score in scores), "Score 8 or more in a quiz."),
        ("📅 Weekly Learner", planner_done >= 7, "Complete all seven study-plan days."),
        ("🔥 Consistent Learner", get_streak() >= 3, "Log study time on three consecutive days."),
    ]
    cols = st.columns(len(badges))
    for col, (badge_name, earned, description) in zip(cols, badges):
        with col:
            if earned:
                st.markdown(f"<div class='glass-card' style='text-align:center'><h3>{badge_name}</h3><p>Unlocked ✨</p><span class='small-muted'>{description}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='glass-card' style='text-align:center;opacity:.65'><h3>🔒 {badge_name}</h3><p>Locked</p><span class='small-muted'>{description}</span></div>", unsafe_allow_html=True)
    st.markdown("### 🧾 Topic completion")
    st.progress(done / total if total else 0)
    st.caption(f"{done} out of {total} topics completed in the selected subject and level.")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#64748B;font-size:.82rem'>"
    "LearnWise AI · Personalized Learning Recommendation System · Student Prototype"
    "</div>",
    unsafe_allow_html=True,
)
