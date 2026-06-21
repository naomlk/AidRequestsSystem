import customtkinter as ctk
from tkinter import messagebox, ttk

class SkillCategoryScreen(ctk.CTkFrame):
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
            text="📁 Skill Categories Management",
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
        # 2. MAIN DATA CONTAINER CARD (Normal layout width size)
        # ========================================================
        # Box stretches normally with fill="both" and expand=True
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 12))
        style.configure("Treeview.Heading", background="#E6E9ED", foreground="#434A54", font=("Segoe UI", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#E6F2FF')], foreground=[('selected', '#1A62E8')])

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        columns = ("catagory_id", "catagory_name")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("catagory_id", text="Category ID")
        self.tree.heading("catagory_name", text="Category Name")

        # 🛠️ Narrow column widths constraint configurations (Leaving empty whitespace on the right)
        self.tree.column("catagory_id", width=150, minwidth=100, stretch=False, anchor="center")
        self.tree.column("catagory_name", width=400, minwidth=180, stretch=False, anchor="w")

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
                SELECT catagory_id, catagory_name 
                FROM public.b_catagory 
                ORDER BY catagory_id ASC;
            """
            cursor.execute(query)
            self.all_categories_data = cursor.fetchall()
            cursor.close()
            
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(self.all_categories_data):
                formatted_row = [str(item) if item is not None else "" for item in row]
                row_tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=formatted_row, tags=(row_tag,))
        except Exception as e:
            print(f"❌ SQL Engine failure fetching category catalog: {e}")

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
            messagebox.showwarning("Selection Missing", "Please select a target category row item from the list.")
            return

        values = self.tree.item(selected_item, "values")
        cat_id = values[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Permanently wipe Category #{cat_id}?")
        if not confirm: return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE public.b_skill SET category_id = NULL WHERE category_id = %s;", (int(cat_id),))
            cursor.execute("DELETE FROM public.b_catagory WHERE catagory_id = %s;", (int(cat_id),))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Pruning Confirmed", "Category record wiped smoothly.")
            self.load_categories_from_db()
        except Exception as e:
            if self.conn: self.conn.rollback()
            messagebox.showerror("SQL Core Exception Fail", f"Database engine refused pruning operation:\n{e}")

    # ========================================================
    # TRANSACTION FORM MODAL VIEW HANDLERS (INSERT / UPDATE)
    # ========================================================
    def open_category_form(self, edit_mode=False, data=None):
        next_id = None
        if not edit_mode:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COALESCE(MAX(catagory_id), 0) + 1 FROM public.b_catagory;")
                next_id = cursor.fetchone()[0]
                cursor.close()
            except Exception as e:
                messagebox.showerror("Handshake Fault", f"Could not sync automatic id properties safely:\n{e}")
                return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Update Category" if edit_mode else "Register New Category")
        form_window.geometry("450x300")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="📁 Category Mapping Node Entry Descriptor", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(20, 15))

        body_frame = ctk.CTkFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        body_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        ctk.CTkLabel(body_frame, text="Category ID:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(15, 2))
        entry_id = ctk.CTkEntry(body_frame, width=350, height=32)
        entry_id.pack(padx=20, pady=(0, 10))
        
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, str(next_id))
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        ctk.CTkLabel(body_frame, text="Category Name:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(body_frame, width=350, height=32, placeholder_text="e.g., Medical Assistance, Logistics...")
        entry_name.pack(padx=20, pady=(0, 20))
        if edit_mode: entry_name.insert(0, data[1])

        def save_form_data():
            c_name = entry_name.get().strip()

            if not c_name:
                messagebox.showwarning("Validation Error", "The category name field requirement is required.", parent=form_window)
                return

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    c_id = data[0]
                    sql = """
                        UPDATE public.b_catagory 
                        SET catagory_name = %s 
                        WHERE catagory_id = %s;
                    """
                    cursor.execute(sql, (c_name, int(c_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(catagory_id), 0) + 1 FROM public.b_catagory;")
                    final_id = cursor.fetchone()[0]

                    sql = """
                        INSERT INTO public.b_catagory (catagory_id, catagory_name) 
                        VALUES (%s, %s);
                    """
                    cursor.execute(sql, (int(final_id), c_name))

                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success Record Saved", "Category saved successfully.", parent=form_window)
                form_window.destroy()
                self.load_categories_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Error Engine Conflict", f"Database transaction failed:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Commit Category Attributes", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 20))