import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.contacts = []

        # Load contacts from file
        self.load_contacts()

        # Labels
        tk.Label(root, text="Name:").grid(row=0, column=0)
        tk.Label(root, text="Phone:").grid(row=1, column=0)
        tk.Label(root, text="Email:").grid(row=2, column=0)

        # Entry widgets
        self.name_entry = tk.Entry(root)
        self.phone_entry = tk.Entry(root)
        self.email_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="View Contacts", command=self.view_contacts).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Edit Contact", command=self.edit_contact).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Delete Contact", command=self.delete_contact).grid(row=6, column=0, columnspan=2)

        # Save contacts to file on closing the window
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Save contacts to file
        self.save_contacts()
        self.root.destroy()

    def save_contacts(self):
        with open("contacts.txt", "w") as file:
            for contact in self.contacts:
                file.write(contact + "\n---\n")

    def load_contacts(self):
        try:
            with open("contacts.txt", "r") as file:
                contacts_text = file.read()

            contacts_list = contacts_text.split("---")
            self.contacts = [contact.strip() for contact in contacts_list if contact.strip()]
        except FileNotFoundError:
            # Ignore if the file is not found
            pass

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone and email:
            contact_info = f"Name: {name}\nPhone: {phone}\nEmail: {email}"
            self.contacts.append(contact_info)
            messagebox.showinfo("Contact Added", "Contact has been added successfully.")
            self.clear_entries()
            self.save_contacts()
        else:
            messagebox.showwarning("Incomplete Information", "Please fill in all the fields.")

    def view_contacts(self):
        if self.contacts:
            contacts_info = "\n\n".join(self.contacts)
            messagebox.showinfo("Contacts", contacts_info)
        else:
            messagebox.showinfo("No Contacts", "No contacts available.")

    def edit_contact(self):
        index = self.get_selected_index()
        if index is not None:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()

            if name and phone and email:
                contact_info = f"Name: {name}\nPhone: {phone}\nEmail: {email}"
                self.contacts[index] = contact_info
                messagebox.showinfo("Contact Updated", "Contact has been updated successfully.")
                self.clear_entries()
                self.save_contacts()
            else:
                messagebox.showwarning("Incomplete Information", "Please fill in all the fields.")
        else:
            messagebox.showwarning("No Contact Selected", "Please select a contact to edit.")

    def delete_contact(self):
        index = self.get_selected_index()
        if index is not None:
            del self.contacts[index]
            messagebox.showinfo("Contact Deleted", "Contact has been deleted successfully.")
            self.clear_entries()
            self.save_contacts()
        else:
            messagebox.showwarning("No Contact Selected", "Please select a contact to delete.")

    def get_selected_index(self):
        try:
            selected_index = simpledialog.askinteger("Select Contact", "Enter the index of the contact:")
            if 0 <= selected_index < len(self.contacts):
                return selected_index
            else:
                messagebox.showwarning("Invalid Index", "Please enter a valid index.")
                return None
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid integer.")
            return None

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
