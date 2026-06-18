import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

class TreatmentsScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_treatments_data = []

        # ========================================================
        # 1. HEADER SECTION (Style 1:1 avec Deliveries)
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(
            self.header_frame,
            text="🎬 Treatments Management",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(side="left", anchor="w")

        btn_create_treatment = ctk.CTkButton(
            self.header_frame,
            text="➕ Create New Treatment",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_create_treatment_modal
        )
        btn_create_treatment.pack(side="right", padx=(0, 20))

        # ========================================================
        # 2. SEARCH BAR SECTION (Style 1:1 avec Deliveries)
        # ========================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 8))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search treatment:",
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
        self.entry_search.set("Search by ID, date, status or item type...")
        self.entry_search.bind("<KeyRelease>", self.filter_search_table)

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

        self.lbl_counter = ctk.CTkLabel(self.search_frame, text="0 treatment(s) shown", font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D")
        self.lbl_counter.pack(side="right", padx=5)

        # ========================================================
        # 3. THE BACKGROUND CONTAINER GRID BLOCK
        # ========================================================
        main_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E6E9ED")
        main_box.pack(fill="both", expand=True, pady=(0, 15))

        # --- TREEVIEW STYLING (Format Zoomé Appliqué) ---
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview.Heading", 
            background="#E6E9ED", 
            foreground="#434A54", 
            font=("Segoe UI", 12, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        style.configure(
            "Treeview", 
            background="#FFFFFF", 
            foreground="#212529", 
            rowheight=40, 
            fieldbackground="#FFFFFF", 
            font=("Segoe UI", 12),
            border_width=0
        )
        style.map("Treeview", background=[("selected", "#E6F2FF")], foreground=[("selected", "#1A62E8")])

        self.tree = ttk.Treeview(
            main_box, 
            columns=("id", "date", "start", "completion", "feedback", "photo", "delivery", "volunteer", "request"), 
            show="headings",
            selectmode="browse"
        )
        
        headings = {
            "id": "Treatment ID", "date": "Date", "start": "Start Time", 
            "completion": "Completion Time", "feedback": "Feedback Notes", 
            "photo": "Photo After", "delivery": "Delivery ID", 
            "volunteer": "Volunteer ID", "request": "Request ID"
        }
        
        for col, text in headings.items():
            self.tree.heading(col, text=text, anchor="center")
            width = 120
            if col == "feedback": width = 240
            if col in ["id", "volunteer", "request", "delivery"]: width = 100
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(main_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 5))
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        # ========================================================
        # 4. LOWER HORIZONTAL ACTION TOOLBAR BUTTONS DECK
        # ========================================================
        action_footer_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        action_footer_bar.pack(fill="x")
        action_footer_bar.pack_propagate(False)

        btn_delete = ctk.CTkButton(
            action_footer_bar, 
            text="🗑 Delete Selected Treatment", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color="#DC3545", hover_color="#BD2130",
            height=38, 
            width=210, 
            corner_radius=8, 
            command=self.execute_delete_treatment
        )
        btn_delete.pack(side="left")

        btn_update = ctk.CTkButton(
            action_footer_bar, 
            text="✏️ Update Selected Treatment", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            fg_color="#1A62E8", hover_color="#1452C7" ,
            height=38, 
            width=210, 
            corner_radius=8, 
            command=self.open_update_treatment_modal
        )
        btn_update.pack(side="left", padx=15)

        lbl_tip = ctk.CTkLabel(action_footer_bar, text="💡 Tip: Double-click any row to modify its parameters.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#AAB2BD")
        lbl_tip.pack(side="right", pady=5)

        self.tree.bind("<Double-1>", lambda event: self.open_update_treatment_modal())

        self.load_treatments_database_records()

    # ========================================================
    # LOGIQUE BACKEND ET RECHERCHE CORRIGÉE
    # ========================================================
    def load_treatments_database_records(self):
        if not self.conn: return
        self.all_treatments_data.clear()
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    t.treatment_id, t.date, t.start_time, t.completion_time, 
                    t.feedback_notes, t.photo_after, t.delivery_id, t.volunteer_id, 
                    t.request_id, r.status_id
                FROM public.a_treatment t
                LEFT JOIN public.a_request r ON r.request_id = t.request_id
                ORDER BY t.treatment_id DESC;
            """)
            self.all_treatments_data = cursor.fetchall()
            cursor.close()
            self.filter_search_table()
        except Exception as e:
            print(f"❌ SQL Engine load failure: {e}")

    def filter_search_table(self, event=None):
        search_keyword = self.entry_search._entry.get().strip().lower()
        if search_keyword == "search by id, date, status or item type...":
            search_keyword = ""
            
        selected_status_filter = self.combo_status.get()
        self.tree.delete(*self.tree.get_children())
        
        shown_count = 0
        for row in self.all_treatments_data:
            t_id, date, start, completion, feedback, photo, del_id, vol_id, req_id, req_status_id = row
            
            if selected_status_filter == "Pending" and req_status_id != 1: continue
            if selected_status_filter == "In Progress" and req_status_id != 2: continue
            if selected_status_filter == "Completed" and req_status_id != 3: continue

            match_string = f"{t_id} {feedback} {vol_id} {req_id} {date}".lower()
            if search_keyword in match_string:
                clean_row_values = [str(item) if item is not None else "" for item in row[:-1]]
                row_tag = "evenrow" if shown_count % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=clean_row_values, tags=(row_tag,))
                shown_count += 1
                
        self.lbl_counter.configure(text=f"{shown_count} treatment(s) shown")

    def clear_search_filter(self):
        self.entry_search._entry.delete(0, "end")
        self.combo_status.set("All Statuses")
        self.filter_search_table()

    # ========================================================
    # POPUPS & MODALS (CREATION / MODIFICATION / SUPPRESSION)
    # ========================================================
    def open_create_treatment_modal(self):
        if not self.conn: return
        pending_requests = []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT request_id, incident_description FROM public.a_request WHERE status_id = 1 ORDER BY request_id;")
            pending_requests = cursor.fetchall()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Query Failure", f"Failed to trace requests:\n{e}")
            return

        if not pending_requests:
            messagebox.showinfo("Empty Queue", "No pending requests available.")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Create New Treatment")
        modal.geometry("450x560")
        modal.grab_set()
        modal.resizable(False, False)

        ctk.CTkLabel(modal, text="➕ Add Treatment Record", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0F4C81").pack(pady=12)
        scroll = ctk.CTkScrollableFrame(modal, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        ctk.CTkLabel(scroll, text="Select Pending Request Source:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(8, 2))
        request_strings = [f"{rid} - {desc[:35]}..." for rid, desc in pending_requests]
        combo_req = ctk.CTkComboBox(scroll, values=request_strings, width=360, height=32)
        combo_req.pack(padx=15, pady=(0, 8))
        combo_req.set("Choose target request...")

        ctk.CTkLabel(scroll, text="Target Assigned Volunteer ID:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_vol = ctk.CTkEntry(scroll, placeholder_text="Enter volunteer ID...", width=360, height=32)
        entry_vol.pack(padx=15, pady=(0, 8))

        ctk.CTkLabel(scroll, text="Date Token (YYYY-MM-DD):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_date = ctk.CTkEntry(scroll, width=360, height=32)
        entry_date.pack(padx=15, pady=(0, 8))
        entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ctk.CTkLabel(scroll, text="Start Timestamp (HH:MM:SS):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_start = ctk.CTkEntry(scroll, width=360, height=32)
        entry_start.pack(padx=15, pady=(0, 8))
        entry_start.insert(0, datetime.now().strftime("%H:%M:%S"))

        ctk.CTkLabel(scroll, text="Completion Clock (Optional):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_comp = ctk.CTkEntry(scroll, placeholder_text="HH:MM:SS (Leave blank if active)", width=360, height=32)
        entry_comp.pack(padx=15, pady=(0, 8))

        ctk.CTkLabel(scroll, text="Feedback Progress Notes:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_feed = ctk.CTkEntry(scroll, placeholder_text="Type intervention comments...", width=360, height=32)
        entry_feed.pack(padx=15, pady=(0, 8))

        ctk.CTkLabel(scroll, text="Photo After Reference Path:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_photo = ctk.CTkEntry(scroll, placeholder_text="e.g., image.png", width=360, height=32)
        entry_photo.pack(padx=15, pady=(0, 15))

        def commit_creation():
            req_val = combo_req.get()
            vol_val = entry_vol.get().strip()
            if req_val.startswith("Choose") or not vol_val:
                messagebox.showwarning("Validation Error", "Please check fields values.", parent=modal)
                return
            try:
                target_rid = int(req_val.split(" - ")[0])
                target_vid = int(vol_val)

                cursor = self.conn.cursor()
                cursor.execute("SELECT 1 FROM public.a_volunteer WHERE volunteer_id = %s;", (target_vid,))
                if not cursor.fetchone():
                    messagebox.showerror("Conflict", f"Volunteer ID #{target_vid} does not exist.", parent=modal)
                    cursor.close()
                    return

                cursor.execute("SELECT COALESCE(MAX(treatment_id), 0) + 1 FROM public.a_treatment;")
                next_tid = cursor.fetchone()[0]

                c_time = entry_comp.get().strip() or None
                f_notes = entry_feed.get().strip() or None
                p_after = entry_photo.get().strip() or None

                cursor.execute("""
                    INSERT INTO public.a_treatment (treatment_id, date, start_time, completion_time, feedback_notes, photo_after, delivery_id, volunteer_id, request_id)
                    VALUES (%s, %s, %s, %s, %s, %s, NULL, %s, %s);
                """, (next_tid, entry_date.get().strip(), entry_start.get().strip(), c_time, f_notes, p_after, target_vid, target_rid))

                new_status = 3 if c_time else 2
                cursor.execute("UPDATE public.a_request SET status_id = %s WHERE request_id = %s;", (new_status, target_rid))

                self.conn.commit()
                cursor.close()
                modal.destroy()
                self.load_treatments_database_records()
                messagebox.showinfo("Success", f"Treatment Record #{next_tid} initialized.")
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Error", f"Transaction rejected:\n{e}", parent=modal)

        ctk.CTkButton(modal, text="💾 Save Log Treatment Node Data", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, command=commit_creation).pack(fill="x", padx=20, pady=15)

    def open_update_treatment_modal(self):
        selected_row = self.tree.selection()
        if not selected_row:
            messagebox.showwarning("Selection Missing", "Please select a row first.")
            return

        values = self.tree.item(selected_row, "values")
        t_id, current_date, current_start, current_comp, current_feed, current_photo, current_del, vol_id, req_id = values

        modal = ctk.CTkToplevel(self)
        modal.title(f"Update Treatment: #{t_id}")
        modal.geometry("450x520")
        modal.grab_set()
        modal.resizable(False, False)

        ctk.CTkLabel(modal, text=f"🔧 Mutate Attributes Set for Node: #{t_id}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0F4C81").pack(pady=12)
        scroll = ctk.CTkScrollableFrame(modal, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        ctk.CTkLabel(scroll, text="Date Configuration Layout String Attribute:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(8, 2))
        entry_date = ctk.CTkEntry(scroll, width=360, height=32)
        entry_date.pack(padx=15, pady=(0, 8))
        entry_date.insert(0, current_date)

        ctk.CTkLabel(scroll, text="Start Clock Execution Time Tracking Parameter:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_start = ctk.CTkEntry(scroll, width=360, height=32)
        entry_start.pack(padx=15, pady=(0, 8))
        entry_start.insert(0, current_start)

        ctk.CTkLabel(scroll, text="Completion Operational Clock (HH:MM:SS / Clear if active):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_comp = ctk.CTkEntry(scroll, width=360, height=32)
        entry_comp.pack(padx=15, pady=(0, 8))
        entry_comp.insert(0, current_comp)

        ctk.CTkLabel(scroll, text="Operational Feedback Narrative Context:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_feed = ctk.CTkEntry(scroll, width=360, height=32)
        entry_feed.pack(padx=15, pady=(0, 8))
        entry_feed.insert(0, current_feed)

        ctk.CTkLabel(scroll, text="Resource Address Reference Photo After Link Key:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_photo = ctk.CTkEntry(scroll, width=360, height=32)
        entry_photo.pack(padx=15, pady=(0, 8))
        entry_photo.insert(0, current_photo)

        ctk.CTkLabel(scroll, text="Mutable Relation Reference Primary Key Link ID Delivery Mapping:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=15, pady=(4, 2))
        entry_del = ctk.CTkEntry(scroll, width=360, height=32)
        entry_del.pack(padx=15, pady=(0, 15))
        entry_del.insert(0, current_del)

        def execute_patch():
            try:
                cursor = self.conn.cursor()
                c_time = entry_comp.get().strip() or None
                f_notes = entry_feed.get().strip() or None
                p_after = entry_photo.get().strip() or None
                d_id = int(entry_del.get().strip()) if entry_del.get().strip().isdigit() else None

                cursor.execute("""
                    UPDATE public.a_treatment 
                    SET date = %s, start_time = %s, completion_time = %s, feedback_notes = %s, photo_after = %s, delivery_id = %s
                    WHERE treatment_id = %s;
                """, (entry_date.get().strip(), entry_start.get().strip(), c_time, f_notes, p_after, d_id, int(t_id)))

                new_status = 3 if c_time else 2
                cursor.execute("UPDATE public.a_request SET status_id = %s WHERE request_id = %s;", (new_status, int(req_id)))

                self.conn.commit()
                cursor.close()
                modal.destroy()
                self.load_treatments_database_records()
                messagebox.showinfo("Success Sync Data", f"Attributes definitions mapped successfully for row entry link token #{t_id}.")
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("Transaction Refused", f"Failed to push attributes mutations profiles sets instructions blocks pipelines:\n{e}", parent=modal)

        ctk.CTkButton(modal, text="💾 Update Log Attribute Configurations", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", height=38, command=execute_patch).pack(fill="x", padx=20, pady=15)

    def execute_delete_treatment(self):
        selected_target = self.tree.selection()
        if not selected_target:
            messagebox.showwarning("Unallocated Cell Link", "Please highlight a target table element mapping row to erase from the active grid dashboard view.")
            return

        values = self.tree.item(selected_target, "values")
        t_id, _, _, _, _, _, del_id, _, req_id = values

        confirm = messagebox.askyesno("Destructive Step Authorization", f"Wipe item treatment tracking row entry map token #{t_id}?\nThis shifts back request sequences loops profiles logs safely.")
        if not confirm: return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM public.a_treatment WHERE treatment_id = %s;", (int(t_id),))

            if del_id and str(del_id).isdigit():
                cursor.execute("DELETE FROM public.a_delivery WHERE delivery_id = %s;", (int(del_id),))

            cursor.execute("UPDATE public.a_request SET status_id = 1 WHERE request_id = %s;", (int(req_id),))

            self.conn.commit()
            cursor.close()
            self.load_treatments_database_records()
            messagebox.showinfo("Wiped Complete Node", f"Mission transaction token row index entry tracking entity row parameter map #{t_id} removed cleanly.")
        except Exception as e:
            if self.conn: self.conn.rollback()
            messagebox.showerror("SQL Core Conflict Error Refusal", f"Database engine rejected execution instructions sequences processing pipelines blocks updates:\n{e}")