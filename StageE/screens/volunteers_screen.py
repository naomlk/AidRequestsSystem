import customtkinter as ctk
from tkinter import ttk, messagebox

class VolunteersScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_volunteer_rows = []
        self.volunteer_search_options = []
        self.volunteer_option_to_id = {}

        # --- HEADER SECTION (With Add Button) ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(self.header_frame, text="PROJET VOLUNTEERS 👷 Volunteers Tracker", font=ctk.CTkFont(size=20, weight="bold"),
                             text_color="#0F4C81")
        title.pack(side="left", anchor="w")

        # Add Action Button at top right corner
        btn_add = ctk.CTkButton(self.header_frame, text="➕ Add New Volunteer", font=ctk.CTkFont(size=13, weight="bold"),
                                fg_color="#1A62E8", hover_color="#1452C7", height=38, corner_radius=8,
                                command=self.open_volunteer_form)
        btn_add.pack(side="right")

        # Main Data Container (White background card)
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1,
                                          border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=35, fieldbackground="#FFFFFF",
                        borderwidth=0, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#F1F3F5", foreground="#495057", font=("Segoe UI", 11, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#1A62E8')], foreground=[('selected', '#FFFFFF')])

        # Data Grid Layout Configuration (11 columns)
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

        # --- SEARCH BAR ---
        self.search_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 0))

        search_lbl = ctk.CTkLabel(
            self.search_frame,
            text="🔎 Search Volunteer:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057"
        )
        search_lbl.pack(side="left", padx=(0, 10))

        self.search_combo = ctk.CTkComboBox(
            self.search_frame,
            values=[],
            width=340,
            height=34,
            command=self.on_search_combo_selected
        )
        self.search_combo.pack(side="left", padx=(0, 10))
        self.search_combo.set("Search by ID, first name, or last name...")

        # Focus & Entry Event Listeners for Automatic Placeholder Clearing Node
        try:
            self.search_combo._entry.bind("<KeyRelease>", self.on_search_key_release)
            self.search_combo._entry.bind("<Return>", self.select_first_search_result)
            self.search_combo._entry.bind("<FocusIn>", self.clear_placeholder_on_click)
            self.search_combo._entry.bind("<FocusOut>", self.restore_placeholder_on_leave)
        except Exception:
            pass

        btn_clear_search = ctk.CTkButton(
            self.search_frame,
            text="Show All",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6C757D",
            hover_color="#5C636A",
            width=90,
            height=34,
            corner_radius=6,
            command=self.clear_volunteer_search
        )
        btn_clear_search.pack(side="left")

        self.search_result_label = ctk.CTkLabel(
            self.search_frame,
            text="",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        self.search_result_label.pack(side="right", padx=(10, 0))

        self.tree.pack(fill="both", expand=True, padx=20, pady=(12, 10))

        # --- TABLE ACTIONS FOOTER BAR ---
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Delete Action Button
        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Delete Selected Volunteer",
                                   font=ctk.CTkFont(size=12, weight="bold"), fg_color="#DC3545", hover_color="#BD2130",
                                   width=180, height=35, corner_radius=6, command=self.delete_selected_volunteer)
        btn_delete.pack(side="left", padx=(0, 10))

        # Update Action Button
        btn_update_selected = ctk.CTkButton(self.footer_frame, text="✏️ Update Selected Profile",
                                            font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1A62E8",
                                            hover_color="#1452C7", width=180, height=35, corner_radius=6,
                                            command=self.on_update_button_click)
        btn_update_selected.pack(side="left")

        hint_lbl = ctk.CTkLabel(self.footer_frame,
                                text="💡 Tip: Double-click any row to view volunteer skills. Select and click 'Update' to edit.",
                                font=ctk.CTkFont(size=11, slant="italic"), text_color="#6C757D")
        hint_lbl.pack(side="right", pady=5)

        self.tree.bind("<Double-1>", self.on_row_double_click)
        self.load_volunteers_from_db()

    # ========================================================
    # SQL ENGINE & DATA STREAM STREAMING
    # ========================================================
    def load_volunteers_from_db(self):
        """Fetches baseline relational volunteer nodes from the system database catalog"""
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT volunteer_id, first_name, last_name, phone_number, 
                       has_equipment, counter, latitude, longitude, 
                       recruitment_date, email, is_active 
                FROM public.a_volunteer 
                ORDER BY volunteer_id ASC;
            """
            cursor.execute(query)
            self.all_volunteer_rows = cursor.fetchall()
            cursor.close()

            self.display_volunteer_rows(self.all_volunteer_rows)
            self.refresh_search_suggestions("")
        except Exception as e:
            messagebox.showerror("SQL Database Error", f"Failed to retrieve data rows from public.a_volunteer:\n{e}")

    # ========================================================
    # VOLUNTEER SEARCH BAR HELPERS & PLACEHOLDER ROUTINES
    # ========================================================
    def clear_placeholder_on_click(self, event):
        """Clears the baseline placeholder text automatically upon gaining focus"""
        current_text = self.search_combo.get().strip()
        if current_text == "Search by ID, first name, or last name...":
            self.search_combo.set("")

    def restore_placeholder_on_leave(self, event):
        """Restores the baseline placeholder text if the entry field is left empty"""
        current_text = self.search_combo.get().strip()
        if not current_text:
            self.search_combo.set("Search by ID, first name, or last name...")

    def display_volunteer_rows(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=row, tags=(tag,))

        if hasattr(self, "search_result_label") and self.search_result_label.winfo_exists():
            self.search_result_label.configure(text=f"{len(rows)} volunteer(s) shown")

    def filter_volunteer_rows(self, search_text):
        query = str(search_text).strip().lower()
        if not query or query.startswith("search by"):
            return self.all_volunteer_rows

        filtered_rows = []
        for row in self.all_volunteer_rows:
            volunteer_id = str(row[0]).lower()
            first_name = str(row[1] or "").lower()
            last_name = str(row[2] or "").lower()
            full_name = f"{first_name} {last_name}"

            if (query in volunteer_id or query in first_name or query in last_name or query in full_name):
                filtered_rows.append(row)
        return filtered_rows

    def build_volunteer_search_option(self, row):
        return f"{row[0]} - {row[1]} {row[2]}"

    def refresh_search_suggestions(self, search_text):
        matching_rows = self.filter_volunteer_rows(search_text)
        options = [self.build_volunteer_search_option(row) for row in matching_rows[:30]]

        self.volunteer_search_options = options
        self.volunteer_option_to_id = {
            self.build_volunteer_search_option(row): str(row[0]) for row in matching_rows[:30]
        }

        if hasattr(self, "search_combo") and self.search_combo.winfo_exists():
            self.search_combo.configure(values=options)

    def on_search_key_release(self, event=None):
        search_text = self.search_combo.get()
        matching_rows = self.filter_volunteer_rows(search_text)
        self.display_volunteer_rows(matching_rows)
        self.refresh_search_suggestions(search_text)

    def on_search_combo_selected(self, selected_value):
        selected_id = self.volunteer_option_to_id.get(selected_value)
        if not selected_id and " - " in selected_value:
            selected_id = selected_value.split(" - ", 1)[0].strip()

        if not selected_id: return

        matching_rows = [row for row in self.all_volunteer_rows if str(row[0]) == str(selected_id)]
        self.display_volunteer_rows(matching_rows)
        self.select_volunteer_row_by_id(selected_id)

    def select_first_search_result(self, event=None):
        if not self.volunteer_search_options: return
        first_option = self.volunteer_search_options[0]
        self.search_combo.set(first_option)
        self.on_search_combo_selected(first_option)

    def select_volunteer_row_by_id(self, volunteer_id):
        for item in self.tree.get_children():
            row_values = self.tree.item(item, "values")
            if row_values and str(row_values[0]) == str(volunteer_id):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def clear_volunteer_search(self):
        if hasattr(self, "search_combo") and self.search_combo.winfo_exists():
            self.search_combo.set("Search by ID, first name, or last name...")
        self.display_volunteer_rows(self.all_volunteer_rows)
        self.refresh_search_suggestions("")

    def on_update_button_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a volunteer from the list before updating.")
            return
        row_values = self.tree.item(selected_item, "values")
        self.open_volunteer_form(edit_mode=True, data=row_values)

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        row_values = self.tree.item(selected_item, "values")
        self.open_volunteer_skills_summary(row_values[0], f"{row_values[1]} {row_values[2]}")

    def open_volunteer_skills_summary(self, volunteer_id, volunteer_name):
        if not self.conn: return
        v_id_clean = int(volunteer_id) if str(volunteer_id).isdigit() else volunteer_id

        profile_win = ctk.CTkToplevel(self)
        profile_win.title(f"Skills Summary - {volunteer_name}")
        profile_win.geometry("680x600")
        profile_win.configure(fg_color="#F8F9FA")
        profile_win.grab_set()
        profile_win.resizable(True, True)

        lbl_header = ctk.CTkLabel(profile_win, text=f"🛠️ Registered Skills For: {volunteer_name}",
                                  font=ctk.CTkFont(size=15, weight="bold"), text_color="#0F4C81")
        lbl_header.pack(pady=12)

        main_box = ctk.CTkScrollableFrame(profile_win, fg_color="#FFFFFF", corner_radius=10, border_width=1,
                                          border_color="#E9ECEF")
        main_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        def load_skills_list():
            for widget in main_box.winfo_children():
                widget.destroy()

            skills_list = []
            try:
                cursor = self.conn.cursor()
                skills_query = """
                    SELECT s.skill_id, s.skill_name, s.description, s.difficulty_level, s.requires_certificate, c.catagory_name
                    FROM public.b_skill s
                    JOIN public.b_volunteer_skill vs ON s.skill_id = vs.skill_id
                    LEFT JOIN public.b_catagory c ON s.category_id = c.catagory_id
                    WHERE vs.volunteer_id = %s;
                """
                cursor.execute(skills_query, (v_id_clean,))
                skills_list = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(f"❌ SQL Error fetching skills for ID {volunteer_id}: {e}")

            if skills_list:
                for skill in skills_list:
                    s_id, s_name, s_desc, s_diff, s_cert, c_name = skill
                    is_cert_required = str(s_cert).strip().upper() in ["Y", "TRUE", "1"]
                    cert_badge = " [📜 Certificate Required]" if is_cert_required else ""
                    cat_display = f" | Category: {c_name}" if c_name else " | 📂 General"

                    skill_frame = ctk.CTkFrame(main_box, fg_color="#F1F3F5", corner_radius=6)
                    skill_frame.pack(fill="x", expand=True, pady=5, padx=10)

                    txt_title = f"• {s_name} (Difficulty: {s_diff}/5){cat_display}{cert_badge}"
                    lbl_title = ctk.CTkLabel(skill_frame, text=txt_title, font=ctk.CTkFont(size=12, weight="bold"),
                                             text_color="#212529", justify="left")
                    lbl_title.pack(anchor="w", padx=10, pady=(5, 2))

                    lbl_desc = ctk.CTkLabel(skill_frame, text=f"Description: {s_desc}",
                                            font=ctk.CTkFont(size=11, slant="italic"), text_color="#495057",
                                            justify="left", wraplength=580)
                    lbl_desc.pack(anchor="w", padx=15, pady=(0, 5))

                    for w in [skill_frame, lbl_title, lbl_desc]:
                        w.bind("<Button-1>", lambda event, sid=s_id, sn=s_name, sd=s_desc, sc=s_cert: select_skill_row(sid, sn, sd, sc))
            else:
                lbl_none = ctk.CTkLabel(main_box, text="No special technical skills registered for this volunteer.",
                                        font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D")
                lbl_none.pack(anchor="center", pady=50)

        selected_row_data = {"id": None, "name": None, "desc": None, "cert": None}

        def select_skill_row(skill_id, skill_name, description, certificate):
            selected_row_data["id"] = skill_id
            selected_row_data["name"] = skill_name
            selected_row_data["desc"] = description
            selected_row_data["cert"] = "Y" if str(certificate).strip().upper() in ["Y", "TRUE", "1"] else "N"
            lbl_selected_status.configure(text=f"🎯 Selected: {skill_name} (ID: #{skill_id})", text_color="#1A62E8")

        def add_new_skill():
            selected_string = combo_available_skills.get()
            if not selected_string or selected_string.startswith("Choose"):
                messagebox.showwarning("Selection Missing", "Please pick an available skill record asset line input.")
                return
            try:
                target_sid = int(selected_string.split(" - ")[0])
                chosen_cert = combo_add_cert.get()

                cursor = self.conn.cursor()
                cursor.execute("UPDATE public.b_skill SET requires_certificate = %s WHERE skill_id = %s;", (chosen_cert, target_sid))
                cursor.execute("INSERT INTO public.b_volunteer_skill (volunteer_id, skill_id) VALUES (%s, %s);", (v_id_clean, target_sid))
                self.conn.commit()
                cursor.close()
                load_skills_list()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("Database Error", f"This volunteer already possesses this skill asset entry row assignment or database failed:\n{e}")

        def open_update_mini_window():
            if not selected_row_data["id"]:
                messagebox.showwarning("Target Selection Missing", "Please click on a skill row layout element above first.")
                return

            edit_win = ctk.CTkToplevel(profile_win)
            edit_win.title(f"Update - {selected_row_data['name']}")
            edit_win.geometry("440x280")
            edit_win.configure(fg_color="#F8F9FA")
            edit_win.grab_set()
            edit_win.resizable(False, False)

            ctk.CTkLabel(edit_win, text=f"🔧 Modify Attributes: {selected_row_data['name']}",
                         font=ctk.CTkFont(size=13, weight="bold"), text_color="#0F4C81").pack(pady=12)

            ctk.CTkLabel(edit_win, text="Skill Description Context Overwrite:", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=25, pady=(5, 2))
            entry_mutate_desc = ctk.CTkEntry(edit_win, width=380, height=30)
            entry_mutate_desc.pack(padx=25, pady=(0, 10))
            entry_mutate_desc.insert(0, selected_row_data["desc"] if selected_row_data["desc"] else "")

            ctk.CTkLabel(edit_win, text="Requires Validated Certificate (Y/N Status):", font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=25, pady=(5, 2))
            combo_mutate_cert = ctk.CTkComboBox(edit_win, values=["Y", "N"], width=80, height=30)
            combo_mutate_cert.pack(anchor="w", padx=25, pady=(0, 20))
            combo_mutate_cert.set(selected_row_data["cert"])

            def execute_update():
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        UPDATE public.b_skill 
                        SET description = %s, requires_certificate = %s 
                        WHERE skill_id = %s;
                    """, (entry_mutate_desc.get().strip(), combo_mutate_cert.get(), selected_row_data["id"]))
                    self.conn.commit()
                    cursor.close()

                    selected_row_data["desc"] = entry_mutate_desc.get().strip()
                    selected_row_data["cert"] = combo_mutate_cert.get()
                    lbl_selected_status.configure(text=f"🎯 Selected: {selected_row_data['name']} (ID: #{selected_row_data['id']})", text_color="#1A62E8")

                    edit_win.destroy()
                    load_skills_list()
                except Exception as e:
                    if self.conn: self.conn.rollback()
                    messagebox.showerror("SQL Error", f"Failed to run attribute changes sync:\n{e}", parent=edit_win)

            ctk.CTkButton(edit_win, text="💾 Save Operational Configurations", font=ctk.CTkFont(size=12, weight="bold"),
                          fg_color="#198754", hover_color="#146C43", height=35, command=execute_update).pack(fill="x", padx=25)

        def delete_selected_skill():
            if not selected_row_data["id"]:
                messagebox.showwarning("Target Selection Missing", "Please click on a skill row layout element above first.")
                return
            if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove '{selected_row_data['name']}' from {volunteer_name}'s profile?"):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM public.b_volunteer_skill WHERE volunteer_id = %s AND skill_id = %s;", (v_id_clean, selected_row_data["id"]))
                    self.conn.commit()
                    cursor.close()

                    lbl_selected_status.configure(text="💡 Click on a skill above to initialize update or delete actions.", text_color="#6C757D")
                    selected_row_data["id"] = None
                    load_skills_list()
                except Exception as e:
                    if self.conn: self.conn.rollback()
                    messagebox.showerror("SQL Error", f"Failed to delete linked relation:\n{e}")

        footer_crud_panel = ctk.CTkFrame(profile_win, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E9ECEF")
        footer_crud_panel.pack(fill="x", padx=20, pady=(0, 15), ipady=10)

        add_title = ctk.CTkLabel(footer_crud_panel, text="➕ Assign New Registered Skill to Profile:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#495057")
        add_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=15, pady=(8, 4))

        all_skills_options = []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT skill_id, skill_name FROM public.b_skill ORDER BY skill_name;")
            all_skills_options = [f"{sid} - {sname}" for sid, sname in cursor.fetchall()]
            cursor.close()
        except:
            pass

        combo_available_skills = ctk.CTkComboBox(footer_crud_panel, values=all_skills_options, width=240, height=30)
        combo_available_skills.grid(row=1, column=0, padx=(15, 5), sticky="w")
        combo_available_skills.set("Choose skill context register row...")

        combo_add_cert = ctk.CTkComboBox(footer_crud_panel, values=["Y", "N"], width=70, height=30)
        combo_add_cert.grid(row=1, column=1, padx=5, sticky="w")
        combo_add_cert.set("N")

        btn_action_add = ctk.CTkButton(footer_crud_panel, text="Assign Skill", font=ctk.CTkFont(size=12, weight="bold"),
                                       fg_color="#1A62E8", hover_color="#1452C7", height=30, width=100, command=add_new_skill)
        btn_action_add.grid(row=1, column=2, padx=(5, 15), sticky="w")

        div_bar = ctk.CTkFrame(footer_crud_panel, fg_color="#E9ECEF", height=1)
        div_bar.grid(row=2, column=0, columnspan=4, sticky="ew", padx=15, pady=12)

        lbl_selected_status = ctk.CTkLabel(footer_crud_panel, text="💡 Click on a skill above to initialize update or delete actions.",
                                           font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D")
        lbl_selected_status.grid(row=3, column=0, columnspan=2, sticky="w", padx=15, pady=(0, 6))

        btn_group_box = ctk.CTkFrame(footer_crud_panel, fg_color="transparent")
        btn_group_box.grid(row=3, column=2, sticky="e", padx=(0, 15))

        ctk.CTkButton(btn_group_box, text="Update Selected", font=ctk.CTkFont(size=11, weight="bold"), fg_color="#198754", hover_color="#146C43", width=110, height=28, command=open_update_mini_window).pack(side="left", padx=2)
        ctk.CTkButton(btn_group_box, text="Delete Selected", font=ctk.CTkFont(size=11, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=110, height=28, command=delete_selected_skill).pack(side="left", padx=2)

        load_skills_list()

    def delete_selected_volunteer(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a volunteer from the list before deleting.")
            return

        values = self.tree.item(selected_item, "values")
        v_id = values[0]
        v_name = f"{values[1]} {values[2]}"

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete the profile for:\n👉 {v_name} (ID: #{v_id})?")
        if confirm:
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM public.b_volunteer_skill WHERE volunteer_id = %s;", (v_id,))
                cursor.execute("DELETE FROM public.a_volunteer WHERE volunteer_id = %s;", (v_id,))
                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success", "Volunteer record successfully removed from database registry.")
                self.load_volunteers_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Transaction Failed", f"Database engine refused delete execution:\n{e}")

    # ========================================================
    # CRUD: FORM INJECTION WINDOW DIALOG MODAL (CREATE / UPDATE)
    # ========================================================
    def open_volunteer_form(self, edit_mode=False, data=None):
        next_id = None
        if not edit_mode:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT COALESCE(MAX(volunteer_id), 0) + 1 FROM public.a_volunteer;")
                next_id = cursor.fetchone()[0]
                cursor.close()
            except Exception as e:
                messagebox.showerror("Sequence Tracker Fault", f"Could not sync automatic primary key pointer node safely:\n{e}")
                return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Volunteer Profile" if edit_mode else "Register New Volunteer")
        form_window.geometry("520x640")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="📝 Volunteer Profile Attributes Form",
                                  font=ctk.CTkFont(size=16, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkScrollableFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1,
                                                 border_color="#E9ECEF")
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # 1. Volunteer ID (Automated Sequential Integer Assignment)
        ctk.CTkLabel(fields_container, text="Volunteer ID (Primary Key)", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_id.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, str(next_id))
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # 2. First Name
        ctk.CTkLabel(fields_container, text="First Name", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_fname = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., Jane")
        entry_fname.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_fname.insert(0, data[1])

        # 3. Last Name
        ctk.CTkLabel(fields_container, text="Last Name", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lname = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., Smith")
        entry_lname.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lname.insert(0, data[2])

        # 4. Phone Number
        ctk.CTkLabel(fields_container, text="Phone Number", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_phone = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 0547654321")
        entry_phone.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_phone.insert(0, data[3])

        # 5. Has Equipment
        ctk.CTkLabel(fields_container, text="Has Equipment Status:", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        combo_equip = ctk.CTkComboBox(fields_container, values=["true", "false"], width=400, height=32)
        combo_equip.pack(padx=20, pady=(0, 8))
        if edit_mode:
            clean_equip = "true" if str(data[4]).strip().lower() in ["true", "y", "yes", "1"] else "false"
            combo_equip.set(clean_equip)
        else:
            combo_equip.set("false")

        # 6. Counter (Missions)
        ctk.CTkLabel(fields_container, text="Missions Completed Counter", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_counter = ctk.CTkEntry(fields_container, width=400, height=32)
        entry_counter.pack(padx=20, pady=(0, 8))
        if edit_mode:
            entry_counter.insert(0, data[5])
        else:
            entry_counter.insert(0, "0")
            entry_counter.configure(state="disabled", fg_color="#F1F3F5")

        # 7. Latitude
        ctk.CTkLabel(fields_container, text="Latitude Coordinates", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lat = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 31.7683")
        entry_lat.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lat.insert(0, data[6])

        # 8. Longitude
        ctk.CTkLabel(fields_container, text="Longitude Coordinates", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_lon = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 35.2137")
        entry_lon.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_lon.insert(0, data[7])

        # 9. Recruitment Date
        ctk.CTkLabel(fields_container, text="Recruitment Date (YYYY-MM-DD)", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_date = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., 2026-06-14")
        entry_date.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_date.insert(0, data[8])

        # 10. Email Address
        ctk.CTkLabel(fields_container, text="Email Address", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_email = ctk.CTkEntry(fields_container, width=400, height=32, placeholder_text="e.g., volunteer@gmail.com")
        entry_email.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_email.insert(0, data[9])

        # 11. Is Active Status
        ctk.CTkLabel(fields_container, text="Is Active Operational Status:", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        combo_active = ctk.CTkComboBox(fields_container, values=["Y", "N"], width=400, height=32)
        combo_active.pack(padx=20, pady=(0, 15))
        if edit_mode:
            clean_active = "Y" if str(data[10]).strip().upper() in ["Y", "TRUE", "1"] else "N"
            combo_active.set(clean_active)
        else:
            combo_active.set("Y")

        def save_form_data():
            try:
                f_name = entry_fname.get().strip()
                l_name = entry_lname.get().strip()
                phone = entry_phone.get().strip()
                equip = combo_equip.get().strip().lower()
                active = combo_active.get().strip().upper()
                count = entry_counter.get().strip()
                lat = entry_lat.get().strip()
                lon = entry_lon.get().strip()
                r_date = entry_date.get().strip()
                email = entry_email.get().strip()

                if not f_name or not l_name or not phone:
                    messagebox.showwarning("Validation Error", "Names and Phone fields must be fully populated.", parent=form_window)
                    return

                has_eq = True if equip == "true" else False
                cnt_val = int(count) if count.isdigit() else 0

                try:
                    lat_val = float(lat.replace(',', '.')) if lat else None
                    lon_val = float(lon.replace(',', '.')) if lon else None
                except ValueError:
                    messagebox.showerror("Format Error", "Latitude and Longitude must be valid decimal numbers.", parent=form_window)
                    return

                date_val = r_date if r_date else None
                email_val = email if email else None
                act_val = active if active in ['Y', 'N'] else 'Y'

                cursor = self.conn.cursor()
                if edit_mode:
                    v_id = data[0]
                    sql = """
                        UPDATE public.a_volunteer 
                        SET first_name = %s, last_name = %s, phone_number = %s, 
                            has_equipment = %s, counter = %s, latitude = %s, 
                            longitude = %s, recruitment_date = %s, email = %s, is_active = %s 
                        WHERE volunteer_id = %s;
                    """
                    cursor.execute(sql, (f_name, l_name, phone, has_eq, cnt_val, lat_val, lon_val, date_val, email_val, act_val, int(v_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(volunteer_id), 0) + 1 FROM public.a_volunteer;")
                    final_generated_id = cursor.fetchone()[0]

                    sql = """
                        INSERT INTO public.a_volunteer (volunteer_id, first_name, last_name, phone_number, has_equipment, counter, latitude, longitude, recruitment_date, email, is_active) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(final_generated_id), f_name, l_name, phone, has_eq, cnt_val, lat_val, lon_val, date_val, email_val, act_val))

                self.conn.commit()
                cursor.close()

                messagebox.showinfo("Success", "Volunteer profile successfully updated.", parent=form_window)
                form_window.destroy()
                self.load_volunteers_from_db()

            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("Database Error", f"The SQL engine refused this transaction:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Save Profile Changes", font=ctk.CTkFont(size=13, weight="bold"),
                                 fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))