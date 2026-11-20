import os
import re
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class EduAPKBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Edu APK Builder Tool")
        self.root.geometry("700x620")
        self.root.configure(bg="#f0f0f0")

        self.selected_source = None
        self.selected_icon = None

        # --- Title ---
        tk.Label(root, text="🎓 Edu APK Builder",
                 font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # --- Input Frame ---
        frame = tk.Frame(root, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, fill="x")

        # 1. Course Name
        tk.Label(frame, text="Course Name:", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.course_entry = tk.Entry(frame, width=35, font=("Arial", 10))
        self.course_entry.grid(row=0, column=1, padx=5, pady=5)

        # 2. APK Name (NEW)
        tk.Label(frame, text="APK Name:", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.apkname_entry = tk.Entry(frame, width=35, font=("Arial", 10))
        self.apkname_entry.grid(row=1, column=1, padx=5, pady=5)

        # 3. Source File (main.py — Kivy code)
        tk.Label(frame, text="Source (main.py):", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.source_label = tk.Label(frame, text="No file selected",
                                     bg="#f0f0f0", font=("Arial", 9),
                                     wraplength=280, anchor="w", justify="left")
        self.source_label.grid(row=2, column=1, padx=5, sticky="w")
        tk.Button(frame, text="Browse", command=self.select_source,
                  bg="#4CAF50", fg="white").grid(row=2, column=2, padx=5)

        # 4. App Icon (Optional)
        tk.Label(frame, text="App Icon (opt):", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.icon_label = tk.Label(frame, text="No icon selected",
                                   bg="#f0f0f0", font=("Arial", 9))
        self.icon_label.grid(row=3, column=1, padx=5, sticky="w")
        tk.Button(frame, text="Browse", command=self.select_icon,
                  bg="#9C27B0", fg="white").grid(row=3, column=2, padx=5)

        # 5. Output Folder
        tk.Label(frame, text="Output Folder:", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        self.output_entry = tk.Entry(frame, width=28, font=("Arial", 10))
        self.output_entry.grid(row=4, column=1, padx=5, pady=5)
        tk.Button(frame, text="Browse", command=self.select_output_dir,
                  bg="#2196F3", fg="white").grid(row=4, column=2, padx=5)

        # 6. Build Type (Debug / Release)
        tk.Label(frame, text="Build Type:", bg="#f0f0f0",
                 font=("Arial", 10)).grid(row=5, column=0, sticky="w", pady=5)
        self.build_type = tk.StringVar(value="debug")
        tk.Radiobutton(frame, text="Debug", variable=self.build_type,
                       value="debug", bg="#f0f0f0").grid(row=5, column=1, sticky="w")
        tk.Radiobutton(frame, text="Release", variable=self.build_type,
                       value="release", bg="#f0f0f0").grid(row=5, column=2, sticky="w")

        # --- Action Button ---
        self.btn_build = tk.Button(root, text="🚀 Build APK",
                                   command=self.start_build_thread,
                                   bg="#FF9800", fg="white",
                                   font=("Arial", 12, "bold"), width=22)
        self.btn_build.pack(pady=15)

        # --- Log Area ---
        log_frame = tk.Frame(root, bg="#333")
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        tk.Label(log_frame, text="Build Log:", bg="#333", fg="white",
                 font=("Arial", 10)).pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12,
                                                  bg="#111", fg="#0f0",
                                                  font=("Courier", 9))
        self.log_text.pack(fill="both", expand=True)

    # ---------- Helpers ----------
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def select_source(self):
        p = filedialog.askopenfilename(
            title="Select main.py (Kivy App)",
            filetypes=[("Python", "*.py"), ("All", "*.*")])
        if p:
            self.selected_source = p
            self.source_label.config(text=os.path.basename(p))
            self.log(f"[INFO] Source: {p}")

    def select_icon(self):
        p = filedialog.askopenfilename(
            title="Select Icon (PNG)",
            filetypes=[("PNG", "*.png"), ("All", "*.*")])
        if p:
            self.selected_icon = p
            self.icon_label.config(text=os.path.basename(p))
            self.log(f"[INFO] Icon: {p}")

    def select_output_dir(self):
        d = filedialog.askdirectory(title="Select Output Directory")
        if d:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, d)
            self.log(f"[INFO] Output: {d}")

    # ---------- Build Thread ----------
    def start_build_thread(self):
        t = threading.Thread(target=self.build_apk, daemon=True)
        t.start()

    # ---------- Main Build Logic ----------
    def build_apk(self):
        course = self.course_entry.get().strip()
        apkname = self.apkname_entry.get().strip()
        source = self.selected_source
        output = self.output_entry.get().strip()
        btype = self.build_type.get()

        # Validation
        if not course:
            messagebox.showwarning("Error", "Enter Course Name!")
            return
        if not apkname:
            messagebox.showwarning("Error", "Enter APK Name!")
            return
        if not source or not os.path.isfile(source):
            messagebox.showwarning("Error", "Select valid main.py file!")
            return
        if not output:
            messagebox.showwarning("Error", "Select Output Folder!")
            return

        # Sanitize names
        safe_apk = re.sub(r'[^A-Za-z0-9_]', '_', apkname)
        safe_course = re.sub(r'[<>:"/\\|?*]', '_', course)

        self.btn_build.config(state=tk.DISABLED)
        self.log("\n=== BUILD STARTED ===")

        try:
            # 1. Create working project folder
            project_dir = os.path.join(output, f"{safe_course}_project")
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            os.makedirs(project_dir, exist_ok=True)

            # 2. Copy source
            shutil.copy2(source, os.path.join(project_dir, "main.py"))
            self.log(f"[OK] Copied main.py → {project_dir}")

            # 3. Create buildozer.spec
            spec_path = os.path.join(project_dir, "buildozer.spec")
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write(f"""[app]
title = {apkname}
package.name = {safe_apk.lower()}
package.domain = org.edu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,plyer
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
""")
            if self.selected_icon:
                shutil.copy2(self.selected_icon,
                             os.path.join(project_dir, "icon.png"))
            self.log("[OK] buildozer.spec created")

            # 4. Run buildozer
            self.log(f"[RUN] buildozer -v android {btype}")
            self.log("⏳ This may take 20–40 minutes on first run...")

            try:
                proc = subprocess.Popen(
                    ["buildozer", "-v", "android", btype],
                    cwd=project_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True, bufsize=1)
                for line in proc.stdout:
                    self.log(line.rstrip())
                proc.wait()
            except FileNotFoundError:
                self.log("[ERROR] 'buildozer' not found!")
                self.log("👉 Install: pip install buildozer (Linux/WSL only)")
                return

            # 5. Copy final APK
            apk_dir = os.path.join(project_dir, "bin")
            if os.path.isdir(apk_dir):
                for f in os.listdir(apk_dir):
                    if f.endswith(".apk"):
                        dst = os.path.join(output, f"{safe_apk}_{f}")
                        shutil.copy2(os.path.join(apk_dir, f), dst)
                        self.log(f"[SUCCESS] APK → {dst}")
                messagebox.showinfo("Done", "APK build finished!\nCheck output folder.")
            else:
                self.log("[WARN] No APK generated — check logs.")

        except Exception as e:
            self.log(f"[ERROR] {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.btn_build.config(state=tk.NORMAL)
            self.log("=== BUILD ENDED ===")


if __name__ == "__main__":
    root = tk.Tk()
    app = EduAPKBuilderGUI(root)
    root.mainloop()
