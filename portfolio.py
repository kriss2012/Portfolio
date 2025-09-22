from ursina import *
import webbrowser, time, random, sys

app = Ursina()
window.title = "KaliOS — Krishna Patil (Simulated)"
window.borderless = False
window.exit_button.visible = False
window.color = color.rgb(6, 10, 18)

# ------------------------------
# Portfolio data (extracted)
# ------------------------------
NAME = "Krishna Patil"
ROLE = "Student — BCA (Bachelor of Computer Applications)"
SUMMARY = ("Organized and dependable candidate successful at managing multiple priorities "
           "with a positive attitude. Willing to take on added responsibilities to meet team goals.")
EMAIL = "202krishnapatil@gmail.com"
PHONE = "+91 95801 59631"
LOCATION = "Pachora, MH 424201 • India"
DOB = "20-02-2006"

EDU_TITLE = "BCA: Computational Science"
EDU_INSTITUTE = "G.H Raisoni College of Engineering and Management Jalgaon, India • Expected Mar 2026"

SKILLS = [
    "Artificial Intelligence (AI) and Machine Learning",
    "Cloud Computing: AWS, Azure, Google Cloud",
    "Full-Stack Development",
    "DevOps",
    "Blockchain",
    "UX/UI Design"
]

PROJECTS = [
    {"title": "Basha Converter",
     "desc": "Converts text and voice between multiple Indian languages. Demo and a live page available.",
     "url": "https://kriss2012.github.io/BashaConverter-Krishna/BashaConverter-Krishna.html"},
    {"title": "Online Book Store",
     "desc": "Web-based platform for browsing and buying books.",
     "url": "https://kriss2012.github.io/Online-Book-Store/"},
    {"title": "Fake Review Identification System",
     "desc": "Detects and flags misleading product reviews using AI.",
     "url": "https://fake-review-id-system-2.onrender.com/"}
]

# ------------------------------
# Helper: z-order for windows
# ------------------------------
z_base = 0
def top_z():
    global z_base
    z_base += 0.001
    return z_base

# ------------------------------
# Background (wallpaper + 3D bits)
# ------------------------------
AmbientLight(color=color.rgba(100,100,100,0.08))
wall_crystal = Entity(model='icosahedron', scale=4.0, position=(0, -1, 12), color=color.hex('1d9bf0'))
bits = []
for i in range(40):
    e = Entity(model='cube',
               scale=random.uniform(0.08,0.35),
               position=(random.uniform(-20,20), random.uniform(-12,12), random.uniform(6,28)),
               rotation=(random.uniform(0,360), random.uniform(0,360), random.uniform(0,360)),
               color=color.rgba(29,155,240, random.randint(30,120)))
    bits.append(e)
# subtle gradient
bg_overlay = Entity(parent=camera.ui, model='quad', scale=(2,2), color=color.rgba(2,8,23,160))

# ------------------------------
# Taskbar and Start Menu
# ------------------------------
taskbar = Entity(parent=camera.ui, model='quad', scale=(2, 0.12), position=(0, -0.92), color=color.rgb(11,16,22))
start_btn = Button(parent=taskbar, text='☰', position=(-0.92, -0.01), scale=(0.07,0.07))
clock_text = Text(parent=taskbar, text=time.strftime("%d %b %Y  %H:%M:%S"), x=0.9, scale=1.3, origin=(0.5,0), color=color.white)

# Start menu panel
start_panel = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.45), position=(-0.78, -0.4), color=color.rgb(12,16,24,230))
start_panel.enabled = False
Text(parent=start_panel, text=NAME, x=-0.35, y=0.18, scale=1.6, color=color.azure)
Text(parent=start_panel, text=ROLE, x=-0.35, y=0.06, scale=0.9, color=color.light_gray)
# Start menu items
def open_terminal_app(): AppWindow.open_terminal()
def open_files_app(): AppWindow.open_files()
def open_projects_app(): AppWindow.open_projects()
Button(parent=start_panel, text="Terminal", position=(-0.35, 0.0), scale=(0.6,0.09), on_click=lambda: (open_terminal_app(), setattr(start_panel, 'enabled', False)))
Button(parent=start_panel, text="Files", position=(-0.35, -0.11), scale=(0.6,0.09), on_click=lambda: (open_files_app(), setattr(start_panel, 'enabled', False)))
Button(parent=start_panel, text="Projects", position=(-0.35, -0.22), scale=(0.6,0.09), on_click=lambda: (open_projects_app(), setattr(start_panel, 'enabled', False)))
Button(parent=start_panel, text="Exit (close app)", position=(-0.35, -0.34), scale=(0.6,0.09), on_click=application.quit)
start_panel.tooltip = Tooltip("Start Menu")

