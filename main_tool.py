import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import shutil

class EduAPKCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Edu APK Creator Tool")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        # --- UI Elements ---

        # Title Label
        title_label = tk.Label(root, text="🎓 Edu APK Creator", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg="#f0f0f0")
        input_frame.pack(pady=10, padx=20, fill="x")

        # Course Name Entry
        tk.Label(input_frame, text="Course Name:", font=("Arial", 10), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.course_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.course_entry.grid(row=0, column=1, padx=5, pady=5)

        # Select APK Button
        btn_select_apk = tk.Button(input_frame, text="Select APK File", command=self.select_apk, bg="#4CAF50", fg="white", font=("Arial", 10))
        btn_select_apk.grid(row=1, column=0, columnspan=2, pady=5)

        # Selected APK Path Label
        self.apk_path_label = tk.Label(input_frame, text="No APK selected", font=("Arial", 9), bg="#f0f0f0", wraplength=300)
        self.apk_path_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # Output Directory Entry
        tk.Label(input_frame, text="Output Folder:", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        self.output_entry = tk.Entry(input_frame, width=25, font=("Arial", 10))
        self.output_entry.grid(row=3, column=1, padx=5, pady=5)
        
        btn_select_output = tk.Button(input_frame, text="Select Output Dir", command=self.select_output_dir, bg="#2196F3", fg="white", font=("Arial", 10))
        btn_select_output.grid(row=3, column=2, padx=5, pady=5)

        # Action Button
        self.btn_process = tk.Button(root, text="🚀 Create APK Bundle", command=self.process_apk, bg="#FF9800", fg="white", font=("Arial", 12, "bold"), width=20)
        self.btn_process.pack(pady=20)

        # Log Area
        log_frame = tk.Frame(root, bg="#333")
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(log_frame, text="Process Log:", font=("Arial", 10), bg="#333", fg="white").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, bg="#222", fg="#0f0", font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True)

    def log_message(self, message):
        """Append messages to the log text area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # Auto scroll to bottom

    def select_apk(self):
        """Open file dialog to select APK"""
        file_path = filedialog.askopenfilename(
            title="Select APK File",
            filetypes=[("APK Files", "*.apk"), ("All Files", "*.*")]
        )
        if file_path:
            self.apk_path_label.config(text=f"Selected: {file_path}")
            self.log_message(f"[INFO] APK Selected: {file_path}")

    def select_output_dir(self):
        """Open directory dialog to select output folder"""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)
            self.log_message(f"[INFO] Output Directory Set: {dir_path}")

    def process_apk(self):
        """Main logic to create the APK"""
        course_name = self.course_entry.get()
        apk_path = self.apk_path_label.cget("text")
        
        # Remove "Selected: " prefix if present
        if apk_path.startswith("Selected: "):
            apk_path = apk_path[10:]
        
        output_dir = self.output_entry.get()

        # Validation
        if not course_name:
            messagebox.showwarning("Input Error", "Please enter a Course Name!")
            return
        
        if apk_path == "No APK selected":
            messagebox.showwarning("Input Error", "Please select an APK file first!")
            return
            
        if not output_dir:
            messagebox.showwarning("Input Error", "Please select an Output Directory!")
            return

        # Disable button during process
        self.btn_process.config(state=tk.DISABLED)
        self.log_message("\n--- Starting Process ---")
        
        try:
            # 1. Create Output Directory structure
            # Format: CourseName/APK_Name
            base_output_dir = os.path.join(output_dir, course_name)
            os.makedirs(base_output_dir, exist_ok=True)
            self.log_message(f"[INFO] Created directory: {base_output_dir}")

            # 2. Copy APK to Output Directory
            apk_filename = os.path.basename(apk_path)
            destination_path = os.path.join(base_output_dir, apk_filename)
            
            shutil.copy2(apk_path, destination_path)
            self.log_message(f"[SUCCESS] Copied {apk_filename} to {base_output_dir}")

            # 3. Create a simple README.txt inside the folder
            readme_path = os.path.join(base_output_dir, "README.txt")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"Course: {course_name}\n")
                f.write(f"APK File: {apk_filename}\n")
                f.write("This folder contains the APK for the course.\n")
            self.log_message("[INFO] Created README.txt")

            # 4. Create a ZIP file of the folder (Optional but good for distribution)
            zip_name = f"{course_name}_APK.zip"
            shutil.make_archive(os.path.join(output_dir, course_name), 'zip', base_output_dir)
            self.log_message(f"[SUCCESS] Created ZIP: {os.path.join(output_dir, zip_name)}")

            messagebox.showinfo("Success", f"APK Bundle created successfully!\n\nLocation:\n{base_output_dir}")
            self.log_message("--- Process Completed Successfully ---")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_message(f"[ERROR] {str(e)}")
        
        finally:
            # Re-enable button
            self.btn_process.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = EduAPKCreatorGUI(root)
    root.mainloop()
