import customtkinter as ctk
from tkinter import ttk, messagebox

class VolunteersScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection

        # --- HEADER SECTION (With Add Button) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(self.header_frame, text="👷 Volunteers Tracker", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        # Add Action Button at top right corner
        btn_add = ctk.CTkButton(self.header_frame, text="➕ Add New Volunteer", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8, command=self.open_volunteer_form)
        btn_add.pack(side="right")

        # Main Data Container (White background card)
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=35, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#F1F3F5", foreground="#495057", font=("Segoe UI", 11, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#1A62E8')], foreground=[('selected', '#FFFFFF')])

        # Data Grid Layout Configuration (All original volunteer attributes)
        columns = (
            "volunteer_id", "first_name", "last_name", "phone_number", 
            "has_equipment", "counter", "latitude", "longitude", 
            "recruitment_date", "email", "is_active"
        )
        self.tree = ttk.Treeview(self.container_box, columns=columns, show="headings")
        
        # Table Headings
        self.tree.heading("volunteer_id", text="ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("phone_number", text="Phone Number")
        self.tree.heading("has_equipment", text="Equipment")
        self.tree.heading("counter", text="Missions")
        self.tree.heading("latitude", text="Latitude")
        self.tree.heading("longitude", text="Longitude")
        self.tree.heading("recruitment_date", text="Recruitment Date")
        self.tree.heading("email", text="Email Address")
        self.tree.heading("is_active", text="Active")

        # Column Formatting & Widths
        self.tree.column("volunteer_id", width=50, anchor="center")
        self.tree.column("first_name", width=95, anchor="w")
        self.tree.column("last_name", width=95, anchor="w")
        self.tree.column("phone_number", width=110, anchor="center")
        self.tree.column("has_equipment", width=80, anchor="center")
        self.tree.column("counter", width=70, anchor="center")
        self.tree.column("latitude", width=80, anchor="center")
        self.tree.column("longitude", width=80, anchor="center")
        self.tree.column("recruitment_date", width=110, anchor="center")
        self.tree.column("email", width=140, anchor="w")
        self.tree.column("is_active", width=60, anchor="center")

        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')

        self.tree.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # --- TABLE ACTIONS FOOTER BAR ---
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Delete Action Button directly under the grid view
        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Delete Selected Volunteer", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=180, height=35, corner_radius=6, command=self.delete_selected_volunteer)
        btn_delete.pack(side="left")

        hint_lbl = ctk.CTkLabel(self.footer_frame, text="💡 Tip: Double-click on any row item to edit/update volunteer records.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#6C757D")
        hint_lbl.pack(side="right", pady=5)

        # Bind the Double-Click gesture to execute the update record routine
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # Trigger data fetching from PostgreSQL
        self.load_volunteers_from_db()

    def load_volunteers_from_db(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT volunteer_id, first_name, last_name, phone_number, 
                       has_equipment, counter, latitude, longitude, 
                       recruitment_date, email, is_active 
                FROM public.a_volunteer 
                ORDER BY volunteer_id;
            """
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
            messagebox.showerror("SQL Database Error", f"Failed to retrieve data rows from public.a_volunteer:\n{e}")

    # ========================================================
    # CRUD: DELETE TRANSACTION ROUTINE
    # ========================================================
    def delete_selected_volunteer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please click on a volunteer from the list before requesting a deletion.")
            return

        values = self.tree.item(selected_item, "values")
        v_id = values[0]
        v_name = f"{values[1]} {values[2]}"

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete the profile for:\n👉 {v_name} (ID: #{v_id})?")
        if confirm:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM public.a_volunteer WHERE volunteer_id = %s;", (v_id,))
                self.conn.commit()
                cursor.close()
                
                messagebox.showinfo("Success", "Volunteer record successfully removed from database registry.")
                self.load_volunteers_from_db()
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
        self.open_volunteer_form(edit_mode=True, data=row_values)

   # ========================================================
    # CRUD: FORM INJECTION WINDOW DIALOG MODAL (CREATE / UPDATE)
    # ========================================================
    def open_volunteer_form(self, edit_mode=False, data=None):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Volunteer Profile" if edit_mode else "Register New Volunteer")
        form_window.geometry("520x640")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="📝 Volunteer Profile Attributes Form", font=ctk.CTkFont(size=16, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkScrollableFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # --- FORM FIELDS GENERATION ---
        
        # 1. ID
        ctk.CTkLabel(fields_container, text="Volunteer ID (Primary Key)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 5001")
        entry_id.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
            entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. First Name
        ctk.CTkLabel(fields_container, text="First Name", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_fname = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., Jane")
        entry_fname.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_fname.insert(0, data[1])

        # 3. Last Name
        ctk.CTkLabel(fields_container, text="Last Name", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lname = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., Smith")
        entry_lname.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lname.insert(0, data[2])

        # 4. Phone Number
        ctk.CTkLabel(fields_container, text="Phone Number", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_phone = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 0547654321")
        entry_phone.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_phone.insert(0, data[3])

        # 5. Has Equipment
        ctk.CTkLabel(fields_container, text="Has Equipment (true/false)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_equip = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="true or false")
        entry_equip.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_equip.insert(0, data[4])

        # 6. Counter (Missions) -> 🛠️ MODIFIÉ POUR VERROUILLAGE À 0 PAR DÉFAUT
        ctk.CTkLabel(fields_container, text="Missions Completed Counter", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_counter = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_counter.pack(padx=20, pady=(0, 8))
        if edit_mode: 
            entry_counter.insert(0, data[5]) # On charge la vraie valeur en mode edit
        else:
            entry_counter.insert(0, "0")    # Valeur par défaut forcée à 0 à la création
            entry_counter.configure(state="disabled", fg_color="#F1F3F5") # Verrouillé et grisé

        # 7. Latitude
        ctk.CTkLabel(fields_container, text="Latitude Coordinates", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lat = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 31.7683")
        entry_lat.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lat.insert(0, data[6])

        # 8. Longitude
        ctk.CTkLabel(fields_container, text="Longitude Coordinates", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lon = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 35.2137")
        entry_lon.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lon.insert(0, data[7])

        # 9. Recruitment Date
        ctk.CTkLabel(fields_container, text="Recruitment Date (YYYY-MM-DD)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_date = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 2026-06-14")
        entry_date.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_date.insert(0, data[8])

        # 10. Email Address
        ctk.CTkLabel(fields_container, text="Email Address", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_email = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., volunteer@gmail.com")
        entry_email.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_email.insert(0, data[9])

        # 11. Is Active Status
        ctk.CTkLabel(fields_container, text="Is Active Status (Y/N)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_active = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="Y or N")
        entry_active.pack(padx=20, pady=(0, 15))
        if edit_mode: entry_active.insert(0, data[10])

        # Save Action Process
        def save_form_data():
            v_id = entry_id.get().strip()
            f_name = entry_fname.get().strip()
            l_name = entry_lname.get().strip()
            phone = entry_phone.get().strip()
            equip = entry_equip.get().strip().lower()
            
            # 🛠️ SÉCURITÉ : Même si le champ est désactivé, get() fonctionne. 
            # On récupère proprement la valeur (qui sera forcément "0" à la création).
            count = entry_counter.get().strip() 
            
            lat = entry_lat.get().strip()
            lon = entry_lon.get().strip()
            r_date = entry_date.get().strip()
            email = entry_email.get().strip()
            active = entry_active.get().strip().upper()

            if not v_id or not f_name or not l_name or not phone:
                messagebox.showwarning("Validation Error", "ID, Names, and Phone fields must be fully populated.", parent=form_window)
                return

            has_eq = True if equip == "true" else False
            cnt_val = int(count) if count.isdigit() else 0
            lat_val = float(lat) if lat else None
            lon_val = float(lon) if lon else None
            date_val = r_date if r_date else None
            email_val = email if email else None
            act_val = active if active in ['Y', 'N'] else 'Y'

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    sql = """
                        UPDATE public.a_volunteer 
                        SET first_name = %s, last_name = %s, phone_number = %s, 
                            has_equipment = %s, counter = %s, latitude = %s, 
                            longitude = %s, recruitment_date = %s, email = %s, is_active = %s 
                        WHERE volunteer_id = %s;
                    """
                    cursor.execute(sql, (f_name, l_name, phone, has_eq, cnt_val, lat_val, lon_val, date_val, email_val, act_val, v_id))
                else:
                    sql = """
                        INSERT INTO public.a_volunteer (volunteer_id, first_name, last_name, phone_number, has_equipment, counter, latitude, longitude, recruitment_date, email, is_active) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(v_id), f_name, l_name, phone, has_eq, cnt_val, lat_val, lon_val, date_val, email_val, act_val))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Volunteer database sync completed successfully.", parent=form_window)
                form_window.destroy()
                self.load_volunteers_from_db()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("SQL Transaction Refused", f"Failed to save changes:\n{e}", parent=form_window)

        # Confirm Action Button
        btn_save = ctk.CTkButton(form_window, text="💾 Save Profile Changes", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))