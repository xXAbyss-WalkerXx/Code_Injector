import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def inject_code(target_file, code_to_inject, position, line_number=None):
    try:
        with open(target_file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
        return

    if position == 'beginning':
        lines = code_to_inject.split('\n') + lines
    elif position == 'end':
        lines += code_to_inject.split('\n')
    elif position == 'after_line':
        if line_number is not None and 0 <= line_number < len(lines):
            lines = lines[:line_number] + code_to_inject.split('\n') + lines[line_number:]
        else:
            messagebox.showerror("Error", "Invalid line number.")
            return

    try:
        with open(target_file, 'w') as f:
            f.write('\n'.join(lines))
        messagebox.showinfo("Success", "Code injected successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error writing to file: {e}")

def select_file():
    file_path = filedialog.askopenfilename(title="Select file")
    if file_path:
        target_file_entry.delete(0, tk.END)
        target_file_entry.insert(0, file_path)

def inject_code_gui():
    target_file = target_file_entry.get()
    code_to_inject = code_text.get("1.0", tk.END).strip()
    position = position_var.get()

    if position not in ['beginning', 'end', 'after_line']:
        messagebox.showerror("Error", "Invalid position. Please choose 'beginning', 'end', or 'after_line'.")
        return

    line_number = None
    if position == 'after_line':
        line_number = simpledialog.askinteger("Line Number", "Enter the line number after which to inject the code:")
        if line_number is None:
            return

    inject_code(target_file, code_to_inject, position, line_number)

# Setup the GUI
root = tk.Tk()
root.title("Code Injector")

tk.Label(root, text="Target File:").grid(row=0, column=0, padx=5, pady=5)
target_file_entry = tk.Entry(root, width=50)
target_file_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Code to Inject:").grid(row=1, column=0, padx=5, pady=5)
code_text = tk.Text(root, width=50, height=10)
code_text.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="Position:").grid(row=2, column=0, padx=5, pady=5)
position_var = tk.StringVar(value='beginning')
positions = ['beginning', 'end', 'after_line']
for pos in positions:
    tk.Radiobutton(root, text=pos.capitalize(), variable=position_var, value=pos).grid(row=2, column=positions.index(pos)+1, padx=5, pady=5)

tk.Button(root, text="Inject Code", command=inject_code_gui).grid(row=3, column=1, columnspan=2, padx=5, pady=5)

root.mainloop()