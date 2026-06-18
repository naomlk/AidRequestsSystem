import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime


class DeliveryScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection
        self.all_deliveries = []
        self.filtered_deliveries = []
        self.delivery_options_map = {}

        # Liste pour stocker uniquement les traitements EN COURS (completion_time IS NULL)
        self.active_treatments_list = []
        self.selected_treatment_id = None

        # ========================================================
        # HEADER SECTION
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title = ctk.CTkLabel(
            self.header_frame,
            text="📦 Deliveries Management",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(side="left", anchor="w")

        btn_send_delivery = ctk.CTkButton(
            self.header_frame,
            text="➕ Create and Send Delivery",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_delivery_form
        )
        btn_send_delivery.pack(side="right", padx=(0, 20))

        # ========================================================
        # MAIN CONTAINER
        # ========================================================
        self.container_box = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        # ========================================================
        # SEARCH BAR (Main Screen)
        # ========================================================
        self.search_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=20, pady=(18, 8))

        search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search delivery:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057"
        )
        search_label.pack(side="left", padx=(0, 8))

        self.search_combo = ctk.CTkComboBox(
            self.search_frame,
            values=[],
            width=330,
            height=34,
            command=self.on_search_combo_select
        )
        self.search_combo.pack(side="left", padx=(0, 10))
        self.search_combo.set("Search by ID, date, status or item type...")
        self.search_combo.bind("<KeyRelease>", self.on_search_typing)
        self.search_combo.bind("<Return>", self.select_first_search_match)

        self.status_filter = ctk.CTkComboBox(
            self.search_frame,
            values=["All Statuses", "Pending", "Delivered", "Cancelled"],
            width=145,
            height=34,
            command=lambda _=None: self.apply_filters()
        )
        self.status_filter.pack(side="left", padx=(0, 10))
        self.status_filter.set("All Statuses")

        self.item_filter = ctk.CTkComboBox(
            self.search_frame,
            values=["All Items", "Water Packs", "Vital Medicines", "Food Basket", "Medical Oxygen"],
            width=170,
            height=34,
            command=lambda _=None: self.apply_filters()
        )
        self.item_filter.pack(side="left", padx=(0, 10))
        self.item_filter.set("All Items")

        btn_show_all = ctk.CTkButton(
            self.search_frame,
            text="Show All",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6C757D",
            hover_color="#5C636A",
            width=90,
            height=34,
            corner_radius=7,
            command=self.reset_filters
        )
        btn_show_all.pack(side="left")

        # ========================================================
        # TABLE STYLE
        # ========================================================
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#212529",
            rowheight=35,
            fieldbackground="#FFFFFF",
            borderwidth=0,
            font=("Segoe UI", 11)
        )
        style.configure(
            "Treeview.Heading",
            background="#F1F3F5",
            foreground="#495057",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            relief="flat"
        )
        style.map("Treeview", background=[("selected", "#1A62E8")], foreground=[("selected", "#FFFFFF")])

        columns = ("delivery_id", "date", "status", "item_type", "quantity")
        self.tree = ttk.Treeview(self.container_box, columns=columns, show="headings")

        self.tree.heading("delivery_id", text="Delivery ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("status", text="Status")
        self.tree.heading("item_type", text="Item Type")
        self.tree.heading("quantity", text="Quantity")

        self.tree.column("delivery_id", width=90, anchor="center")
        self.tree.column("date", width=130, anchor="center")
        self.tree.column("status", width=130, anchor="center")
        self.tree.column("item_type", width=220, anchor="w")
        self.tree.column("quantity", width=90, anchor="center")

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")
        self.tree.tag_configure("delivered", foreground="#198754")
        self.tree.tag_configure("pending", foreground="#B45309")
        self.tree.tag_configure("cancelled", foreground="#DC3545")

        self.tree.pack(fill="both", expand=True, padx=20, pady=(8, 10))

        self.tree.bind("<Button-3>", self.on_right_click_show_treatment)
        self.tree.bind("<Double-1>", self.on_double_click_update)

        # ========================================================
        # FOOTER ACTIONS
        # ========================================================
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        btn_delete = ctk.CTkButton(
            self.footer_frame,
            text="🗑️ Delete Selected Delivery",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=190,
            height=35,
            corner_radius=6,
            command=self.delete_selected_delivery
        )
        btn_delete.pack(side="left", padx=(0, 10))

        btn_update_selected = ctk.CTkButton(
            self.footer_frame,
            text="✏️ Update Selected Delivery",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            width=190,
            height=35,
            corner_radius=6,
            command=self.on_update_button_click
        )
        btn_update_selected.pack(side="left")

        hint_lbl = ctk.CTkLabel(
            self.footer_frame,
            text="💡 Right-click a delivery to view its assigned treatment. Double-click to update.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        hint_lbl.pack(side="right", pady=5)

        self.load_deliveries_from_db()

    # ========================================================
    # DB LOADING & FILTERS
    # ========================================================
    def load_deliveries_from_db(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT delivery_id, date, status, item_type, quantity
                FROM public.a_delivery
                ORDER BY delivery_id;
            """)
            rows = cursor.fetchall()
            cursor.close()

            self.all_deliveries = rows
            self.filtered_deliveries = list(rows)
            self.refresh_search_options(rows)
            self.render_deliveries(rows)
        except Exception as e:
            messagebox.showerror("SQL Database Error", f"Failed to retrieve deliveries:\n{e}")

    def render_deliveries(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, row in enumerate(rows):
            delivery_id, date_val, status, item_type, quantity = row
            row_tags = ["evenrow" if i % 2 == 0 else "oddrow"]
            status_clean = str(status).strip().lower() if status else ""
            if status_clean == "delivered":
                row_tags.append("delivered")
            elif status_clean == "pending":
                row_tags.append("pending")
            elif status_clean == "cancelled":
                row_tags.append("cancelled")
            self.tree.insert("", "end", values=row, tags=tuple(row_tags))

    def refresh_search_options(self, rows):
        options = []
        self.delivery_options_map.clear()
        for row in rows:
            delivery_id, date_val, status, item_type, quantity = row
            label = f"#{delivery_id} — {date_val} — {item_type} x{quantity} — {status}"
            options.append(label)
            self.delivery_options_map[label] = delivery_id
        self.search_combo.configure(values=options)

    def on_search_typing(self, event=None):
        self.apply_filters()

    def apply_filters(self):
        query = self.search_combo.get().strip().lower()
        if query.startswith("search by"):
            query = ""
        selected_status = self.status_filter.get()
        selected_item = self.item_filter.get()

        filtered = []
        matching_options = []
        for row in self.all_deliveries:
            delivery_id, date_val, status, item_type, quantity = row
            searchable = f"{delivery_id} {date_val} {status} {item_type} {quantity}".lower()
            if query and query not in searchable:
                continue
            if selected_status != "All Statuses" and str(status) != selected_status:
                continue
            if selected_item != "All Items" and str(item_type) != selected_item:
                continue
            filtered.append(row)
            label = f"#{delivery_id} — {date_val} — {item_type} x{quantity} — {status}"
            matching_options.append(label)
            self.delivery_options_map[label] = delivery_id

        self.filtered_deliveries = filtered
        self.search_combo.configure(values=matching_options)
        self.render_deliveries(filtered)

    def on_search_combo_select(self, selected_value):
        delivery_id = self.delivery_options_map.get(selected_value)
        if delivery_id is None:
            return
        selected_rows = [row for row in self.all_deliveries if row[0] == delivery_id]
        self.filtered_deliveries = selected_rows
        self.render_deliveries(selected_rows)
        self.select_delivery_in_tree(delivery_id)

    def select_first_search_match(self, event=None):
        if not self.filtered_deliveries:
            return
        self.select_delivery_in_tree(self.filtered_deliveries[0][0])

    def select_delivery_in_tree(self, delivery_id):
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values and str(values[0]) == str(delivery_id):
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                return

    def reset_filters(self):
        self.search_combo.set("Search by ID, date, status or item type...")
        self.status_filter.set("All Statuses")
        self.item_filter.set("All Items")
        self.filtered_deliveries = list(self.all_deliveries)
        self.refresh_search_options(self.all_deliveries)
        self.render_deliveries(self.all_deliveries)

    # ========================================================
    # DETAILS EXTRACTION & CRUD ACTIONS
    # ========================================================
    def on_right_click_show_treatment(self, event):
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        self.tree.selection_set(row_id)
        values = self.tree.item(row_id, "values")
        if values:
            self.show_assigned_treatment(values[0])

    def show_assigned_treatment(self, delivery_id):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT t.treatment_id, t.date, t.start_time, t.completion_time,
                       COALESCE(v.first_name || ' ' || v.last_name, 'Unknown volunteer'),
                       COALESCE(r.incident_description, 'No description'),
                       COALESCE(rc.category_name, 'Unknown category'),
                       d.item_type, d.quantity, d.status
                FROM public.a_treatment t
                LEFT JOIN public.a_volunteer v ON v.volunteer_id = t.volunteer_id
                LEFT JOIN public.a_request r ON r.request_id = t.request_id
                LEFT JOIN public.a_requestcategory rc ON rc.category_id = r.category_id
                LEFT JOIN public.a_delivery d ON d.delivery_id = t.delivery_id
                WHERE t.delivery_id = %s LIMIT 1;
            """, (delivery_id,))
            treatment = cursor.fetchone()
            cursor.close()

            if not treatment:
                messagebox.showinfo("Assigned Treatment", f"Delivery #{delivery_id} has no linked treatment.")
                return

            messagebox.showinfo("Assigned Treatment",
                                f"Treatment ID: {treatment[0]}\nDate: {treatment[1]}\n"
                                f"Volunteer: {treatment[4]}\nCategory: {treatment[6]}\n"
                                f"Description: {treatment[5]}")
        except Exception as e:
            messagebox.showerror("SQL Error", f"Failed to load treatment:\n{e}")

    def on_update_button_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a delivery to update.")
            return
        self.open_delivery_form(edit_mode=True, data=self.tree.item(selected_item, "values"))

    def on_double_click_update(self, event=None):
        self.on_update_button_click()

    def delete_selected_delivery(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Missing", "Please select a delivery to delete.")
            return
        values = self.tree.item(selected_item, "values")
        delivery_id = values[0]

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM public.a_treatment WHERE delivery_id = %s;", (delivery_id,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Delete Blocked", "This delivery is linked to a treatment.")
                cursor.close()
                return
            cursor.close()
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))
            return

        if messagebox.askyesno("Confirm", f"Permanently delete delivery #{delivery_id}?"):
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM public.a_delivery WHERE delivery_id = %s;", (delivery_id,))
                self.conn.commit()
                cursor.close()
                self.load_deliveries_from_db()
            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("Error", str(e))

    # ========================================================
    # LOOKUP ENGINE: DYNAMIC EN COURS (completion_time IS NULL)
    # ========================================================
    def fetch_active_treatments_pool(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT t.treatment_id, rc.category_name, r.incident_description
                FROM public.a_treatment t
                JOIN public.a_request r ON t.request_id = r.request_id
                JOIN public.a_requestcategory rc ON r.category_id = rc.category_id
                WHERE t.completion_time IS NULL 
                  AND t.delivery_id IS NULL
                ORDER BY t.treatment_id;
            """)
            self.active_treatments_list = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Error caching treatments: {e}")

    # ========================================================
    # WINDOW FORM WITH AUTO-COLLAPSE SUGGESTIONS
    # ========================================================
    def open_delivery_form(self, edit_mode=False, data=None):
        self.fetch_active_treatments_pool()
        self.selected_treatment_id = None

        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Delivery" if edit_mode else "Create and Send Delivery")
        form_window.geometry("540x560")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(
            form_window,
            text="✏️ Update Delivery Details" if edit_mode else "🚚 Send Delivery Details",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#0F4C81"
        )
        form_title.pack(pady=(12, 6))

        main_scrollable = ctk.CTkScrollableFrame(
            form_window,
            fg_color="#FFFFFF",
            corner_radius=8,
            border_width=1,
            border_color="#E9ECEF"
        )
        main_scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        # --- ZONE DE RECHERCHE DE TRAITEMENT EN COURS ---
        ctk.CTkLabel(
            main_scrollable, text="Search Active Treatment (In Progress Only)",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(8, 1))

        search_entry = ctk.CTkEntry(
            main_scrollable, width=420, height=30,
            placeholder_text="Type Treatment ID, Category or description..."
        )
        search_entry.pack(padx=15, pady=(0, 2))

        # Zone de suggestions réactive
        suggestion_frame = ctk.CTkScrollableFrame(main_scrollable, width=400, height=65, fg_color="#F8F9FA")
        suggestion_frame.pack(padx=15, pady=(0, 4))

        def select_treatment(t_id, display_text):
            self.selected_treatment_id = t_id
            search_entry.delete(0, "end")
            search_entry.insert(0, display_text)

            # --- ACTION : Masquer complètement le cadre vide ---
            suggestion_frame.pack_forget()

            lbl_status.configure(text=f"✅ Linked to Active Treatment #{t_id}", text_color="#198754")

        def update_suggestions(event=None):
            query = search_entry.get().strip().lower()

            # Si l'utilisateur efface sa sélection, on réaffiche le cadre de choix
            if not self.selected_treatment_id or query == "":
                self.selected_treatment_id = None
                lbl_status.configure(text="⚠️ No active treatment selected yet", text_color="#B45309")
                suggestion_frame.pack(padx=15, pady=(0, 4), before=lbl_status)

            for child in suggestion_frame.winfo_children():
                child.destroy()

            match_count = 0
            for t_id, cat_name, desc in self.active_treatments_list:
                full_text = f"ID #{t_id} — [{cat_name}] {desc or ''}"
                if not query or query in full_text.lower():
                    btn_text = f"ID #{t_id} — {cat_name} ({desc[:25]}...)" if desc else f"ID #{t_id} — {cat_name}"
                    btn = ctk.CTkButton(
                        suggestion_frame, text=btn_text, font=ctk.CTkFont(size=11),
                        fg_color="transparent", text_color="#212529", hover_color="#E9ECEF",
                        anchor="w", height=22,
                        command=lambda idx=t_id, txt=full_text: select_treatment(idx, txt)
                    )
                    btn.pack(fill="x", pady=1)
                    match_count += 1
                    if match_count >= 10:
                        break

            # Si aucun résultat ne correspond à la frappe, on cache temporairement
            if match_count == 0:
                suggestion_frame.pack_forget()

        search_entry.bind("<KeyRelease>", update_suggestions)

        lbl_status = ctk.CTkLabel(
            main_scrollable, text="⚠️ No active treatment selected yet",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#B45309"
        )
        lbl_status.pack(anchor="w", padx=17, pady=(0, 6))

        if edit_mode:
            search_entry.configure(state="disabled")
            suggestion_frame.pack_forget()
            lbl_status.pack_forget()
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    SELECT t.treatment_id, rc.category_name FROM public.a_treatment t
                    JOIN public.a_request r ON t.request_id = r.request_id
                    JOIN public.a_requestcategory rc ON r.category_id = rc.category_id
                    WHERE t.delivery_id = %s;
                """, (data[0],))
                res = cursor.fetchone()
                cursor.close()
                if res:
                    search_entry.configure(state="normal")
                    search_entry.insert(0, f"ID #{res[0]} — [{res[1]}]")
                    search_entry.configure(state="disabled", fg_color="#F1F3F5")
            except:
                pass
        else:
            update_suggestions()

        # Delivery ID
        ctk.CTkLabel(
            main_scrollable, text="Delivery ID (Generated Key)",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(4, 1))
        entry_id = ctk.CTkEntry(main_scrollable, width=420, height=30)
        entry_id.pack(padx=15, pady=(0, 8))
        if edit_mode:
            entry_id.insert(0, data[0])
        else:
            entry_id.insert(0, "[Calculated Dynamically on Save]")
        entry_id.configure(state="disabled", fg_color="#F1F3F5")

        # Date
        ctk.CTkLabel(
            main_scrollable, text="Delivery Date (YYYY-MM-DD)",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(4, 1))
        entry_date = ctk.CTkEntry(main_scrollable, width=420, height=30)
        entry_date.pack(padx=15, pady=(0, 8))
        entry_date.insert(0, data[1] if edit_mode else datetime.now().strftime("%Y-%m-%d"))

        # Status
        ctk.CTkLabel(
            main_scrollable, text="Delivery Status",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(4, 1))
        combo_status = ctk.CTkComboBox(main_scrollable, values=["Pending", "Delivered", "Cancelled"], width=420,
                                       height=30)
        combo_status.pack(padx=15, pady=(0, 8))
        combo_status.set(data[2] if edit_mode else "Delivered")

        # Item Type
        ctk.CTkLabel(
            main_scrollable, text="Item Type",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(4, 1))
        combo_item = ctk.CTkComboBox(main_scrollable,
                                     values=["Water Packs", "Vital Medicines", "Food Basket", "Medical Oxygen"],
                                     width=420, height=30)
        combo_item.pack(padx=15, pady=(0, 8))
        combo_item.set(data[3] if edit_mode else "Water Packs")

        # Quantity
        ctk.CTkLabel(
            main_scrollable, text="Quantity",
            font=ctk.CTkFont(size=11, weight="bold"), text_color="#6C757D"
        ).pack(anchor="w", padx=15, pady=(4, 1))
        entry_quantity = ctk.CTkEntry(main_scrollable, width=420, height=30)
        entry_quantity.pack(padx=15, pady=(0, 10))
        entry_quantity.insert(0, data[4] if edit_mode else "1")

        def save_form_data():
            try:
                delivery_date = entry_date.get().strip()
                status = combo_status.get().strip()
                item_type = combo_item.get().strip()
                quantity = entry_quantity.get().strip()

                if not edit_mode and self.selected_treatment_id is None:
                    messagebox.showwarning("Validation Error",
                                           "Please look up and select a valid active treatment from the list.",
                                           parent=form_window)
                    return

                if not delivery_date or not status or not item_type or not quantity:
                    messagebox.showwarning("Validation Error", "All fields must be populated.", parent=form_window)
                    return

                try:
                    datetime.strptime(delivery_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Format Error", "Date format must be YYYY-MM-DD.", parent=form_window)
                    return

                try:
                    quantity_int = int(quantity)
                    if quantity_int <= 0: raise ValueError()
                except ValueError:
                    messagebox.showerror("Format Error", "Quantity must be a positive integer.", parent=form_window)
                    return

                cursor = self.conn.cursor()

                if edit_mode:
                    cursor.execute("""
                        UPDATE public.a_delivery
                        SET date = %s, status = %s, item_type = %s, quantity = %s
                        WHERE delivery_id = %s;
                    """, (delivery_date, status, item_type, quantity_int, data[0]))
                else:
                    cursor.execute("SELECT completion_time FROM public.a_treatment WHERE treatment_id = %s;",
                                   (self.selected_treatment_id,))
                    chk = cursor.fetchone()
                    if chk and chk[0] is not None:
                        messagebox.showerror("Action Blocked",
                                             "This treatment has just been completed and is no longer active.",
                                             parent=form_window)
                        cursor.close()
                        return

                    cursor.execute("SELECT COALESCE(MAX(delivery_id), 0) + 1 FROM public.a_delivery;")
                    next_id = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO public.a_delivery (delivery_id, date, status, item_type, quantity)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (next_id, delivery_date, status, item_type, quantity_int))

                    cursor.execute("""
                        UPDATE public.a_treatment
                        SET delivery_id = %s
                        WHERE treatment_id = %s;
                    """, (next_id, self.selected_treatment_id))

                self.conn.commit()
                cursor.close()

                messagebox.showinfo("Success", "Delivery saved and mapped successfully.", parent=form_window)
                form_window.destroy()
                self.load_deliveries_from_db()

            except Exception as e:
                if self.conn: self.conn.rollback()
                messagebox.showerror("Database Error", f"SQL rejection code details:\n{e}", parent=form_window)

        btn_save = ctk.CTkButton(
            form_window, text="💾 Save Delivery", font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#198754", hover_color="#146C43", height=38, corner_radius=6, command=save_form_data
        )
        btn_save.pack(fill="x", padx=20, pady=(0, 12))