import customtkinter as ctk
from tkinter import messagebox
import psycopg2
from datetime import datetime
import math

try:
    from tkintermapview import TkinterMapView

    MAP_AVAILABLE = True
except Exception:
    MAP_AVAILABLE = False

# Importing screen layouts from the local screens subdirectory
from screens.families_screen import FamiliesScreen
from screens.volunteers_screen import VolunteersScreen
from screens.requests_screen import RequestsScreen
from screens.training_screen import TrainingScreen
from screens.location_screen import LocationScreen

# General modern configuration initialization
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ==========================================
# POSTGRESQL DATABASE CONTEXT CONFIGURATION
# ==========================================
DB_HOST = "localhost"
DB_NAME = "finaldb"    #"finaldb"
DB_USER = "ochrith"
DB_PASSWORD = "ochrith"
DB_PORT = "5432"


class YedidimCleanArchitectureApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Frame Engine Configurations
        self.title("Yedidim Family Assistance - Enterprise Application")
        self.geometry("1100x680")
        self.configure(fg_color="#F8F9FA")
        self.resizable(True, True)

        # Establish shared runtime backend database communication channel
        self.conn = self.connect_to_db()

        # Dictionary registries used to reference widgets for background sync
        self.metric_labels = {}

        # ==========================================
        # SIDEBAR PANEL NAVIGATION COMPONENT
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#FFFFFF", corner_radius=0, border_width=1,
                                    border_color="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Application Branded Logo Design
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(padx=20, pady=(30, 40), fill="x")

        self.logo_icon = ctk.CTkLabel(self.logo_frame, text="Y", font=ctk.CTkFont(size=24, weight="bold"),
                                      fg_color="#FF7A00", text_color="white", width=40, height=40, corner_radius=8)
        self.logo_icon.pack(side="left", padx=(0, 10))

        self.logo_text = ctk.CTkLabel(self.logo_frame, text="YEDIDIM\nFAMILY ASSISTANCE",
                                      font=ctk.CTkFont(size=12, weight="bold"), text_color="#0F4C81", justify="left")
        self.logo_text.pack(side="left")

        # Application Primary Navigation Buttons
        self.btn_dash = ctk.CTkButton(self.sidebar, text="📊   Dashboard", font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="#1A62E8", text_color="white", height=40, corner_radius=8, anchor="w",
                                      command=self.show_dashboard_view)
        self.btn_dash.pack(padx=15, pady=8, fill="x")

        self.btn_families = ctk.CTkButton(self.sidebar, text="👥   Families", font=ctk.CTkFont(size=14),
                                          fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA",
                                          height=40, anchor="w", command=self.show_families_page)
        self.btn_families.pack(padx=15, pady=4, fill="x")

        self.btn_volunteers = ctk.CTkButton(self.sidebar, text="👷   Volunteers", font=ctk.CTkFont(size=14),
                                            fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA",
                                            height=40, anchor="w", command=self.show_volunteers_page)
        self.btn_volunteers.pack(padx=15, pady=4, fill="x")

        self.btn_requests = ctk.CTkButton(self.sidebar, text="📋   Requests Management", font=ctk.CTkFont(size=14),
                                          fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA",
                                          height=40, anchor="w", command=self.show_requests_page)
        self.btn_requests.pack(padx=15, pady=4, fill="x")

        self.btn_training = ctk.CTkButton(
            self.sidebar,
            text="🎓   Trainings",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="#6C757D",
            hover_color="#F8F9FA",
            height=40,
            anchor="w",
            command=self.show_training_page
        )
        self.btn_training.pack(padx=15, pady=4, fill="x")
        self.btn_locations = ctk.CTkButton(
            self.sidebar,
            text="📍   Locations",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color="#6C757D",
            hover_color="#F8F9FA",
            height=40,
            anchor="w",
            command=self.show_locations_page
        )
        self.btn_locations.pack(padx=15, pady=4, fill="x")

        # ==========================================
        # INTERACTIVE MAIN CONTENT WORKSPACE VIEW
        # ==========================================
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True, padx=30, pady=20)

        # Upper Layout Row for Admin Profile Badge
        self.top_bar = ctk.CTkFrame(self.main_container, fg_color="transparent", height=50)
        self.top_bar.pack(fill="x", pady=(0, 20))

        self.admin_profile = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.admin_profile.pack(side="right")

        self.admin_text = ctk.CTkLabel(self.admin_profile, text="System Security Admin\nCommand Center Node",
                                       font=ctk.CTkFont(size=11, weight="bold"), text_color="#212529", justify="right")
        self.admin_text.pack(side="left", padx=10)

        self.admin_avatar = ctk.CTkLabel(self.admin_profile, text="SA", font=ctk.CTkFont(size=13, weight="bold"),
                                         fg_color="#1A62E8", text_color="white", width=35, height=35, corner_radius=18)
        self.admin_avatar.pack(side="left")

        # Dynamic screen initialization panel attachment node
        self.content_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_view.pack(fill="both", expand=True)

        # Run background metrics loops immediately
        self.update_live_metrics()

        # Load home dashboard landing parameters view configuration by default
        self.show_dashboard_view()

    def connect_to_db(self):
        try:
            return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
        except Exception as e:
            messagebox.showerror("Database Connection Error", f"Database handshake protocol failed:\n{e}")
            return None

    def clear_view(self):
        """Clears the active layout viewport container before changing views"""
        self.metric_labels.clear()
        for widget in self.content_view.winfo_children():
            widget.destroy()

    # ========================================================
    # RENDER METRIC BLOCKS & SECTIONS
    # ========================================================
    def show_dashboard_view(self):
        self.clear_view()

        # --- 4 Statistics Counter Widgets ---
        self.stats_frame = ctk.CTkFrame(self.content_view, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(0, 25))
        self.stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, pad=15)

        stats_labels = ["Total Requests", "Active Missions", "Total Volunteers", "Completed Today"]

        for i, title in enumerate(stats_labels):
            card = ctk.CTkFrame(self.stats_frame, fg_color="#FFFFFF", height=100, corner_radius=12, border_width=1,
                                border_color="#E9ECEF")
            card.grid(row=0, column=i, sticky="nsew")
            card.grid_propagate(False)

            val_lbl = ctk.CTkLabel(card, text="--", font=ctk.CTkFont(size=28, weight="bold"), text_color="#212529")
            val_lbl.pack(side="bottom", anchor="w", padx=20, pady=(0, 15))

            self.metric_labels[title] = val_lbl

            title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="bold"), text_color="#6C757D")
            title_lbl.pack(side="top", anchor="w", padx=20, pady=(15, 0))

        # --- Lower Subgrid (Alert Monitoring & Hall of Fame) ---
        self.bottom_grid = ctk.CTkFrame(self.content_view, fg_color="transparent")
        self.bottom_grid.pack(fill="both", expand=True)
        self.bottom_grid.grid_columnconfigure(0, weight=2, pad=20)
        self.bottom_grid.grid_columnconfigure(1, weight=1)

        # LEFT WORKSPACE PANEL: Urgent Real-Time Operational Queue Block
        self.left_panel = ctk.CTkFrame(self.bottom_grid, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        alert_title = ctk.CTkLabel(self.left_panel, text="⚠️ Life-Critical Alerts",
                                   font=ctk.CTkFont(size=18, weight="bold"), text_color="#DC3545")
        alert_title.pack(anchor="w", pady=(0, 15))

        # Dynamic Scrollable Container to stack multiple real-time alert modules seamlessly
        self.alerts_container = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent", height=700)  #change HERE
        self.alerts_container.pack(fill="both", expand=True)

        # RIGHT WORKSPACE PANEL: Dynamic Scrollable Hall of Fame Card
        self.hof_card = ctk.CTkFrame(self.bottom_grid, fg_color="#FFFFFF", corner_radius=12, border_width=1,
                                     border_color="#E9ECEF")
        self.hof_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        hof_title = ctk.CTkLabel(self.hof_card, text="🏆 Top 10 Volunteers", font=ctk.CTkFont(size=16, weight="bold"),
                                 text_color="#212529")
        hof_title.pack(anchor="w", padx=20, pady=(15, 5))

        self.hof_list_container = ctk.CTkScrollableFrame(self.hof_card, fg_color="transparent")
        self.hof_list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Trigger immediate data load for statistical components
        self.load_live_database_metrics()

    # ========================================================
    # AUTOMATED BACKGROUND METRICS LIVE UPDATE ENGINE
    # ========================================================
    def update_live_metrics(self):
        if hasattr(self, 'hof_list_container'):
            self.load_live_database_metrics()
        self.after(5000, self.update_live_metrics)

    def load_live_database_metrics(self):
        if not self.conn:
            return
        try:
            cursor = self.conn.cursor()

            # --- 1. FETCH SYSTEM COUNTERS ---
            cursor.execute("SELECT COUNT(*) FROM public.a_volunteer;")
            total_volunteers = cursor.fetchone()[0]
            if "Total Volunteers" in self.metric_labels and self.metric_labels["Total Volunteers"].winfo_exists():
                self.metric_labels["Total Volunteers"].configure(text=str(total_volunteers))

            cursor.execute("SELECT COUNT(*) FROM public.a_request;")
            total_requests = cursor.fetchone()[0]
            if "Total Requests" in self.metric_labels and self.metric_labels["Total Requests"].winfo_exists():
                self.metric_labels["Total Requests"].configure(text=str(total_requests))

            # --- 2. FETCH ALL LIVE CRITICAL PENDING REQUESTS IN REAL TIME ---
            if hasattr(self, 'alerts_container') and self.alerts_container.winfo_exists():
                # Query matches all status_id=1 (Pending) and prioriry_level>=4 (Critical) entries
                critical_query = """
                    SELECT request_id, incident_description, latitude, longitude, date, category_id, prioriry_level
                    FROM public.a_request 
                    WHERE status_id = 1 AND prioriry_level >= 4 
                    ORDER BY date ASC;
                """
                cursor.execute(critical_query)
                critical_incidents = cursor.fetchall()

                # Safely clear stale layout frames before reloading new queue cards
                for widget in self.alerts_container.winfo_children():
                    widget.destroy()

                if critical_incidents:
                    # Dynamically loop and build distinct alert modules for every row returned
                    for incident in critical_incidents:
                        request_id, desc, lat, lon, req_date, category_id, priority = incident
                        desc = desc or "No description"
                        short_title = desc[:45] + "..." if len(desc) > 45 else desc

                        box = ctk.CTkFrame(self.alerts_container, fg_color="#FFF5F5", corner_radius=12, border_width=1,
                                           border_color="#FEB2B2")
                        box.pack(fill="x", pady=5, ipady=10)

                        alert_icon = ctk.CTkLabel(box, text="🚨", font=ctk.CTkFont(size=22), fg_color="#DC3545",
                                                  text_color="white", width=40, height=40, corner_radius=8)
                        alert_icon.pack(side="left", padx=20, pady=10)

                        details = ctk.CTkFrame(box, fg_color="transparent")
                        details.pack(side="left", fill="both", expand=True, pady=10)

                        lbl_title = ctk.CTkLabel(details, text=f"Critical Alert #{request_id}: {short_title}",
                                                 font=ctk.CTkFont(size=14, weight="bold"), text_color="#741B1B")
                        lbl_title.pack(anchor="w")

                        lbl_desc = ctk.CTkLabel(details, text=f'"{desc}"', font=ctk.CTkFont(size=12, weight="bold"),
                                                text_color="#9B2C2C")
                        lbl_desc.pack(anchor="w")

                        lbl_loc = ctk.CTkLabel(details,
                                               text=f"📍 Coordinates: {lat}, {lon}  |  🕒 Date: {req_date}  |  Priority: {priority}",
                                               font=ctk.CTkFont(size=11), text_color="#E53E3E")
                        lbl_loc.pack(anchor="w", pady=(4, 0))

                        btn_dispatch = ctk.CTkButton(
                            box,
                            text="Dispatch",
                            font=ctk.CTkFont(size=13, weight="bold"),
                            fg_color="#DC3545",
                            hover_color="#C53030",
                            text_color="white",
                            width=90,
                            height=35,
                            corner_radius=8,
                            command=lambda rid=request_id: self.open_dispatch_map_for_request(rid)
                        )
                        btn_dispatch.pack(side="right", padx=20)
                else:
                    # Safe fallbacks layout configuration rendered when queue reads empty
                    box = ctk.CTkFrame(self.alerts_container, fg_color="#F0FDF4", corner_radius=12, border_width=1,
                                       border_color="#BBF7D0")
                    box.pack(fill="x", pady=5, ipady=10)

                    ok_icon = ctk.CTkLabel(box, text="✅", font=ctk.CTkFont(size=22), fg_color="#16A34A",
                                           text_color="white", width=40, height=40, corner_radius=8)
                    ok_icon.pack(side="left", padx=20, pady=10)

                    details = ctk.CTkFrame(box, fg_color="transparent")
                    details.pack(side="left", fill="both", expand=True, pady=10)

                    lbl_title = ctk.CTkLabel(details, text="System Secure", font=ctk.CTkFont(size=14, weight="bold"),
                                             text_color="#14532D")
                    lbl_title.pack(anchor="w")
                    lbl_desc = ctk.CTkLabel(details, text="No life-critical pending requests active at this moment.",
                                            font=ctk.CTkFont(size=12, slant="italic"), text_color="#166534")
                    lbl_desc.pack(anchor="w")

            # --- 3. FETCH TOP 10 RANKING VOLUNTEERS FOR THE HALL OF FAME ---
            if hasattr(self, 'hof_list_container') and self.hof_list_container.winfo_exists():
                query = """
                    SELECT first_name, last_name, counter 
                    FROM public.a_volunteer 
                    ORDER BY counter DESC, last_name ASC 
                    LIMIT 10;
                """
                cursor.execute(query)
                top_volunteers = cursor.fetchall()

                for widget in self.hof_list_container.winfo_children():
                    widget.destroy()

                for rank, (f_name, l_name, missions) in enumerate(top_volunteers, start=1):
                    v_row = ctk.CTkFrame(self.hof_list_container, fg_color="transparent", height=35)
                    v_row.pack(fill="x", pady=4)
                    v_row.pack_propagate(False)

                    if rank == 1:
                        badge_bg, badge_fg = "#FEFCBF", "#B7791F"
                    elif rank == 2:
                        badge_bg, badge_fg = "#E2E8F0", "#4A5568"
                    elif rank == 3:
                        badge_bg, badge_fg = "#FFDAC1", "#C05621"
                    else:
                        badge_bg, badge_fg = "#F1F3F5", "#6C757D"

                    badge = ctk.CTkLabel(v_row, text=str(rank), font=ctk.CTkFont(size=11, weight="bold"),
                                         fg_color=badge_bg, text_color=badge_fg, width=24, height=24, corner_radius=12)
                    badge.pack(side="left", padx=(5, 10))

                    full_display_name = f"{f_name} {l_name}"
                    v_name = ctk.CTkLabel(v_row, text=full_display_name, font=ctk.CTkFont(size=12, weight="bold"),
                                          text_color="#212529", anchor="w")
                    v_name.pack(side="left", fill="x", expand=True)

                    v_score = ctk.CTkLabel(v_row, text=f"{missions} mis.", font=ctk.CTkFont(size=11, weight="bold"),
                                           text_color="#1A62E8", anchor="e")
                    v_score.pack(side="right", padx=5)

            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"[Metrics Engine Log] Live sync lookup skipped: {e}")
            try:
                self.conn.rollback()
            except:
                pass

    # ========================================================
    # DISPATCH MAP FROM DASHBOARD
    # ========================================================
    def open_dispatch_map_for_request(self, request_id):
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection available.")
            return

        if not MAP_AVAILABLE:
            messagebox.showwarning(
                "Map Module Missing",
                "The map module is not installed. Install it with:\npip install tkintermapview"
            )
            return

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT
                    r.request_id,
                    r.incident_description,
                    r.prioriry_level,
                    r.category_id,
                    r.latitude,
                    r.longitude,
                    c.category_name
                FROM public.a_request r
                LEFT JOIN public.a_requestcategory c
                    ON c.category_id = r.category_id
                WHERE r.request_id = %s;
            """, (request_id,))
            request_row = cursor.fetchone()

            if not request_row:
                cursor.close()
                messagebox.showerror("Request Not Found", f"Request #{request_id} was not found.")
                return

            (
                req_id,
                description,
                priority,
                category_id,
                req_lat,
                req_lon,
                category_name
            ) = request_row

            req_lat = self.safe_float(req_lat)
            req_lon = self.safe_float(req_lon)

            if req_lat is None or req_lon is None:
                cursor.close()
                messagebox.showwarning(
                    "Missing Request Coordinates",
                    "Cannot open dispatch map because this request has missing coordinates."
                )
                return

            # We intentionally load all volunteers with coordinates.
            # Python then keeps only volunteers within 15 km and with equipment.
            cursor.execute("""
                SELECT
                    v.volunteer_id,
                    v.first_name,
                    v.last_name,
                    v.phone_number,
                    v.has_equipment,
                    v.counter,
                    v.latitude,
                    v.longitude,
                    (
                        COALESCE(v.is_active, 'N') = 'Y'
                        OR EXISTS (
                            SELECT 1
                            FROM public.a_treatment t
                            WHERE t.volunteer_id = v.volunteer_id
                              AND t.completion_time IS NULL
                        )
                    ) AS is_busy,
                    COALESCE(string_agg(DISTINCT s.skill_name, ', '), '') AS all_skills,
                    COALESCE(
                        string_agg(DISTINCT s.skill_name, ', ') FILTER (WHERE s.category_id = %s),
                        ''
                    ) AS matching_skills
                FROM public.a_volunteer v
                LEFT JOIN public.b_volunteer_skill vs
                    ON vs.volunteer_id = v.volunteer_id
                LEFT JOIN public.b_skill s
                    ON s.skill_id = vs.skill_id
                WHERE v.latitude IS NOT NULL
                  AND v.longitude IS NOT NULL
                GROUP BY
                    v.volunteer_id,
                    v.first_name,
                    v.last_name,
                    v.phone_number,
                    v.has_equipment,
                    v.counter,
                    v.latitude,
                    v.longitude
                ORDER BY v.counter DESC NULLS LAST, v.last_name ASC;
            """, (category_id,))
            volunteer_rows = cursor.fetchall()
            cursor.close()

            request_data = {
                "request_id": req_id,
                "description": description or "No description",
                "priority": priority,
                "category_id": category_id,
                "category_name": category_name or "Unknown category",
                "lat": req_lat,
                "lon": req_lon,
                "max_distance_km": 15,
            }

            volunteers = []
            for row in volunteer_rows:
                (
                    volunteer_id,
                    first_name,
                    last_name,
                    phone_number,
                    has_equipment,
                    counter,
                    lat,
                    lon,
                    is_busy,
                    all_skills,
                    matching_skills
                ) = row

                volunteer_lat = self.safe_float(lat)
                volunteer_lon = self.safe_float(lon)
                distance_km = self.haversine_km(req_lat, req_lon, volunteer_lat, volunteer_lon)

                # In the dispatch popup we show only volunteers within 15 km from the request.
                if distance_km is None or distance_km > 15:
                    continue

                # New rule: do not display volunteers without equipment for this request.
                if not has_equipment:
                    continue

                volunteers.append({
                    "volunteer_id": volunteer_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "name": f"{first_name} {last_name}",
                    "phone_number": phone_number,
                    "has_equipment": has_equipment,
                    "counter": counter,
                    "lat": volunteer_lat,
                    "lon": volunteer_lon,
                    "is_busy": bool(is_busy),
                    "all_skills": all_skills or "No skills registered",
                    "matching_skills": matching_skills or "No matching skill for this request",
                    "has_matching_skill": bool(matching_skills),
                    "distance_km": distance_km
                })

            # Sort by real distance so the map stays readable and the closest volunteers are prioritized.
            volunteers.sort(key=lambda v: v["distance_km"] if v["distance_km"] is not None else 999999)

            green_volunteers = [
                v for v in volunteers
                if v.get("distance_km") is not None and v["distance_km"] <= 5
            ]

            # Display rule requested:
            # If there are several very-close volunteers, keep only the 10 closest green ones
            # and hide orange/red markers to avoid invading the map.
            if len(green_volunteers) > 1:
                volunteers_to_display = green_volunteers[:10]
                request_data["display_rule"] = "Showing the 10 closest green volunteers only. Orange/red volunteers are hidden."
            else:
                volunteers_to_display = volunteers
                request_data["display_rule"] = "Showing equipped volunteers within 15 km, colored by distance."

            self.show_dispatch_popup(request_data, volunteers_to_display)

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Dispatch Error", f"Could not open dispatch map:\n{e}")

    def show_dispatch_popup(self, request_data, volunteers):
        popup = ctk.CTkToplevel(self)
        popup.title(f"Dispatch Request #{request_data['request_id']}")
        popup.geometry("980x690")
        popup.resizable(True, True)
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=3)
        popup.grid_columnconfigure(1, weight=1)
        popup.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(popup, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 10))

        title = ctk.CTkLabel(
            header,
            text=f"🚨 Dispatch Request #{request_data['request_id']} — {request_data['category_name']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#DC3545"
        )
        title.pack(anchor="w", padx=16, pady=(12, 4))

        desc = ctk.CTkLabel(
            header,
            text=(
                f"Priority: {request_data['priority']}  |  "
                f"{request_data.get('display_rule', 'Volunteers shown: within 15 km')}  |  "
                f"{request_data['description']}"
            ),
            font=ctk.CTkFont(size=12),
            text_color="#495057",
            wraplength=880,
            justify="left"
        )
        desc.pack(anchor="w", padx=16, pady=(0, 12))

        map_frame = ctk.CTkFrame(popup, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        map_frame.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=(0, 8))

        info_frame = ctk.CTkFrame(popup, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        info_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 16), pady=(0, 8))

        legend_frame = ctk.CTkFrame(popup, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E9ECEF")
        legend_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))

        legend_title = ctk.CTkLabel(
            legend_frame,
            text="Distance legend around the request:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#495057"
        )
        legend_title.pack(side="left", padx=(14, 10), pady=8)

        legend_green = ctk.CTkLabel(
            legend_frame,
            text="● Green: ≤ 5 km",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#16A34A"
        )
        legend_green.pack(side="left", padx=8)

        legend_orange = ctk.CTkLabel(
            legend_frame,
            text="● Orange: ≤ 10 km",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#F59E0B"
        )
        legend_orange.pack(side="left", padx=8)

        legend_red = ctk.CTkLabel(
            legend_frame,
            text="● Red: ≤ 15 km",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#DC3545"
        )
        legend_red.pack(side="left", padx=8)

        legend_note = ctk.CTkLabel(
            legend_frame,
            text="No equipment hidden. If 2+ green: only 10 closest green shown.",
            font=ctk.CTkFont(size=10, slant="italic"),
            text_color="#6C757D"
        )
        legend_note.pack(side="right", padx=14)

        info_title = ctk.CTkLabel(
            info_frame,
            text="👷 Selected Volunteer",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#212529"
        )
        info_title.pack(anchor="w", padx=16, pady=(16, 8))

        info_label = ctk.CTkLabel(
            info_frame,
            text=(
                "Click a volunteer on the map to see details.\n\n"
                "Green = within 5 km\n"
                "Orange = within 10 km\n"
                "Red = within 15 km\n"
                "No equipment = hidden\n"
                "If 2+ green volunteers exist: only the 10 closest green volunteers are shown."
            ),
            font=ctk.CTkFont(size=12),
            text_color="#6C757D",
            justify="left",
            wraplength=230
        )
        info_label.pack(anchor="w", padx=16, pady=(0, 8))

        busy_field_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7A5B00",
            fg_color="transparent",
            corner_radius=8,
            justify="left",
            wraplength=230
        )
        busy_field_label.pack(anchor="w", fill="x", padx=16, pady=(0, 8))

        equipment_field_label = ctk.CTkLabel(
            info_frame,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#7A5B00",
            fg_color="transparent",
            corner_radius=8,
            justify="left",
            wraplength=230
        )
        equipment_field_label.pack(anchor="w", fill="x", padx=16, pady=(0, 12))

        selected_holder = {"volunteer": None}

        assign_btn = ctk.CTkButton(
            info_frame,
            text="Assign this volunteer to the request",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#16A34A",
            hover_color="#15803D",
            height=38,
            corner_radius=8,
            state="disabled",
            command=lambda: self.create_treatment_for_dispatch(
                request_data,
                selected_holder["volunteer"],
                popup
            )
        )
        assign_btn.pack(fill="x", padx=16, pady=(8, 16))

        def update_info(volunteer):
            selected_holder["volunteer"] = volunteer
            equipment_text = "Yes" if volunteer["has_equipment"] else "No"
            distance_text = self.format_distance(volunteer.get("distance_km"))
            busy_text = "Yes" if volunteer.get("is_busy") else "No"
            available_text = "No" if volunteer.get("is_busy") else "Yes"
            has_skill_text = "Yes" if volunteer.get("has_matching_skill") else "No"

            info_label.configure(
                text=(
                    f"Name: {volunteer['name']}\n"
                    f"Phone: {volunteer['phone_number']}\n"
                    f"Distance from request: {distance_text}\n"
                    f"Available now: {available_text}\n"
                    f"Has required skill: {has_skill_text}\n\n"
                    f"Matching skills:\n{volunteer['matching_skills']}\n\n"
                    f"All volunteer skills:\n{volunteer['all_skills']}"
                ),
                text_color="#212529" if not volunteer.get("is_busy") else "#DC3545"
            )

            if volunteer.get("has_equipment"):
                equipment_field_label.configure(
                    text="Equipment for this request: Yes",
                    fg_color="#FFF3CD",
                    text_color="#7A5B00"
                )
            else:
                equipment_field_label.configure(
                    text="⚠️ Equipment for this request: No",
                    fg_color="#F8D7DA",
                    text_color="#842029"
                )

            if volunteer.get("is_busy"):
                busy_field_label.configure(
                    text="Busy on another mission: Yes",
                    fg_color="#FFF3CD",
                    text_color="#7A5B00"
                )
                assign_btn.configure(
                    state="disabled",
                    text="Volunteer is busy"
                )
            else:
                busy_field_label.configure(
                    text="Busy on another mission: No",
                    fg_color="transparent",
                    text_color="#198754"
                )
                assign_btn.configure(
                    state="normal",
                    text="Assign this volunteer to the request"
                )

        map_widget = TkinterMapView(map_frame, corner_radius=10)
        map_widget.pack(fill="both", expand=True, padx=12, pady=12)
        map_widget.set_position(request_data["lat"], request_data["lon"])
        map_widget.set_zoom(13)

        # Bright yellow request marker.
        # The outside color is also yellow because a red border made the request icon look red/hidden.
        # Code corrigé
        map_widget.set_marker(
            request_data["lat"],
            request_data["lon"],
            text=f"Request #{request_data['request_id']}",  # Retrait de l'émoji textuel qui peut bugger
            marker_color_circle="#FFCC00",  # Jaune vif pour le centre
            marker_color_outside="#CC9900",  # Une bordure légèrement plus sombre pour le contraste
            text_color="#000000"  # Texte en noir pour une lisibilité maximale sur la carte
        )

        valid_points = [(request_data["lat"], request_data["lon"])]

        for volunteer in volunteers:
            if volunteer["lat"] is None or volunteer["lon"] is None:
                continue

            distance = volunteer.get("distance_km")

            # --- DÉTECTION DU CAS OÙ LE VOLONTAIRE EST SUR LA REQUÊTE ---
            if volunteer["lat"] == request_data["lat"] and volunteer["lon"] == request_data["lon"]:
                circle_color = "#FFD60A"  # Jaune vif (couleur de la requête)
                outside_color = "#16A34A"  # Vert (couleur du volontaire proche)
                text_color = "#14532D"  # Vert foncé pour le texte
                display_text = f"👷 (Ici) {volunteer['name']}"

            # --- CAS STANDARDS DE DISTANCE ---
            elif distance is not None and distance <= 5:
                circle_color = "#16A34A"  # Vert : très proche
                outside_color = "#14532D"
                text_color = "#14532D"
                display_text = f"👷 {volunteer['name']}"
            elif distance is not None and distance <= 10:
                circle_color = "#F59E0B"  # Orange : distance moyenne
                outside_color = "#B45309"
                text_color = "#92400E"
                display_text = f"👷 {volunteer['name']}"
            else:
                circle_color = "#DC3545"  # Rouge : éloigné
                outside_color = "#741B1B"
                text_color = "#741B1B"
                display_text = f"👷 {volunteer['name']}"

            # Ajout du marqueur mis à jour sur la carte
            map_widget.set_marker(
                volunteer["lat"],
                volunteer["lon"],
                text=display_text,
                marker_color_circle=circle_color,
                marker_color_outside=outside_color,
                text_color=text_color,
                command=lambda marker, v=volunteer: update_info(v)
            )
            valid_points.append((volunteer["lat"], volunteer["lon"]))

        if len(valid_points) > 1:
            avg_lat = sum(p[0] for p in valid_points) / len(valid_points)
            avg_lon = sum(p[1] for p in valid_points) / len(valid_points)
            map_widget.set_position(avg_lat, avg_lon)
            map_widget.set_zoom(12)

    def ask_dispatch_confirmation(self, request_data, volunteer):
        result = {"confirmed": False}

        confirm_popup = ctk.CTkToplevel(self)
        confirm_popup.title("Confirm Dispatch")
        confirm_popup.geometry("390x190")
        confirm_popup.resizable(False, False)
        confirm_popup.grab_set()
        confirm_popup.focus_force()

        title = ctk.CTkLabel(
            confirm_popup,
            text="Confirm Dispatch",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#212529"
        )
        title.pack(pady=(20, 8))

        message = ctk.CTkLabel(
            confirm_popup,
            text=f"Assign Request #{request_data['request_id']} to {volunteer['name']}?",
            font=ctk.CTkFont(size=13),
            text_color="#495057",
            justify="center",
            wraplength=340
        )
        message.pack(pady=(0, 18))

        buttons = ctk.CTkFrame(confirm_popup, fg_color="transparent")
        buttons.pack(fill="x", padx=30)

        def choose_yes():
            result["confirmed"] = True
            confirm_popup.destroy()

        def choose_no():
            result["confirmed"] = False
            confirm_popup.destroy()

        yes_btn = ctk.CTkButton(
            buttons,
            text="Yes",
            fg_color="#16A34A",
            hover_color="#15803D",
            height=36,
            command=choose_yes
        )
        yes_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        no_btn = ctk.CTkButton(
            buttons,
            text="No",
            fg_color="#6C757D",
            hover_color="#5C636A",
            height=36,
            command=choose_no
        )
        no_btn.pack(side="left", fill="x", expand=True, padx=(8, 0))

        confirm_popup.protocol("WM_DELETE_WINDOW", choose_no)
        self.wait_window(confirm_popup)
        return result["confirmed"]

    def create_treatment_for_dispatch(self, request_data, volunteer, popup=None):
        if not self.conn:
            messagebox.showerror("Database Error", "No database connection available.")
            return

        if not volunteer:
            messagebox.showwarning("Selection Missing", "Please select a volunteer first.")
            return

        confirm = self.ask_dispatch_confirmation(request_data, volunteer)
        if not confirm:
            return

        try:
            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT 1
                FROM public.a_treatment
                WHERE request_id = %s
                  AND completion_time IS NULL
                LIMIT 1;
            """, (request_data["request_id"],))

            if cursor.fetchone():
                cursor.close()
                messagebox.showwarning(
                    "Already Assigned",
                    f"Request #{request_data['request_id']} already has an active treatment."
                )
                return

            cursor.execute("""
                SELECT 1
                FROM public.a_treatment
                WHERE volunteer_id = %s
                  AND completion_time IS NULL
                LIMIT 1;
            """, (volunteer["volunteer_id"],))

            if cursor.fetchone():
                cursor.close()
                messagebox.showwarning(
                    "Volunteer Busy",
                    f"{volunteer['name']} is already assigned to another active mission."
                )
                return

            cursor.execute("""
                SELECT COALESCE(is_active, 'N')
                FROM public.a_volunteer
                WHERE volunteer_id = %s;
            """, (volunteer["volunteer_id"],))

            status_row = cursor.fetchone()

            if status_row and status_row[0] == "Y":
                cursor.close()
                messagebox.showwarning(
                    "Volunteer Busy",
                    f"{volunteer['name']} is already marked as busy."
                )
                return
            cursor.execute("""
                INSERT INTO public.a_treatment (
                    treatment_id,
                    date,
                    start_time,
                    completion_time,
                    feedback_notes,
                    photo_after,
                    delivery_id,
                    volunteer_id,
                    request_id
                )
                VALUES (
                    (SELECT COALESCE(MAX(treatment_id), 0) + 1 FROM public.a_treatment),
                    CURRENT_DATE,
                    CURRENT_TIME,
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    %s,
                    %s
                )
                RETURNING treatment_id;
            """, (volunteer["volunteer_id"], request_data["request_id"]))

            treatment_id = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE public.a_request
                SET status_id = 2
                WHERE request_id = %s;
            """, (request_data["request_id"],))

            self.conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Dispatch Created",
                f"Treatment #{treatment_id} was created.\n"
                f"Request #{request_data['request_id']} assigned to {volunteer['name']}."
            )

            if popup and popup.winfo_exists():
                popup.destroy()

            self.load_live_database_metrics()

        except Exception as e:
            try:
                self.conn.rollback()
            except Exception:
                pass
            messagebox.showerror("Dispatch Error", f"Could not create treatment:\n{e}")

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

    def format_distance(self, distance):
        if distance is None:
            return "N/A"
        return f"{distance:.2f} km"

    def safe_float(self, value):
        try:
            if value is None or value == "":
                return None
            return float(value)
        except Exception:
            return None

    def show_families_page(self):
        self.clear_view()
        self.families_screen = FamiliesScreen(self.content_view, self.conn)
        self.families_screen.pack(fill="both", expand=True)

    def show_volunteers_page(self):
        self.clear_view()
        self.volunteers_screen = VolunteersScreen(self.content_view, self.conn)
        self.volunteers_screen.pack(fill="both", expand=True)

    def show_placeholder_page(self, module_title):
        self.clear_view()
        lbl = ctk.CTkLabel(self.content_view, text=f"[ Temporary Abstract Container Structure for {module_title} ]",
                           font=ctk.CTkFont(size=14, slant="italic"), text_color="#6C757D")
        lbl.pack(pady=100)

    def show_requests_page(self):
        self.clear_view()
        self.requests_screen = RequestsScreen(self.content_view, self.conn)
        self.requests_screen.pack(fill="both", expand=True)

    def show_training_page(self):
        self.clear_view()
        self.training_screen = TrainingScreen(self.content_view, self.conn)
        self.training_screen.pack(fill="both", expand=True)

    def show_locations_page(self):
        self.clear_view()
        self.location_screen = LocationScreen(self.content_view, self.conn)
        self.location_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = YedidimCleanArchitectureApp()
    app.mainloop()