# Toggle start menu
def toggle_start():
    start_panel.enabled = not start_panel.enabled

start_btn.on_click = toggle_start

# ------------------------------
# Desktop icons helpers
# ------------------------------
def make_desktop_icon(text_label, pos, callback):
    icon = Button(parent=camera.ui, text=text_label, position=pos, scale=(0.16,0.2), color=color.rgba(10,14,18,220))
    icon.text_entity.color = color.white
    icon.on_click = callback
    return icon

# ------------------------------
# Window system (custom)
# ------------------------------
class AppWindow:
    instances = []
    @staticmethod
    def close_all():
        for w in list(AppWindow.instances):
            w.close()

    def __init__(self, title="Window", size=(0.6, 0.6), position=(0,0)):
        self.container = Entity(parent=camera.ui, model='quad', scale=size, position=position, color=color.rgba(0,0,0,220))
        self.container.z = top_z()
        self.title_bar = Entity(parent=self.container, model='quad', scale=(size[0], 0.06), position=(0, size[1]/2 - 0.03), color=color.rgb(30,30,30))
        self.title_text = Text(parent=self.title_bar, text=title, x=-0.45, y=-0.01, scale=1.4, color=color.azure)
        # control buttons
        self.btn_close = Button(parent=self.title_bar, text='✕', position=(0.44, 0.01), scale=(0.08,0.08), color=color.rgb(170,70,80))
        self.btn_min = Button(parent=self.title_bar, text='—', position=(0.34, 0.01), scale=(0.08,0.08), color=color.rgb(90,90,90))
        self.btn_max = Button(parent=self.title_bar, text='□', position=(0.39, 0.01), scale=(0.08,0.08), color=color.rgb(110,110,110))
        # body area to attach content
        self.body = Entity(parent=self.container, model='quad', scale=(size[0]*0.96, size[1]-0.08), position=(0, -0.02), color=color.rgba(2,6,12,0))
        self.body_text = None
        # state
        self.dragging = False
        self.offset = (0,0)
        self.minimized = False
        self.maximized = False
        # events
        self.btn_close.on_click = self.close
        self.btn_min.on_click = self.minimize
        self.btn_max.on_click = self.maximize_restore
        # bring to front on click
        self.container.on_click = self.bring_to_front
        self.title_bar.on_click = self.start_drag
        self.title_bar.on_mouse_up = self.stop_drag
        # register
        AppWindow.instances.append(self)

    def start_drag(self):
        # record offset relative to mouse
        self.dragging = True
        self.offset = (mouse.x - self.container.x, mouse.y - self.container.y)
        self.container.z = top_z()

    def stop_drag(self):
        self.dragging = False

    def update_drag(self):
        if self.dragging:
            self.container.x = mouse.x - self.offset[0]
            self.container.y = mouse.y - self.offset[1]

    def bring_to_front(self):
        self.container.z = top_z()

    def minimize(self):
        self.container.enabled = False
        self.minimized = True

    def maximize_restore(self):
        if not self.maximized:
            self.prev_pos = (self.container.x, self.container.y)
            self.prev_scale = (self.container.scale_x, self.container.scale_y)
            self.container.scale = (1.95, 1.6)
            self.container.position = (0, 0.05)
            self.maximized = True
        else:
            self.container.scale = self.prev_scale
            self.container.position = self.prev_pos
            self.maximized = False

    def close(self):
        try:
            AppWindow.instances.remove(self)
        except:
            pass
        destroy(self.container)

    # convenience to add text content
    def set_text(self, text, fontsize=1.2, y=0.35):
        if self.body_text:
            destroy(self.body_text)
        self.body_text = Text(parent=self.body, text=text, x=-0.45, y=y, scale=fontsize, color=color.white, origin=(-0.0,0.5), line_height=1.4)

    # convenience to add an interactive list (vertical)
    def add_list(self, items, callback=None):
        # items: list of (label, payload)
        base_y = 0.28
        step = 0.08
        self.buttons = []
        for i, item in enumerate(items):
            label = item[0]
            payload = item[1] if len(item) > 1 else None
            b = Button(parent=self.body, text=label, position=(-0.0, base_y - i*step), scale=(0.9,0.07), color=color.rgba(6,12,18,220))
            b.on_click = (lambda p=payload: callback(p)) if callback else None
            self.buttons.append(b)

    # convenience to add custom entity to body (e.g., project details)
    def add_entity(self, ent):
        ent.parent = self.body

    # toggle show (for start menu to open window)
    def show(self):
        self.container.enabled = True
        self.container.z = top_z()

    # static helpers to open specialized windows
    @staticmethod
    def open_terminal():
        w = AppWindow(title="Terminal — portfolio", size=(0.74, 0.5), position=(0.0, 0.05))
        # simulate a read-only terminal: show profile lines
        lines = [
            f"{NAME}@kali:~$ whoami", NAME, "",
            f"{NAME}@kali:~$ cat profile.txt", ROLE, "", SUMMARY, "",
            "Contact:", f" Email: {EMAIL}", f" Phone: {PHONE}", f" Location: {LOCATION}", "",
            "Education:", EDU_TITLE, EDU_INSTITUTE, "", "Skills:"
        ] + SKILLS + ["", "Type 'open files' or open Files from Start Menu to view Projects."]
        w.set_text("\n".join(lines), fontsize=1.1, y=0.3)

    @staticmethod
    def open_files():
        w = AppWindow(title="Files — portfolio (virtual)", size=(0.7, 0.6), position=(-0.2, 0.05))
        # show sections as files/folders
        items = [
            ("About.txt", ("About", None)),
            ("Contact.txt", ("Contact", None)),
            ("Education.txt", ("Education", None)),
            ("Skills.txt", ("Skills", None)),
            ("Projects", ("ProjectsFolder", None))
        ]
        # callback to open virtual file/folder
        def on_pick(payload):
            kind = payload[0]
            if kind == "About":
                w2 = AppWindow(title="About.txt", size=(0.6,0.5), position=(0.18, 0.05))
                w2.set_text(f"{NAME}\n\n{ROLE}\n\n{SUMMARY}", fontsize=1.15, y=0.28)
            elif kind == "Contact":
                w2 = AppWindow(title="Contact.txt", size=(0.5,0.35), position=(0.2, -0.05))
                w2.set_text(f"Email: {EMAIL}\nPhone: {PHONE}\nLocation: {LOCATION}", fontsize=1.2, y=0.25)
            elif kind == "Education":
                w2 = AppWindow(title="Education.txt", size=(0.6,0.35), position=(0.18, -0.12))
                w2.set_text(f"{EDU_TITLE}\n{EDU_INSTITUTE}", fontsize=1.2, y=0.25)
            elif kind == "Skills":
                w2 = AppWindow(title="Skills.txt", size=(0.6,0.45), position=(0.18, 0.0))
                w2.set_text("\n".join(SKILLS), fontsize=1.15, y=0.3)
            elif kind == "ProjectsFolder":
                AppWindow.open_projects()

        # provide list
        list_items = [("About.txt", ("About", None)),
                      ("Contact.txt", ("Contact", None)),
                      ("Education.txt", ("Education", None)),
                      ("Skills.txt", ("Skills", None)),
                      ("Projects", ("ProjectsFolder", None))]
        w.add_list(list_items, callback=on_pick)

    @staticmethod
    def open_projects():
        w = AppWindow(title="Projects — internal browser", size=(0.86, 0.72), position=(0.0, 0.02))
        # show list of projects on left and a content area on right
        # we'll construct left list using add_list, and right content manually
        # left list (we'll reuse add_list but need to keep reference)
        left_items = [(p['title'], p) for p in PROJECTS]
        # callback to load project into right content area
        def load_project(p):
            # clear existing right content
            # create a panel inside w.body to act as right content
            if hasattr(w, 'proj_right'):
                destroy(w.proj_right)
            w.proj_right = Entity(parent=w.body, model='quad', scale=(0.55, 0.88*w.container.scale_y), position=(0.3, 0.0), color=color.rgba(4,8,12,0))
            # title
            Text(parent=w.proj_right, text=p['title'], x=-0.45, y=0.38, scale=1.8, color=color.azure)
            # description (wrapped)
            desc = p.get('desc', 'No description provided.')
            Text(parent=w.proj_right, text=desc, x=-0.45, y=0.12, scale=1.1, color=color.white, origin=(-0.0,0.5), line_height=1.4)
            # "Open in external browser" button
            btn = Button(parent=w.proj_right, text="Open in external browser", position=(-0.02, -0.32), scale=(0.6, 0.08))
            btn.on_click = Func(webbrowser.open, p['url'])
            # "Open inside OS (simulated)" button: open a simple internal viewer that shows text and minimal nav
            btn2 = Button(parent=w.proj_right, text="Open inside OS (simulated)", position=(-0.02, -0.44), scale=(0.6, 0.08))
            def open_internal():
                # create a new AppWindow that simulates a web page by showing the title + url + optional content
                w2 = AppWindow(title=p['title'] + " — viewer", size=(0.8, 0.7), position=(0.0, 0.0))
                w2.set_text(f"{p['title']}\n\n{desc}\n\nURL: {p['url']}\n\n(Click 'Open Externally' below to view in your real browser.)", fontsize=1.15, y=0.32)
                open_btn = Button(parent=w2.body, text="Open Externally", position=(0, -0.42), scale=(0.5,0.08))
                open_btn.on_click = Func(webbrowser.open, p['url'])
            btn2.on_click = open_internal

        # left list UI (place within the window's body)
        w.add_list(left_items, callback=load_project)
        # initial right area placeholder
        w.proj_right = Entity(parent=w.body, model='quad', scale=(0.55, 0.88*w.container.scale_y), position=(0.3, 0.0), color=color.rgba(4,8,12,0.0))
        Text(parent=w.proj_right, text="Select a project from the left to view details.", x=-0.45, y=0.18, scale=1.2, color=color.white)

