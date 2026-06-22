import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime


class ReportsProceduresScreen(ctk.CTkFrame):
    """
    Reports & Procedures screen for Stage E.

    Purpose:
    - Run analytical SELECT queries from Stage B.
    - Run database function/procedure from Stage D.
    - Display all results in a user-friendly table.
    """

    PLACEHOLDER_FROM = "YYYY-MM-DD"
    PLACEHOLDER_TO = "YYYY-MM-DD"

    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")
        self.conn = db_connection

        self._build_header()
        self._build_main_layout()
        self._build_results_table()

        self.show_welcome_message()

    # ========================================================
    # UI BUILDERS
    # ========================================================
    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 15))

        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.pack(side="left", fill="x", expand=True)

        title = ctk.CTkLabel(
            title_box,
            text="📈 Reports & Database Procedures",
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Stage B analytical queries + Stage D database function/procedure",
            font=ctk.CTkFont(size=12),
            text_color="#6C757D"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

    def _build_main_layout(self):
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True)

        self.body.grid_columnconfigure(0, weight=0)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        self.actions_panel = ctk.CTkScrollableFrame(
            self.body,
            width=315,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.actions_panel.grid(row=0, column=0, sticky="ns", padx=(0, 14))

        self.results_panel = ctk.CTkFrame(
            self.body,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.results_panel.grid(row=0, column=1, sticky="nsew")
        self.results_panel.grid_rowconfigure(2, weight=1)
        self.results_panel.grid_columnconfigure(0, weight=1)

        self._build_stage_b_section()
        self._build_stage_d_section()
        self._build_trigger_note_section()

    def _section_title(self, text):
        lbl = ctk.CTkLabel(
            self.actions_panel,
            text=text,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#212529"
        )
        lbl.pack(anchor="w", padx=18, pady=(18, 8))
        return lbl

    def _action_button(self, text, command, color="#1A62E8", hover="#1452C7"):
        btn = ctk.CTkButton(
            self.actions_panel,
            text=text,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=color,
            hover_color=hover,
            height=38,
            corner_radius=8,
            anchor="w",
            command=command
        )
        btn.pack(fill="x", padx=18, pady=5)
        return btn

    def _build_stage_b_section(self):
        self._section_title("🔎 Stage B Queries")

        self._action_button(
            "Top 15 Families by Requests",
            self.run_top_families_query
        )

        self._action_button(
            "Monthly Requests Summary",
            self.run_monthly_requests_summary
        )

        self._action_button(
            "Top Volunteers Above Average",
            self.run_top_volunteers_above_average
        )

        date_box = ctk.CTkFrame(self.actions_panel, fg_color="#F8F9FA", corner_radius=10)
        date_box.pack(fill="x", padx=18, pady=(10, 6))

        date_title = ctk.CTkLabel(
            date_box,
            text="Treatments by Date Range",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#495057"
        )
        date_title.pack(anchor="w", padx=12, pady=(10, 4))

        self.entry_from_date = ctk.CTkEntry(date_box, height=32, placeholder_text="From: YYYY-MM-DD")
        self.entry_from_date.pack(fill="x", padx=12, pady=4)
        self.entry_from_date.insert(0, "2026-03-01")

        self.entry_to_date = ctk.CTkEntry(date_box, height=32, placeholder_text="To: YYYY-MM-DD")
        self.entry_to_date.pack(fill="x", padx=12, pady=4)
        self.entry_to_date.insert(0, "2026-03-31")

        run_date_btn = ctk.CTkButton(
            date_box,
            text="Run Date Range Query",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0F4C81",
            hover_color="#0B3A63",
            height=34,
            corner_radius=7,
            command=self.run_treatments_by_date_range
        )
        run_date_btn.pack(fill="x", padx=12, pady=(6, 12))

    def _build_stage_d_section(self):
        self._section_title("⚙️ Stage D Function / Procedure")

        self._action_button(
            "Show Blocked Busy Volunteers",
            self.run_busy_without_active_treatment_function,
            color="#6F42C1",
            hover="#5A32A3"
        )

        self._action_button(
            "Reset Volunteer Availability",
            self.run_reset_volunteer_availability_procedure,
            color="#198754",
            hover="#146C43"
        )

    def _build_trigger_note_section(self):
        note = ctk.CTkFrame(self.actions_panel, fg_color="#FFF3CD", corner_radius=10)
        note.pack(fill="x", padx=18, pady=(18, 18))

        title = ctk.CTkLabel(
            note,
            text="🔔 Trigger Demonstration",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7A5B00"
        )
        title.pack(anchor="w", padx=12, pady=(10, 2))

        body = ctk.CTkLabel(
            note,
            text=(
                "The trigger trg_treatment_status_sync runs automatically "
                "when a treatment is inserted or when completion_time is updated.\n\n"
                "Demo: create or complete a treatment in the Treatments / Dispatch screen, "
                "then check the volunteer availability here."
            ),
            font=ctk.CTkFont(size=11),
            text_color="#7A5B00",
            justify="left",
            wraplength=255
        )
        body.pack(anchor="w", padx=12, pady=(0, 12))

    def _build_results_table(self):
        self.result_title = ctk.CTkLabel(
            self.results_panel,
            text="Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#212529"
        )
        self.result_title.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 2))

        self.result_subtitle = ctk.CTkLabel(
            self.results_panel,
            text="Choose an action on the left panel.",
            font=ctk.CTkFont(size=12),
            text_color="#6C757D",
            justify="left",
            wraplength=650
        )
        self.result_subtitle.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 10))

        table_holder = ctk.CTkFrame(self.results_panel, fg_color="transparent")
        table_holder.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 12))
        table_holder.grid_rowconfigure(0, weight=1)
        table_holder.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Reports.Treeview",
            background="#FFFFFF",
            foreground="#212529",
            rowheight=36,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 11),
            borderwidth=0
        )
        style.configure(
            "Reports.Treeview.Heading",
            background="#F1F3F5",
            foreground="#495057",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0
        )
        style.map(
            "Reports.Treeview",
            background=[("selected", "#E6F2FF")],
            foreground=[("selected", "#1A62E8")]
        )

        self.tree = ttk.Treeview(
            table_holder,
            columns=("message",),
            show="headings",
            style="Reports.Treeview"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_holder, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.tag_configure("evenrow", background="#FFFFFF")
        self.tree.tag_configure("oddrow", background="#F8F9FA")

        self.footer_label = ctk.CTkLabel(
            self.results_panel,
            text="0 row(s)",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D"
        )
        self.footer_label.grid(row=3, column=0, sticky="e", padx=18, pady=(0, 12))

    # ========================================================
    # GENERAL HELPERS
    # ========================================================
    def show_welcome_message(self):
        self.display_results(
            title="Reports & Procedures Center",
            subtitle=(
                "This screen was created for Stage E. It runs selected Stage B analytical queries "
                "and Stage D database subprograms directly from the graphical interface."
            ),
            columns=[("message", "Available Actions")],
            rows=[
                ("Stage B: Top 15 Families by Requests",),
                ("Stage B: Monthly Requests Summary",),
                ("Stage B: Top Volunteers Above Average",),
                ("Stage B: Treatments by Date Range",),
                ("Stage D Function: get_busy_volunteers_with_no_active_treatment()",),
                ("Stage D Procedure: reset_volunteer_availability()",),
                ("Stage D Trigger: trg_treatment_status_sync is demonstrated through Treatments/Dispatch",),
            ]
        )

    def display_results(self, title, subtitle, columns, rows):
        self.result_title.configure(text=title)
        self.result_subtitle.configure(text=subtitle)

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = [col_key for col_key, _ in columns]

        for col_key, col_title in columns:
            self.tree.heading(col_key, text=col_title, anchor="center")
            width = 150
            if "name" in col_key.lower() or "message" in col_key.lower():
                width = 260
            if "description" in col_key.lower() or "feedback" in col_key.lower():
                width = 330
            self.tree.column(col_key, width=width, anchor="center")

        for i, row in enumerate(rows):
            clean_row = tuple("" if value is None else str(value) for value in row)
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=clean_row, tags=(tag,))

        self.footer_label.configure(text=f"{len(rows)} row(s)")

    def execute_select_query(self, query, params, title, subtitle, columns):
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection available.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            cursor.close()
            self.conn.commit()
            self.display_results(title, subtitle, columns, rows)
        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("SQL Error", f"Failed to run query:\n{e}")

    def validate_date(self, date_text, field_name):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showwarning("Invalid Date", f"{field_name} must be in YYYY-MM-DD format.")
            return False

    # ========================================================
    # STAGE B QUERIES
    # ========================================================
    def run_top_families_query(self):
        query = """
            SELECT
                f.contactperson_name AS family_contact,
                COUNT(r.request_id) AS total_requests
            FROM public.a_family f
            JOIN public.a_request r
                ON f.contactperson_id = r.contactperson_id
            GROUP BY f.contactperson_id, f.contactperson_name
            ORDER BY total_requests DESC
            LIMIT 15;
        """
        self.execute_select_query(
            query=query,
            params=None,
            title="Top 15 Families by Number of Requests",
            subtitle="Stage B query using JOIN between a_family and a_request. Foreign key IDs are replaced by the family contact name.",
            columns=[("family_contact", "Family Contact"), ("total_requests", "Total Requests")]
        )

    def run_monthly_requests_summary(self):
        query = """
            SELECT
                TRIM(TO_CHAR(date, 'Month')) AS month_name,
                EXTRACT(YEAR FROM date)::INT AS year_nb,
                COUNT(*) AS nb_requests
            FROM public.a_request
            GROUP BY year_nb, month_name, EXTRACT(MONTH FROM date)
            ORDER BY year_nb DESC, EXTRACT(MONTH FROM date) DESC;
        """
        self.execute_select_query(
            query=query,
            params=None,
            title="Monthly Requests Summary",
            subtitle="Stage B query summarizing requests by month and year.",
            columns=[("month_name", "Month"), ("year_nb", "Year"), ("nb_requests", "Requests")]
        )

    def run_top_volunteers_above_average(self):
        query = """
            SELECT
                first_name || ' ' || last_name AS volunteer_name,
                counter
            FROM public.a_volunteer
            WHERE counter > (SELECT AVG(counter) FROM public.a_volunteer)
            ORDER BY counter DESC, volunteer_name ASC;
        """
        self.execute_select_query(
            query=query,
            params=None,
            title="Top Performing Volunteers Above Average",
            subtitle="Stage B query showing volunteers whose activity counter is above the global average.",
            columns=[("volunteer_name", "Volunteer"), ("counter", "Completed Missions")]
        )

    def run_treatments_by_date_range(self):
        from_date = self.entry_from_date.get().strip()
        to_date = self.entry_to_date.get().strip()

        if not self.validate_date(from_date, "From date"):
            return
        if not self.validate_date(to_date, "To date"):
            return
        if from_date > to_date:
            messagebox.showwarning("Invalid Range", "From date cannot be later than To date.")
            return

        query = """
            SELECT
                t.date,
                v.first_name || ' ' || v.last_name AS volunteer_name,
                COALESCE(r.incident_description, 'No description') AS request_description,
                COALESCE(t.feedback_notes, '') AS feedback_notes
            FROM public.a_treatment t
            LEFT JOIN public.a_volunteer v
                ON v.volunteer_id = t.volunteer_id
            LEFT JOIN public.a_request r
                ON r.request_id = t.request_id
            WHERE t.date BETWEEN %s AND %s
            ORDER BY t.date ASC, volunteer_name ASC;
        """
        self.execute_select_query(
            query=query,
            params=(from_date, to_date),
            title="Filtered Treatments by Date Range",
            subtitle="Stage B query adapted with JOINs, showing volunteer names and request descriptions instead of IDs.",
            columns=[
                ("date", "Date"),
                ("volunteer_name", "Volunteer"),
                ("request_description", "Request"),
                ("feedback_notes", "Feedback")
            ]
        )

    # ========================================================
    # STAGE D FUNCTION / PROCEDURE
    # ========================================================
    def run_busy_without_active_treatment_function(self):
        """Runs get_busy_volunteers_with_no_active_treatment(), which returns a REFCURSOR."""
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection available.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT public.get_busy_volunteers_with_no_active_treatment();")
            cursor_name = cursor.fetchone()[0]

            # The cursor name is created by our own function, but we still quote it safely.
            safe_cursor_name = str(cursor_name).replace('"', '')
            cursor.execute(f'FETCH ALL FROM "{safe_cursor_name}";')
            rows = cursor.fetchall()
            cursor.execute(f'CLOSE "{safe_cursor_name}";')

            cursor.close()
            self.conn.commit()

            self.display_results(
                title="Busy Volunteers With No Active Treatment",
                subtitle=(
                    "Stage D function: get_busy_volunteers_with_no_active_treatment(). "
                    "It finds volunteers marked as busy although they do not have an active treatment."
                ),
                columns=[
                    ("volunteer_id", "Volunteer ID"),
                    ("first_name", "First Name"),
                    ("last_name", "Last Name"),
                    ("is_active", "Busy Flag")
                ],
                rows=rows
            )

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Function Error", f"Failed to execute Stage D function:\n{e}")

    def run_reset_volunteer_availability_procedure(self):
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection available.")
            return

        confirm = messagebox.askyesno(
            "Confirm Procedure Execution",
            "This will run reset_volunteer_availability() and set inconsistent busy volunteers back to available.\n\nContinue?"
        )
        if not confirm:
            return

        try:
            # Clear old server notices before running the procedure.
            try:
                self.conn.notices.clear()
            except Exception:
                pass

            cursor = self.conn.cursor()
            cursor.execute("CALL public.reset_volunteer_availability();")
            cursor.close()
            self.conn.commit()

            notices = [notice.strip() for notice in getattr(self.conn, "notices", []) if notice.strip()]
            rows = [(notice,) for notice in notices] if notices else [("Procedure completed successfully. No PostgreSQL notices were returned.",)]

            self.display_results(
                title="Reset Volunteer Availability Procedure",
                subtitle="Stage D procedure: reset_volunteer_availability(). It calls the cursor function and corrects blocked volunteers.",
                columns=[("notice", "PostgreSQL Notice / Result")],
                rows=rows
            )

            messagebox.showinfo("Procedure Completed", "Volunteer availability reset procedure completed successfully.")

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Procedure Error", f"Failed to execute Stage D procedure:\n{e}")
