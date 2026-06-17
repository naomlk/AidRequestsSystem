import customtkinter as ctk
from tkinter import ttk, messagebox


class TrainingScreen(ctk.CTkFrame):
    TRAINING_TABLE = "b_training"
    SCHEDULED_TABLE = "b_scheduled"
    VOLUNTEER_TRAINING_TABLE = "b_volunteer_training"

    TRAINING_ID_COLUMN = "training_id"
    VOLUNTEER_ID_COLUMN = "volunteer_id"

    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")

        self.conn = db_connection
        self.training_columns = []

        # ========================================================
        # HEADER
        # ========================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            self.header_frame,
            text="🎓 Training Management System",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(side="left", anchor="w")

        btn_add = ctk.CTkButton(
            self.header_frame,
            text="➕ Add New Training",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            corner_radius=8,
            command=self.open_training_form
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
            border_color="#E9ECEF"
        )
        self.container_box.pack(fill="both", expand=True, padx=5, pady=5)

        self.configure_tree_style()

        self.table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        self.training_columns = self.get_table_columns(self.TRAINING_TABLE)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.training_columns,
            show="headings"
        )

        scrollbar_y = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar_x = ttk.Scrollbar(
            self.table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        for col in self.training_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, minwidth=100, anchor="center")

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        # ========================================================
        # FOOTER ACTIONS
        # ========================================================
        self.footer_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=20, pady=(5, 15))

        btn_delete = ctk.CTkButton(
            self.footer_frame,
            text="🗑️ Delete Training",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=150,
            height=35,
            corner_radius=6,
            command=self.delete_selected_training
        )
        btn_delete.pack(side="left")

        btn_schedule = ctk.CTkButton(
            self.footer_frame,
            text="📅 Show Schedule Info",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6F42C1",
            hover_color="#5A32A3",
            width=175,
            height=35,
            corner_radius=6,
            command=self.open_schedule_window_for_selected_training
        )
        btn_schedule.pack(side="left", padx=(10, 0))

        btn_volunteers = ctk.CTkButton(
            self.footer_frame,
            text="👷 Manage Volunteers",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0F4C81",
            hover_color="#0B3A63",
            width=175,
            height=35,
            corner_radius=6,
            command=self.open_volunteers_window_for_selected_training
        )
        btn_volunteers.pack(side="left", padx=(10, 0))

        hint_lbl = ctk.CTkLabel(
            self.footer_frame,
            text="💡 Double-click a training to edit it. Use Schedule / Volunteers for linked data.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        hint_lbl.pack(side="right", pady=5)

        self.tree.bind("<Double-1>", self.on_training_double_click)

        self.load_trainings_from_db()

    # ========================================================
    # GENERAL HELPERS
    # ========================================================
    def configure_tree_style(self):
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
        style.map(
            "Treeview",
            background=[("selected", "#1A62E8")],
            foreground=[("selected", "#FFFFFF")]
        )

    def q(self, identifier):
        return '"' + identifier.replace('"', '""') + '"'

    def get_table_columns(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position;
                """,
                (table_name,)
            )

            columns = [row[0] for row in cursor.fetchall()]
            cursor.close()

            if not columns:
                messagebox.showwarning(
                    "Table Warning",
                    f"No columns found for public.{table_name}. Check the table name."
                )

            return columns

        except Exception as e:
            messagebox.showerror(
                "SQL Metadata Error",
                f"Failed to read columns for {table_name}:\n{e}"
            )
            return []

    def get_selected_values(self):
        selected_item = self.tree.selection()

        if not selected_item:
            return None

        return self.tree.item(selected_item, "values")

    def get_training_id_from_values(self, values):
        try:
            index = self.training_columns.index(self.TRAINING_ID_COLUMN)
            return values[index]

        except ValueError:
            messagebox.showerror(
                "Column Missing",
                f"Column '{self.TRAINING_ID_COLUMN}' was not found in {self.TRAINING_TABLE}."
            )
            return None

    # ========================================================
    # LOAD TRAININGS
    # ========================================================
    def load_trainings_from_db(self):
        if not self.conn or not self.training_columns:
            return

        try:
            cursor = self.conn.cursor()

            cols_sql = ", ".join(self.q(col) for col in self.training_columns)

            if self.TRAINING_ID_COLUMN in self.training_columns:
                order_sql = self.q(self.TRAINING_ID_COLUMN)
            else:
                order_sql = "1"

            query = f"""
                SELECT {cols_sql}
                FROM public.{self.q(self.TRAINING_TABLE)}
                ORDER BY {order_sql};
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))

            cursor.close()

        except Exception as e:
            messagebox.showerror(
                "SQL Database Error",
                f"Failed to retrieve rows from public.{self.TRAINING_TABLE}:\n{e}"
            )

    # ========================================================
    # ADD / UPDATE TRAINING
    # ========================================================
    def on_training_double_click(self, event):
        selected_values = self.get_selected_values()

        if not selected_values:
            return

        self.open_training_form(edit_mode=True, data=selected_values)

    def open_training_form(self, edit_mode=False, data=None):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Training" if edit_mode else "Add New Training")
        form_window.geometry("520x640")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(
            form_window,
            text="📝 Training Attributes Form",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#0F4C81"
        )
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkScrollableFrame(
            form_window,
            fg_color="#FFFFFF",
            corner_radius=8,
            border_width=1,
            border_color="#E9ECEF"
        )
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        entries = {}

        for i, col in enumerate(self.training_columns):
            ctk.CTkLabel(
                fields_container,
                text=col,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#6C757D"
            ).pack(anchor="w", padx=20, pady=(10 if i == 0 else 5, 2))

            entry = ctk.CTkEntry(fields_container, width=400, height=32)
            entry.pack(padx=20, pady=(0, 8))

            if edit_mode:
                entry.insert(0, "" if data[i] is None else str(data[i]))

                if col == self.TRAINING_ID_COLUMN:
                    entry.configure(state="disabled", fg_color="#F1F3F5")

            entries[col] = entry

        def save_form_data():
            values = {}

            for col, entry in entries.items():
                value = entry.get().strip()
                values[col] = value if value != "" else None

            if self.TRAINING_ID_COLUMN not in values or values[self.TRAINING_ID_COLUMN] is None:
                messagebox.showwarning(
                    "Validation Error",
                    "training_id is required.",
                    parent=form_window
                )
                return

            try:
                cursor = self.conn.cursor()

                if edit_mode:
                    update_columns = [
                        col for col in self.training_columns
                        if col != self.TRAINING_ID_COLUMN
                    ]

                    set_clause = ", ".join(
                        f"{self.q(col)} = %s"
                        for col in update_columns
                    )

                    sql = f"""
                        UPDATE public.{self.q(self.TRAINING_TABLE)}
                        SET {set_clause}
                        WHERE {self.q(self.TRAINING_ID_COLUMN)} = %s;
                    """

                    params = [values[col] for col in update_columns]
                    params.append(values[self.TRAINING_ID_COLUMN])

                    cursor.execute(sql, params)

                else:
                    cols_sql = ", ".join(
                        self.q(col)
                        for col in self.training_columns
                    )

                    placeholders = ", ".join(
                        ["%s"] * len(self.training_columns)
                    )

                    sql = f"""
                        INSERT INTO public.{self.q(self.TRAINING_TABLE)}
                        ({cols_sql})
                        VALUES ({placeholders});
                    """

                    params = [values[col] for col in self.training_columns]
                    cursor.execute(sql, params)

                self.conn.commit()
                cursor.close()

                messagebox.showinfo(
                    "Success",
                    "Training saved successfully.",
                    parent=form_window
                )

                form_window.destroy()
                self.load_trainings_from_db()

            except Exception as e:
                self.conn.rollback()
                messagebox.showerror(
                    "SQL Transaction Error",
                    f"Failed to save training:\n{e}",
                    parent=form_window
                )

        btn_save = ctk.CTkButton(
            form_window,
            text="💾 Save Training",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#198754",
            hover_color="#146C43",
            height=38,
            corner_radius=6,
            command=save_form_data
        )
        btn_save.pack(fill="x", padx=25, pady=(0, 15))

    # ========================================================
    # DELETE TRAINING + LINKED ROWS
    # ========================================================
    def delete_selected_training(self):
        selected_values = self.get_selected_values()

        if not selected_values:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a training row before deleting."
            )
            return

        training_id = self.get_training_id_from_values(selected_values)

        if training_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"""Are you sure you want to permanently delete Training #{training_id}?

This will also delete:
- scheduled rows from {self.SCHEDULED_TABLE}
- volunteer assignments from {self.VOLUNTEER_TRAINING_TABLE}"""
        )

        if not confirm:
            return

        try:
            cursor = self.conn.cursor()

            # 1. Delete volunteer-training associations first
            cursor.execute(
                f"""
                DELETE FROM public.{self.q(self.VOLUNTEER_TRAINING_TABLE)}
                WHERE {self.q(self.TRAINING_ID_COLUMN)} = %s;
                """,
                (training_id,)
            )

            # 2. Delete scheduled rows linked to this training
            cursor.execute(
                f"""
                DELETE FROM public.{self.q(self.SCHEDULED_TABLE)}
                WHERE {self.q(self.TRAINING_ID_COLUMN)} = %s;
                """,
                (training_id,)
            )

            # 3. Delete training itself
            cursor.execute(
                f"""
                DELETE FROM public.{self.q(self.TRAINING_TABLE)}
                WHERE {self.q(self.TRAINING_ID_COLUMN)} = %s;
                """,
                (training_id,)
            )

            self.conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Success",
                "Training and linked rows were deleted successfully."
            )

            self.load_trainings_from_db()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror(
                "SQL Transaction Failed",
                f"Could not delete training and linked records:\n{e}"
            )

    # ========================================================
    # OPEN LINKED WINDOWS
    # ========================================================
    def open_schedule_window_for_selected_training(self):
        selected_values = self.get_selected_values()

        if not selected_values:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a training row first."
            )
            return

        training_id = self.get_training_id_from_values(selected_values)

        if training_id is None:
            return

        ScheduleWindow(
            parent=self,
            db_connection=self.conn,
            training_id=training_id,
            scheduled_table=self.SCHEDULED_TABLE,
            training_id_column=self.TRAINING_ID_COLUMN
        )

    def open_volunteers_window_for_selected_training(self):
        selected_values = self.get_selected_values()

        if not selected_values:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a training row first."
            )
            return

        training_id = self.get_training_id_from_values(selected_values)

        if training_id is None:
            return

        ManageTrainingVolunteersWindow(
            parent=self,
            db_connection=self.conn,
            training_id=training_id,
            volunteer_training_table=self.VOLUNTEER_TRAINING_TABLE,
            training_id_column=self.TRAINING_ID_COLUMN,
            volunteer_id_column=self.VOLUNTEER_ID_COLUMN
        )


