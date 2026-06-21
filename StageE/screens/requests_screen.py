import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date as datetime_date

class RequestsScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_requests_data = []

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(self.header_frame, text="📋 Requests Management System", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(self.header_frame, text="➕ Create New Request", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8, command=self.open_request_form)
        btn_add.pack(side="right")

        # ========================================================
        # SEARCH BAR SECTION
        # ========================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 8))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search request:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057"
        )
        search_label.pack(side="left", padx=(0, 8))

        self.entry_search = ctk.CTkComboBox(
            self.search_frame,
            values=[],
            width=330,
            height=34,
            command=self.filter_search_table
        )
        self.entry_search.pack(side="left", padx=(0, 10))
        self.entry_search.set("Search by ID, status, description or coordinates...")
        self.entry_search.bind("<KeyRelease>", self.filter_search_table)
        # 🚀 Focus Management event bindings for the search field
        self.entry_search._entry.bind("<FocusIn>", self.clear_placeholder_on_click)
      

        self.combo_status = ctk.CTkComboBox(
            self.search_frame,
            values=["All Statuses", "Pending", "In Progress", "Completed"],
            width=145,
            height=34,
            command=self.filter_search_table
        )
        self.combo_status.pack(side="left", padx=(0, 10))
        self.combo_status.set("All Statuses")

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

        self.lbl_counter = ctk.CTkLabel(self.search_frame, text="0 request(s) shown", font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D")
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

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        # Adjusted columns sequence layout schema map tracking names
        columns = (
            "request_id", "date", "image", "incident_description", 
            "prioriry_level", "contactperson_id", "category_name", 
            "status_label", "latitude", "longitude"
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Table Headings
        self.tree.heading("request_id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("image", text="Image Path")
        self.tree.heading("incident_description", text="Description")
        self.tree.heading("prioriry_level", text="Priority")
        self.tree.heading("contactperson_id", text="Family ID")
        self.tree.heading("category_name", text="Category Name")
        self.tree.heading("status_label", text="Status")
        self.tree.heading("latitude", text="Latitude")
        self.tree.heading("longitude", text="Longitude")

        # Column Formatting
        self.tree.column("request_id", width=60, minwidth=50, anchor="center")
        self.tree.column("date", width=110, minwidth=90, anchor="center")
        self.tree.column("image", width=130, minwidth=100, anchor="w")
        self.tree.column("incident_description", width=250, minwidth=180, anchor="w")
        self.tree.column("prioriry_level", width=80, minwidth=60, anchor="center")
        self.tree.column("contactperson_id", width=110, minwidth=80, anchor="center")
        self.tree.column("category_name", width=140, minwidth=100, anchor="w")
        self.tree.column("status_label", width=110, minwidth=80, anchor="center")
        self.tree.column("latitude", width=110, minwidth=80, anchor="center")
        self.tree.column("longitude", width=110, minwidth=80, anchor="center")

        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')

        # --- ACTIONS FOOTER BAR ---
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(5, 15))

        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Cancel / Delete Request", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=180, height=35, corner_radius=6, command=self.delete_selected_request)
        btn_delete.pack(side="left")

        hint_lbl = ctk.CTkLabel(self.footer_frame, text="💡 Tip: Double-click on any active incident row to update its status or description.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#6C757D")
        hint_lbl.pack(side="right", pady=5)

        self.tree.bind("<Double-1>", self.on_row_double_click)
        self.load_requests_from_db()

    # ========================================================
    # LOGIQUE RECHERCHE ET CHARGEMENT DYNAMIQUE
    # ========================================================
    def load_requests_from_db(self):
        if not self.conn:
            return
        self.all_requests_data.clear()
        try:
            cursor = self.conn.cursor()
            # SQL Query joined with request category and status data mapping references nodes
            query = """
                SELECT r.request_id, r.date, r.image, r.incident_description, 
                       r.prioriry_level, r.contactperson_id, c.category_name, 
                       s.status_label, r.latitude, r.longitude 
                FROM public.a_request r
                LEFT JOIN public.a_requestcategory c ON r.category_id = c.category_id
                LEFT JOIN public.a_status s ON r.status_id = s.status_id
                ORDER BY r.request_id DESC;
            """
            cursor.execute(query)
            self.all_requests_data = cursor.fetchall()
            cursor.close()

            search_suggestions = []
            for row in self.all_requests_data:
                r_id, _, _, desc, priority, _, _, _, _, _ = row
                desc_clean = desc or "No description"
                desc_short = desc_clean[:30] + "..." if len(desc_clean) > 30 else desc_clean
                
                suggestion_string = f"ID #{r_id} | Prio: {priority} | {desc_short}"
                search_suggestions.append(suggestion_string)

            self.entry_search.configure(values=search_suggestions)
            self.filter_search_table()
        except Exception as e:
            messagebox.showerror("SQL Database Error", f"Failed to retrieve requests:\n{e}")

    def filter_search_table(self, event=None):
        raw_keyword = self.entry_search._entry.get().strip().lower()
        is_exact_id_match = False
        search_keyword = raw_keyword
        
        if "id #" in raw_keyword:
            search_keyword = raw_keyword.split("id #")[1].split(" ")[0].strip()
            is_exact_id_match = True
        elif raw_keyword == "search by id, status, description or coordinates...":
            search_keyword = ""
            
        selected_status_filter = self.combo_status.get()
        self.tree.delete(*self.tree.get_children())
        
        shown_count = 0
        for row in self.all_requests_data:
            r_id, req_date, img, desc, priority, cp_id, cat_name, status_name, lat, lon = row
            
            # Filtering validation using text mapping properties indices
            if selected_status_filter != "All Statuses" and str(status_label) != selected_status_filter:
                continue

            if is_exact_id_match:
                if str(r_id) != search_keyword: continue
            else:
                match_string = f"{r_id} {str(desc).lower()} {lat} {lon} {req_date}".lower()
                if search_keyword not in match_string: continue

            row_tag = "evenrow" if shown_count % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(row_tag,))
            shown_count += 1
                
        self.lbl_counter.configure(text=f"{shown_count} request(s) shown")

    def clear_search_filter(self):
        self.entry_search._entry.delete(0, "end")
        self.combo_status.set("All Statuses")
        self.filter_search_table()

    def clear_placeholder_on_click(self, event):
        """Clears the baseline placeholder text automatically upon gaining focus"""
        current_text = self.entry_search.get().strip()
        if current_text == "Search by ID, status, description or coordinates...":
            self.entry_search.set("")

    def delete_selected_request(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a request row item from the list before deleting.")
            return

        values = self.tree.item(selected_item, "values")
        req_id = values[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete Request #{req_id}?")
        if confirm:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM public.a_request WHERE request_id = %s;", (req_id,))
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Request successfully purged from database.")
                self.load_requests_from_db()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("SQL Transaction Failed", f"Database refused operation:\n{e}")

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        row_values = self.tree.item(selected_item, "values")
        self.open_request_form(edit_mode=True, data=row_values)

    # ========================================================
    # FORM DIALOG MODAL (CREATE / UPDATE WITH MAPPED COMBOBOXES)
    # ========================================================
    def open_request_form(self, edit_mode=False, data=None):
        categories_map = {}
        statuses_map = {}
        next_id = None

        try:
            cursor = self.conn.cursor()
            # Fetch relational configuration mapping dictionaries categories variables indicators properties
            cursor.execute("SELECT category_id, category_name FROM public.a_requestcategory ORDER BY category_name;")
            for cid, cname in cursor.fetchall():
                categories_map[cname] = cid

            cursor.execute("SELECT status_id, status_label FROM public.a_status ORDER BY status_id;")
            for sid, sname in cursor.fetchall():
                statuses_map[sname] = sid

            # Sequence lookup tracker calculations algorithm sequence loop context node
            if not edit_mode:
                cursor.execute("SELECT COALESCE(MAX(request_id), 0) + 1 FROM public.a_request;")
                next_id = cursor.fetchone()[0]

            cursor.close()
        except Exception as e:
            messagebox.showerror("Relational Sync Error", f"Failed to pre-fetch options schemas indicators maps:\n{e}")
            return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Request Information" if edit_mode else "File New Assistance Request")
        form_window.geometry("520x640")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="📝 Incident Request Attributes Form", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkScrollableFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # 1. Request ID (Calculated dynamically on create sequence tracking)
        ctk.CTkLabel(fields_container, text="Request ID (Primary Key Reference Pointer)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_id.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, str(next_id))
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. Date
        ctk.CTkLabel(fields_container, text="Incident Date (YYYY-MM-DD)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_date = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_date.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_date.insert(0, data[1])
        else: entry_date.insert(0, str(datetime_date.today()))

        # 3. Image URL/Path
        ctk.CTkLabel(fields_container, text="Incident Image File Path", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_img = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="images/elevator_stuck.png")
        entry_img.pack(padx=20, pady=(0, 8))
        if edit_mode and data[2] and data[2] != 'None': entry_img.insert(0, data[2])

        # 4. Incident Description
        ctk.CTkLabel(fields_container, text="Detailed Incident Description", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_desc = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., Person stuck in elevator on 4th floor")
        entry_desc.pack(padx=20, pady=(0, 8))
        if edit_mode and data[3]: entry_desc.insert(0, data[3])

        # 5. Priority Level ComboBox (Restricted integer range constraints 1-5 selection node)
        ctk.CTkLabel(fields_container, text="Priority Level Mapping Scope:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_priority = ctk.CTkComboBox(fields_container, values=["1", "2", "3", "4", "5"], width=400, height=32)
        entry_priority.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_priority.set(data[4])
        else: entry_priority.set("1")

        # 6. Contact Person ID
        ctk.CTkLabel(fields_container, text="Associated Family ID (contactperson_id)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_cp_id = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="Must exist in a_family table")
        entry_cp_id.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_cp_id.insert(0, data[5])

        # 7. Category Name ComboBox 
        ctk.CTkLabel(fields_container, text="Category Assignment Branch:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        category_options = list(categories_map.keys())
        entry_cat = ctk.CTkComboBox(fields_container, values=category_options, width=400, height=32)
        entry_cat.pack(padx=20, pady=(0, 8))
        if edit_mode and data[6]: entry_cat.set(data[6])

        # 8. Status Name ComboBox
        ctk.CTkLabel(fields_container, text="Status Management Registry State:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        status_options = list(statuses_map.keys())
        entry_status = ctk.CTkComboBox(fields_container, values=status_options, width=400, height=32)
        entry_status.pack(padx=20, pady=(0, 8))
        if edit_mode and data[7]: 
            entry_status.set(data[7])
        else:
            entry_status.set("Pending")
            entry_status.configure(state="disabled", fg_color="#F1F3F5")

        # 9. Latitude
        ctk.CTkLabel(fields_container, text="Latitude coordinates (Israel)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lat = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 31.7683")
        entry_lat.pack(padx=20, pady=(0, 8))
        if edit_mode and data[8] and data[8] != 'None': entry_lat.insert(0, data[8])

        # 10. Longitude
        ctk.CTkLabel(fields_container, text="Longitude coordinates (Israel)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 15))
        entry_lon = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 35.2137")
        entry_lon.pack(padx=20, pady=(0, 15))
        if edit_mode and data[9] and data[9] != 'None': entry_lon.insert(0, data[9])

        # Process Submission
        def save_form_data():
            r_date = entry_date.get().strip()
            img = entry_img.get().strip()
            desc = entry_desc.get().strip()
            prio = entry_priority.get().strip()
            cp_id = entry_cp_id.get().strip()
            selected_cat_name = entry_cat.get()
            selected_stat_name = entry_status.get()
            lat = entry_lat.get().strip()
            lon = entry_lon.get().strip()

            if not prio or not cp_id or not selected_cat_name or not selected_stat_name:
                messagebox.showwarning("Validation Error", "Please fill out all required key attributes properties options.", parent=form_window)
                return

            cat_id = categories_map.get(selected_cat_name)
            stat_id = statuses_map.get(selected_stat_name)

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    r_id = data[0]
                    sql = """
                        UPDATE public.a_request 
                        SET date = %s, image = %s, incident_description = %s, prioriry_level = %s, 
                            contactperson_id = %s, category_id = %s, status_id = %s, latitude = %s, longitude = %s 
                        WHERE request_id = %s;
                    """
                    cursor.execute(sql, (r_date, img if img else None, desc, int(prio), int(cp_id), int(cat_id), int(stat_id), float(lat) if lat else None, float(lon) if lon else None, int(r_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(request_id), 0) + 1 FROM public.a_request;")
                    final_generated_id = cursor.fetchone()[0]

                    sql = """
                        INSERT INTO public.a_request (request_id, date, image, incident_description, prioriry_level, contactperson_id, category_id, status_id, latitude, longitude) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(final_generated_id), r_date, img if img else None, desc, int(prio), int(cp_id), int(cat_id), int(stat_id), float(lat) if lat else None, float(lon) if lon else None))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Incident request committed successfully to backend schemas.", parent=form_window)
                form_window.destroy()
                self.load_requests_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Transaction Error", f"Database engine refused execution:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Save Request Details", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))