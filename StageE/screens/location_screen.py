import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import math
from datetime import datetime

try:
    from tkintermapview import TkinterMapView
    MAP_AVAILABLE = True
except Exception:
    MAP_AVAILABLE = False


class LocationScreen(ctk.CTkFrame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, fg_color="transparent")

        self.conn = db_connection
        self.all_rows = []
        self.filtered_rows = []
        self.selected_row = None
        self.selected_card = None
        self.map_markers = []

        # ========================================================
        # HEADER
        # ========================================================
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", pady=(0, 15))

        title_box = ctk.CTkFrame(self.header, fg_color="transparent")
        title_box.pack(side="left")

        title = ctk.CTkLabel(
            title_box,
            text="📍 Dispatch & Location Center",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#0F4C81"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Live map of volunteers currently assigned to active treatments",
            font=ctk.CTkFont(size=12),
            text_color="#6C757D"
        )
        subtitle.pack(anchor="w")

        btn_refresh = ctk.CTkButton(
            self.header,
            text="🔄 Refresh",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1A62E8",
            hover_color="#1452C7",
            height=38,
            width=120,
            corner_radius=8,
            command=self.load_active_missions_from_db
        )
        btn_refresh.pack(side="right", padx=(8, 0))

        btn_route = ctk.CTkButton(
            self.header,
            text="🧭 Open Route",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#198754",
            hover_color="#146C43",
            height=38,
            width=135,
            corner_radius=8,
            command=self.open_route_for_selected
        )
        btn_route.pack(side="right", padx=(8, 0))

        # ========================================================
        # MAIN LAYOUT
        # ========================================================
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(fill="both", expand=True)

        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(1, weight=4)
        self.main_area.grid_rowconfigure(0, weight=1)

        # ========================================================
        # LEFT PANEL
        # ========================================================
        self.left_panel = ctk.CTkFrame(
            self.main_area,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        left_title = ctk.CTkLabel(
            self.left_panel,
            text="🚑 Active Missions",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#212529"
        )
        left_title.pack(anchor="w", padx=18, pady=(16, 4))

        self.stats_label = ctk.CTkLabel(
            self.left_panel,
            text="Loading missions...",
            font=ctk.CTkFont(size=11),
            text_color="#6C757D"
        )
        self.stats_label.pack(anchor="w", padx=18, pady=(0, 12))

        # Search
        self.search_entry = ctk.CTkEntry(
            self.left_panel,
            width=260,
            height=34,
            placeholder_text="Search volunteer / request..."
        )
        self.search_entry.pack(fill="x", padx=18, pady=(0, 8))
        self.search_entry.bind("<KeyRelease>", self.apply_filters)
        self.search_entry.bind("<Return>", self.select_first_visible_card)

        # Filters
        self.priority_filter = ctk.CTkComboBox(
            self.left_panel,
            values=["All priorities", "Critical >= 4", "Normal <= 3"],
            height=34,
            command=lambda value: self.apply_filters()
        )
        self.priority_filter.pack(fill="x", padx=18, pady=(0, 8))
        self.priority_filter.set("All priorities")

        self.long_only_var = ctk.BooleanVar(value=False)
        self.long_check = ctk.CTkCheckBox(
            self.left_panel,
            text="Only long treatments > 60 min",
            variable=self.long_only_var,
            command=self.apply_filters,
            text_color="#495057"
        )
        self.long_check.pack(anchor="w", padx=18, pady=(2, 8))

        self.missing_only_var = ctk.BooleanVar(value=False)
        self.missing_check = ctk.CTkCheckBox(
            self.left_panel,
            text="Only missing coordinates",
            variable=self.missing_only_var,
            command=self.apply_filters,
            text_color="#495057"
        )
        self.missing_check.pack(anchor="w", padx=18, pady=(0, 12))

        # Mission cards list
        self.cards_frame = ctk.CTkScrollableFrame(
            self.left_panel,
            fg_color="#F8F9FA",
            corner_radius=10
        )
        self.cards_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Bottom buttons
        self.left_buttons = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.left_buttons.pack(fill="x", padx=18, pady=(0, 16))

        btn_vol = ctk.CTkButton(
            self.left_buttons,
            text="👷 Volunteer",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0F4C81",
            hover_color="#0B3A63",
            height=34,
            corner_radius=7,
            command=self.open_volunteer_location_for_selected
        )
        btn_vol.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_req = ctk.CTkButton(
            self.left_buttons,
            text="🚨 Request",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6F42C1",
            hover_color="#5A32A3",
            height=34,
            corner_radius=7,
            command=self.open_request_location_for_selected
        )
        btn_req.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # ========================================================
        # RIGHT MAP PANEL
        # ========================================================
        self.map_panel = ctk.CTkFrame(
            self.main_area,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color="#E9ECEF"
        )
        self.map_panel.grid(row=0, column=1, sticky="nsew")

        self.map_header = ctk.CTkFrame(self.map_panel, fg_color="transparent")
        self.map_header.pack(fill="x", padx=18, pady=(16, 8))

        map_title = ctk.CTkLabel(
            self.map_header,
            text="🗺️ Israel Live Mission Map",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#212529"
        )
        map_title.pack(side="left")

        self.selected_info_label = ctk.CTkLabel(
            self.map_header,
            text="Select a mission to focus the map",
            font=ctk.CTkFont(size=12),
            text_color="#6C757D"
        )
        self.selected_info_label.pack(side="right")

        if MAP_AVAILABLE:
            self.map_widget = TkinterMapView(
                self.map_panel,
                corner_radius=10
            )
            self.map_widget.pack(fill="both", expand=True, padx=18, pady=(0, 18))

            # Center on Israel
            self.map_widget.set_position(31.7683, 35.2137)
            self.map_widget.set_zoom(8)
        else:
            self.map_widget = None

            fallback = ctk.CTkFrame(
                self.map_panel,
                fg_color="#FFF8E1",
                corner_radius=12,
                border_width=1,
                border_color="#FFE082"
            )
            fallback.pack(fill="both", expand=True, padx=18, pady=(0, 18))

            fallback_msg = ctk.CTkLabel(
                fallback,
                text=(
                    "Map module is not installed.\n\n"
                    "Install it with:\n"
                    "pip install tkintermapview\n\n"
                    "The mission list and Google Maps buttons still work."
                ),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color="#7A5B00",
                justify="center"
            )
            fallback_msg.pack(expand=True)

        self.load_active_missions_from_db()

    # ========================================================
    # DB LOAD
    # ========================================================
    def load_active_missions_from_db(self):
        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()

            query = """
                SELECT 
                    t.treatment_id,
                    t.request_id,
                    t.volunteer_id,
                    t.date,
                    t.start_time,
                    t.completion_time,

                    v.first_name,
                    v.last_name,
                    v.phone_number,
                    v.latitude AS volunteer_latitude,
                    v.longitude AS volunteer_longitude,

                    r.incident_description,
                    r.prioriry_level,
                    r.status_id,
                    r.latitude AS request_latitude,
                    r.longitude AS request_longitude

                FROM public.a_treatment t
                JOIN public.a_volunteer v
                    ON v.volunteer_id = t.volunteer_id
                JOIN public.a_request r
                    ON r.request_id = t.request_id
                WHERE t.completion_time IS NULL
                ORDER BY r.prioriry_level DESC, t.start_time ASC;
            """

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            self.all_rows.clear()

            for row in rows:
                (
                    treatment_id,
                    request_id,
                    volunteer_id,
                    treatment_date,
                    start_time,
                    completion_time,
                    first_name,
                    last_name,
                    phone_number,
                    volunteer_lat,
                    volunteer_lon,
                    incident_description,
                    priority,
                    status_id,
                    request_lat,
                    request_lon
                ) = row

                volunteer_lat = self.safe_float(volunteer_lat)
                volunteer_lon = self.safe_float(volunteer_lon)
                request_lat = self.safe_float(request_lat)
                request_lon = self.safe_float(request_lon)

                distance = self.haversine_km(
                    volunteer_lat,
                    volunteer_lon,
                    request_lat,
                    request_lon
                )

                duration = self.calculate_duration_minutes(treatment_date,start_time)

                self.all_rows.append({
                    "treatment_id": treatment_id,
                    "request_id": request_id,
                    "volunteer_id": volunteer_id,
                    "start_time": start_time,
                    "volunteer_name": f"{first_name} {last_name}",
                    "phone_number": phone_number,
                    "volunteer_lat": volunteer_lat,
                    "volunteer_lon": volunteer_lon,
                    "description": incident_description,
                    "priority": priority,
                    "status_id": status_id,
                    "request_lat": request_lat,
                    "request_lon": request_lon,
                    "duration_min": duration,
                    "distance_km": distance
                })

            self.selected_row = None
            self.selected_card = None
            self.apply_filters()

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "SQL Database Error",
                f"Failed to load active missions:\n{e}"
            )

    # ========================================================
    # FILTERS
    # ========================================================
    def apply_filters(self, event=None):
        search = self.search_entry.get().strip().lower()
        priority_mode = self.priority_filter.get()
        long_only = self.long_only_var.get()
        missing_only = self.missing_only_var.get()

        result = []

        for row in self.all_rows:
            text_blob = (
                f"{row['treatment_id']} "
                f"{row['request_id']} "
                f"{row['volunteer_id']} "
                f"{row['volunteer_name']} "
                f"{row['phone_number']} "
                f"{row['description']}"
            ).lower()

            if search and search not in text_blob:
                continue

            priority = int(row["priority"]) if row["priority"] is not None else 0

            if priority_mode == "Critical >= 4" and priority < 4:
                continue

            if priority_mode == "Normal <= 3" and priority > 3:
                continue

            if long_only:
                duration = row["duration_min"]
                if duration is None or duration <= 60:
                    continue

            missing_coords = self.has_missing_coordinates(row)

            if missing_only and not missing_coords:
                continue

            result.append(row)

        self.filtered_rows = result
        self.render_cards()
        self.render_map()

    # ========================================================
    # RENDER CARDS
    # ========================================================
    def render_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        total = len(self.all_rows)
        shown = len(self.filtered_rows)

        critical = sum(
            1 for row in self.all_rows
            if row["priority"] is not None and int(row["priority"]) >= 4
        )

        missing = sum(
            1 for row in self.all_rows
            if self.has_missing_coordinates(row)
        )

        self.stats_label.configure(
            text=f"{shown}/{total} shown  •  Critical: {critical}  •  Missing coords: {missing}"
        )

        if not self.filtered_rows:
            empty = ctk.CTkLabel(
                self.cards_frame,
                text="No active missions match your filters.",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="#6C757D"
            )
            empty.pack(pady=25)
            return

        for row in self.filtered_rows:
            self.create_mission_card(row)

    def create_mission_card(self, row):
        priority = int(row["priority"]) if row["priority"] is not None else 0
        duration = row["duration_min"]
        distance = row["distance_km"]

        if self.has_missing_coordinates(row):
            border_color = "#ADB5BD"
            status_text = "Missing coordinates"
            status_color = "#6C757D"
            icon = "⚠️"
        elif priority >= 4:
            border_color = "#F5A3A3"
            status_text = f"Critical priority {priority}"
            status_color = "#DC3545"
            icon = "🚨"
        elif duration is not None and duration > 60:
            border_color = "#FFD166"
            status_text = "Long treatment"
            status_color = "#B7791F"
            icon = "⏱️"
        else:
            border_color = "#B7E4C7"
            status_text = "Active"
            status_color = "#198754"
            icon = "👷"

        card = ctk.CTkFrame(
            self.cards_frame,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=2,
            border_color=border_color
        )
        card.pack(fill="x", padx=5, pady=6)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(10, 2))

        name = ctk.CTkLabel(
            top,
            text=f"{icon} {row['volunteer_name']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#212529"
        )
        name.pack(side="left")

        status = ctk.CTkLabel(
            top,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        )
        status.pack(side="right")

        details_text = (
            f"Treatment #{row['treatment_id']}  •  Request #{row['request_id']}\n"
            f"Phone: {row['phone_number']}\n"
            f"Duration: {self.format_duration(duration)}  •  Distance: {self.format_distance(distance)}"
        )

        details = ctk.CTkLabel(
            card,
            text=details_text,
            font=ctk.CTkFont(size=11),
            text_color="#495057",
            justify="left"
        )
        details.pack(anchor="w", padx=12, pady=(2, 6))

        desc = row["description"] if row["description"] else "No description"
        if len(desc) > 75:
            desc = desc[:75] + "..."

        desc_label = ctk.CTkLabel(
            card,
            text=f"“{desc}”",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#6C757D",
            justify="left",
            wraplength=260
        )
        desc_label.pack(anchor="w", padx=12, pady=(0, 10))

        # Click handlers
        card.bind("<Button-1>", lambda event, r=row, c=card: self.select_mission(r, c))
        top.bind("<Button-1>", lambda event, r=row, c=card: self.select_mission(r, c))
        name.bind("<Button-1>", lambda event, r=row, c=card: self.select_mission(r, c))
        details.bind("<Button-1>", lambda event, r=row, c=card: self.select_mission(r, c))
        desc_label.bind("<Button-1>", lambda event, r=row, c=card: self.select_mission(r, c))

    # ========================================================
    # SELECT MISSION
    # ========================================================
    def select_mission(self, row, card=None):
        if self.selected_card and self.selected_card.winfo_exists():
            self.selected_card.configure(border_width=2)

        self.selected_row = row
        self.selected_card = card

        if card:
            card.configure(border_width=4, border_color="#FF7A00")

        self.selected_info_label.configure(
            text=f"Selected: {row['volunteer_name']} → Request #{row['request_id']}"
        )

        self.focus_map_on_row(row)

    def select_first_visible_card(self, event=None):
        if not self.filtered_rows:
            return

        first_row = self.filtered_rows[0]
        self.selected_row = first_row
        self.selected_info_label.configure(
            text=f"Selected: {first_row['volunteer_name']} → Request #{first_row['request_id']}"
        )
        self.focus_map_on_row(first_row)

    # ========================================================
    # MAP
    # ========================================================
    def render_map(self):
        if not self.map_widget:
            return

        self.clear_map_markers()

        valid_points = []

        for row in self.filtered_rows:
            v_lat = row["volunteer_lat"]
            v_lon = row["volunteer_lon"]
            r_lat = row["request_lat"]
            r_lon = row["request_lon"]

            if v_lat is not None and v_lon is not None:
                marker = self.map_widget.set_marker(
                    v_lat,
                    v_lon,
                    text=f"👷 {row['volunteer_name']}",
                    command=lambda marker, r=row: self.open_call_popup_from_map(r)
                )
                self.map_markers.append(marker)
                valid_points.append((v_lat, v_lon))
            #if r_lat is not None and r_lon is not None:
               # marker = self.map_widget.set_marker(
                 #   r_lat,
                   # r_lon,
                   # text=f"🚨 Request #{row['request_id']}\nPriority {row['priority']}"
              #  )

        if valid_points:
            avg_lat = sum(p[0] for p in valid_points) / len(valid_points)
            avg_lon = sum(p[1] for p in valid_points) / len(valid_points)
            self.map_widget.set_position(avg_lat, avg_lon)
            self.map_widget.set_zoom(10)
        else:
            self.map_widget.set_position(31.7683, 35.2137)
            self.map_widget.set_zoom(8)

    def clear_map_markers(self):
        if not self.map_widget:
            return

        for marker in self.map_markers:
            try:
                marker.delete()
            except Exception:
                pass

        self.map_markers.clear()

    def focus_map_on_row(self, row):
        if not self.map_widget or not row:
            return

        v_lat = row["volunteer_lat"]
        v_lon = row["volunteer_lon"]

        if v_lat is not None and v_lon is not None:
            self.map_widget.set_position(v_lat, v_lon)
            self.map_widget.set_zoom(15)

    # ========================================================
    # MAP CALL ACTION
    # ========================================================
    def open_call_popup_from_map(self, row):
        self.selected_row = row

        phone = row.get("phone_number")
        volunteer_name = row.get("volunteer_name", "Volunteer")

        if not phone:
            messagebox.showwarning(
                "Missing Phone Number",
                f"No phone number found for {volunteer_name}."
            )
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Call Volunteer")
        popup.geometry("320x190")
        popup.resizable(False, False)
        popup.grab_set()

        title = ctk.CTkLabel(
            popup,
            text="📞 Call Volunteer",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#DC3545"
        )
        title.pack(pady=(18, 8))

        info = ctk.CTkLabel(
            popup,
            text=f"{volunteer_name}\nPhone: {phone}",
            font=ctk.CTkFont(size=13),
            text_color="#212529",
            justify="center"
        )
        info.pack(pady=(0, 16))

        buttons = ctk.CTkFrame(popup, fg_color="transparent")
        buttons.pack(fill="x", padx=20)

        call_btn = ctk.CTkButton(
            buttons,
            text="📞 Call",
            fg_color="#DC3545",
            hover_color="#B02A37",
            height=36,
            command=lambda: self.call_phone_number(phone)
        )
        call_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))

        close_btn = ctk.CTkButton(
            buttons,
            text="Cancel",
            fg_color="#6C757D",
            hover_color="#5C636A",
            height=36,
            command=popup.destroy
        )
        close_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))

    def call_phone_number(self, phone):
        if not phone:
            messagebox.showwarning("Missing Phone Number", "No phone number available.")
            return

        clean_phone = str(phone).replace(" ", "").replace("-", "")
        webbrowser.open(f"tel:{clean_phone}")

    # ========================================================
    # GOOGLE MAPS ACTIONS
    # ========================================================
    def open_volunteer_location_for_selected(self):
        if not self.selected_row:
            messagebox.showwarning("Selection Missing", "Please select a mission first.")
            return

        self.open_google_maps_point(
            self.selected_row["volunteer_lat"],
            self.selected_row["volunteer_lon"]
        )

    def open_request_location_for_selected(self):
        if not self.selected_row:
            messagebox.showwarning("Selection Missing", "Please select a mission first.")
            return

        self.open_google_maps_point(
            self.selected_row["request_lat"],
            self.selected_row["request_lon"]
        )

    def open_route_for_selected(self):
        if not self.selected_row:
            messagebox.showwarning("Selection Missing", "Please select a mission first.")
            return

        row = self.selected_row

        self.open_google_maps_route(
            row["volunteer_lat"],
            row["volunteer_lon"],
            row["request_lat"],
            row["request_lon"]
        )

    def open_google_maps_point(self, lat, lon):
        lat = self.safe_float(lat)
        lon = self.safe_float(lon)

        if lat is None or lon is None:
            messagebox.showwarning(
                "Missing Coordinates",
                "This location has missing or invalid coordinates."
            )
            return

        url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        webbrowser.open(url)

    def open_google_maps_route(self, start_lat, start_lon, end_lat, end_lon):
        start_lat = self.safe_float(start_lat)
        start_lon = self.safe_float(start_lon)
        end_lat = self.safe_float(end_lat)
        end_lon = self.safe_float(end_lon)

        if None in (start_lat, start_lon, end_lat, end_lon):
            messagebox.showwarning(
                "Missing Coordinates",
                "Cannot open route because volunteer or request coordinates are missing."
            )
            return

        url = f"https://www.google.com/maps/dir/{start_lat},{start_lon}/{end_lat},{end_lon}"
        webbrowser.open(url)

    # ========================================================
    # HELPERS
    # ========================================================
    def safe_float(self, value):
        try:
            if value is None or value == "":
                return None
            return float(value)
        except Exception:
            return None

    def calculate_duration_minutes(self, treatment_date, start_time):
        if treatment_date is None or start_time is None:
            return None

        try:
            if isinstance(start_time, datetime):
                start_dt = start_time
            else:
                date_str = str(treatment_date)
                time_str = str(start_time)

                if " " in time_str:
                    time_str = time_str.split(" ")[1]

                if "+" in time_str:
                    time_str = time_str.split("+")[0]

                start_dt = datetime.fromisoformat(f"{date_str} {time_str}")

            now = datetime.now()
            diff = now - start_dt

            minutes = int(diff.total_seconds() // 60)

            if minutes < 0:
                return 0

            return minutes

        except Exception as e:
            print(f"[Duration Debug] Could not calculate duration: {e}")
            print(f"[Duration Debug] treatment_date={treatment_date}, start_time={start_time}")
            return None
    def haversine_km(self, lat1, lon1, lat2, lon2):
        lat1 = self.safe_float(lat1)
        lon1 = self.safe_float(lon1)
        lat2 = self.safe_float(lat2)
        lon2 = self.safe_float(lon2)

        if None in (lat1, lon1, lat2, lon2):
            return None

        radius = 6371.0

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

    def has_missing_coordinates(self, row):
        return (
            row["volunteer_lat"] is None
            or row["volunteer_lon"] is None
            or row["request_lat"] is None
            or row["request_lon"] is None
        )

    def format_duration(self, duration):
        if duration is None:
            return "N/A"

        if duration < 60:
            return f"{duration} min"

        hours = duration // 60
        minutes = duration % 60

        return f"{hours}h {minutes}m"

    def format_distance(self, distance):
        if distance is None:
            return "N/A"

        return f"{distance:.2f} km"