import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# ------------------------------------------------------------
# LearnWise AI - Personalized Learning Recommendation System
# Beginner-friendly Streamlit prototype
# ------------------------------------------------------------

st.set_page_config(
    page_title="LearnWise AI | Personalized Learning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
      radial-gradient(ellipse at 8% 0%, rgba(62, 119, 191, .16), transparent 38%),
      radial-gradient(ellipse at 92% 12%, rgba(104, 94, 190, .10), transparent 32%),
      linear-gradient(145deg, #0b1220 0%, #101a2b 52%, #0c1422 100%);
    color: #f4f6ff;
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111d30 0%, #0d1728 100%);
    border-right: 1px solid rgba(148,163,184,.14);
}
.block-container { padding-top: 1.8rem; padding-bottom: 2.5rem; max-width: 1300px; }
h1, h2, h3 { color: #f7f8ff !important; letter-spacing: -.03em; }
p, label, li { color: #d8def6; }
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(148,163,184,.16);
    padding: 18px 20px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,.12);
}
div[data-testid="stMetric"] label { color: #aeb9df !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #ffffff !important; }
.glass-card {
    background: linear-gradient(145deg, rgba(255,255,255,.065), rgba(255,255,255,.025));
    border: 1px solid rgba(148,163,184,.16);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 14px 38px rgba(0,0,0,.15);
    margin-bottom: 14px;
}
.hero {
    background: linear-gradient(115deg, rgba(55,105,170,.24), rgba(91,85,160,.10));
    border: 1px solid rgba(148,163,184,.20);
    border-radius: 26px;
    padding: 30px;
    margin-bottom: 22px;
}
.hero h1 { font-size: 2.5rem; margin: 0; }
.hero p { color: #d9e1ff; font-size: 1.05rem; margin-top: 10px; }
.small-muted { color: #aab5dc; font-size: .9rem; }
.pill {
    display: inline-block; border-radius: 999px; padding: 5px 11px;
    background: rgba(83,130,190,.15); border: 1px solid rgba(130,170,220,.22);
    color: #dceaff; font-size: .78rem; margin: 2px;
}
div.stButton > button, div.stFormSubmitButton > button {
    border-radius: 12px; border: 1px solid rgba(180,190,255,.28);
    background: linear-gradient(100deg, #416b9f, #397fbd);
    color: white; font-weight: 700; padding: .62rem 1.1rem;
}
div.stButton > button:hover, div.stFormSubmitButton > button:hover {
    border-color: #a8c9e8; color: white; filter: brightness(1.08);
}
div[data-testid="stProgress"] > div > div { background: linear-gradient(90deg,#547eae,#79b7d8); }
hr { border-color: rgba(180,190,255,.16); }
a { color: #9fdcff !important; }
[data-testid="stRadio"] label { color: #edf0ff !important; }
.stAlert { border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

# -------------------- Question bank --------------------
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
    "Artificial Intelligence": [
        ("Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course"),
        ("IBM AI resources", "https://www.ibm.com/think/topics/artificial-intelligence"),
        ("Elements of AI", "https://www.elementsofai.com/"),
    ],
}

# -------------------- Session state --------------------
defaults = {
    "student_name": "Learner",
    "subject": "Python",
    "level": "Beginner",
    "goal": "Coding Practice",
    "planner_checks": {},
    "completed_topics": set(),
    "quiz_results": {},
    "quiz_submissions": {},
    "quiz_answers": {},
    "topic_attempts": {},
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🧠 LearnWise AI")
    st.caption("Your personalized learning companion")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Learning Recommendations", "Study Planner", "Learning Resources", "Practice Quiz", "My Progress"],
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
subject = st.session_state.subject
level = st.session_state.level
goal = st.session_state.goal

# -------------------- Helpers --------------------
def heading(title, subtitle=None):
    st.markdown(f"<h1 style='margin-bottom:0'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='small-muted' style='margin-top:7px'>{subtitle}</p>", unsafe_allow_html=True)

def topic_key(topic):
    return f"{subject}::{level}::{topic}"

def all_topics_count():
    return sum(len(level_topics) for levels in TOPICS.values() for level_topics in levels.values())

def show_topic_progress():
    topics = TOPICS[subject][level]
    done = sum(1 for t in topics if topic_key(t) in st.session_state.completed_topics)
    return done, len(topics)

def planner_key(day_number, task):
    return f"{subject}-{level}-{day_number}-{task}"

def quiz_key(subject_name):
    return f"quiz_{subject_name}"

# -------------------- Pages --------------------
if page == "Dashboard":
    st.markdown(f"""
    <div class="hero">
      <div class="pill">✨ YOUR PERSONAL AI LEARNING SPACE</div>
      <h1>Welcome back, {name} 👋</h1>
      <p>Build skills one focused session at a time. Your next learning steps are ready.</p>
    </div>
    """, unsafe_allow_html=True)

    done, total = show_topic_progress()
    quiz_score = st.session_state.quiz_results.get(subject, None)
    quiz_text = f"{quiz_score}/10" if quiz_score is not None else "Not taken"
    planner_done = sum(1 for i in range(1, 8) if st.session_state.planner_checks.get(planner_key(i, "done"), False))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Topics completed", f"{done}/{total}")
    c2.metric("Current subject", subject)
    c3.metric("Latest quiz score", quiz_text)
    c4.metric("Study plan", f"{planner_done}/7 days")

    st.markdown("### 🚀 Your learning snapshot")
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("<div class='glass-card'><h3>Recommended next step</h3>", unsafe_allow_html=True)
        next_topic = next((t for t in TOPICS[subject][level] if topic_key(t) not in st.session_state.completed_topics), "Review your completed topics")
        st.markdown(f"**{next_topic}**")
        st.write(f"Focus on this topic based on your selected level: **{level}** and goal: **{goal}**.")
        if st.button("Open learning recommendations", key="dash_recommend"):
            st.session_state["page_jump"] = "Learning Recommendations"
            st.info("Choose Learning Recommendations from the sidebar to continue.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='glass-card'><h3>Learning progress</h3>", unsafe_allow_html=True)
        st.progress(done / total if total else 0)
        st.write(f"{round(done / total * 100) if total else 0}% of your {subject} topics completed.")
        st.markdown("<span class='pill'>Keep going</span> <span class='pill'>Small steps matter</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🧭 Quick access")
    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown("<div class='glass-card'><h3>📖 Learn</h3><p>Explore a personalized topic roadmap.</p></div>", unsafe_allow_html=True)
    with q2:
        st.markdown("<div class='glass-card'><h3>📝 Practice</h3><p>Test your knowledge with a 10-question quiz.</p></div>", unsafe_allow_html=True)
    with q3:
        st.markdown("<div class='glass-card'><h3>📊 Track</h3><p>Review scores and completed study sessions.</p></div>", unsafe_allow_html=True)

elif page == "Learning Recommendations":
    heading("🧠 Learning Recommendations", "A simple rules-based roadmap tailored to your subject, level, and learning goal.")
    st.markdown(f"<div class='hero'><div class='pill'>{subject.upper()} • {level.upper()}</div><h2>Your personalized roadmap</h2><p>Goal: {goal}. Complete each topic and mark it finished to update your progress.</p></div>", unsafe_allow_html=True)
    topics = TOPICS[subject][level]
    for index, topic in enumerate(topics, start=1):
        is_done = topic_key(topic) in st.session_state.completed_topics
        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{index:02d} · {topic}**")
                advice = {
                    "Theory": "Read the concept, write a short summary, and review an example.",
                    "Coding Practice": "Understand the concept, then solve 2–3 small coding exercises.",
                    "Projects": "Connect this topic to a small feature in a mini project.",
                }[goal]
                st.caption(advice)
            with col2:
                if st.checkbox("Done", value=is_done, key=f"topic_check_{subject}_{level}_{index}"):
                    st.session_state.completed_topics.add(topic_key(topic))
                else:
                    st.session_state.completed_topics.discard(topic_key(topic))
            st.markdown("</div>", unsafe_allow_html=True)
    done, total = show_topic_progress()
    st.progress(done / total if total else 0)
    st.caption(f"{done} of {total} topics completed for {subject} ({level}).")

    st.markdown("### 🎯 Adaptive topic check-in")
    st.write("Record a topic score to get a next-step recommendation. Repeated low scores trigger extra practice advice.")
    topic_options = TOPICS[subject][level]
    with st.form("topic_score_form"):
        assessed_topic = st.selectbox("Topic you practiced", topic_options, key="assessed_topic")
        assessed_score = st.slider("Your score (out of 10)", min_value=0, max_value=10, value=6, key="assessed_score")
        record_score = st.form_submit_button("Get my recommendation")
    if record_score:
        attempt_key = f"{subject}::{level}::{assessed_topic}"
        st.session_state.topic_attempts.setdefault(attempt_key, []).append(int(assessed_score))
        st.session_state["latest_topic_assessment"] = {"key": attempt_key, "topic": assessed_topic, "score": int(assessed_score), "subject": subject, "level": level}

    assessment = st.session_state.get("latest_topic_assessment")
    if assessment and assessment.get("subject") == subject and assessment.get("level") == level:
        attempts = st.session_state.topic_attempts.get(assessment["key"], [])
        score = assessment["score"]
        st.markdown("#### Your personalized next step")
        if score < 5:
            st.warning(f"You scored {score}/10 in **{assessment['topic']}**. Review this topic before moving ahead.")
            st.markdown("- Re-read the concept notes and examples.")
            st.markdown("- Practice 3–5 simpler questions, then try the topic check-in again.")
            if len([value for value in attempts if value < 5]) >= 2:
                st.info("You have scored below 50% more than once on this topic. Extra practice is recommended: break the topic into smaller parts, review a worked example, and retry a short practice set.")
        elif score >= 8:
            next_topic = next((t for t in topic_options if t != assessment["topic"] and topic_key(t) not in st.session_state.completed_topics), None)
            if next_topic:
                st.success(f"Strong result: {score}/10. You can move on to **{next_topic}** next.")
            else:
                st.success(f"Strong result: {score}/10. Consider an advanced challenge or mark **{assessment['topic']}** complete.")
        else:
            st.info(f"You scored {score}/10 in **{assessment['topic']}**. Review the key points and do a little more practice before moving on.")
        if level == "Beginner":
            st.markdown("**Beginner-friendly resources:** start with the simple explanation and examples, then practice. Use the resources below:")
            for resource_title, resource_url in RESOURCES[subject][:2]:
                st.markdown(f"- [{resource_title}]({resource_url})")
        st.caption(f"Recorded check-ins for this topic: {len(attempts)}")

elif page == "Study Planner":
    heading("📅 7-Day Study Planner", "A practical weekly plan. Check off each day when you finish your study session.")
    daily_topics = TOPICS[subject][level]
    for day_num in range(1, 8):
        topic = daily_topics[(day_num - 1) % len(daily_topics)]
        plan_label = f"Day {day_num} · {topic}"
        k = planner_key(day_num, "done")
        with st.container():
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{plan_label}**")
                st.caption("Suggested session: 25 minutes learning + 15 minutes practice + 5 minutes recap.")
            with col2:
                st.checkbox("Complete", key=k)
            st.markdown("</div>", unsafe_allow_html=True)
    completed_days = sum(1 for i in range(1, 8) if st.session_state.get(planner_key(i, "done"), False))
    st.progress(completed_days / 7)
    st.caption(f"Weekly plan progress: {completed_days}/7 days.")
    # Keep checkbox state in a compact session mapping
    for day_num in range(1, 8):
        st.session_state.planner_checks[planner_key(day_num, "done")] = st.session_state.get(planner_key(day_num, "done"), False)

elif page == "Learning Resources":
    heading("📚 Learning Resources", "Curated beginner-friendly resources for each subject.")
    selected_resource_subject = st.selectbox("Choose a subject", list(RESOURCES.keys()), index=list(RESOURCES.keys()).index(subject))
    st.markdown(f"<div class='hero'><div class='pill'>RESOURCE LIBRARY</div><h2>{selected_resource_subject}</h2><p>Use these resources to learn concepts and practice at your own pace.</p></div>", unsafe_allow_html=True)
    for title, url in RESOURCES[selected_resource_subject]:
        st.markdown(f"<div class='glass-card'><h3>🔗 {title}</h3><p><a href='{url}' target='_blank'>{url}</a></p></div>", unsafe_allow_html=True)

elif page == "Practice Quiz":
    heading("📝 Practice Quiz", "Choose a subject, answer 10 questions, and submit to see your result.")
    quiz_subject = st.selectbox("Quiz subject", list(QUIZZES.keys()), index=list(QUIZZES.keys()).index(subject))
    questions = QUIZZES[quiz_subject]
    st.markdown(f"<div class='hero'><div class='pill'>10 QUESTIONS • 10 POINTS</div><h2>{quiz_subject} Knowledge Check</h2><p>Choose one answer for every question. Your score and explanations appear after submission.</p></div>", unsafe_allow_html=True)
    submitted = st.session_state.quiz_submissions.get(quiz_subject, False)
    with st.form(key=f"quiz_form_{quiz_subject}"):
        answers = []
        for i, (question, options, correct, explanation) in enumerate(questions):
            st.markdown(f"<div class='glass-card'><b>Question {i+1} of 10</b><br>{question}</div>", unsafe_allow_html=True)
            answer = st.radio(
                f"Select an answer for question {i+1}",
                options,
                index=None,
                key=f"{quiz_subject}_answer_{i}",
                label_visibility="collapsed",
            )
            answers.append(answer)
        submit = st.form_submit_button("🚀 Submit Quiz")
    if submit:
        score = 0
        chosen_indices = []
        for i, answer in enumerate(answers):
            options = questions[i][1]
            selected_index = options.index(answer) if answer in options else None
            chosen_indices.append(selected_index)
            if selected_index == questions[i][2]:
                score += 1
        st.session_state.quiz_results[quiz_subject] = score
        st.session_state.quiz_answers[quiz_subject] = chosen_indices
        st.session_state.quiz_submissions[quiz_subject] = True
        st.rerun()

    if st.session_state.quiz_submissions.get(quiz_subject, False):
        score = st.session_state.quiz_results.get(quiz_subject, 0)
        chosen = st.session_state.quiz_answers.get(quiz_subject, [])
        st.markdown("---")
        st.markdown(f"<div class='hero'><div class='pill'>QUIZ RESULT</div><h2>Your score: {score}/10</h2><p>{'Excellent work! 🌟' if score >= 9 else 'Great effort! Keep practicing. 💪' if score >= 7 else 'Good start. Review the explanations and try again. 📘'}</p></div>", unsafe_allow_html=True)
        st.progress(score / 10)
        if score < 5:
            st.warning("📘 Recommendation: Revise the basics of this topic and try again.")

        elif score < 8:
            st.info("📝 Recommendation: Practice more questions on this topic.")

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

elif page == "My Progress":
    heading("📊 My Progress", "See your learning completion, quiz performance, and achievements.")
    done, total = show_topic_progress()
    total_quizzes = len(st.session_state.quiz_results)
    scores = list(st.session_state.quiz_results.values())
    average = sum(scores) / len(scores) if scores else 0
    planner_done = sum(1 for i in range(1, 8) if st.session_state.planner_checks.get(planner_key(i, "done"), False))
    a, b, c, d = st.columns(4)
    a.metric("Topics completed", f"{done}/{total}")
    b.metric("Quiz attempts", total_quizzes)
    c.metric("Average quiz score", f"{average:.1f}/10" if scores else "—")
    d.metric("Study days completed", f"{planner_done}/7")

    st.markdown("### 📈 Quiz performance")
    if st.session_state.quiz_results:
        score_df = pd.DataFrame({"Subject": list(st.session_state.quiz_results.keys()), "Score": list(st.session_state.quiz_results.values())})
        fig = px.bar(score_df, x="Subject", y="Score", range_y=[0, 10], text="Score", title="Latest quiz score by subject")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e9edff", title_font_color="#ffffff",
            xaxis=dict(gridcolor="rgba(180,190,255,.10)"),
            yaxis=dict(gridcolor="rgba(180,190,255,.10)"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Take a quiz to see your score chart here.")

    st.markdown("### 🏆 Achievements")
    badges = [
        ("🌱 First Steps", len(st.session_state.completed_topics) >= 1, "Complete your first learning topic."),
        ("📚 Topic Explorer", len(st.session_state.completed_topics) >= 5, "Complete five topics."),
        ("📝 Quiz Starter", len(st.session_state.quiz_results) >= 1, "Submit your first quiz."),
        ("🎯 High Scorer", any(score >= 8 for score in st.session_state.quiz_results.values()), "Score 8 or more in a quiz."),
        ("📅 Weekly Learner", planner_done >= 7, "Complete all seven study-plan days."),
    ]
    cols = st.columns(len(badges))
    for col, (badge_name, earned, description) in zip(cols, badges):
        with col:
            if earned:
                st.markdown(f"<div class='glass-card' style='text-align:center'><h3>{badge_name}</h3><p>Unlocked ✨</p><span class='small-muted'>{description}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='glass-card' style='text-align:center;opacity:.55'><h3>🔒 {badge_name}</h3><p>Locked</p><span class='small-muted'>{description}</span></div>", unsafe_allow_html=True)

    st.markdown("### 🧾 Topic completion")
    st.progress(done / total if total else 0)
    st.caption(f"{done} out of {total} topics completed in the selected subject and level.")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#9ca9d2;font-size:.82rem'>"
    "LearnWise AI · Personalized Learning Recommendation System · Student Prototype"
    "</div>",
    unsafe_allow_html=True,
)
