import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import qrcode
import json
from PIL import Image, ImageTk

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

def save_products(data):
    with open('products.json', 'w') as f:
        json.dump(data, f, indent=4)

def generate_qr_image(data_string, filename):
    qr = qrcode.make(data_string)
    path = f"{filename}.png"
    qr.save(path)
    return path

root = tk.Tk()
root.geometry("1000x700")
root.title("Paybee Billing")
root.configure(bg="white")

img = Image.open("logo.png")
img = img.resize((250, 250))
photo = ImageTk.PhotoImage(img)
splash_label = tk.Label(root, image=photo, bg="white")
splash_label.pack(expand=True)

def launch_main_ui():
    splash_label.destroy()
    root.configure(bg="#003af8")

    new = load_products()
    orders = []
    total_bill = 0

    left_frame = tk.Frame(root, bg="#5e9dfb")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    right_frame = tk.Frame(root, bg="#80cdd5")
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    content_frame = tk.Frame(left_frame, bg="#d0f0ff")
    content_frame.pack(pady=10, fill="both")

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
        tree.pack(pady=10)

        for order in orders:
            tree.insert("", "end", values=(order["name"], order["qty"], f"₹{order['price']}", f"₹{order['total']}"))

        def bill_add():
            nonlocal tree, total_bill, new
            try:
                pid = str(pid_entry.get())
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
                save_products(new)
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
            nonlocal new
            pid = str(del_entry.get())
            if pid in new:
                del new[pid]
                save_products(new)
                messagebox.showinfo("Deleted", f"Product ID {pid} deleted.")
                del_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Product not found.")
        tk.Button(content_frame, text="Delete Product", bg="red", fg="white", command=delete_action).pack(pady=5)

    def pro_bill():
        for widget in content_frame.winfo_children():
            widget.destroy()
        entries = {}
        for label in ["New Product ID", "Name", "Category", "Price", "Quantity"]:
            tk.Label(content_frame, text=f"Enter {label}", bg="#d0f0ff").pack(pady=2)
            e = tk.Entry(content_frame)
            e.pack(pady=2)
            entries[label] = e

        def add_product():
            nonlocal new
            pid = entries["New Product ID"].get()
            name = entries["Name"].get()
            cat = entries["Category"].get()
            try:
                price = int(entries["Price"].get())
                qty = int(entries["Quantity"].get())
                if pid in new:
                    messagebox.showerror("Error", "Product ID already exists.")
                    return
                new[pid] = {"name": name, "category": cat, "price": price, "quantity": qty}
                save_products(new)
                messagebox.showinfo("Success", f"Product '{name}' added.")
                for e in entries.values():
                    e.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Invalid entry.")

        tk.Button(content_frame, text="Add Product", bg="green", fg="white", command=add_product).pack(pady=5)

    def view_products():
        for widget in right_frame.winfo_children():
            widget.destroy()
        canvas = tk.Canvas(right_frame, bg="white")
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        headers = ["Product ID", "Name", "Category", "Price", "Quantity", "QR Code"]
        for i, h in enumerate(headers):
            tk.Label(scroll_frame, text=h, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=18, bg="#d0f0ff").grid(row=0, column=i, sticky="nsew")

        for idx, (pid, item) in enumerate(new.items(), start=1):
            tk.Label(scroll_frame, text=pid, borderwidth=1, relief="solid", width=18).grid(row=idx, column=0)
            tk.Label(scroll_frame, text=item["name"], borderwidth=1, relief="solid", width=18).grid(row=idx, column=1)
            tk.Label(scroll_frame, text=item["category"], borderwidth=1, relief="solid", width=18).grid(row=idx, column=2)
            tk.Label(scroll_frame, text=f"₹{item['price']}", borderwidth=1, relief="solid", width=18).grid(row=idx, column=3)
            tk.Label(scroll_frame, text=item["quantity"], borderwidth=1, relief="solid", width=18).grid(row=idx, column=4)

            qr_data = f"ID: {pid}, Name: {item['name']}, Price: ₹{item['price']}, Qty: {item['quantity']}"
            qr_path = generate_qr_image(qr_data, f"qr_{pid}")
            img = Image.open(qr_path).resize((100, 100))
            img_qr = ImageTk.PhotoImage(img)
            label = tk.Label(scroll_frame, image=img_qr, borderwidth=1, relief="solid")
            label.image = img_qr
            label.grid(row=idx, column=5, padx=2, pady=2)

    def show_bill():
        for widget in right_frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(right_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
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
        gst = total_bill * 0.18
        grand_total = total_bill + gst
        display.insert(tk.END, f"\nSubtotal: ₹{total_bill:.2f}\nGST (18%): ₹{gst:.2f}\nTotal Amount: ₹{grand_total:.2f}\n")

        upi_url = f"upi://pay?pa=767676767667@upi&pn=GPay%20User&am={grand_total:.2f}&cu=INR"
        qr = qrcode.make(upi_url).resize((150, 150))
        qr_img = ImageTk.PhotoImage(qr)
        tk.Label(scroll_frame, image=qr_img, bg="#ffffff").pack(pady=10)
        scroll_frame.qr_img = qr_img

    def daily():
        messagebox.showinfo("Total Bill", f" ₹{total_bill:.2f}")

    def contactme():
        for widget in right_frame.winfo_children():
            widget.destroy()
        display = tk.Text(right_frame, width=60, height=30, font=("Courier New", 10), bg="#ffffff", bd=0)
        display.pack(pady=10)
        display.insert(tk.END, "------------------- ABC STORES -----------------\n")
        display.insert(tk.END, "-------------- ABC CITY, KERALA, 678356 -------------\n")
        display.insert(tk.END, "Harikrishan K :- Owner\nPhone: 8746389362\n")

    tk.Button(left_frame, bg="#8af410", text="Add to Bill", command=gen_bill).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#45f410", text="Show Final Bill", command=show_bill).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#7af410", text="Check Total", command=daily).pack(pady=10, fill='x')
    tk.Button(left_frame, bg="#10f451", text="Add Product", command=pro_bill).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#f41010", text="Delete Product", command=del_bill).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#1095f4", text="Refresh", command=refresh_app).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#ffffff", text="Contact", command=contactme).pack(pady=5, fill='x')
    tk.Button(left_frame, bg="#c0c0c0", text="View All Products", command=view_products).pack(pady=5, fill='x')

root.after(3000, launch_main_ui)
root.mainloop()