# ============================================================
# WINDOW 1: SCHEDULE INFO FOR SELECTED TRAINING
# ============================================================
class ScheduleWindow(ctk.CTkToplevel):
    def __init__(self, parent, db_connection, training_id, scheduled_table, training_id_column):
        super().__init__(parent)

        self.conn = db_connection
        self.training_id = training_id
        self.scheduled_table = scheduled_table
        self.training_id_column = training_id_column
        self.scheduled_columns = self.get_table_columns(self.scheduled_table)

        self.title(f"Schedule Info - Training #{training_id}")
        self.geometry("900x520")
        self.configure(fg_color="#F8F9FA")
        self.grab_set()
        self.resizable(True, True)

        title = ctk.CTkLabel(
            self,
            text=f"📅 Scheduled Information for Training #{training_id}",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(anchor="w", padx=25, pady=(20, 10))

        self.container_box = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.container_box.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        self.configure_tree_style()

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.scheduled_columns,
            show="headings"
        )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        for col in self.scheduled_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, minwidth=100, anchor="center")

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        footer = ctk.CTkFrame(self.container_box, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(5, 15))

        btn_add = ctk.CTkButton(
            footer,
            text="➕ Add Schedule Row",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            width=160,
            height=35,
            corner_radius=6,
            command=self.open_schedule_form
        )
        btn_add.pack(side="left")

        btn_delete = ctk.CTkButton(
            footer,
            text="🗑️ Delete Selected Row",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=170,
            height=35,
            corner_radius=6,
            command=self.delete_selected_schedule
        )
        btn_delete.pack(side="left", padx=(10, 0))

        hint = ctk.CTkLabel(
            footer,
            text="💡 Double-click a scheduled row to update it.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        hint.pack(side="right")

        self.tree.bind("<Double-1>", self.on_schedule_double_click)

        self.load_schedule_rows()

    def configure_tree_style(self):
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
        style.map(
            "Treeview",
            background=[("selected", "#1A62E8")],
            foreground=[("selected", "#FFFFFF")]
        )

    def q(self, identifier):
        return '"' + identifier.replace('"', '""') + '"'

    def get_table_columns(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                ORDER BY ordinal_position;
                """,
                (table_name,)
            )

            columns = [row[0] for row in cursor.fetchall()]
            cursor.close()

            return columns

        except Exception as e:
            messagebox.showerror(
                "SQL Metadata Error",
                f"Failed to read columns for {table_name}:\n{e}"
            )
            return []

    def load_schedule_rows(self):
        if not self.scheduled_columns:
            return

        try:
            cursor = self.conn.cursor()

            cols_sql = ", ".join(self.q(col) for col in self.scheduled_columns)

            sql = f"""
                SELECT {cols_sql}
                FROM public.{self.q(self.scheduled_table)}
                WHERE {self.q(self.training_id_column)} = %s
                ORDER BY 1;
            """

            cursor.execute(sql, (self.training_id,))
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))

            cursor.close()

        except Exception as e:
            messagebox.showerror(
                "SQL Database Error",
                f"Failed to load scheduled rows:\n{e}"
            )

    def on_schedule_double_click(self, event):
        selected_item = self.tree.selection()

        if not selected_item:
            return

        row_values = self.tree.item(selected_item, "values")
        self.open_schedule_form(edit_mode=True, data=row_values)

    def open_schedule_form(self, edit_mode=False, data=None):
        form_window = ctk.CTkToplevel(self)
        form_window.title("Edit Schedule Row" if edit_mode else "Add Schedule Row")
        form_window.geometry("500x600")
        form_window.configure(fg_color="#F8F9FA")
        form_window.grab_set()
        form_window.resizable(False, False)

        form_title = ctk.CTkLabel(
            form_window,
            text="📝 Scheduled Training Form",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#0F4C81"
        )
        form_title.pack(pady=(15, 10))

        fields_container = ctk.CTkScrollableFrame(
            form_window,
            fg_color="#FFFFFF",
            corner_radius=8,
            border_width=1,
            border_color="#E9ECEF"
        )
        fields_container.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        entries = {}

        for i, col in enumerate(self.scheduled_columns):
            ctk.CTkLabel(
                fields_container,
                text=col,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#6C757D"
            ).pack(anchor="w", padx=20, pady=(10 if i == 0 else 5, 2))

            entry = ctk.CTkEntry(fields_container, width=380, height=32)
            entry.pack(padx=20, pady=(0, 8))

            if edit_mode:
                entry.insert(0, "" if data[i] is None else str(data[i]))

            else:
                if col == self.training_id_column:
                    entry.insert(0, str(self.training_id))

            if col == self.training_id_column:
                entry.configure(state="disabled", fg_color="#F1F3F5")

            entries[col] = entry

        def save_form_data():
            values = {}

            for col, entry in entries.items():
                value = entry.get().strip()
                values[col] = value if value != "" else None

            values[self.training_id_column] = self.training_id

            try:
                cursor = self.conn.cursor()

                if edit_mode:
                    set_clause = ", ".join(
                        f"{self.q(col)} = %s"
                        for col in self.scheduled_columns
                    )

                    where_clause = " AND ".join(
                        f"{self.q(col)} IS NOT DISTINCT FROM %s"
                        for col in self.scheduled_columns
                    )

                    sql = f"""
                        UPDATE public.{self.q(self.scheduled_table)}
                        SET {set_clause}
                        WHERE {where_clause};
                    """

                    new_params = [values[col] for col in self.scheduled_columns]
                    old_params = list(data)

                    cursor.execute(sql, new_params + old_params)

                else:
                    cols_sql = ", ".join(
                        self.q(col)
                        for col in self.scheduled_columns
                    )

                    placeholders = ", ".join(
                        ["%s"] * len(self.scheduled_columns)
                    )

                    sql = f"""
                        INSERT INTO public.{self.q(self.scheduled_table)}
                        ({cols_sql})
                        VALUES ({placeholders});
                    """

                    params = [values[col] for col in self.scheduled_columns]
                    cursor.execute(sql, params)

                self.conn.commit()
                cursor.close()

                messagebox.showinfo(
                    "Success",
                    "Scheduled row saved successfully.",
                    parent=form_window
                )

                form_window.destroy()
                self.load_schedule_rows()

            except Exception as e:
                self.conn.rollback()
                messagebox.showerror(
                    "SQL Transaction Error",
                    f"Failed to save scheduled row:\n{e}",
                    parent=form_window
                )

        btn_save = ctk.CTkButton(
            form_window,
            text="💾 Save Schedule Row",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#198754",
            hover_color="#146C43",
            height=38,
            corner_radius=6,
            command=save_form_data
        )
        btn_save.pack(fill="x", padx=25, pady=(0, 15))

    def delete_selected_schedule(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a scheduled row before deleting.",
                parent=self
            )
            return

        row_values = self.tree.item(selected_item, "values")

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this scheduled row?",
            parent=self
        )

        if not confirm:
            return

        try:
            cursor = self.conn.cursor()

            where_clause = " AND ".join(
                f"{self.q(col)} IS NOT DISTINCT FROM %s"
                for col in self.scheduled_columns
            )

            sql = f"""
                DELETE FROM public.{self.q(self.scheduled_table)}
                WHERE {where_clause};
            """

            cursor.execute(sql, list(row_values))

            self.conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Success",
                "Scheduled row deleted successfully.",
                parent=self
            )

            self.load_schedule_rows()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror(
                "SQL Transaction Error",
                f"Failed to delete scheduled row:\n{e}",
                parent=self
            )


# ============================================================
# WINDOW 2: MANAGE VOLUNTEERS FOR SELECTED TRAINING
# ============================================================
class ManageTrainingVolunteersWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        db_connection,
        training_id,
        volunteer_training_table,
        training_id_column,
        volunteer_id_column
    ):
        super().__init__(parent)

        self.conn = db_connection
        self.training_id = training_id
        self.volunteer_training_table = volunteer_training_table
        self.training_id_column = training_id_column
        self.volunteer_id_column = volunteer_id_column

        self.volunteer_map = {}
        self.all_volunteer_display_values = []

        self.title(f"Manage Volunteers - Training #{training_id}")
        self.geometry("950x590")
        self.configure(fg_color="#F8F9FA")
        self.grab_set()
        self.resizable(True, True)

        title = ctk.CTkLabel(
            self,
            text=f"👷 Volunteers Assigned to Training #{training_id}",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(anchor="w", padx=25, pady=(20, 10))

        # ========================================================
        # SEARCH + COMBOBOX AREA
        # ========================================================
        action_box = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        action_box.pack(fill="x", padx=25, pady=(0, 15))

        label_search = ctk.CTkLabel(
            action_box,
            text="Search volunteer:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#6C757D"
        )
        label_search.grid(row=0, column=0, padx=(20, 8), pady=(15, 5), sticky="w")

        self.entry_search = ctk.CTkEntry(
            action_box,
            width=260,
            height=35,
            placeholder_text="Type ID, first name, or last name..."
        )
        self.entry_search.grid(row=0, column=1, padx=8, pady=(15, 5), sticky="w")

        # typing filters the combobox
        self.entry_search.bind("<KeyRelease>", self.filter_volunteers_combobox)

        # Enter highlights the volunteer in the assigned volunteers table
        self.entry_search.bind("<Return>", self.highlight_assigned_volunteer_from_search)

        label_combo = ctk.CTkLabel(
            action_box,
            text="Choose volunteer:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#6C757D"
        )
        label_combo.grid(row=1, column=0, padx=(20, 8), pady=(5, 15), sticky="w")

        self.load_volunteers_for_combobox()

        self.combo_volunteers = ctk.CTkComboBox(
            action_box,
            values=self.all_volunteer_display_values,
            width=330,
            height=35
        )
        self.combo_volunteers.grid(row=1, column=1, padx=8, pady=(5, 15), sticky="w")

        if self.all_volunteer_display_values:
            self.combo_volunteers.set(self.all_volunteer_display_values[0])
        else:
            self.combo_volunteers.set("No volunteers found")

        btn_add = ctk.CTkButton(
            action_box,
            text="➕ Add Volunteer",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#198754",
            hover_color="#146C43",
            width=150,
            height=35,
            corner_radius=6,
            command=self.add_selected_volunteer
        )
        btn_add.grid(row=0, column=2, padx=(20, 10), pady=(15, 5), sticky="w")

        # NEW: visible remove button near the add button
        btn_remove_top = ctk.CTkButton(
            action_box,
            text="🗑️ Remove Selected",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=160,
            height=35,
            corner_radius=6,
            command=self.delete_selected_assignment
        )
        btn_remove_top.grid(row=1, column=2, padx=(20, 10), pady=(5, 15), sticky="w")

        info_lbl = ctk.CTkLabel(
            action_box,
            text="Press Enter after searching to highlight the volunteer if already assigned.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        info_lbl.grid(row=0, column=3, rowspan=2, padx=(10, 20), pady=15, sticky="w")

        # ========================================================
        # TABLE CARD
        # ========================================================
        self.container_box = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.container_box.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        self.configure_tree_style()

        table_frame = ctk.CTkFrame(self.container_box, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        self.columns = (
            "training_id",
            "volunteer_id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "is_active"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.columns,
            show="headings"
        )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        headings = {
            "training_id": "Training ID",
            "volunteer_id": "Volunteer ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone_number": "Phone",
            "email": "Email",
            "is_active": "Active"
        }

        for col in self.columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=130, minwidth=90, anchor="center")

        self.tree.column("first_name", anchor="w")
        self.tree.column("last_name", anchor="w")
        self.tree.column("email", width=170, anchor="w")

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        # Highlight color when pressing Enter after search   #autre rose sumpa #FFD6E7
        self.tree.tag_configure("highlightrow", background="#F8D7DA")

        footer = ctk.CTkFrame(self.container_box, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(5, 15))

        btn_delete = ctk.CTkButton(
            footer,
            text="🗑️ Remove Selected Volunteer From This Training",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#DC3545",
            hover_color="#BD2130",
            width=290,
            height=35,
            corner_radius=6,
            command=self.delete_selected_assignment
        )
        btn_delete.pack(side="left")

        hint = ctk.CTkLabel(
            footer,
            text="💡 Select a row then click Remove Selected, or press Delete.",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        hint.pack(side="right")

        # Extra easy controls
        self.tree.bind("<Delete>", self.delete_selected_assignment)
        self.tree.bind("<Double-1>", self.delete_selected_assignment)

        self.load_assigned_volunteers()

    # ========================================================
    # STYLE + HELPERS
    # ========================================================
    def configure_tree_style(self):
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
        style.map(
            "Treeview",
            background=[("selected", "#1A62E8")],
            foreground=[("selected", "#FFFFFF")]
        )

    def q(self, identifier):
        return '"' + identifier.replace('"', '""') + '"'

    # ========================================================
    # LOAD VOLUNTEERS FOR COMBOBOX
    # ========================================================
    def load_volunteers_for_combobox(self):
        try:
            cursor = self.conn.cursor()

            cursor.execute(
                """
                SELECT volunteer_id, first_name, last_name
                FROM public.a_volunteer
                ORDER BY volunteer_id;
                """
            )

            rows = cursor.fetchall()
            cursor.close()

            self.volunteer_map.clear()
            self.all_volunteer_display_values.clear()

            for volunteer_id, first_name, last_name in rows:
                display = f"{volunteer_id} - {first_name} {last_name}"
                self.all_volunteer_display_values.append(display)
                self.volunteer_map[display] = volunteer_id

        except Exception as e:
            messagebox.showerror(
                "SQL Database Error",
                f"Failed to load volunteers from a_volunteer:\n{e}",
                parent=self
            )

    # ========================================================
    # DYNAMIC SEARCH FILTER
    # ========================================================
    def filter_volunteers_combobox(self, event=None):
        search_text = self.entry_search.get().strip().lower()

        if not search_text:
            filtered_values = self.all_volunteer_display_values
        else:
            filtered_values = [
                display
                for display in self.all_volunteer_display_values
                if search_text in display.lower()
            ]

        if filtered_values:
            self.combo_volunteers.configure(values=filtered_values)
            self.combo_volunteers.set(filtered_values[0])
        else:
            self.combo_volunteers.configure(values=[])
            self.combo_volunteers.set("No matching volunteers")

    # ========================================================
    # ENTER SEARCH: HIGHLIGHT ASSIGNED VOLUNTEER ROW
    # ========================================================
    def highlight_assigned_volunteer_from_search(self, event=None):
        search_text = self.entry_search.get().strip().lower()

        if not search_text:
            messagebox.showinfo(
                "Search Empty",
                "Type a volunteer ID, first name, or last name first.",
                parent=self
            )
            return

        found_item = None

        # reset row colors before highlighting
        for index, item in enumerate(self.tree.get_children()):
            normal_tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(normal_tag,))

        for item in self.tree.get_children():
            values = self.tree.item(item, "values")

            volunteer_id = str(values[1]).lower()
            first_name = str(values[2]).lower()
            last_name = str(values[3]).lower()
            full_name = f"{first_name} {last_name}"

            if (
                volunteer_id.startswith(search_text)
                or first_name.startswith(search_text)
                or last_name.startswith(search_text)
                or search_text in full_name
            ):
                found_item = item
                break

        if found_item:
            self.tree.item(found_item, tags=("highlightrow",))
            self.tree.selection_set(found_item)
            self.tree.focus(found_item)
            self.tree.see(found_item)
        else:
            messagebox.showinfo(
                "Not Found",
                "This volunteer was not found in the assigned volunteers list for this training.",
                parent=self
            )

    # ========================================================
    # LOAD ASSIGNED VOLUNTEERS
    # ========================================================
    def load_assigned_volunteers(self):
        try:
            cursor = self.conn.cursor()

            sql = f"""
                SELECT vt.{self.q(self.training_id_column)},
                       vt.{self.q(self.volunteer_id_column)},
                       v.first_name,
                       v.last_name,
                       v.phone_number,
                       v.email,
                       v.is_active
                FROM public.{self.q(self.volunteer_training_table)} vt
                JOIN public.a_volunteer v
                    ON v.volunteer_id = vt.{self.q(self.volunteer_id_column)}
                WHERE vt.{self.q(self.training_id_column)} = %s
                ORDER BY vt.{self.q(self.volunteer_id_column)};
            """

            cursor.execute(sql, (self.training_id,))
            rows = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))

            cursor.close()

        except Exception as e:
            messagebox.showerror(
                "SQL Database Error",
                f"Failed to load assigned volunteers:\n{e}",
                parent=self
            )

    # ========================================================
    # ADD VOLUNTEER TO TRAINING
    # ========================================================
    def add_selected_volunteer(self):
        selected = self.combo_volunteers.get()

        if (
            not selected
            or selected == "No volunteers found"
            or selected == "No matching volunteers"
        ):
            messagebox.showwarning(
                "Selection Missing",
                "Please select a valid volunteer from the list.",
                parent=self
            )
            return

        volunteer_id = self.volunteer_map.get(selected)

        if volunteer_id is None:
            messagebox.showwarning(
                "Invalid Selection",
                "The selected volunteer could not be found.",
                parent=self
            )
            return

        try:
            cursor = self.conn.cursor()

            sql = f"""
                INSERT INTO public.{self.q(self.volunteer_training_table)}
                    ({self.q(self.training_id_column)}, {self.q(self.volunteer_id_column)})
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM public.{self.q(self.volunteer_training_table)}
                    WHERE {self.q(self.training_id_column)} = %s
                      AND {self.q(self.volunteer_id_column)} = %s
                );
            """

            cursor.execute(
                sql,
                (self.training_id, volunteer_id, self.training_id, volunteer_id)
            )

            inserted_count = cursor.rowcount

            self.conn.commit()
            cursor.close()

            if inserted_count == 0:
                messagebox.showinfo(
                    "Already Assigned",
                    "This volunteer is already assigned to this training.",
                    parent=self
                )
            else:
                messagebox.showinfo(
                    "Success",
                    "Volunteer assigned to training successfully.",
                    parent=self
                )

            self.load_assigned_volunteers()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror(
                "SQL Transaction Error",
                f"Failed to assign volunteer to training:\n{e}",
                parent=self
            )

    # ========================================================
    # DELETE VOLUNTEER FROM THIS TRAINING ONLY
    # ========================================================
    def delete_selected_assignment(self, event=None):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "Selection Missing",
                "Please select a volunteer assignment to remove.",
                parent=self
            )
            return

        values = self.tree.item(selected_item, "values")

        training_id = values[0]
        volunteer_id = values[1]
        volunteer_name = f"{values[2]} {values[3]}"

        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"""Remove volunteer {volunteer_name} from Training #{training_id}?

This will only delete the association from b_volunteer_training.
The volunteer will stay in a_volunteer.""",
            parent=self
        )

        if not confirm:
            return

        try:
            cursor = self.conn.cursor()

            sql = f"""
                DELETE FROM public.{self.q(self.volunteer_training_table)}
                WHERE {self.q(self.training_id_column)} = %s
                  AND {self.q(self.volunteer_id_column)} = %s;
            """

            cursor.execute(sql, (training_id, volunteer_id))

            self.conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Success",
                "Volunteer removed from this training successfully.",
                parent=self
            )

            self.load_assigned_volunteers()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror(
                "SQL Transaction Error",
                f"Failed to remove volunteer assignment:\n{e}",
                parent=self
            )