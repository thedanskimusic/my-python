#!/usr/bin/env python3
"""
My Python Learning Project
"""

def main():
    print("Hello, Python!")
    print("Welcome to your learning journey!")
    
    # Example: Working with variables
    name = "Python Learner"
    age = 0  # Just starting!
    
    print(f"\nHi, I'm {name} and I'm {age} years into learning Python!")
    
    # Example: Working with lists
    topics = ["variables", "functions", "loops", "data structures"]
    print(f"\nTopics to learn: {', '.join(topics)}")
    
    # Example: Simple loop
    print("\nCounting to 5:")
    for i in range(1, 6):
        print(f"  {i}")

if __name__ == "__main__":
    main()

