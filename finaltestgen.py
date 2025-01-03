import tkinter as tk
from tkinter import messagebox, scrolledtext

# Sample questions list
questions = [
    {
        "question": "01.Guillermo is the system administrator for a midsized retail organization. Guillermo has been tasked with writing a document that describes, step-by-step, how to securely install the operating system on a new laptop. This document is an example of a ________.",
        "options": ["A. Policy", "B. Standard", "C. Guideline", "D. Procedure"],
        "correct_answer": ["D"]
    },
    {
        "question": "02. A common network device used to filter traffic.",
        "options": ["A. Server", "B. Endpoint", "C. Ethernet", "D. Firewall"],
        "correct_answer": ["D"]
    },
    {
        "question": "03. A set of security controls or system settings used to ensure uniformity of configuration through the IT environment.",
        "options": ["A. Patches", "B. Inventory", "C. Baseline", "D. Policy"],
        "correct_answer": ["C"]
    },
    {
        "question": "04. Who is responsible for publishing and signing the organization’s policies?",
        "options": ["A. The security office", "B. Human resources", "C. The legal department", "D. Senior management"],
        "correct_answer": ["D"]
    },
    {
        "question": "05. What is meant by non-repudiation?",
        "options": [
            "A. If a user does something, they can’t later claim that they didn’t do it.",
            "B. Controls to protect the organization’s reputation from harm due to inappropriate social media postings by employees, even if on their private accounts and personal time.",
            "C. It is part of the rules set by administrative controls.",
            "D. It is a security feature that prevents session replay attacks."
        ],
        "correct_answer": ["A"]
    },
    {
        "question": "06. Which of these components is very likely to be instrumental to any disaster recovery (DR) effort?",
        "options": ["A. Routers", "B. Laptops", "C. Firewalls", "D. Backups"],
        "correct_answer": ["D"]
    },
    {
        "question": "07. Which of the following is a subject?",
        "options": ["A. A file", "B. A fence", "C. A user", "D. A filename"],
        "correct_answer": ["C"]
    },
    {
        "question": "08. Is it possible to avoid risk?",
        "options": ["A. Yes", "B. No", "C. Sometimes", "D. Never"],
        "correct_answer": ["A"]
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Simulator")

        # Initialize variables
        self.question_index = 0
        self.user_answers = [[] for _ in questions]

        # Create widgets
        self.question_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.option_vars = []
        self.option_labels = []  # To store option labels for color modification
        for i in range(4):
            var = tk.BooleanVar()
            option = tk.Checkbutton(root, text="", variable=var, font=("Arial", 10), onvalue=True, offvalue=False,
                                    command=lambda i=i: self.update_colors(i))  # Add command to update colors
            option.pack(anchor="w", padx=20)
            self.option_vars.append((var, option))
            self.option_labels.append(option)

        self.prev_button = tk.Button(root, text="Previous", command=self.prev_question, state="disabled")
        self.prev_button.pack(side="left", padx=20, pady=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(side="left", padx=20)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_quiz, state="disabled")
        self.submit_button.pack(side="right", padx=20)

        # Timer label
        self.timer_label = tk.Label(root, text="Time Remaining: 00:00", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        # Time selection window
        self.set_time_window()

    def set_time_window(self):
        # Create a new window for selecting time
        time_window = tk.Toplevel(self.root)
        time_window.title("Select Time Limit")

        tk.Label(time_window, text="Select time for the quiz:").pack(pady=10)

        # Create time options
        time_options = [("1 Hour", 3600), ("2 Hours", 7200), ("3 Hours", 10800), ("1/2 Hour", 1800)]

        for label, time in time_options:
            button = tk.Button(time_window, text=label, command=lambda time=time: self.set_time(time, time_window))
            button.pack(pady=5)

    def set_time(self, time_limit, time_window):
        # Set the selected time and close the time selection window
        self.timer_seconds = time_limit
        self.update_timer()
        time_window.destroy()
        self.show_question()

    def update_timer(self):
        # Update the timer label
        if self.timer_seconds > 0:
            minutes, seconds = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)  # Update every second
        else:
            self.submit_quiz()  # Automatically submit the quiz when time is up

    def show_question(self):
        question_data = questions[self.question_index]

        # Update question label
        self.question_label.config(text=question_data["question"])

        # Update options
        for i, option_text in enumerate(question_data["options"]):
            self.option_vars[i][1].config(text=option_text, state="normal")
            self.option_vars[i][0].set(False)  # Reset each option's check status
            self.option_labels[i].config(fg="black")  # Reset the color to black when showing a new question

        # Disable unused options
        for i in range(len(question_data["options"]), 4):
            self.option_vars[i][1].config(text="", state="disabled")

        # Set selected answer if previously answered
        if self.user_answers[self.question_index]:
            for i, (var, _) in enumerate(self.option_vars):
                var.set(question_data["options"][i][0] in self.user_answers[self.question_index])

        # Update button states
        self.prev_button.config(state="normal" if self.question_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.question_index < len(questions) - 1 else "disabled")
        self.submit_button.config(state="normal" if self.question_index == len(questions) - 1 else "disabled")

    def prev_question(self):
        if self.question_index > 0:
            self.save_answer()
            self.question_index -= 1
            self.show_question()

    def next_question(self):
        self.save_answer()  # Save the answer before moving to the next question
        if self.question_index < len(questions) - 1:
            self.question_index += 1
            self.show_question()

    def save_answer(self):
        self.user_answers[self.question_index] = []
        for i, (var, _) in enumerate(self.option_vars):
            if var.get():
                self.user_answers[self.question_index].append(questions[self.question_index]["options"][i][0])

    def update_colors(self, option_index):
        question_data = questions[self.question_index]
        correct_answers = question_data["correct_answer"]

        # For each option, check if it's selected and apply the color
        for i, (var, option) in enumerate(self.option_vars):
            if var.get():  # If option is selected
                if question_data["options"][i][0] in correct_answers:
                    option.config(fg="green")  # Correct answer
                else:
                    option.config(fg="red")  # Incorrect answer
            else:
                option.config(fg="black")  # Default color when not selected

        # Lock options that are not selected
        for i, (var, option) in enumerate(self.option_vars):
            if not var.get():  # If the option is not selected
                option.config(state="disabled")  # Lock the option
            else:
                option.config(state="normal")  # Keep the selected option enabled

    def submit_quiz(self):
        self.save_answer()

        score = 0
        for i, question in enumerate(questions):
            correct_answers = question["correct_answer"]
            user_answer = self.user_answers[i]
            if isinstance(correct_answers, list):
                if sorted(user_answer) == sorted(correct_answers):
                    score += 1
            else:
                if user_answer == [correct_answers]:
                    score += 1

        # Create result window
        result_window = tk.Toplevel(self.root)
        result_window.title("Quiz Results")

        # Create a scrolled text box for results
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
        result_text.pack(padx=10, pady=10)

        result_text.insert(tk.END, f"Your Score: {score}/{len(questions)}\n\n")
        result_text.insert(tk.END, "Your Answers:\n")

        for i, question in enumerate(questions):
            result_text.insert(tk.END, f"{i + 1}. {question['question']}\n")
            result_text.insert(tk.END, f"Options: {', '.join(question['options'])}\n")
            result_text.insert(tk.END, f"Your answer(s): {', '.join(self.user_answers[i]) if self.user_answers[i] else 'None'}\n")
            result_text.insert(tk.END, f"Correct answer(s): {', '.join(question['correct_answer'])}\n\n")

        result_text.config(state=tk.DISABLED)  # Make the text box read-only

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
