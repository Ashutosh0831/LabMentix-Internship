import requests
import json
import os
import sqlite3
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# ------------------ GLOBAL VARIABLES ------------------ #
last_response_data = None
current_theme = "light"

# ------------------ SEND API REQUEST FUNCTION ------------------ #
def send_api_request():
    url = url_entry.get().strip()
    method = method_var.get().upper()
    headers_text = headers_entry.get("1.0", END).strip()
    body_text = body_entry.get("1.0", END).strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a URL.")
        return

    # Parse headers
    try:
        headers = json.loads(headers_text) if headers_text else {}
    except json.JSONDecodeError:
        messagebox.showerror("Invalid Headers", "Headers must be in valid JSON format.")
        return

    # Parse body
    try:
        data = json.loads(body_text) if body_text else None
    except json.JSONDecodeError:
        data = body_text  # fallback to raw text

    try:
        start_time = time.time()
        response = requests.request(
            method, url,
            headers=headers,
            json=data if isinstance(data, dict) else None,
            data=data if isinstance(data, str) else None
        )
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)  # ms

        # Display status and response
        status_label.config(text=f"Status: {response.status_code} | Time: {response_time} ms")
        response_text.delete("1.0", END)

        try:
            parsed_json = response.json()
            formatted = json.dumps(parsed_json, indent=4, ensure_ascii=False)
        except ValueError:
            formatted = response.text.strip()

        response_text.insert(END, formatted)

        global last_response_data
        last_response_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "url": url,
            "method": method,
            "headers": headers,
            "body": body_text,
            "status": response.status_code,
            "time_ms": response_time,
            "response": formatted
        }

        save_to_db(last_response_data)

    except Exception as e:
        messagebox.showerror("Request Error", str(e))


# ------------------ SAVE RESPONSE FUNCTION ------------------ #
def save_response():
    if not last_response_data:
        messagebox.showwarning("No Response", "No response to save yet.")
        return

    os.makedirs("data", exist_ok=True)
    history_file = "data/history.json"
    history = []

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(last_response_data)

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Saved", f"Response saved to {history_file}")


# ------------------ EXPORT RESPONSE FUNCTION ------------------ #
def export_response():
    if not last_response_data:
        messagebox.showwarning("No Response", "No response available to export.")
        return

    filetypes = [("JSON files", "*.json"), ("Text files", "*.txt")]
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=filetypes)

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                if file_path.endswith(".json"):
                    json.dump(last_response_data, f, indent=4, ensure_ascii=False)
                else:
                    f.write(last_response_data["response"])
            messagebox.showinfo("Export Successful", f"Response saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


# ------------------ CLEAR ALL FIELDS ------------------ #
def clear_fields():
    url_entry.delete(0, END)
    headers_entry.delete("1.0", END)
    body_entry.delete("1.0", END)
    response_text.delete("1.0", END)
    status_label.config(text="Status: ")
    global last_response_data
    last_response_data = None


# ------------------ DATABASE FUNCTIONS ------------------ #
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/history.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    url TEXT,
                    method TEXT,
                    status INTEGER,
                    time_ms REAL
                )''')
    conn.commit()
    conn.close()


def save_to_db(entry):
    try:
        conn = sqlite3.connect("data/history.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (timestamp, url, method, status, time_ms) VALUES (?, ?, ?, ?, ?)",
                  (entry["timestamp"], entry["url"], entry["method"], entry["status"], entry["time_ms"]))
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save to DB: {e}")


# ------------------ THEME TOGGLE FUNCTION ------------------ #
def toggle_theme():
    global current_theme
    if current_theme == "light":
        set_dark_theme()
        current_theme = "dark"
    else:
        set_light_theme()
        current_theme = "light"


def set_dark_theme():
    root.configure(bg="#1e1e1e")
    for widget in root.winfo_children():
        try:
            widget.configure(bg="#1e1e1e", fg="white")
        except:
            pass

    response_text.configure(bg="#252526", fg="#bcdf4a", insertbackground="white")
    headers_entry.configure(bg="#252526", fg="#eaf694", insertbackground="white")
    body_entry.configure(bg="#252526", fg="#dcdcdc", insertbackground="white")
    status_label.configure(bg="#1e1e1e", fg="#f2f8f5")


def set_light_theme():
    root.configure(bg="#f7f7f7")
    for widget in root.winfo_children():
        try:
            widget.configure(bg="#f7f7f7", fg="black")
        except:
            pass

    response_text.configure(bg="#fafafa", fg="black", insertbackground="black")
    headers_entry.configure(bg="#fafafa", fg="black", insertbackground="black")
    body_entry.configure(bg="#fafafa", fg="black", insertbackground="black")
    status_label.configure(bg="#f7f7f7", fg="black")


# ------------------ UI SETUP ------------------ #
def run_app():
    global url_entry, headers_entry, body_entry, response_text, method_var, status_label, root

    root = Tk()
    root.title("Mini API Tester")
    root.geometry("800x720")
    root.resizable(False, False)
    root.configure(bg="#f7f7f7")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=6, relief="flat", font=("Arial", 10, "bold"))

    Label(root, text="Mini API Tester", font=("Arial", 16, "bold"), bg="#f7f7f7").pack(pady=10)

    Button(root, text="🌗 Toggle Theme", command=toggle_theme, bg="#5555ff", fg="white").pack(pady=15)

    Label(root, text="URL:", bg="#f7f7f7", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    url_entry = Entry(root, width=85, font=("Arial", 10))
    url_entry.pack(padx=10, pady=5)

    Label(root, text="Method:", bg="#f7f7f7", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    method_var = StringVar(value="GET")
    ttk.Combobox(root, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE"], width=10).pack(padx=10, pady=5)

    Label(root, text="Headers (JSON):", bg="#f7f7f7", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    headers_entry = Text(root, height=5, width=95, font=("Courier New", 10))
    headers_entry.pack(padx=10, pady=5)

    Label(root, text="Body (JSON/Text):", bg="#f7f7f7", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    body_entry = Text(root, height=8, width=95, font=("Courier New", 10))
    body_entry.pack(padx=10, pady=5)

    frame = Frame(root, bg="#f7f7f7")
    frame.pack(pady=10)
    Button(frame, text="Send Request", command=send_api_request, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
    Button(frame, text="Clear Fields", command=clear_fields, bg="#f44336", fg="white", width=15).grid(row=0, column=1, padx=5)
    Button(frame, text="Save Response", command=save_response, bg="#2196F3", fg="white", width=15).grid(row=0, column=2, padx=5)
    Button(frame, text="Export Response", command=export_response, bg="#9C27B0", fg="white", width=15).grid(row=0, column=3, padx=5)

    status_label = Label(root, text="Status: ", font=("Arial", 10, "bold"), bg="#f7f7f7")
    status_label.pack(pady=5)

    Label(root, text="Response:", bg="#f7f7f7", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    response_text = Text(root, height=18, width=95, font=("Courier New", 10), bg="#fafafa")
    response_text.pack(padx=10, pady=5)

    init_db()
    root.mainloop()


# ------------------ RUN APP ------------------ #
if __name__ == '__main__':
    run_app()
