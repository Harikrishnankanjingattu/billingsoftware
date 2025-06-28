import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import qrcode
from PIL import ImageTk

new = {
    1001: {"name": "iPhone 15", "category": "Electronics", "price": 79900, "quantity": 10},
    1002: {"name": "Dairy Milk", "category": "Food", "price": 100, "quantity": 50},
    1003: {"name": "HP Laptop", "category": "Electronics", "price": 55000, "quantity": 5},
    1004: {"name": "Parachute Oil", "category": "Personal Care", "price": 95, "quantity": 20},
    1005: {"name": "Notebook", "category": "Stationery", "price": 45, "quantity": 100}
}

orders = []
total_bill = 0

root = tk.Tk()
root.title("Billing System")
root.geometry("1000x700")
root.configure(bg="#003af8")

left_frame = tk.Frame(root, bg="#5e9dfb")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = tk.Frame(root, bg="#80cdd5")
right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

content_frame = tk.Frame(left_frame, bg="#d0f0ff")
content_frame.pack(pady=10, fill="both")

qr_label = None

def refresh_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def gen_bill():
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Enter Product ID", bg="#d0f0ff").pack(pady=2)
    pid_entry = tk.Entry(content_frame)
    pid_entry.pack(pady=2)

    tk.Label(content_frame, text="Enter Quantity", bg="#d0f0ff").pack(pady=2)
    qty_entry = tk.Entry(content_frame)
    qty_entry.pack(pady=2)

    tree = ttk.Treeview(content_frame, columns=("Name", "Qty", "Price", "Total"), show='headings', height=8)
    tree.heading("Name", text="Product Name")
    tree.heading("Qty", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Total", text="Total")
    tree.column("Name", width=120)
    tree.column("Qty", width=80, anchor='center')
    tree.column("Price", width=80, anchor='center')
    tree.column("Total", width=100, anchor='center')
    tree.pack(pady=10)

    for order in orders:
        tree.insert("", "end", values=(order["name"], order["qty"], f"₹{order['price']}", f"₹{order['total']}"))

    def bill_add():
        nonlocal tree
        global total_bill
        try:
            pid = int(pid_entry.get())
            qty = int(qty_entry.get())
            if pid not in new:
                messagebox.showerror("Error", "Product ID not found.")
                return
            product = new[pid]
            if qty > product['quantity']:
                messagebox.showerror("Error", f"Only {product['quantity']} units available.")
                return
            total = product['price'] * qty
            orders.append({"name": product['name'], "price": product['price'], "qty": qty, "total": total})
            new[pid]['quantity'] -= qty
            total_bill += total
            tree.insert("", "end", values=(product["name"], qty, f"₹{product['price']}", f"₹{total}"))
            pid_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid input", "Enter valid numbers.")

    tk.Button(content_frame, text="Add to Bill", bg="light blue", command=bill_add).pack(pady=5)

def del_bill():
    for widget in content_frame.winfo_children():
        widget.destroy()
    tk.Label(content_frame, text="Enter Product ID to delete", bg="#d0f0ff").pack(pady=2)
    del_entry = tk.Entry(content_frame)
    del_entry.pack(pady=2)
    def delete_action():
        try:
            pid = int(del_entry.get())
            if pid in new:
                del new[pid]
                messagebox.showinfo("Deleted", f"Product ID {pid} deleted.")
                del_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Product not found.")
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a valid Product ID.")
    tk.Button(content_frame, text="Delete Product", bg="red", fg="white", command=delete_action).pack(pady=5)

def pro_bill():
    for widget in content_frame.winfo_children():
        widget.destroy()
    tk.Label(content_frame, text="Enter New Product ID", bg="#d0f0ff").pack(pady=2)
    pid_entry = tk.Entry(content_frame)
    pid_entry.pack(pady=2)
    tk.Label(content_frame, text="Enter Name", bg="#d0f0ff").pack(pady=2)
    name_entry = tk.Entry(content_frame)
    name_entry.pack(pady=2)
    tk.Label(content_frame, text="Category", bg="#d0f0ff").pack(pady=2)
    cat_entry = tk.Entry(content_frame)
    cat_entry.pack(pady=2)
    tk.Label(content_frame, text="Price", bg="#d0f0ff").pack(pady=2)
    price_entry = tk.Entry(content_frame)
    price_entry.pack(pady=2)
    tk.Label(content_frame, text="Quantity", bg="#d0f0ff").pack(pady=2)
    qty_entry = tk.Entry(content_frame)
    qty_entry.pack(pady=2)
    def add_product():
        try:
            pid = int(pid_entry.get())
            name = name_entry.get()
            cat = cat_entry.get()
            price = int(price_entry.get())
            qty = int(qty_entry.get())
            if pid in new:
                messagebox.showerror("Error", "Product ID already exists.")
                return
            new[pid] = {"name": name, "category": cat, "price": price, "quantity": qty}
            messagebox.showinfo("Success", f"Product '{name}' added.")
            for entry in [pid_entry, name_entry, cat_entry, price_entry, qty_entry]:
                entry.delete(0, tk.END)
            for widget in right_frame.winfo_children():
                widget.destroy()
            display = tk.Text(right_frame, width=70, height=25, font=("Courier New", 10))
            display.pack(pady=10)
            display.insert(tk.END, "---------- Product Inventory ----------\n")
            display.insert(tk.END, f"{'ID':<6} {'Name':<20} {'Qty':<8} {'Price':<10}\n")
            display.insert(tk.END, "-" * 50 + "\n")
            for pid, item in new.items():
                display.insert(tk.END, f"{pid:<6} {item['name'][:20]:<20} {item['quantity']:<8} ₹{item['price']:<10}\n")
        except ValueError:
            messagebox.showerror("Invalid input", "Enter valid details.")
    tk.Button(content_frame, text="Add Product", bg="green", fg="white", command=add_product).pack(pady=5)

def show_bill():
    global qr_label
    for widget in right_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(right_frame, bg="#ffffff")
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#ffffff")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    display = tk.Text(scroll_frame, width=60, height=30, font=("Courier New", 10), bg="#ffffff", bd=0)
    display.pack(pady=10)
    display.insert(tk.END, "------------------- ABC STORES -----------------\n")
    display.insert(tk.END, "-------------- ABC CITY, KERALA, 678356 -------------\n")
    display.insert(tk.END, "-------------------- Final Bill --------------------\n\n")
    display.insert(tk.END, "=====================================================\n")
    display.insert(tk.END, f"{'Name':20} {'Qty':>5} {'Price':>10} {'Total':>10}\n")
    display.insert(tk.END, "=====================================================\n")
    for item in orders:
        line = f"{item['name'][:20].ljust(20)} {str(item['qty']).rjust(5)} ₹{str(item['price']).rjust(8)} ₹{str(item['total']).rjust(8)}\n"
        display.insert(tk.END, line)
    display.insert(tk.END, "=====================================================\n")
    display.insert(tk.END, f"\nSubtotal: ₹{total_bill:.2f}\n")
    gst = total_bill * 0.18
    display.insert(tk.END, f"GST (18%): ₹{gst:.2f}\n")
    grand_total = total_bill + gst
    display.insert(tk.END, f"Total Amount: ₹{grand_total:.2f}\n")
    display.insert(tk.END, "=====================================================\n")

    amount = f"{grand_total:.2f}"
    upi_url = f"upi://pay?pa=767676767667@upi&pn=GPay%20User&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    qr = qr.resize((150, 150))
    qr_img = ImageTk.PhotoImage(qr)

    qr_label = tk.Label(scroll_frame, image=qr_img, bg="#ffffff")
    qr_label.image = qr_img
    qr_label.pack(pady=10)

def daily():
    messagebox.showinfo("Total Bill", f" ₹{total_bill:.2f}")
def contactme():
    global qr_label
    for widget in right_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(right_frame, bg="#ffffff")
    scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#ffffff")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    display = tk.Text(scroll_frame, width=60, height=30, font=("Courier New", 10), bg="#ffffff", bd=0)
    display.pack(pady=10)
    display.insert(tk.END, "------------------- ABC STORES -----------------\n")
    display.insert(tk.END, "-------------- ABC CITY, KERALA, 678356 -------------\n")
    display.insert(tk.END, "Harikrishan K :-Owner\n\n")
    display.insert(tk.END, "8746389362\n\n")
    display.insert(tk.END, "=====================================================\n")

tk.Button(left_frame, bg="#8af410", text="Add to Bill", command=gen_bill).pack(pady=5, fill='x')
tk.Button(left_frame, bg="#45f410", text="Show Final Bill", command=show_bill).pack(pady=5, fill='x')
tk.Button(left_frame, bg="#7af410", text="Check Total", command=daily).pack(pady=10, fill='x')
tk.Button(left_frame, bg="#10f451", text="Add Product", command=pro_bill).pack(pady=5, fill='x')
tk.Button(left_frame, bg="#f41010", text="Delete Product", command=del_bill).pack(pady=5, fill='x')
tk.Button(left_frame, bg="#1095f4", text="Refresh", command=refresh_app).pack(pady=5, fill='x')
tk.Button(left_frame, bg="#ffffff", text="Contact", command=contactme).pack(pady=5, fill='x')
root.mainloop()
