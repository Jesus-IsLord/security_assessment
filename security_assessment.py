import tkinter as tk
from tkinter import messagebox, simpledialog
import matplotlib.pyplot as plt
import json
import os


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

# Function to create or load a user profile
def create_or_load_profile():
    user_data = load_user_data()
    username = simpledialog.askstring("User Profile", "Enter your username:")
    
    if username:
        if username not in user_data:
            user_data[username] = {'history': []}  # Initialize history if new user
            save_user_data(user_data)
            messagebox.showinfo("Profile Created", f"Profile for {username} created!")
        else:
            messagebox.showinfo("Profile Loaded", f"Welcome back, {username}!")
        
        return username, user_data[username]
    return None, None

def choose_category(username):
    category_window = tk.Toplevel()
    category_window.title("Choose Assessment Category")
    category_window.configure(bg="#f0f0f0")

    label = tk.Label(category_window, text="Select the category of questions:", bg="#f0f0f0", font=("Arial", 14))
    label.pack(pady=20)

    categories = ['Password Management', 'Phishing Awareness', 'Device Security']
    for category in categories:
        button = tk.Button(category_window, text=category, command=lambda c=category: start_assessment(c, username), bg="#007bff", fg="white", font=("Arial", 12), relief=tk.FLAT)
        button.pack(pady=10, padx=20, fill=tk.X)

def start_assessment(category, username):
    global responses
    responses = []
    question_index = 0  # Initialize question index

    assessment_window = tk.Toplevel()
    assessment_window.title(f"{category} Assessment")
    assessment_window.geometry("500x400")
    assessment_window.configure(bg="#ffffff")

    questions_dict = {
        'Password Management': [
            "Do you use unique passwords for each of your accounts?",
            "Do you use a password manager?",
            "Do you regularly update your passwords?",
            "Have you enabled password expiration notifications?",
            "Do you use a mix of letters, numbers, and symbols in your passwords?",
            "Do you change default passwords on devices?",
            "Do you use multi-factor authentication?",
            "Have you ever had a password compromised?",
            "Do you avoid using easily guessed passwords?"
        ],
        'Phishing Awareness': [
            "Have you ever clicked on a suspicious link in an email or message?",
            "Are you aware of how to recognize a phishing email?",
            "Do you verify the sender's email address before clicking links?",
            "Do you use two-factor authentication for email accounts?",
            "Do you report phishing attempts to your email provider?",
            "Have you been trained to recognize phishing attempts?",
            "Do you check URLs before entering sensitive information?",
            "Do you know how to verify a website's security?",
            "Have you discussed phishing awareness with your colleagues or family?"
        ],
        'Device Security': [
            "Do you use antivirus software on your devices?",
            "Do you regularly update your software and apps?",
            "Do you log out of accounts when using public computers?",
            "Do you use encrypted messaging apps?",
            "Have you checked your devices for malware recently?",
            "Do you back up your data regularly?",
            "Do you use a firewall on your devices?",
            "Do you secure your Wi-Fi network with a strong password?",
            "Have you disabled sharing options on public networks?"
        ]
    }

    questions = questions_dict.get(category, [])

    def ask_question():
        nonlocal question_index  # Allow modification of the question index
        if question_index < len(questions):
            question_label.config(text=questions[question_index])
        else:
            assess_vulnerability(responses)
            assessment_window.destroy()  # Close the assessment window after completing all questions

    def submit_response(answer):
        nonlocal question_index
        responses.append(answer)
        question_index += 1
        ask_question()  # Ask the next question

    question_label = tk.Label(assessment_window, text="", bg="#ffffff", font=("Arial", 14), wraplength=450)
    question_label.pack(pady=20)

    # Response buttons
    yes_button = tk.Button(assessment_window, text="Yes", command=lambda: submit_response('yes'), bg="#007bff", fg="white", font=("Arial", 12))
    yes_button.pack(side=tk.LEFT, padx=50, pady=20)

    no_button = tk.Button(assessment_window, text="No", command=lambda: submit_response('no'), bg="#007bff", fg="white", font=("Arial", 12))
    no_button.pack(side=tk.RIGHT, padx=50, pady=20)

    # Start the questioning process
    ask_question()