# ------------------------------
# Desktop icons
# ------------------------------
make_desktop_icon("Terminal", (-0.72, 0.6), lambda: AppWindow.open_terminal())
make_desktop_icon("Files", (-0.72, 0.4), lambda: AppWindow.open_files())
make_desktop_icon("Projects", (-0.72, 0.2), lambda: AppWindow.open_projects())
make_desktop_icon("Email", (-0.72, 0.0), lambda: webbrowser.open(f"mailto:{EMAIL}"))
make_desktop_icon("LinkedIn", (-0.72, -0.2), lambda: webbrowser.open("https://www.linkedin.com/in/krishna-chandrakant-patil-3396"))

# ------------------------------
# Drag/update loop
# ------------------------------
def update():
    # animate wallpaper
    wall_crystal.rotation_y += time.dt * 10
    for i, e in enumerate(bits):
        e.rotation_y += time.dt * (5 + (i % 5))
    # update clock
    clock_text.text = time.strftime("%d %b %Y  %H:%M:%S")
    # update all windows drag states
    for w in list(AppWindow.instances):
        w.update_drag()

# ------------------------------
# Quick shortcuts
# ------------------------------
def input(key):
    if key == '`':  # toggle start menu with backtick for convenience
        toggle_start()
    if key == 'f1':
        AppWindow.open_projects()
    if key == 'f2':
        AppWindow.open_files()
    if key == 'f3':
        AppWindow.open_terminal()

# Start with a welcome message window
welcome = AppWindow(title="Welcome to KaliOS (Simulated Desktop)", size=(0.7,0.45), position=(0.0,0.15))
welcome.set_text(f"Welcome, {NAME}.\n\nThis is a simulated Linux-like desktop built with Ursina.\nUse the Start menu or desktop icons to explore your portfolio.\nProjects open inside the OS (simulated) or externally in your browser.", fontsize=1.1, y=0.25)
invoke(welcome.close, delay=6.5)

# Run
app.run()
