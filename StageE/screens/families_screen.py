import customtkinter as ctk
from tkinter import ttk, messagebox


class FamiliesScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_families = []
        self.filtered_families = []


        # ========================================================
        # HEADER
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            self.header_frame,
            text="👥 Families Management System",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81",
        )
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(
            self.header_frame,
            text="➕ Add New Family",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_family_form,
        )
        btn_add.pack(side="right")

        # ========================================================
        # MAIN CONTAINER
        # ========================================================
        self.container_box = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF",
        )
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # ========================================================
        # SEARCH BAR
        # ========================================================
        self.search_frame = ctk.CTkFrame(self.container_box, fg_color="#F8F9FA", corner_radius=10)
        self.search_frame.pack(fill="x", padx=20, pady=(20, 0))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔎 Search family",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057",
        )
        search_label.pack(side="left", padx=(12, 8), pady=10)

        self.search_by_combo = ctk.CTkComboBox(
            self.search_frame,
            values=["All", "ID", "Name", "Phone"],
            width=120,
            height=32,
            state="readonly",
            command=lambda _value: self.apply_search_filter(),
        )
        self.search_by_combo.set("All")
        self.search_by_combo.pack(side="left", padx=(0, 8), pady=10)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=280,
            height=32,
            placeholder_text="Type ID, name or phone number...",
        )
        self.search_entry.pack(side="left", padx=(0, 8), pady=10)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.apply_search_filter())
        self.search_entry.bind("<Return>", self.highlight_first_search_result)

        self.search_count_label = ctk.CTkLabel(
            self.search_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#6C757D",
        )
        self.search_count_label.pack(side="left", padx=(4, 8), pady=10)

        btn_clear_search = ctk.CTkButton(
            self.search_frame,
            text="Show All",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#6C757D",
            hover_color="#5C636A",
            width=90,
            height=32,
            corner_radius=6,
            command=self.clear_search,
        )
        btn_clear_search.pack(side="right", padx=(8, 12), pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#212529",
            rowheight=35,
            fieldbackground="#FFFFFF",
            borderwidth=0,
            font=("Segoe UI", 11),
        )
        style.configure(
            "Treeview.Heading",
            background="#F1F3F5",
            foreground="#495057",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", "#1A62E8")],
            foreground=[("selected", "#FFFFFF")],
        )

        columns = (
            "contactperson_id",
            "contactperson_name",
            "phone_number",
            "number_of_members",
            "special_features",
        )
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

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        self.tree.pack(fill="both", expand=True, padx=20, pady=(12, 10))

        # ========================================================
        # FOOTER ACTIONS
        # ========================================================
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        btn_delete = ctk.CTkButton(
            self.footer_frame,
            text="🗑️ Delete Selected Family",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=180,
            height=35,
            corner_radius=6,
            command=self.delete_selected_family,
        )
        btn_delete.pack(side="left")

        hint_lbl = ctk.CTkLabel(
            self.footer_frame,
            text="💡 Tip: Double-click or right-click a row to edit/update the family profile.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D",
        )
        hint_lbl.pack(side="right", pady=5)

        self.tree.bind("<Double-1>", self.on_row_double_click)
        self.tree.bind("<Button-3>", self.on_row_right_click)
        self.load_families_from_db()

    # ========================================================
    # HELPERS
    # ========================================================
    def show_sql_error(self, title, error, parent=None):
        if self.conn:
            self.conn.rollback()
        messagebox.showerror(title, f"Database operation failed:\n{error}", parent=parent)

    def family_id_exists(self, contactperson_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT 1 FROM public.a_family WHERE contactperson_id = %s LIMIT 1;",
            (contactperson_id,),
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def phone_exists(self, phone_number, exclude_contactperson_id=None):
        cursor = self.conn.cursor()
        if exclude_contactperson_id is None:
            cursor.execute(
                "SELECT 1 FROM public.a_family WHERE phone_number = %s LIMIT 1;",
                (phone_number,),
            )
        else:
            cursor.execute(
                """
                SELECT 1
                FROM public.a_family
                WHERE phone_number = %s
                  AND contactperson_id <> %s
                LIMIT 1;
                """,
                (phone_number, exclude_contactperson_id),
            )
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def refresh_tree(self, rows=None):
        rows = self.filtered_families if rows is None else rows

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

        total = len(self.all_families)
        shown = len(rows)
        if total == 0:
            self.search_count_label.configure(text="No families")
        elif shown == total:
            self.search_count_label.configure(text=f"{total} family/families")
        else:
            self.search_count_label.configure(text=f"{shown} / {total} shown")

    def apply_search_filter(self):
        query = self.search_entry.get().strip().lower()
        search_by = self.search_by_combo.get()

        if not query:
            self.filtered_families = list(self.all_families)
            self.refresh_tree(self.filtered_families)
            return

        filtered = []
        for row in self.all_families:
            contactperson_id = str(row[0]).lower()
            contactperson_name = str(row[1] or "").lower()
            phone_number = str(row[2] or "").lower()

            if search_by == "ID" and query in contactperson_id:
                filtered.append(row)
            elif search_by == "Name" and query in contactperson_name:
                filtered.append(row)
            elif search_by == "Phone" and query in phone_number:
                filtered.append(row)
            elif search_by == "All" and (
                query in contactperson_id
                or query in contactperson_name
                or query in phone_number
            ):
                filtered.append(row)

        self.filtered_families = filtered
        self.refresh_tree(self.filtered_families)

    def clear_search(self):
        self.search_by_combo.set("All")
        self.search_entry.delete(0, "end")
        self.filtered_families = list(self.all_families)
        self.refresh_tree(self.filtered_families)

    def highlight_first_search_result(self, event=None):
        children = self.tree.get_children()
        if not children:
            return

        first_item = children[0]
        self.tree.selection_set(first_item)
        self.tree.focus(first_item)
        self.tree.see(first_item)

    def get_selected_row_values(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return None
        return self.tree.item(selected_items[0], "values")

    # ========================================================
    # READ
    # ========================================================
    def load_families_from_db(self):
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection is available.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT contactperson_id,
                       contactperson_name,
                       phone_number,
                       number_of_members,
                       special_features
                FROM public.a_family
                ORDER BY contactperson_id;
                """
            )
            rows = cursor.fetchall()
            cursor.close()

            self.all_families = rows
            self.apply_search_filter()

        except Exception as e:
            self.show_sql_error("SQL Database Error", e)

    # ========================================================
    # DELETE
    # ========================================================
    def delete_selected_family(self):
        values = self.get_selected_row_values()
        if values is None:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a family before deleting.",
            )
            return
        family_id = values[0]
        family_name = values[1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this family?\n\n{family_name} (ID: {family_id})",
        )
        if not confirm:
            return

        try:
            cursor = self.conn.cursor()

            # Do not delete a family/contact person that is still linked to requests.
            cursor.execute(
                "SELECT COUNT(*) FROM public.a_request WHERE contactperson_id = %s;",
                (family_id,),
            )
            linked_requests = cursor.fetchone()[0]
            if linked_requests > 0:
                cursor.close()
                messagebox.showwarning(
                    "Cannot Delete",
                    f"This family is linked to {linked_requests} request(s), so it cannot be deleted.",
                )
                return

            cursor.execute(
                "DELETE FROM public.a_family WHERE contactperson_id = %s;",
                (family_id,),
            )
            self.conn.commit()
            cursor.close()

            messagebox.showinfo("Success", "Family deleted successfully.")
            self.load_families_from_db()

        except Exception as e:
            self.show_sql_error("SQL Transaction Failed", e)

    # ========================================================
    # ROW EDIT HANDLERS
    # ========================================================
    def open_selected_family_for_edit(self):
        row_values = self.get_selected_row_values()
        if row_values is None:
            return
        self.open_family_form(edit_mode=True, data=row_values)

    def on_row_double_click(self, event):
        self.open_selected_family_for_edit()

    def on_row_right_click(self, event):
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return

        self.tree.selection_set(row_id)
        self.tree.focus(row_id)
        self.open_selected_family_for_edit()

    # ========================================================
    # CREATE / UPDATE FORM
    # ========================================================
    def open_family_form(self, edit_mode=False, data=None):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Family" if edit_mode else "Add New Family")
        form_window.geometry("470x610")
        form_window.configure(fg_color="#F8F9FA")
        form_window.resizable(False, False)
        form_window.grab_set()
        form_window.focus_force()

        form_title = ctk.CTkLabel(
            form_window,
            text="📝 Family Profile Form",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#0F4C81",
        )
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkFrame(
            form_window,
            fg_color="#FFFFFF",
            corner_radius=8,
            border_width=1,
            border_color="#E9ECEF",
        )
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        # Error label used for ID/phone duplicates and validation errors.
        error_label = ctk.CTkLabel(
            fields_container,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#DC3545",
            wraplength=380,
            justify="left",
        )
        error_label.pack(anchor="w", padx=20, pady=(10, 0))

        def set_error(message):
            error_label.configure(text=message)

        def clear_error(*_):
            error_label.configure(text="")

        # ---------------- ID ----------------
        ctk.CTkLabel(
            fields_container,
            text="Contact Person ID (manual primary key)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6C757D",
        ).pack(anchor="w", padx=20, pady=(8, 2))
        entry_id = ctk.CTkEntry(
            fields_container,
            width=380,
            height=32,
            placeholder_text="Example: 209727366",
        )
        entry_id.pack(padx=20, pady=(0, 6))
        entry_id.bind("<KeyRelease>", clear_error)

        if edit_mode:
            entry_id.insert(0, data[0])
            entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # ---------------- Name ----------------
        ctk.CTkLabel(
            fields_container,
            text="Contact Person Full Name",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6C757D",
        ).pack(anchor="w", padx=20, pady=(5, 2))
        entry_name = ctk.CTkEntry(
            fields_container,
            width=380,
            height=32,
            placeholder_text="Example: John Doe",
        )
        entry_name.pack(padx=20, pady=(0, 6))
        entry_name.bind("<KeyRelease>", clear_error)
        if edit_mode:
            entry_name.insert(0, data[1])

        # ---------------- Phone ----------------
        ctk.CTkLabel(
            fields_container,
            text="Phone Number (must be unique)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6C757D",
        ).pack(anchor="w", padx=20, pady=(5, 2))
        entry_phone = ctk.CTkEntry(
            fields_container,
            width=380,
            height=32,
            placeholder_text="Example: 0501234567",
        )
        entry_phone.pack(padx=20, pady=(0, 6))
        entry_phone.bind("<KeyRelease>", clear_error)
        if edit_mode:
            entry_phone.insert(0, data[2])

        # ---------------- Members ----------------
        ctk.CTkLabel(
            fields_container,
            text="Number of Members",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6C757D",
        ).pack(anchor="w", padx=20, pady=(5, 2))
        entry_members = ctk.CTkEntry(
            fields_container,
            width=380,
            height=32,
            placeholder_text="Example: 4",
        )
        entry_members.pack(padx=20, pady=(0, 6))
        entry_members.bind("<KeyRelease>", clear_error)
        if edit_mode:
            entry_members.insert(0, data[3])

        # ---------------- Features ----------------
        ctk.CTkLabel(
            fields_container,
            text="Special Features / Assistance Notes",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#6C757D",
        ).pack(anchor="w", padx=20, pady=(5, 2))
        entry_features = ctk.CTkEntry(
            fields_container,
            width=380,
            height=32,
            placeholder_text="Example: Wheelchair access",
        )
        entry_features.pack(padx=20, pady=(0, 15))
        entry_features.bind("<KeyRelease>", clear_error)
        if edit_mode and data[4] is not None:
            entry_features.insert(0, data[4])

        def validate_form():
            cp_id_raw = entry_id.get().strip()
            cp_name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            members_raw = entry_members.get().strip()
            features = entry_features.get().strip()

            if not cp_id_raw:
                set_error("Family ID is required.")
                return None
            if not cp_name:
                set_error("Contact person name is required.")
                return None
            if not phone:
                set_error("Phone number is required.")
                return None
            if not members_raw:
                set_error("Number of members is required.")
                return None

            try:
                cp_id = int(cp_id_raw)
                if cp_id <= 0:
                    raise ValueError
            except ValueError:
                set_error("Family ID must be a positive whole number.")
                return None

            try:
                members = int(members_raw)
                if members <= 0:
                    raise ValueError
            except ValueError:
                set_error("Number of members must be a positive whole number.")
                return None

            return cp_id, cp_name, phone, members, features

        def save_form_data():
            validated = validate_form()
            if validated is None:
                return

            cp_id, cp_name, phone, members, features = validated

            try:
                if not edit_mode:
                    if self.family_id_exists(cp_id):
                        set_error("This family ID already exists.")
                        return
                    if self.phone_exists(phone):
                        set_error("This phone number already exists.")
                        return
                else:
                    original_id = int(data[0])
                    if self.phone_exists(phone, exclude_contactperson_id=original_id):
                        set_error("This phone number already exists.")
                        return

                cursor = self.conn.cursor()
                if edit_mode:
                    cursor.execute(
                        """
                        UPDATE public.a_family
                        SET contactperson_name = %s,
                            phone_number = %s,
                            number_of_members = %s,
                            special_features = %s
                        WHERE contactperson_id = %s;
                        """,
                        (cp_name, phone, members, features, cp_id),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO public.a_family (
                            contactperson_id,
                            contactperson_name,
                            phone_number,
                            number_of_members,
                            special_features
                        )
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (cp_id, cp_name, phone, members, features),
                    )

                self.conn.commit()
                cursor.close()

                messagebox.showinfo(
                    "Success",
                    "Family saved successfully.",
                    parent=form_window,
                )
                form_window.destroy()
                self.load_families_from_db()

            except Exception as e:
                self.show_sql_error("SQL Engine Transaction Refused", e, parent=form_window)

        btn_save = ctk.CTkButton(
            form_window,
            text="💾 Save Family" if not edit_mode else "💾 Update Family",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#198754",
            hover_color="#146C43",
            height=38,
            corner_radius=6,
            command=save_form_data,
        )
        btn_save.pack(fill="x", padx=25, pady=(0, 15))
