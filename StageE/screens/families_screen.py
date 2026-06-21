import customtkinter as ctk
from tkinter import ttk, messagebox

class FamiliesScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_families_data = []

        # --- HEADER SECTION (With Add Button) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(self.header_frame, text="👥 Families Management System", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        # Add Family Action Button placed at the top right corner
        btn_add = ctk.CTkButton(self.header_frame, text="➕ Add New Family", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8, command=self.open_family_form)
        btn_add.pack(side="right")

        # ========================================================
        # 🚀 NEW SECTION: HARMONIZED DYNAMIC SEARCH BAR
        # ========================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 8))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search family:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057"
        )
        search_label.pack(side="left", padx=(0, 8))

        # Dynamic Autocomplete ComboBox Registry Entry
        self.entry_search = ctk.CTkComboBox(
            self.search_frame,
            values=[],
            width=330,
            height=34,
            command=self.filter_search_table
        )
        self.entry_search.pack(side="left", padx=(0, 10))
        self.entry_search.set("Search by ID, name, phone or special features...")
        self.entry_search.bind("<KeyRelease>", self.filter_search_table)
        self.entry_search._entry.bind("<FocusIn>", self.clear_placeholder_on_click)

        btn_show_all = ctk.CTkButton(
            self.search_frame,
            text="Show All",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6C757D",
            hover_color="#5C636A",
            width=90,
            height=34,
            corner_radius=7,
            command=self.clear_search_filter
        )
        btn_show_all.pack(side="left")

        self.lbl_counter = ctk.CTkLabel(self.search_frame, text="0 family(ies) shown", font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D")
        self.lbl_counter.pack(side="right", padx=5)

        # Main Data Container Card
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=35, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#E6E9ED", foreground="#434A54", font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#1A62E8')], foreground=[('selected', '#FFFFFF')])

        # Table containment sub-frame to properly align view grids
        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        # Data Grid Layout Configuration
        columns = ("contactperson_id", "contactperson_name", "phone_number", "number_of_members", "special_features")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)
        
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

        # --- TABLE ACTIONS FOOTER BAR ---
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(5, 15))

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

    # ========================================================
    # DATA RETRIEVAL & FILTERING ENGINE
    # ========================================================
    def load_families_from_db(self):
        if not self.conn:
            return
        self.all_families_data.clear()
        try:
            cursor = self.conn.cursor()
            query = "SELECT contactperson_id, contactperson_name, phone_number, number_of_members, special_features FROM public.a_family ORDER BY contactperson_id ASC;"
            cursor.execute(query)
            self.all_families_data = cursor.fetchall()
            cursor.close()

            # Dynamic string suggestions builder block
            search_suggestions = []
            for row in self.all_families_data:
                cp_id, cp_name, _, _, _ = row
                search_suggestions.append(f"ID #{cp_id} | {cp_name}")

            self.entry_search.configure(values=search_suggestions)
            self.filter_search_table()
        except Exception as e:
            messagebox.showerror("SQL Database Error", f"Failed to retrieve data rows from a_family:\n{e}")

    def filter_search_table(self, event=None):
        raw_keyword = self.entry_search._entry.get().strip().lower()
        is_exact_id_match = False
        search_keyword = raw_keyword

        if "id #" in raw_keyword:
            search_keyword = raw_keyword.split("id #")[1].split(" ")[0].strip()
            is_exact_id_match = True
        elif raw_keyword == "search by id, name, phone or special features...":
            search_keyword = ""

        self.tree.delete(*self.tree.get_children())
        shown_count = 0

        for row in self.all_families_data:
            cp_id, cp_name, phone, members, features = row
            features_clean = features or ""

            if is_exact_id_match:
                if str(cp_id) != search_keyword: continue
            else:
                match_string = f"{cp_id} {str(cp_name).lower()} {phone} {str(features_clean).lower()}".lower()
                if search_keyword not in match_string: continue

            formatted_row = [str(item) if item is not None else "" for item in row]
            row_tag = "evenrow" if shown_count % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=formatted_row, tags=(row_tag,))
            shown_count += 1

        self.lbl_counter.configure(text=f"{shown_count} family(ies) shown")

    def clear_search_filter(self):
        self.entry_search._entry.delete(0, "end")
        self.filter_search_table()

    def clear_placeholder_on_click(self, event):
        """Clears the baseline placeholder text automatically upon gaining focus"""
        current_text = self.entry_search.get()
        if current_text == "Search by ID, name, phone or special features...":
            self.entry_search.set("")
            
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

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete the profile for:\n👉 {family_name} (ID: #{family_id})?")
        if confirm:
            try:
                cursor = self.conn.cursor()
                # Safeguard cascade rule handling to avoid broken constraint pipelines
                cursor.execute("UPDATE public.a_request SET contactperson_id = NULL WHERE contactperson_id = %s;", (family_id,))
                cursor.execute("DELETE FROM public.a_family WHERE contactperson_id = %s;", (family_id,))
                self.conn.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Family record successfully truncated from database registry.")
                self.load_families_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Transaction Failed", f"Database engine refused delete constraint execution:\n{e}")

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        row_values = self.tree.item(selected_item, "values")
        self.open_family_form(edit_mode=True, data=row_values)

    # ========================================================
    # CRUD: FORM INJECTION WINDOW DIALOG MODAL (CREATE / UPDATE)
    # ========================================================
    def open_family_form(self, edit_mode=False, data=None):
        next_id = None
        if not edit_mode:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COALESCE(MAX(contactperson_id), 0) + 1 FROM public.a_family;")
                next_id = cursor.fetchone()[0]
                cursor.close()
            except Exception as e:
                messagebox.showerror("Sequence Tracker Fault", f"Could not sync automatic primary key pointer node safely:\n{e}")
                return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Family Registry" if edit_mode else "Register New Family Profile")
        form_window.geometry("450x520")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set() 
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="📝 Family Profile Attributes Form", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # 1. Contact Person ID (Automated Sequential Integer Assignment)
        ctk.CTkLabel(fields_container, text="Contact Person ID (Primary Key Reference Pointer)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=360, height=32)
        entry_id.pack(padx=20, pady=(0, 8))
        
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, str(next_id))
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. Name Field Entry Layout
        ctk.CTkLabel(fields_container, text="Contact Person Full Name *", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., John Doe")
        entry_name.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_name.insert(0, data[1])

        # 3. Phone Number Field Layout Component
        ctk.CTkLabel(fields_container, text="Phone Number *", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_phone = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., 0501234567")
        entry_phone.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_phone.insert(0, data[2])

        # 4. Members Int Counter Layout Field Widget
        ctk.CTkLabel(fields_container, text="Number of Members *", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_members = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., 4")
        entry_members.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_members.insert(0, data[3])

        # 5. Special Features Blob Data Attribute Block Area Entry Component
        ctk.CTkLabel(fields_container, text="Special Features / Assistance Notes", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_features = ctk.CTkEntry(fields_container, width=360, height=32, placeholder_text="e.g., Wheelchair access")
        entry_features.pack(padx=20, pady=(0, 15))
        if edit_mode and data[4] != 'None': entry_features.insert(0, data[4])

        # Save Button Event Routine Logic Processing
        def save_form_data():
            cp_name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            members = entry_members.get().strip()
            features = entry_features.get().strip() or None

            if not cp_name or not phone or not members:
                messagebox.showwarning("Validation Error", "All primary record form properties fields must be populated completely before saving changes.", parent=form_window)
                return

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    cp_id = data[0]
                    sql = """
                        UPDATE public.a_family 
                        SET contactperson_name = %s, phone_number = %s, number_of_members = %s, special_features = %s 
                        WHERE contactperson_id = %s;
                    """
                    cursor.execute(sql, (cp_name, phone, int(members), features, int(cp_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(contactperson_id), 0) + 1 FROM public.a_family;")
                    final_generated_id = cursor.fetchone()[0]
                    
                    sql = """
                        INSERT INTO public.a_family (contactperson_id, contactperson_name, phone_number, number_of_members, special_features) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(final_generated_id), cp_name, phone, int(members), features))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Database storage sync transaction completed successfully.", parent=form_window)
                form_window.destroy()
                self.load_families_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Engine Transaction Refused", f"Failed to commit database rows state change validation rules:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Save Profile Changes", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))