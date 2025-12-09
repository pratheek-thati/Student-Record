import tkinter as tk
from tkinter import messagebox
import json
import os


class StudentRecords:
    """Manages student data using a dictionary for fast lookup (Registration No.)."""
    def __init__(self):
       
        self.records = {}
        self.file_path = "srms_records.json"
        self.load_records()

    def load_records(self):
        """Loads records from a JSON file if it exists."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    self.records = json.load(f)
            except json.JSONDecodeError:
               
                self.records = {}
       
    def save_records(self):
        """Saves current records to a JSON file."""
       
        with open(self.file_path, 'w') as f:
            json.dump(self.records, f, indent=4)

    def add_record(self, reg_no, name, program, cgpa):
        """Adds a new student record."""
        if reg_no in self.records:
            return f"Error: Registration No. {reg_no} already exists."
        
        self.records[reg_no] = {
            "name": name,
            "program": program,
            "cgpa": cgpa,
            "university": "SRM University AP" 
        }
        self.save_records()
        return f"Success: Record for {name} ({reg_no}) added."

    def view_record(self, reg_no):
        """Retrieves a single student record."""
       
        return self.records.get(reg_no)

    def update_record(self, reg_no, name, program, cgpa):
        """Updates an existing student's details."""
        if reg_no not in self.records:
            return f"Error: Registration No. {reg_no} not found for update."
        
        self.records[reg_no].update({
            "name": name,
            "program": program,
            "cgpa": cgpa
        })
        self.save_records()
        return f"Success: Record for {reg_no} updated."

    def delete_record(self, reg_no):
        """Deletes a student record."""
        if reg_no in self.records:
            del self.records[reg_no]
            self.save_records()
            return f"Success: Record {reg_no} deleted."
        return f"Error: Registration No. {reg_no} not found for deletion."