def assess_vulnerability(responses):
    score = 0
    strengths = []
    weaknesses = []

    assessment_criteria = {
        'Do you use unique passwords for each of your accounts?': "Using unique passwords",
        'Do you use a password manager?': "Using a password manager",
        'Do you regularly update your passwords?': "Regularly updating passwords",
        'Have you enabled password expiration notifications?': "Enabling password expiration notifications",
        'Do you use a mix of letters, numbers, and symbols in your passwords?': "Using complex passwords",
        'Do you change default passwords on devices?': "Changing default passwords",
        'Do you use multi-factor authentication?': "Using multi-factor authentication",
        'Have you ever had a password compromised?': "Being aware of compromised passwords",
        'Do you avoid using easily guessed passwords?': "Avoiding easily guessed passwords",
        'Have you ever clicked on a suspicious link in an email or message?': "Being aware of phishing attempts",
        'Are you aware of how to recognize a phishing email?': "Aware of how to recognize phishing emails",
        'Do you verify the sender\'s email address before clicking links?': "Verifying sender's email",
        'Do you use two-factor authentication for email accounts?': "Using two-factor authentication for emails",
        'Do you report phishing attempts to your email provider?': "Reporting phishing attempts",
        'Do you use antivirus software on your devices?': "Using antivirus software",
        'Do you regularly update your software and apps?': "Regularly updating software and apps",
        'Do you log out of accounts when using public computers?': "Logging out of accounts on public computers",
        'Do you use encrypted messaging apps?': "Using encrypted messaging apps",
        'Have you checked your devices for malware recently?': "Checking devices for malware",
        'Do you back up your data regularly?': "Backing up data regularly",
        'Do you use a firewall on your devices?': "Using a firewall on devices",
        'Do you secure your Wi-Fi network with a strong password?': "Securing Wi-Fi network",
        'Have you disabled sharing options on public networks?': "Disabling sharing options on public networks"
    }

    for question in assessment_criteria.keys():
        if question in responses:
            answer = responses.pop(0)  # Get the answer and remove it from the list
            if answer == 'yes':
                score += 1
                strengths.append(assessment_criteria[question])
            else:
                weaknesses.append(f"Not {assessment_criteria[question].lower()}")

    show_results(score, strengths, weaknesses)

def recommend_resources(weaknesses):
    recommendations = []
    if "Not using unique passwords" in weaknesses:
        recommendations.append("Use a password manager: [LastPass](https://www.lastpass.com/)")
    if "Not enabling two-factor authentication" in weaknesses:
        recommendations.append("Learn about two-factor authentication: [2FA Guide](https://twilio.com/docs/verify/2fa)")
    if "Not using antivirus software" in weaknesses:
        recommendations.append("Recommended antivirus: [Norton](https://us.norton.com/) or [McAfee](https://www.mcafee.com/)")
    if "Not being aware of phishing attempts" in weaknesses:
        recommendations.append("Learn to recognize phishing: [Phishing Awareness](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams)")
    if "Not logging out of accounts on public computers" in weaknesses:
        recommendations.append("Always log out of accounts when using public computers.")
    if "Not using encrypted messaging apps" in weaknesses:
        recommendations.append("Consider using encrypted messaging apps like [Signal](https://signal.org/en/).")
    
    return recommendations

def show_results(score, strengths, weaknesses):
    result_window = tk.Toplevel()
    result_window.title("Assessment Results")
    result_window.geometry("600x600")
    result_window.configure(bg="#ffffff")

    header_label = tk.Label(result_window, text="Assessment Results", bg="#007bff", fg="white", font=("Arial", 20))
    header_label.pack(pady=20)

    score_label = tk.Label(result_window, text=f"Score: {score}/{len(strengths) + len(weaknesses)}", bg="#ffffff", font=("Arial", 16))
    score_label.pack(pady=10)

    strengths_label = tk.Label(result_window, text="Strengths:", bg="#ffffff", font=("Arial", 14))
    strengths_label.pack(anchor="w", padx=20)
    
    for strength in strengths:
        strength_label = tk.Label(result_window, text=f"- {strength}", bg="#ffffff", font=("Arial", 12))
        strength_label.pack(anchor="w", padx=40)

    weaknesses_label = tk.Label(result_window, text="Weaknesses:", bg="#ffffff", font=("Arial", 14))
    weaknesses_label.pack(anchor="w", padx=20)

    for weakness in weaknesses:
        weakness_label = tk.Label(result_window, text=f"- {weakness}", bg="#ffffff", font=("Arial", 12))
        weakness_label.pack(anchor="w", padx=40)

    # Recommend resources
    recommendations = recommend_resources(weaknesses)
    if recommendations:
        recommendations_label = tk.Label(result_window, text="Recommended Resources:", bg="#ffffff", font=("Arial", 14))
        recommendations_label.pack(anchor="w", padx=20)
        
        for rec in recommendations:
            rec_label = tk.Label(result_window, text=f"- {rec}", bg="#ffffff", font=("Arial", 12), fg="blue")
            rec_label.pack(anchor="w", padx=40)

    close_button = tk.Button(result_window, text="Close", command=result_window.destroy, bg="#007bff", fg="white", font=("Arial", 12))
    close_button.pack(pady=20)

# Main application
def main():
    root = tk.Tk()
    root.title("Online Security Vulnerability Assessment Tool")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    welcome_label = tk.Label(root, text="Welcome to the Online Security Assessment Tool!", bg="#f0f0f0", font=("Arial", 16))
    welcome_label.pack(pady=20)

    start_button = tk.Button(root, text="Create/Load Profile", command=lambda: choose_category(create_or_load_profile()[0]), bg="#007bff", fg="white", font=("Arial", 12))
    start_button.pack(pady=20)

    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#007bff", fg="white", font=("Arial", 12))
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()





