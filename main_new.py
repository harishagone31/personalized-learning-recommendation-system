print("=" * 45)
print("PERSONALIZED LEARNING RECOMMENDATION SYSTEM")
print("=" * 45)

name = input("\nEnter your name: ")

print("\nChoose a subject:")
print("1. Python")
print("2. Java")
print("3. Data Structures")
print("4. Artificial Intelligence")

choice = input("Enter your choice (1-4): ")

print("\nChoose your learning level:")
print("1. Beginner")
print("2. Intermediate")
print("3. Advanced")

level = input("Enter your level (1-3): ")

print("\nWhat do you want to improve?")
print("1. Theory")
print("2. Coding Practice")
print("3. Projects")

goal = input("Enter your goal (1-3): ")

subjects = {
    "1": "Python",
    "2": "Java",
    "3": "Data Structures",
    "4": "Artificial Intelligence"
}

levels = {
    "1": "Beginner",
    "2": "Intermediate",
    "3": "Advanced"
}

goals = {
    "1": "Theory",
    "2": "Coding Practice",
    "3": "Projects"
}

print("\n" + "=" * 45)
print("YOUR PERSONALIZED LEARNING PLAN")
print("=" * 45)

if choice in subjects and level in levels and goal in goals:
    print("Student:", name)
    print("Subject:", subjects[choice])
    print("Level:", levels[level])
    print("Learning goal:", goals[goal])

    # Subject-specific recommendation
    if choice == "1":
        print("Subject resource: Practice Python programs.")
    elif choice == "2":
        print("Subject resource: Practice Java programs.")
    elif choice == "3":
        print("Subject resource: Practice data structure problems.")
    elif choice == "4":
        print("Subject resource: Learn AI concepts and build AI projects.")

    # Level-based recommendation
    if level == "1":
        print("Level recommendation: Start with basic concepts.")
    elif level == "2":
        print("Level recommendation: Practice intermediate exercises.")
    else:
        print("Level recommendation: Solve advanced problems.")

    # Goal-based recommendation
    if goal == "1":
        print("Learning resource: Read theory notes.")
    elif goal == "2":
        print("Learning resource: Solve coding exercises.")
    else:
        print("Learning resource: Build a small practical project.")

    print("\nYour personalized learning plan is ready!")
    print("Keep practicing to improve your skills!")

else:
    print("Invalid choice. Please run the program again.")

print("=" * 45)