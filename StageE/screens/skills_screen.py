import customtkinter as ctk
from tkinter import messagebox, ttk

class SkillsScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_skills_data = []

        # ========================================================
        # 1. HEADER SECTION
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(
            self.header_frame,
            text="🎓 Skills & Competencies Registry",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(
            self.header_frame,
            text="➕ Create New Skill",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_skill_form
        )
        btn_add.pack(side="right", padx=(0, 20))

        # ========================================================
        # 2. SEARCH BAR SECTION
        # ========================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 8))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search skill:",
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
        self.entry_search.set("Search by ID, name, description...")
        self.entry_search.bind("<KeyRelease>", self.filter_search_table)
        self.entry_search._entry.bind("<FocusIn>", self.clear_placeholder_on_click)

        self.combo_difficulty_filter = ctk.CTkComboBox(
            self.search_frame,
            values=["All Difficulties", "1", "2", "3", "4", "5"],
            width=140,
            height=34,
            command=self.filter_search_table
        )
        self.combo_difficulty_filter.pack(side="left", padx=(0, 10))
        self.combo_difficulty_filter.set("All Difficulties")

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

        self.lbl_counter = ctk.CTkLabel(self.search_frame, text="0 skill(s) shown", font=ctk.CTkFont(size=12, slant="italic"), text_color="#6C757D")
        self.lbl_counter.pack(side="right", padx=5)

        # Main Data Container Card
        self.container_box = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # --- DATA TABLE STYLE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#FFFFFF", foreground="#212529", rowheight=40, fieldbackground="#FFFFFF", borderwidth=0, font=("Segoe UI", 12))
        style.configure("Treeview.Heading", background="#E6E9ED", foreground="#434A54", font=("Segoe UI", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview", background=[('selected', '#E6F2FF')], foreground=[('selected', '#1A62E8')])

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("skill_id", "skill_name", "description", "difficulty_level", "requires_certificate", "category_name")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("skill_id", text="Skill ID")
        self.tree.heading("skill_name", text="Skill Name")
        self.tree.heading("description", text="Description")
        self.tree.heading("difficulty_level", text="Difficulty Level")
        self.tree.heading("requires_certificate", text="Requires Cert. (Y/N)")
        self.tree.heading("category_name", text="Category Name")

        self.tree.column("skill_id", width=80, anchor="center")
        self.tree.column("skill_name", width=180, anchor="w")
        self.tree.column("description", width=260, anchor="w")
        self.tree.column("difficulty_level", width=110, anchor="center")
        self.tree.column("requires_certificate", width=130, anchor="center")
        self.tree.column("category_name", width=150, anchor="center")

        self.tree.tag_configure('evenrow', background='#FFFFFF')
        self.tree.tag_configure('oddrow', background='#F8F9FA')

        # ========================================================
        # 3. ACTIONS FOOTER BAR (With Update Button added)
        # ========================================================
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent", height=50)
        self.footer_frame.pack(fill="x", padx=20, pady=(5, 15))
        self.footer_frame.pack_propagate(False)

        btn_delete = ctk.CTkButton(self.footer_frame, text="🗑️ Delete Selected Skill", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#DC3545", hover_color="#BD2130", width=190, height=38, corner_radius=8, command=self.delete_selected_skill)
        btn_delete.pack(side="left")

        # 🚀 NEW : Update button handles modification flow on single selection click
        btn_update = ctk.CTkButton(self.footer_frame, text="✏️ Update Selected Skill", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", hover_color="#1452C7", width=190, height=38, corner_radius=8, command=self.trigger_update_button_click)
        btn_update.pack(side="left", padx=15)

        hint_lbl = ctk.CTkLabel(self.footer_frame, text="💡 Tip: Double-click any row to view assigned volunteers.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#AAB2BD")
        hint_lbl.pack(side="right", pady=5)

        # 🚀 MODIFICATION : Double click now triggers volunteers tracking modal
        self.tree.bind("<Double-1>", self.open_linked_volunteers_modal)
        self.load_skills_from_db()

    # ========================================================
    # SQL ENGINE & DATA MANAGEMENT
    # ========================================================
    def load_skills_from_db(self):
        if not self.conn: return
        self.all_skills_data.clear()
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT s.skill_id, s.skill_name, s.description, s.difficulty_level, s.requires_certificate, c.catagory_name
                FROM public.b_skill s
                LEFT JOIN public.b_catagory c ON s.category_id = c.catagory_id
                ORDER BY s.skill_id ASC;
            """
            cursor.execute(query)
            self.all_skills_data = cursor.fetchall()
            cursor.close()

            search_suggestions = []
            for row in self.all_skills_data:
                s_id, name, _, _, _, _ = row
                search_suggestions.append(f"ID #{s_id} | {name}")

            self.entry_search.configure(values=search_suggestions)
            self.filter_search_table()
        except Exception as e:
            print(f"❌ SQL Engine failure fetching skills catalog: {e}")

    def filter_search_table(self, event=None):
        raw_keyword = self.entry_search._entry.get().strip().lower()
        is_exact_id_match = False
        search_keyword = raw_keyword

        if "id #" in raw_keyword:
            search_keyword = raw_keyword.split("id #")[1].split(" ")[0].strip()
            is_exact_id_match = True
        elif raw_keyword == "search by id, name, description...":
            search_keyword = ""

        selected_difficulty_filter = self.combo_difficulty_filter.get()
        self.tree.delete(*self.tree.get_children())
        shown_count = 0

        for row in self.all_skills_data:
            s_id, name, desc, diff, cert, cat_name = row
            
            if selected_difficulty_filter != "All Difficulties" and str(diff) != selected_difficulty_filter:
                continue

            if is_exact_id_match:
                if str(s_id) != search_keyword: 
                    continue
            else:
                match_string = f"{s_id} {str(name).lower()} {str(desc).lower()} {str(cat_name).lower()}"
                if search_keyword not in match_string: 
                    continue

            formatted_row = [str(item) if item is not None else "" for item in row]
            row_tag = "evenrow" if shown_count % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=formatted_row, tags=(row_tag,))
            shown_count += 1

        self.lbl_counter.configure(text=f"{shown_count} skill(s) shown")

    def clear_search_filter(self):
        self.entry_search._entry.delete(0, "end")
        self.combo_difficulty_filter.set("All Difficulties")
        self.filter_search_table()
    
    def clear_placeholder_on_click(self, event):
        """Clears the baseline placeholder text automatically upon gaining focus"""
        current_text = self.entry_search.get().strip()
        if current_text == "Search by ID, name, description...":
            self.entry_search.set("")
            
    # ========================================================
    # 🚀 NEW FUNCTION: DOUBLE-CLICK VOLUNTEERS VISUALIZER MODAL
    # ========================================================
    def open_linked_volunteers_modal(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        
        values = self.tree.item(selected_item, "values")
        skill_id, skill_name = values[0], values[1]
        
        # Pull assignments list from database
        volunteers_list = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT v.volunteer_id, v.first_name, v.last_name, v.phone_number
                FROM public.b_volunteer_skill vs
                JOIN public.a_volunteer v ON vs.volunteer_id = v.volunteer_id
                WHERE vs.skill_id = %s
                ORDER BY v.volunteer_id;
            """
            cursor.execute(query, (int(skill_id),))
            volunteers_list = cursor.fetchall()
            cursor.close()
        except Exception as e:
            messagebox.showerror("Query Failure", f"Failed to retrieve linked volunteers tracking list:\n{e}")
            return

        modal = ctk.CTkToplevel(self)
        modal.title(f"Volunteers with Skill #{skill_id}")
        modal.geometry("550x400")
        modal.grab_set()
        
        ctk.CTkLabel(modal, text=f"👥 Volunteers Assigned to: {skill_name}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#0F4C81").pack(pady=12)
        
        table_frame = ctk.CTkFrame(modal, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        sub_tree = ttk.Treeview(table_frame, columns=("id", "first", "last", "phone"), show="headings")
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=sub_tree.yview)
        sub_tree.configure(yscrollcommand=v_scroll.set)
        
        v_scroll.pack(side="right", fill="y")
        sub_tree.pack(side="left", fill="both", expand=True)
        
        sub_tree.heading("id", text="Volunteer ID")
        sub_tree.heading("first", text="First Name")
        sub_tree.heading("last", text="Last Name")
        sub_tree.heading("phone", text="Phone Number")
        
        sub_tree.column("id", width=95, anchor="center")
        sub_tree.column("first", width=120, anchor="w")
        sub_tree.column("last", width=120, anchor="w")
        sub_tree.column("phone", width=130, anchor="center")
        
        style = ttk.Style()
        sub_tree.tag_configure('evenrow', background='#FFFFFF')
        sub_tree.tag_configure('oddrow', background='#F8F9FA')
        
        for i, row in enumerate(volunteers_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            sub_tree.insert("", "end", values=[str(x) for x in row], tags=(tag,))
            
        ctk.CTkLabel(modal, text=f"Total: {len(volunteers_list)} volunteer(s) found.", font=ctk.CTkFont(size=11, slant="italic"), text_color="#6C757D").pack(pady=(0, 10))

    # ========================================================
    # SINGLE CLICK MODIFICATION DECK ROUTINES
    # ========================================================
    def trigger_update_button_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please click once on a row item from the list to update.")
            return
        row_values = self.tree.item(selected_item, "values")
        self.open_skill_form(edit_mode=True, data=row_values)

    def delete_selected_skill(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a target skill row item from the list.")
            return

        values = self.tree.item(selected_item, "values")
        skill_id = values[0]

        confirm = messagebox.askyesno("Confirm Deletion", f"Permanently wipe Skill #{skill_id}?\nThis will disconnect this skill mapping from all volunteers tables database configurations automatically.")
        if not confirm: return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM public.b_volunteer_skill WHERE skill_id = %s;", (int(skill_id),))
            cursor.execute("DELETE FROM public.b_skill WHERE skill_id = %s;", (int(skill_id),))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Pruning Confirmed", "Skill registry tracking constraint wiped smoothly.")
            self.load_skills_from_db()
        except Exception as e:
            if self.conn: self.conn.rollback()
            messagebox.showerror("SQL Core Exception Fail", f"Database engine refused pruning sequence operations pipeline:\n{e}")

    # ========================================================
    # TRANSACTION FORM MODAL VIEW HANDLERS (INSERT / UPDATE)
    # ========================================================
    def open_skill_form(self, edit_mode=False, data=None):
        categories_map = {}
        next_id = None
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT catagory_id, catagory_name FROM public.b_catagory ORDER BY catagory_name;")
            for cid, cname in cursor.fetchall():
                categories_map[cname] = cid
            
            if not edit_mode:
                cursor.execute("SELECT COALESCE(MAX(skill_id), 0) + 1 FROM public.b_skill;")
                next_id = cursor.fetchone()[0]
                
            cursor.close()
        except Exception as e:
            messagebox.showerror("Handshake Fault", f"Could not sync application runtime registries properties safely:\n{e}")
            return

        form_window = ctk.CTkToplevel(self)
        form_window.title("Update Skill Definition" if edit_mode else "Register New Skill")
        form_window.geometry("480x540")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(form_window, text="🎓 Competency Node Mapping Entry Descriptor", font=ctk.CTkFont(size=15, weight="bold"), text_color="#0F4C81")
        form_title.pack(pady=(15, 10))

        scroll = ctk.CTkScrollableFrame(form_window, fg_color="#FFFFFF", corner_radius=8, border_width=1, border_color="#E9ECEF")
        scroll.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        ctk.CTkLabel(scroll, text="Skill ID (Primary Key Reference Pointer):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(10, 2))
        entry_id = ctk.CTkEntry(scroll, width=360, height=32)
        entry_id.pack(padx=20, pady=(0, 8))
        
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, str(next_id))
            
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        ctk.CTkLabel(scroll, text="Skill Name:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(scroll, width=360, height=32, placeholder_text="e.g., Heavy Truck Driver License")
        entry_name.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_name.insert(0, data[1])

        ctk.CTkLabel(scroll, text="Detailed Description:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_desc = ctk.CTkEntry(scroll, width=360, height=32, placeholder_text="Enter operational capability comments details text logs...")
        entry_desc.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_desc.insert(0, data[2])

        ctk.CTkLabel(scroll, text="Difficulty Grade Evaluation Ranking Level:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_diff = ctk.CTkComboBox(scroll, values=["1", "2", "3", "4", "5"], width=360, height=32)
        entry_diff.pack(padx=20, pady=(0, 8))
        if edit_mode: 
            entry_diff.set(data[3])
        else:
            entry_diff.set("1")

        ctk.CTkLabel(scroll, text="Requires Verified Authorized Certificate (Y / N):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        entry_cert = ctk.CTkComboBox(scroll, values=["N", "Y"], width=360, height=32)
        entry_cert.pack(padx=20, pady=(0, 8))
        if edit_mode: entry_cert.set(data[4])

        ctk.CTkLabel(scroll, text="Category Name:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D").pack(anchor="w", padx=20, pady=(5, 2))
        category_options_list = list(categories_map.keys())
        entry_cat = ctk.CTkComboBox(scroll, values=category_options_list, width=360, height=32)
        entry_cat.pack(padx=20, pady=(0, 15))
        if edit_mode and data[5]: entry_cat.set(data[5])

        def save_form_data():
            s_name = entry_name.get().strip()
            s_desc = entry_desc.get().strip() or None
            s_diff = entry_diff.get().strip()
            s_cert = entry_cert.get().strip()
            selected_cat_name = entry_cat.get()

            if not s_name or not s_diff or selected_cat_name.startswith("Choose"):
                messagebox.showwarning("Validation Error", "All primary fields structural requirements are required.", parent=form_window)
                return

            cat_id = categories_map.get(selected_cat_name)

            try:
                cursor = self.conn.cursor()
                if edit_mode:
                    s_id = data[0]
                    sql = """
                        UPDATE public.b_skill 
                        SET skill_name = %s, description = %s, difficulty_level = %s, requires_certificate = %s, category_id = %s
                        WHERE skill_id = %s;
                    """
                    cursor.execute(sql, (s_name, s_desc, int(s_diff), s_cert, int(cat_id), int(s_id)))
                else:
                    cursor.execute("SELECT COALESCE(MAX(skill_id), 0) + 1 FROM public.b_skill;")
                    final_id = cursor.fetchone()[0]

                    sql = """
                        INSERT INTO public.b_skill (skill_id, skill_name, description, difficulty_level, requires_certificate, category_id) 
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (int(final_id), s_name, s_desc, int(s_diff), s_cert, int(cat_id)))

                self.conn.commit()
                cursor.close()
                messagebox.showinfo("Success Record Saved", "Skill metadata mapping properties context saved smoothly.", parent=form_window)
                form_window.destroy()
                self.load_skills_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("SQL Error Engine Conflict", f"Database transaction execution pipeline failed rejected updates:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(form_window, text="💾 Commit Competency Profile Attributes Sets", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data)
        btn_save.pack(fill="x", padx=25, pady=(0, 15))