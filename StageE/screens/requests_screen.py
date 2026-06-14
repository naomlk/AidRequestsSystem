import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date as datetime_date

class RequestsScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(self.header_frame, text="📋 Requests Management System", font=ctk.CTkFont(size=20, weight="bold"), text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(self.header_frame, text="➕ Create New Request", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8, command=self.open_request_form)
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

        # 🛠️ NOUVEAU CONTENEUR POUR ACCUEILLIR LES BARRES DE DÉFILEMENT
        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        # Data Grid Layout Configuration
        columns = (
            "request_id", "date", "image", "incident_description", 
            "prioriry_level", "contactperson_id", "category_id", 
            "status_id", "latitude", "longitude"
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 🛠️ AJOUT DES BARRES COULISSANTES (SCROLLBARS)
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Placement des barres et du tableau dans le sous-conteneur
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
        self.tree.heading("category_id", text="Category ID")
        self.tree.heading("status_id", text="Status ID")
        self.tree.heading("latitude", text="Latitude")
        self.tree.heading("longitude", text="Longitude")

        # Column Formatting (Largeurs minimales définies pour permettre le glissement horizontal)
        self.tree.column("request_id", width=60, minwidth=50, anchor="center")
        self.tree.column("date", width=110, minwidth=90, anchor="center")
        self.tree.column("image", width=130, minwidth=100, anchor="w")
        self.tree.column("incident_description", width=250, minwidth=180, anchor="w")
        self.tree.column("prioriry_level", width=80, minwidth=60, anchor="center")
        self.tree.column("contactperson_id", width=110, minwidth=80, anchor="center")
        self.tree.column("category_id", width=110, minwidth=80, anchor="center")
        self.tree.column("status_id", width=110, minwidth=80, anchor="center")
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

        # Bindings
        self.tree.bind("<Double-1>", self.on_row_double_click)

        # Initial Load
        self.load_requests_from_db()

    def load_requests_from_db(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT request_id, date, image, incident_description, 
                       prioriry_level, contactperson_id, category_id, 
                       status_id, latitude, longitude 
                FROM public.a_request 
                ORDER BY request_id;
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
            messagebox.showerror("SQL Database Error", f"Failed to retrieve requests:\n{e}")

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
        if not selected_item:
            return
        row_values = self.tree.item(selected_item, "values")
        self.open_request_form(edit_mode=True, data=row_values)

    # ========================================================
    # FORM DIALOG MODAL (CREATE / UPDATE)
    # ========================================================
    def open_request_form(self, edit_mode=False, data=None):
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

        # 1. Request ID
        ctk.CTkLabel(fields_container, text="Request ID (Primary Key)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 8001")
        entry_id.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
            entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. Date
        ctk.CTkLabel(fields_container, text="Incident Date (YYYY-MM-DD)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_date = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_date.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_date.insert(0, data[1])
        else:
            entry_date.insert(0, str(datetime_date.today()))

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

        # 5. Priority Level
        ctk.CTkLabel(fields_container, text="Priority Level (Integer 1-5)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_priority = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 5 (Life Critical)")
        entry_priority.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_priority.insert(0, data[4])

        # 6. Contact Person ID
        ctk.CTkLabel(fields_container, text="Associated Family ID (contactperson_id)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_cp_id = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="Must exist in a_family table")
        entry_cp_id.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_cp_id.insert(0, data[5])

        # 7. Category ID
        ctk.CTkLabel(fields_container, text="Category ID reference", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_cat = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 1")
        entry_cat.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_cat.insert(0, data[6])

        # 8. Status ID 
        ctk.CTkLabel(fields_container, text="Status ID reference", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_status = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 1")
        entry_status.pack(padx=20, pady=(0, 8))
        
        if edit_mode:
            entry_status.insert(0, data[7])
           
        else:
        
            entry_status.insert(0, "1")
            entry_status.configure(state="disabled", fg_color="#F1F3F5")

        # 9. Latitude
        ctk.CTkLabel(fields_container, text="Latitude coordinates (Israel)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lat = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 31.7683")
        entry_lat.pack(padx=20, pady=(0, 8))
        if edit_mode and data[8] and data[8] != 'None': entry_lat.insert(0, data[8])

        # 10. Longitude
        ctk.CTkLabel(fields_container, text="Longitude coordinates (Israel)", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lon = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 35.2137")
        entry_lon.pack(padx=20, pady=(0, 15))
        if edit_mode and data[9] and data[9] != 'None': entry_lon.insert(0, data[9])

        # Process Submission
        def save_form_data():
            r_id = entry_id.get().strip()
            r_date = entry_date.get().strip()
            img = entry_img.get().strip()
            desc = entry_desc.get().strip()
            prio = entry_priority.get().strip()
            cp_id = entry_cp_id.get().strip()
            cat = entry_cat.get().strip()
            stat = entry_status.get().strip()
            lat = entry_lat.get().strip()
            lon = entry_lon.get().strip()

            if not r_id  or not prio or not cp_id or not cat or not stat:
                messagebox.showwarning("Validation Error", "Please fill out all required transactional key properties.", parent=form_window)
                return

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    sql = """
                        UPDATE public.a_request 
                        SET date = %s, image = %s, incident_description = %s, prioriry_level = %s, 
                            contactperson_id = %s, category_id = %s, status_id = %s, latitude = %s, longitude = %s 
                        WHERE request_id = %s;
                    """
                    cursor.execute(sql, (r_date, img if img else None, desc, int(prio), int(cp_id), int(cat), int(stat), float(lat) if lat else None, float(lon) if lon else None, int(r_id)))
                else:
                    sql = """
                        INSERT INTO public.a_request (request_id, date, image, incident_description, prioriry_level, contactperson_id, category_id, status_id, latitude, longitude) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(r_id), r_date, img if img else None, desc, int(prio), int(cp_id), int(cat), int(stat), float(lat) if lat else None, float(lon) if lon else None))
                
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Incident request committed successfully to backend schemas.", parent=form_window)
                form_window.destroy()
                self.load_requests_from_db()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("SQL Transaction Error", f"Database engine refused execution:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Save Request Details", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))