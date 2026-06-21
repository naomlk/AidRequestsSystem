import customtkinter as ctk
from tkinter import ttk, messagebox

class RequestCategoryScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_categories_data = []

        # ========================================================
        # 1. HEADER SECTION
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            self.header_frame,
            text="🏷️ Request Categories Management",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(
            self.header_frame,
            text="➕ Create New Category",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_category_form
        )
        btn_add.pack(side="right", padx=(0, 20))

        # ========================================================
        # 2. MAIN DATA CONTAINER CARD
        # ========================================================
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#E6E9ED", foreground="#434A54", font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#E6F2FF')], foreground=[('selected', '#1A62E8')])

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Updated columns definition including description and required_skills
        columns = ("category_id", "category_name", "description", "required_skills")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("category_id", text="ID")
        self.tree.heading("category_name", text="Category Name")
        self.tree.heading("description", text="Description")
        self.tree.heading("required_skills", text="Required Skills")

        # Column structural configuration
        self.tree.column("category_id", width=60, minwidth=50, stretch=False, anchor="center")
        self.tree.column("category_name", width=180, minwidth=150, stretch=False, anchor="w")
        self.tree.column("description", width=500, minwidth=250, stretch=False, anchor="w")
        self.tree.column("required_skills", width=250, minwidth=150, stretch=False, anchor="w")

        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')

        # ========================================================
        # 3. ACTIONS FOOTER BAR
        # ========================================================
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent", height=50)
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.footer_frame.pack_propagate(False)

        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Delete", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=120, height=38, corner_radius=8, command=self.delete_selected_category)
        btn_delete.pack(side="left")

        btn_update = ctk.CTkButton(self.footer_frame, text="✏️ Update", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", width=120, height=38, corner_radius=8, command=self.trigger_update_button_click)
        btn_update.pack(side="left", padx=15)

        self.load_categories_from_db()

    # ========================================================
    # SQL ENGINE & DATA MANAGEMENT
    # ========================================================
    def load_categories_from_db(self):
        if not self.conn: return
        self.all_categories_data.clear()
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT category_id, category_name, description, required_skills 
                FROM public.a_requestcategory 
                ORDER BY category_id ASC;
            """
            cursor.execute(query)
            self.all_categories_data = cursor.fetchall()
            cursor.close()
            
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(self.all_categories_data):
                # Clean None values for display
                formatted_row = [str(item) if item is not None else "" for item in row]
                row_tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=formatted_row, tags=(row_tag,))
        except Exception as e:
            print(f"❌ SQL Engine failure fetching categories: {e}")

    def trigger_update_button_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a category item from the list to update.")
            return
        row_values = self.tree.item(selected_item, "values")
        self.open_category_form(edit_mode=True, data=row_values)

    def delete_selected_category(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a target row.")
            return

        values = self.tree.item(selected_item, "values")
        cat_id = values[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Permanently wipe Category #{cat_id}?")
        if not confirm: return

        try:
            cursor = self.conn.cursor()
            # Safety: disconnect from requests first
            cursor.execute("UPDATE public.a_request SET category_id = NULL WHERE category_id = %s;", (int(cat_id),))
            cursor.execute("DELETE FROM public.a_requestcategory WHERE category_id = %s;", (int(cat_id),))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Success", "Category purged smoothly.")
            self.load_categories_from_db()
        except Exception as e:
            if self.conn: self.conn.rollback()
            messagebox.showerror("SQL Error", f"Database engine error: {e}")

    # ========================================================
    # TRANSACTION FORM MODAL VIEW HANDLERS (INSERT / UPDATE)
    # ========================================================
    def open_category_form(self, edit_mode=False, data=None):
        next_id = None
        if not edit_mode:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM public.a_requestcategory;")
                next_id = cursor.fetchone()[0]
                cursor.close()
            except Exception as e:
                messagebox.showerror("Sync Error", f"Could not calculate next ID: {e}")
                return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Category" if edit_mode else "Register New Category")
        form_window.geometry("500x580") # Slightly taller to accommodate new fields
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="🏷️ Request Category Data Entry", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(20, 15))

        body_frame = ctk.CTkScrollableFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        body_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # 1. ID
        ctk.CTkLabel(body_frame, text="Category ID:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(body_frame, width=400, height=32)
        entry_id.pack(padx=20, pady=(0, 10))
        if edit_mode: entry_id.insert(0, data[0])
        else: entry_id.insert(0, str(next_id))
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. Name
        ctk.CTkLabel(body_frame, text="Category Name:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(body_frame, width=400, height=32)
        entry_name.pack(padx=20, pady=(0, 10))
        if edit_mode: entry_name.insert(0, data[1])

        # 3. Description
        ctk.CTkLabel(body_frame, text="Detailed Description:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_desc = ctk.CTkEntry(body_frame, width=400, height=32, placeholder_text="Enter purpose of this category...")
        entry_desc.pack(padx=20, pady=(0, 10))
        if edit_mode and data[2] != 'None': entry_desc.insert(0, data[2])

        # 4. Required Skills
        ctk.CTkLabel(body_frame, text="Required Skills (Tag references):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_skills = ctk.CTkEntry(body_frame, width=400, height=32, placeholder_text="e.g., First Aid, Driving, Plumbing...")
        entry_skills.pack(padx=20, pady=(0, 20))
        if edit_mode and data[3] != 'None': entry_skills.insert(0, data[3])

        def save_form_data():
            c_name = entry_name.get().strip()
            c_desc = entry_desc.get().strip() or None
            c_skills = entry_skills.get().strip() or None

            if not c_name:
                messagebox.showwarning("Error", "Category Name is required.", parent=form_window)
                return

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    c_id = data[0]
                    sql = """
                        UPDATE public.a_requestcategory 
                        SET category_name = %s, description = %s, required_skills = %s 
                        WHERE category_id = %s;
                    """
                    cursor.execute(sql, (c_name, c_desc, c_skills, int(c_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(category_id), 0) + 1 FROM public.a_requestcategory;")
                    final_id = cursor.fetchone()[0]
                    sql = """
                        INSERT INTO public.a_requestcategory (category_id, category_name, description, required_skills) 
                        VALUES (%s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(final_id), c_name, c_desc, c_skills))

                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Category updated successfully.", parent=form_window)
                form_window.destroy()
                self.load_categories_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Error", f"Operation failed: {e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Commit Changes", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 20))