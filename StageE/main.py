import customtkinter as ctk
from tkinter import messagebox
import psycopg2

# Importing screen layouts from the local screens subdirectory
from screens.families_screen import FamiliesScreen
from screens.volunteers_screen import VolunteersScreen
from screens.requests_screen import RequestsScreen

# General modern configuration initialization
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue")

# ==========================================
# POSTGRESQL DATABASE CONTEXT CONFIGURATION
# ==========================================
DB_HOST = "localhost"
DB_NAME = "finaldb"
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
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#FFFFFF", corner_radius=0, border_width=1, border_color="#E9ECEF")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Application Branded Logo Design
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(padx=20, pady=(30, 40), fill="x")
        
        self.logo_icon = ctk.CTkLabel(self.logo_frame, text="Y", font=ctk.CTkFont(size=24, weight="bold"), fg_color="#FF7A00", text_color="white", width=40, height=40, corner_radius=8)
        self.logo_icon.pack(side="left", padx=(0, 10))
        
        self.logo_text = ctk.CTkLabel(self.logo_frame, text="YEDIDIM\nFAMILY ASSISTANCE", font=ctk.CTkFont(size=12, weight="bold"), text_color="#0F4C81", justify="left")
        self.logo_text.pack(side="left")

        # Application Primary Navigation Buttons
        self.btn_dash = ctk.CTkButton(self.sidebar, text="📊   Dashboard", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#1A62E8", text_color="white", height=40, corner_radius=8, anchor="w", command=self.show_dashboard_view)
        self.btn_dash.pack(padx=15, pady=8, fill="x")

        self.btn_families = ctk.CTkButton(self.sidebar, text="👥   Families", font=ctk.CTkFont(size=14), fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA", height=40, anchor="w", command=self.show_families_page)
        self.btn_families.pack(padx=15, pady=4, fill="x")

        self.btn_volunteers = ctk.CTkButton(self.sidebar, text="👷   Volunteers", font=ctk.CTkFont(size=14), fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA", height=40, anchor="w", command=self.show_volunteers_page)
        self.btn_volunteers.pack(padx=15, pady=4, fill="x")

        self.btn_requests = ctk.CTkButton(self.sidebar, text="📋   Requests Management", font=ctk.CTkFont(size=14), fg_color="transparent", text_color="#6C757D", hover_color="#F8F9FA", height=40, anchor="w", command=self.show_requests_page)
        self.btn_requests.pack(padx=15, pady=4, fill="x")

    


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
        
        self.admin_text = ctk.CTkLabel(self.admin_profile, text="System Security Admin\nCommand Center Node", font=ctk.CTkFont(size=11, weight="bold"), text_color="#212529", justify="right")
        self.admin_text.pack(side="left", padx=10)
        
        self.admin_avatar = ctk.CTkLabel(self.admin_profile, text="SA", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#1A62E8", text_color="white", width=35, height=35, corner_radius=18)
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
            card = ctk.CTkFrame(self.stats_frame, fg_color="#FFFFFF", height=100, corner_radius=12, border_width=1, border_color="#E9ECEF")
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

        alert_title = ctk.CTkLabel(self.left_panel, text="⚠️ Life-Critical Alerts", font=ctk.CTkFont(size=18, weight="bold"), text_color="#DC3545")
        alert_title.pack(anchor="w", pady=(0, 15))

        # Dynamic Scrollable Container to stack multiple real-time alert modules seamlessly
        self.alerts_container = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent", height=320)
        self.alerts_container.pack(fill="both", expand=True)

        # RIGHT WORKSPACE PANEL: Dynamic Scrollable Hall of Fame Card
        self.hof_card = ctk.CTkFrame(self.bottom_grid, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E9ECEF")
        self.hof_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        hof_title = ctk.CTkLabel(self.hof_card, text="🏆 Top 10 Volunteers", font=ctk.CTkFont(size=16, weight="bold"), text_color="#212529")
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
                    SELECT incident_description, latitude, longitude, date 
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
                        desc, lat, lon, req_date = incident
                        short_title = desc[:45] + "..." if len(desc) > 45 else desc

                        box = ctk.CTkFrame(self.alerts_container, fg_color="#FFF5F5", corner_radius=12, border_width=1, border_color="#FEB2B2")
                        box.pack(fill="x", pady=5, ipady=10)

                        alert_icon = ctk.CTkLabel(box, text="🚨", font=ctk.CTkFont(size=22), fg_color="#DC3545", text_color="white", width=40, height=40, corner_radius=8)
                        alert_icon.pack(side="left", padx=20, pady=10)

                        details = ctk.CTkFrame(box, fg_color="transparent")
                        details.pack(side="left", fill="both", expand=True, pady=10)

                        lbl_title = ctk.CTkLabel(details, text=f"Critical Alert: {short_title}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#741B1B")
                        lbl_title.pack(anchor="w")
                        
                        lbl_desc = ctk.CTkLabel(details, text=f'"{desc}"', font=ctk.CTkFont(size=12, weight="bold"), text_color="#9B2C2C")
                        lbl_desc.pack(anchor="w")
                        
                        lbl_loc = ctk.CTkLabel(details, text=f"📍 Coordinates: {lat}, {lon}  |  🕒 Date: {req_date}", font=ctk.CTkFont(size=11), text_color="#E53E3E")
                        lbl_loc.pack(anchor="w", pady=(4, 0))

                        btn_dispatch = ctk.CTkButton(box, text="Dispatch", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#DC3545", hover_color="#C53030", text_color="white", width=90, height=35, corner_radius=8)
                        btn_dispatch.pack(side="right", padx=20)
                else:
                    # Safe fallbacks layout configuration rendered when queue reads empty
                    box = ctk.CTkFrame(self.alerts_container, fg_color="#F0FDF4", corner_radius=12, border_width=1, border_color="#BBF7D0")
                    box.pack(fill="x", pady=5, ipady=10)
                    
                    ok_icon = ctk.CTkLabel(box, text="✅", font=ctk.CTkFont(size=22), fg_color="#16A34A", text_color="white", width=40, height=40, corner_radius=8)
                    ok_icon.pack(side="left", padx=20, pady=10)
                    
                    details = ctk.CTkFrame(box, fg_color="transparent")
                    details.pack(side="left", fill="both", expand=True, pady=10)
                    
                    lbl_title = ctk.CTkLabel(details, text="System Secure", font=ctk.CTkFont(size=14, weight="bold"), text_color="#14532D")
                    lbl_title.pack(anchor="w")
                    lbl_desc = ctk.CTkLabel(details, text="No life-critical pending requests active at this moment.", font=ctk.CTkFont(size=12, slant="italic"), text_color="#166534")
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

                    if rank == 1: badge_bg, badge_fg = "#FEFCBF", "#B7791F"
                    elif rank == 2: badge_bg, badge_fg = "#E2E8F0", "#4A5568"
                    elif rank == 3: badge_bg, badge_fg = "#FFDAC1", "#C05621"
                    else: badge_bg, badge_fg = "#F1F3F5", "#6C757D"

                    badge = ctk.CTkLabel(v_row, text=str(rank), font=ctk.CTkFont(size=11, weight="bold"), fg_color=badge_bg, text_color=badge_fg, width=24, height=24, corner_radius=12)
                    badge.pack(side="left", padx=(5, 10))

                    full_display_name = f"{f_name} {l_name}"
                    v_name = ctk.CTkLabel(v_row, text=full_display_name, font=ctk.CTkFont(size=12, weight="bold"), text_color="#212529", anchor="w")
                    v_name.pack(side="left", fill="x", expand=True)

                    v_score = ctk.CTkLabel(v_row, text=f"{missions} mis.", font=ctk.CTkFont(size=11, weight="bold"), text_color="#1A62E8", anchor="e")
                    v_score.pack(side="right", padx=5)

            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"[Metrics Engine Log] Live sync lookup skipped: {e}")
            try:
                self.conn.rollback()
            except:
                pass

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
        lbl = ctk.CTkLabel(self.content_view, text=f"[ Temporary Abstract Container Structure for {module_title} ]", font=ctk.CTkFont(size=14, slant="italic"), text_color="#6C757D")
        lbl.pack(pady=100)

    def show_requests_page(self):
        self.clear_view()
        self.requests_screen = RequestsScreen(self.content_view, self.conn)
        self.requests_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = YedidimCleanArchitectureApp()
    app.mainloop()