class SRMSGUI:
    def __init__(self, master):
        self.master = master
        master.title("SRM University AP - Student Record Management System")
        
        master.geometry("600x450")
        master.resizable(False, False)

        self.srms = StudentRecords()

        
        self.reg_no_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.program_var = tk.StringVar(value="B.Tech CSE") 
        self.cgpa_var = tk.StringVar()
        self.status_text = tk.StringVar(value="Status: Ready")

        header_label = tk.Label(master, text="SRM University AP", font=('Arial', 16, 'bold'), fg="#1434A4") # SRM Blue
        header_label.pack(pady=(10, 5))

        
        input_frame = tk.Frame(master)
        
        input_frame.columnconfigure(1, weight=1) 
        input_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(input_frame, text="Reg No.:", width=15, anchor='w').grid(row=0, column=0, pady=3, sticky='w')
        tk.Entry(input_frame, textvariable=self.reg_no_var, width=30).grid(row=0, column=1, pady=3, sticky='ew')
        
        tk.Label(input_frame, text="Name:", width=15, anchor='w').grid(row=1, column=0, pady=3, sticky='w')
        tk.Entry(input_frame, textvariable=self.name_var, width=30).grid(row=1, column=1, pady=3, sticky='ew')
        
        tk.Label(input_frame, text="Program:", width=15, anchor='w').grid(row=2, column=0, pady=3, sticky='w')
        programs = ["B.Tech CSE", "B.Tech ECE", "B.Sc Physics", "B.Com"]
        tk.OptionMenu(input_frame, self.program_var, *programs).grid(row=2, column=1, pady=3, sticky='ew')
        
        tk.Label(input_frame, text="CGPA:", width=15, anchor='w').grid(row=3, column=0, pady=3, sticky='w')
        tk.Entry(input_frame, textvariable=self.cgpa_var, width=30).grid(row=3, column=1, pady=3, sticky='ew')

       
        control_frame = tk.Frame(master)
        control_frame.pack(pady=15)

        button_style = {'width': 15, 'fg': 'white', 'font': ('Arial', 9, 'bold')}

        tk.Button(control_frame, text="Add Record", command=self.add_student, bg="#5cb85c", **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="View Record", command=self.view_student, bg="#337ab7", **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Update Record", command=self.update_student, bg="#f0ad4e", **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Delete Record", command=self.delete_student, bg="#d9534f", **button_style).pack(side=tk.LEFT, padx=5)

       
        output_label = tk.Label(master, text="Output / View Details:", font=('Arial', 10, 'bold'))
        output_label.pack(pady=(10, 0))
        self.output_text = tk.Text(master, height=6, width=70, state='disabled', wrap='word', bd=2, relief='sunken')
        self.output_text.pack(pady=5, padx=20)
        
        status_label = tk.Label(master, textvariable=self.status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
       

    def clear_inputs(self, keep_reg_no=False):
        """Clears all input fields, optionally keeping the Reg No."""
        if not keep_reg_no:
            self.reg_no_var.set("")
            
        self.name_var.set("")
        self.cgpa_var.set("")
        self.program_var.set("B.Tech CSE") 

    def display_output(self, content):
        """Enables, clears, inserts content, and disables the output text area."""
       
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', content)
        self.output_text.configure(state='disabled')

    def validate_inputs(self, reg_only=False):
        """Validates input fields."""
        reg_no = self.reg_no_var.get().strip()
        if not reg_no:
            messagebox.showerror("Input Error", "Registration Number is required.")
            return None, None, None, None
        
        if reg_only:
            return reg_no, None, None, None
        
        name = self.name_var.get().strip()
        program = self.program_var.get().strip()
        cgpa_str = self.cgpa_var.get().strip()

        if not name or not program or not cgpa_str:
            messagebox.showerror("Input Error", "All fields must be filled for Add/Update.")
            return None, None, None, None

        try:
           
            cgpa = float(cgpa_str)
            if not (0.0 <= cgpa <= 10.0):
                 messagebox.showerror("Input Error", "CGPA must be between 0.0 and 10.0.")
                 return None, None, None, None
        except ValueError:
            messagebox.showerror("Input Error", "CGPA must be a valid number.")
            return None, None, None, None

        return reg_no, name, program, cgpa

    def add_student(self):
        reg_no, name, program, cgpa = self.validate_inputs()
        if reg_no is None: return

        message = self.srms.add_record(reg_no, name, program, cgpa)
        self.status_text.set(f"Status: {message}")
        self.display_output(message)
        
        if "Success" in message:
            self.clear_inputs()

    def view_student(self):
        reg_no, _, _, _ = self.validate_inputs(reg_only=True)
        if reg_no is None: return

        record = self.srms.view_record(reg_no)
        if record:
            output = f"Registration No: {reg_no}\n"
            output += f"Name: {record['name']}\n"
            output += f"Program: {record['program']}\n"
            output += f"CGPA: {record['cgpa']:.2f}\n"
            output += f"University: {record['university']}"
            
            self.name_var.set(record['name'])
            self.program_var.set(record['program'])
            self.cgpa_var.set(str(record['cgpa']))

            self.status_text.set(f"Status: Found record for {record['name']}.")
            self.display_output(output)
        else:
            message = f"Error: Registration No. {reg_no} not found."
            self.status_text.set(f"Status: {message}")
            self.display_output(message)
          
            self.clear_inputs(keep_reg_no=False)

    def update_student(self):
        reg_no, name, program, cgpa = self.validate_inputs()
        if reg_no is None: return
        
        message = self.srms.update_record(reg_no, name, program, cgpa)
        self.status_text.set(f"Status: {message}")
        self.display_output(message)
       
        if "Success" in message:
            self.clear_inputs()

    def delete_student(self):
        reg_no, _, _, _ = self.validate_inputs(reg_only=True)
        if reg_no is None: return
        
        if not messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record for {reg_no}?"):
            self.status_text.set("Status: Deletion cancelled.")
            return

        message = self.srms.delete_record(reg_no)
        self.status_text.set(f"Status: {message}")
        self.display_output(message)
       
        if "Success" in message:
            self.clear_inputs()

if __name__ == "__main__":
    root = tk.Tk()
    app = SRMSGUI(root)
    root.mainloop()