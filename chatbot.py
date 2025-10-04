import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

# --- Function to get AI Answer ---
def get_ai_answer(question):
    try:
        params = {
            "q": question,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1
        }
        response = requests.get("https://api.duckduckgo.com/", params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("Answer"):
            return data["Answer"]
        elif data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if "Text" in topic:
                    return topic["Text"]
            return "I found some related information, but not an exact answer."
        else:
            return "Sorry, I couldn’t find an answer to that."
    except Exception as e:
        return f"Error: {e}"

# --- When user clicks 'Ask' ---
def ask_question():
    question = entry.get().strip()
    if not question:
        messagebox.showwarning("Input Error", "Please enter a question!")
        return
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    output_text.insert(tk.END, f"\n🕐 {timestamp}\n", "time")
    output_text.insert(tk.END, f"You: {question}\n", "user")

    entry.delete(0, tk.END)
    output_text.insert(tk.END, "Bot: Thinking...\n", "bot_thinking")
    output_text.update()

    answer = get_ai_answer(question)
    
    # Remove "Thinking..." and replace with real answer
    output_text.delete("end-2l linestart", "end-1l")
    output_text.insert(tk.END, f"Bot: {answer}\n", "bot")

    output_text.see(tk.END)

# --- UI Setup ---
root = tk.Tk()
root.title("🤖 AI Q&A Bot (Styled Free Version)")
root.geometry("600x600")
root.config(bg="#121212")

# --- Title ---
title_label = tk.Label(root, text="🤖 AI Q&A Bot (Free API)", 
                       font=("Helvetica", 20, "bold"), bg="#121212", fg="#00e0c6")
title_label.pack(pady=10)

# --- Chat Box ---
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12),
                                        bg="#1e1e1e", fg="white", height=22,
                                        bd=0, relief="flat", padx=10, pady=10)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# --- Text Formatting ---
output_text.tag_config("user", foreground="#00e0c6", font=("Consolas", 12, "bold"))
output_text.tag_config("bot", foreground="#ffffff", spacing1=4, spacing3=4)
output_text.tag_config("bot_thinking", foreground="#aaaaaa", font=("Consolas", 12, "italic"))
output_text.tag_config("time", foreground="#777777", font=("Consolas", 10, "italic"))

output_text.insert(tk.END, "👋 Welcome! Ask me anything...\n\n", "bot")

# --- Entry Frame ---
entry_frame = tk.Frame(root, bg="#121212")
entry_frame.pack(pady=10, fill=tk.X)

entry = tk.Entry(entry_frame, font=("Consolas", 14), width=45, bg="#2d2d2d", fg="white",
                 insertbackground="white", relief="flat")
entry.grid(row=0, column=0, padx=10, ipady=8, sticky="ew")

ask_button = tk.Button(entry_frame, text="Ask", font=("Arial", 12, "bold"),
                       bg="#00e0c6", fg="black", relief="flat",
                       activebackground="#00bfa5", activeforeground="white",
                       command=ask_question)
ask_button.grid(row=0, column=1, padx=10)

entry_frame.columnconfigure(0, weight=1)

root.mainloop()
