import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def get_user_input(question, root):
    question_window = tk.Toplevel(root)
    question_window.title(question)

    label = tk.Label(question_window, text=question)
    label.pack(pady=10)

    answer_var = tk.StringVar(value='no')

    yes_button = tk.Radiobutton(question_window, text="Yes", variable=answer_var, value='yes')
    yes_button.pack()

    no_button = tk.Radiobutton(question_window, text="No", variable=answer_var, value='no')
    no_button.pack()

    def submit():
        question_window.destroy()
        responses.append(answer_var.get())

    submit_button = tk.Button(question_window, text="Submit", command=submit)
    submit_button.pack(pady=10)

    question_window.wait_window()

def assess_vulnerability(responses):
    score = 0
    strengths = []
    weaknesses = []

    assessment_criteria = {
        'Do you use unique passwords for each of your accounts?': "Using unique passwords",
        'Do you use a password manager?': "Using a password manager",
        'Do you enable two-factor authentication on your important accounts?': "Enabling two-factor authentication",
        'Do you use antivirus software on your devices?': "Using antivirus software",
        'Have you ever clicked on a suspicious link in an email or message?': "Being aware of phishing attempts",
        'Do you often share personal information on social media?': "Not sharing personal info on social media",
        'Do you regularly update your software and apps?': "Regularly updating software and apps",
        'Are you aware of how to recognize a phishing email?': "Aware of how to recognize phishing emails",
        'Do you log out of accounts when using public computers?': "Logging out of accounts on public computers",
        'Do you review your privacy settings on social media regularly?': "Reviewing privacy settings on social media regularly"
    }

    for question, strength in assessment_criteria.items():
        answer = responses.pop(0)  # Get the answer and remove it from the list
        if answer == 'yes':
            score += 1
            strengths.append(strength)
        else:
            weaknesses.append(f"Not {strength.lower()}")

    return score, strengths, weaknesses

def recommend_resources(weaknesses):
    recommendations = []
    if "Not using unique passwords" in weaknesses:
        recommendations.append("Use a password manager: [LastPass](https://www.lastpass.com/)")
    if "Not enabling two-factor authentication" in weaknesses:
        recommendations.append("Learn about two-factor authentication: [2FA Guide](https://www.twilio.com/docs/verify/2fa)")
    if "Not using antivirus software" in weaknesses:
        recommendations.append("Recommended antivirus: [Norton](https://us.norton.com/) or [McAfee](https://www.mcafee.com/)")
    if "Not being aware of phishing attempts" in weaknesses:
        recommendations.append("Learn to recognize phishing: [Phishing Awareness](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams)")
    if "Not logging out of accounts on public computers" in weaknesses:
        recommendations.append("Always log out of accounts when using public computers.")

    return recommendations

def show_results(score, strengths, weaknesses):
    results_window = tk.Toplevel()
    results_window.title("Assessment Results")

    # Vulnerability Level
    if score <= 3:
        level = "High"
    elif score <= 6:
        level = "Medium"
    elif score <= 9:
        level = "Low"
    else:
        level = "Very Low"

    messagebox.showinfo("Assessment Results", f"Vulnerability Level: {level}")

    # Display Strengths and Weaknesses
    results_text = f"Strengths:\n" + "\n".join(strengths) + "\n\nWeaknesses:\n" + "\n".join(weaknesses)
    results_label = tk.Label(results_window, text=results_text, justify='left')
    results_label.pack(pady=10)

    # Recommendations
    recommendations = recommend_resources(weaknesses)
    if recommendations:
        recommendations_label = tk.Label(results_window, text="Recommended Resources:")
        recommendations_label.pack(pady=5)

        for recommendation in recommendations:
            rec_label = tk.Label(results_window, text=f"- {recommendation}", justify='left')
            rec_label.pack()

    # Display Statistics
    stats_text = f"\nStatistics:\nTotal Questions: 10\nScore: {score}/10\n"
    stats_label = tk.Label(results_window, text=stats_text)
    stats_label.pack(pady=10)

    # Create and display the chart
    strengths_count = len(strengths)
    weaknesses_count = len(weaknesses)

    labels = ['Strengths', 'Weaknesses']
    sizes = [strengths_count, weaknesses_count]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, sizes, color=['green', 'red'])
    plt.title('Strengths vs Weaknesses')
    plt.ylabel('Count')
    plt.ylim(0, 10)  # Adjust as necessary for your question count

    # Show the chart
    plt.tight_layout()
    plt.show()

def main():
    global responses
    responses = []

    root = tk.Tk()
    root.title("Online Security Vulnerability Assessment Tool")
    root.geometry("400x400")

    questions = [
        "Do you use unique passwords for each of your accounts?",
        "Do you use a password manager?",
        "Do you enable two-factor authentication on your important accounts?",
        "Do you use antivirus software on your devices?",
        "Have you ever clicked on a suspicious link in an email or message?",
        "Do you often share personal information on social media?",
        "Do you regularly update your software and apps?",
        "Are you aware of how to recognize a phishing email?",
        "Do you log out of accounts when using public computers?",
        "Do you review your privacy settings on social media regularly?"
    ]

    for question in questions:
        get_user_input(question, root)

    score, strengths, weaknesses = assess_vulnerability(responses)
    show_results(score, strengths, weaknesses)

    root.mainloop()

if __name__ == "__main__":
    main()





