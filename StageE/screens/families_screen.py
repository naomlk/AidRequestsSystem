import customtkinter as ctk
from tkinter import ttk, messagebox

class FamiliesScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection

        # --- HEADER SECTION (With Add Button) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(self.header_frame, text="👥 Families Management System", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        # Add Family Action Button placed at the top right corner
        btn_add = ctk.CTkButton(self.header_frame, text="➕ Add New Family", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8, command=self.open_family_form)
        btn_add.pack(side="right")

        # Main Data Container Card
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=35, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#F1F3F5", foreground="#495057", font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#1A62E8')], foreground=[('selected', '#FFFFFF')])

        # Data Grid Layout Configuration
        columns = ("contactperson_id", "contactperson_name", "phone_number", "number_of_members", "special_features")
        self.tree = ttk.Treeview(self.container_box, columns=columns, show="headings")
        
        self.tree.heading("contactperson_id", text="Contact Person ID")
        self.tree.heading("contactperson_name", text="Contact Person Name")
        self.tree.heading("phone_number", text="Phone Number")
        self.tree.heading("number_of_members", text="Members Count")
        self.tree.heading("special_features", text="Special Features")

        self.tree.column("contactperson_id", width=120, anchor="center")
        self.tree.column("contactperson_name", width=180, anchor="w")
        self.tree.column("phone_number", width=140, anchor="center")
        self.tree.column("number_of_members", width=120, anchor="center")
        self.tree.column("special_features", width=220, anchor="w")

        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')

        self.tree.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # --- TABLE ACTIONS FOOTER BAR ---
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Delete Action Button located directly under the grid view
        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Delete Selected Family", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=180, height=35, corner_radius=6, command=self.delete_selected_family)
        btn_delete.pack(side="left")

        # Hint description label matching your project requirements
        hint_lbl = ctk.CTkLabel(self.footer_frame, text="💡 Tip: Double-click on any row item to edit/update family profile records.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#6C757D")
        hint_lbl.pack(side="right", pady=5)

        # Bind the Double-Click gesture to execute the update record routine
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # Fetch active records from PostgreSQL schema container instance
        self.load_families_from_db()

    def load_families_from_db(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            query = "SELECT contactperson_id, contactperson_name, phone_number, number_of_members, special_features FROM public.a_family ORDER BY contactperson_id;"
            cursor.execute(query)
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, row in enumerate(rows):
                if i % 2 == 0:
                    self.tree.insert("", "end", values=row, tags=('evenrow',))
                else:
                    self.tree.insert("", "end", values=row, tags=('oddrow',))

            cursor.close()
        except Exception as e:
            messagebox.showerror("SQL Database Error", f"Failed to retrieve data rows from a_family:\n{e}")

    # ========================================================
    # CRUD: DELETE TRANSACTION ROUTINE
    # ========================================================
    def delete_selected_family(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please click on a family row item from the list before requesting a deletion.")
            return

        values = self.tree.item(selected_item, "values")
        family_id = values[0]
        family_name = values[1]

        # Security double-check handshake modal step
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete the profile for:\n👉 {family_name} (ID: #{family_id})?")
        if confirm:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM public.a_family WHERE contactperson_id = %s;", (family_id,))
                self.conn.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Family record successfully truncated from database registry.")
                self.load_families_from_db() # Refresh list view UI
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("SQL Transaction Failed", f"Database engine refused delete constraint execution:\n{e}")

    # ========================================================
    # CRUD: INTERACTIVE ROW DOUBLE-CLICK BINDING (UPDATE ROUTE)
    # ========================================================
    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item, "values")
        # Open form populating values inside context variables for immediate update changes
        self.open_family_form(edit_mode=True, data=row_values)

    # ========================================================
    # CRUD: FORM INJECTION WINDOW DIALOG MODAL (CREATE / UPDATE)
    # ========================================================
    def open_family_form(self, edit_mode=False, data=None):
        # Instantiate a clean dedicated Toplevel window layout frame shell
        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Family Registry" if edit_mode else "Register New Family Profile")
        form_window.geometry("450x520")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set() # Lock main window focus context interaction until window gets closed
        form_window.resizable(False, False)

        # Window Frame Title Visual Labels Block
        form_title = ctk.CTkLabel(form_window, text="📝 Family Profile Attributes Form", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # ID Field Label Management Handling Block Context
        ctk.CTkLabel(fields_container, text="Contact Person ID (Primary Key)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., 1001")
        entry_id.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
            entry_id.configure(state="disabled", fg_color="#F1F3F5") # Lock Primary Key on updates

        # Name Field Entry Layout
        ctk.CTkLabel(fields_container, text="Contact Person Full Name", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., John Doe")
        entry_name.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_name.insert(0, data[1])

        # Phone Number Field Layout Component
        ctk.CTkLabel(fields_container, text="Phone Number", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_phone = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., 0501234567")
        entry_phone.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_phone.insert(0, data[2])

        # Members Int Counter Layout Field Widget
        ctk.CTkLabel(fields_container, text="Number of Members", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_members = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., 4")
        entry_members.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_members.insert(0, data[3])

        # Special Features Blob Data Attribute Block Area Entry Component
        ctk.CTkLabel(fields_container, text="Special Features / Assistance Notes", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_features = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., Wheelchair access")
        entry_features.pack(padx=20, pady=(0, 15))
        if edit_mode: entry_features.insert(0, data[4])

        # Save Button Event Routine Logic Processing
        def save_form_data():
            cp_id = entry_id.get().strip()
            cp_name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            members = entry_members.get().strip()
            features = entry_features.get().strip()

            if not cp_id or not cp_name or not phone or not members:
                messagebox.showwarning("Validation Error", "All primary record form properties fields must be populated completely before saving changes.", parent=form_window)
                return

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    sql = """
                        UPDATE public.a_family 
                        SET contactperson_name = %s, phone_number = %s, number_of_members = %s, special_features = %s 
                        WHERE contactperson_id = %s;
                    """
                    cursor.execute(sql, (cp_name, phone, int(members), features, cp_id))
                else:
                    sql = """
                        INSERT INTO public.a_family (contactperson_id, contactperson_name, phone_number, number_of_members, special_features) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(cp_id), cp_name, phone, int(members), features))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Database storage sync transaction completed successfully.", parent=form_window)
                form_window.destroy()
                self.load_families_from_db() # Reload data grid list
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("SQL Engine Transaction Refused", f"Failed to commit database rows state change validation rules:\n{e}", parent=form_window)

       
        btn_save = ctk.CTkButton(form_window, text="💾 Save Profile Changes", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))