import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# सर्व खर्च साठवण्यासाठी लिस्ट (List of Dictionaries)
expenses = []

def add_expense():
    item = entry_item.get().strip()
    cat = combo_cat.get()
    amt_str = entry_amt.get().strip()

    if not item or not amt_str:
        messagebox.showwarning("Input Error", "Please enter Expense Name and Amount!")
        return

    # Exception Handling: रक्कम नंबरमध्येच आहे का ते तपासणे
    try:
        amt = float(amt_str)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Please enter a valid number for Amount!")
        return

    date_now = datetime.now().strftime("%d-%m-%Y")
    
    # Dictionary मध्ये डेटा सेव्ह करून List मध्ये टाकणे
    expenses.append({"date": date_now, "item": item, "cat": cat, "amt": amt})
    
    # टेबलमध्ये नवीन ओळ दाखवणे
    tree.insert("", tk.END, values=(date_now, item, cat, f"{amt:.2f}"))

    # बॉक्स रिकामे करणे
    entry_item.delete(0, tk.END)
    entry_amt.delete(0, tk.END)

    update_summary()

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Item", "Please select an expense from the table to delete!")
        return
    
    for sel in selected:
        idx = tree.index(sel)
        tree.delete(sel)
        del expenses[idx]
        
    update_summary()

def clear_all():
    expenses.clear()
    for row in tree.get_children():
        tree.delete(row)
    update_summary()

def update_summary():
    total = sum(e["amt"] for e in expenses)
    lbl_total.config(text=f"TOTAL SPENT: ₹{total:.2f}")

    # उजव्या बाजूचा रिपोर्ट तयार करणे
    lines = []
    lines.append("      ATHARV EXPENSE TRACKER")
    lines.append("          MONTHLY REPORT")
    lines.append("=" * 36)
    lines.append(f"Date       : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}")
    lines.append(f"Total Items: {len(expenses)}")
    lines.append("-" * 36)
    lines.append(f"{'Item':<14}{'Category':<12}{'Amount':>10}")
    lines.append("-" * 36)

    for e in expenses:
        lines.append(f"{e['item']:<14}{e['cat']:<12}{e['amt']:>10.2f}")

    lines.append("-" * 36)
    lines.append(f"         TOTAL SPENT: ₹{total:.2f}")
    lines.append("=" * 36)
    lines.append("   Smart Saving, Smart Future!")

    txt_report.delete(1.0, tk.END)
    txt_report.insert(tk.END, "\n".join(lines))

def save_report():
    if not expenses:
        messagebox.showwarning("Empty", "Add some expenses before saving the report!")
        return
    try:
        with open("Atharv_Expense_Report.txt", "w", encoding="utf-8") as f:
            f.write(txt_report.get(1.0, tk.END))
        messagebox.showinfo("Saved", "Report saved in 'Atharv_Expense_Report.txt'!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")

# --- Main Window Setup ---
root = tk.Tk()
root.title("Atharv Smart Expense Tracker - Practical No. 22")
root.geometry("900x580")
root.config(bg="#eef5f0")

# 1. Top Green Header
header = tk.Frame(root, bg="#1b5e20", height=65)
header.pack(fill=tk.X)
tk.Label(header, text="ATHARV SMART EXPENSE TRACKER", font=("Segoe UI", 20, "bold"), bg="#1b5e20", fg="white").pack(pady=(8, 0))
tk.Label(header, text="PERSONAL FINANCE & BUDGET SYSTEM", font=("Segoe UI", 9), bg="#1b5e20", fg="#c8e6c9").pack(pady=(0, 8))

# 2. Input Section
frame_input = tk.LabelFrame(root, text="Add New Expense", font=("Segoe UI", 9, "bold"), bg="#eef5f0", padx=10, pady=8)
frame_input.pack(fill=tk.X, padx=15, pady=10)

tk.Label(frame_input, text="Expense Title (e.g. Coffee, Petrol):", bg="#eef5f0", font=("Segoe UI", 9)).grid(row=0, column=0, padx=5, sticky="w")
entry_item = tk.Entry(frame_input, width=25, font=("Segoe UI", 10))
entry_item.grid(row=1, column=0, padx=5, pady=4)

tk.Label(frame_input, text="Select Category:", bg="#eef5f0", font=("Segoe UI", 9)).grid(row=0, column=1, padx=15, sticky="w")
combo_cat = ttk.Combobox(frame_input, values=["Food & Snacks", "Petrol / Travel", "College / Books", "Gym / Diet", "Recharge / Bills", "Other"], width=18, state="readonly", font=("Segoe UI", 10))
combo_cat.current(0)
combo_cat.grid(row=1, column=1, padx=15, pady=4)

tk.Label(frame_input, text="Amount (₹):", bg="#eef5f0", font=("Segoe UI", 9)).grid(row=0, column=2, padx=10, sticky="w")
entry_amt = tk.Entry(frame_input, width=15, font=("Segoe UI", 10))
entry_amt.grid(row=1, column=2, padx=10, pady=4)

tk.Button(frame_input, text="+ Add Expense", bg="#2e7d32", fg="white", font=("Segoe UI", 9, "bold"), width=14, command=add_expense).grid(row=1, column=3, padx=12)
tk.Button(frame_input, text="Delete Selected", bg="#c62828", fg="white", font=("Segoe UI", 9, "bold"), width=14, command=delete_expense).grid(row=1, column=4, padx=5)

# 3. Middle Section (Table on Left, Report Preview on Right)
frame_mid = tk.Frame(root, bg="#eef5f0")
frame_mid.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

# Left Table
frame_left = tk.LabelFrame(frame_mid, text="Expense Records", font=("Segoe UI", 9, "bold"), bg="#eef5f0", padx=5, pady=5)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

cols = ("Date", "Expense Title", "Category", "Amount (₹)")
tree = ttk.Treeview(frame_left, columns=cols, show="headings", height=11)
for c in cols:
    tree.heading(c, text=c)

tree.column("Date", width=85, anchor="center")
tree.column("Expense Title", width=140, anchor="w")
tree.column("Category", width=110, anchor="center")
tree.column("Amount (₹)", width=90, anchor="e")
tree.pack(fill=tk.BOTH, expand=True)

# Right Report Preview
frame_right = tk.LabelFrame(frame_mid, text="Live Expense Report", font=("Segoe UI", 9, "bold"), bg="#eef5f0", padx=5, pady=5)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

txt_report = tk.Text(frame_right, font=("Consolas", 9), bg="white", fg="black", width=38, height=14)
txt_report.pack(fill=tk.BOTH, expand=True)

# 4. Bottom Bar
frame_bot = tk.Frame(root, bg="#eef5f0")
frame_bot.pack(fill=tk.X, padx=15, pady=12)

lbl_total = tk.Label(frame_bot, text="TOTAL SPENT: ₹0.00", font=("Segoe UI", 15, "bold"), bg="#eef5f0", fg="#1b5e20")
lbl_total.pack(side=tk.LEFT)

tk.Button(frame_bot, text="Save Report to File", bg="#1565c0", fg="white", font=("Segoe UI", 10, "bold"), width=18, command=save_report).pack(side=tk.RIGHT, padx=5)
tk.Button(frame_bot, text="Clear All", bg="#ef6c00", fg="white", font=("Segoe UI", 10, "bold"), width=12, command=clear_all).pack(side=tk.RIGHT, padx=5)

update_summary()
root.mainloop()