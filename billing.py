import tkinter as tk
from tkinter import messagebox
import time
new = {
    1001: {"name": "Apple iPhone 15", "category": "Electronics", "price": 79900, "quantity": 10, "supplier": "Apple Store", "expiry_date": "2025-06-05"},
    1002: {"name": "Dairy Milk Chocolate", "category": "Food", "price": 100, "quantity": 50, "supplier": "Cadbury", "expiry_date": "2025-12-01"},
    1003: {"name": "HP Laptop", "category": "Electronics", "price": 55000, "quantity": 5, "supplier": "HP India", "expiry_date": "2025-12-10"},
    1004: {"name": "Parachute Oil", "category": "Personal Care", "price": 95, "quantity": 20, "supplier": "Marico", "expiry_date": "2026-01-01"},
    1005: {"name": "Dettol Handwash", "category": "Personal Care", "price": 150, "quantity": 30, "supplier": "Reckitt", "expiry_date": "2025-11-15"},
    1006: {"name": "Notebook", "category": "Stationery", "price": 45, "quantity": 100, "supplier": "Classmate", "expiry_date": "2029-12-31"},
    1007: {"name": "Bluetooth Speaker", "category": "Electronics", "price": 2499, "quantity": 15, "supplier": "Boat", "expiry_date": "2027-09-25"},
    1008: {"name": "Sugar 1kg", "category": "Food", "price": 45, "quantity": 70, "supplier": "Bharat Sugar", "expiry_date": "2025-10-20"},
    1009: {"name": "Wheat Flour 5kg", "category": "Food", "price": 180, "quantity": 40, "supplier": "Ashirvaad", "expiry_date": "2025-09-12"},
    1010: {"name": "Face Cream", "category": "Cosmetics", "price": 299, "quantity": 25, "supplier": "Ponds", "expiry_date": "2026-06-30"}
}
orders = []
total_bill = 0
root = tk.Tk()
root.title("Billing System")
root.geometry("600x600")
root.configure(bg="#d0f0ff")
tk.Label(root, text="Enter Product ID").pack()
product_id_entry = tk.Entry(root)
product_id_entry.pack()
tk.Label(root, text="Enter Product Quantity").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()
display = tk.Text(root, width=60, height=20)
display.pack(pady=20)
def add_to_bill():
    global total_bill
    try:
        pid = int(product_id_entry.get())
        qty = int(quantity_entry.get())
        if pid not in new:
            messagebox.showerror("Error", "Product ID not found.")
            return
        product = new[pid]
        if qty > product['quantity']:
            messagebox.showerror("Error", f"Only {product['quantity']} units available.")
            return
        total = product['price'] * qty
        orders.append({
            "name": product['name'],"price": product['price'],"qty": qty,"total": total
        })
        new[pid]['quantity'] -= qty
        total_bill += total
        messagebox.showinfo("Added", f"{product['name']} added to bill.")
        product_id_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")
def show_bill():
    display.delete(1.0, tk.END)
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

def daily():
    messagebox.showinfo("Total Bill", f" ₹{total_bill:.2f}")
tk.Button(root, text="Add to Bill", command=add_to_bill).pack(pady=5)
tk.Button(root, text="Show Final Bill", command=show_bill).pack(pady=5)
tk.Button(root, text="Check Total", command=daily).pack(pady=10)

root.mainloop()
