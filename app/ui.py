import threading
import webbrowser
from multiprocessing import Queue
from pathlib import Path

import speech_recognition as sr
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

from llm import DEFAULT_MODEL_NAME
from utils.settings import Settings
from version import version


def open_link(url) -> None:
    webbrowser.open_new(url)


class UI:
    def __init__(self):
        self.main_window = self.MainWindow()

    def run(self) -> None:
        self.main_window.mainloop()

    def display_current_status(self, text: str):
        self.main_window.update_message(text)

    class AdvancedSettingsWindow(ttk.Toplevel):
        """
        Self-contained settings sub-window for the UI
        """

        def __init__(self, parent):
            super().__init__(parent)
            self.title('Advanced Settings')
            self.minsize(300, 300)
            self.settings = Settings()
            self.create_widgets()

            # Populate UI
            settings_dict = self.settings.get_dict()

            if 'base_url' in settings_dict:
                self.base_url_entry.insert(0, settings_dict['base_url'])
            if 'model' in settings_dict:
                self.model_entry.insert(0, settings_dict['model'])
                self.model_var.set(settings_dict.get('model', 'custom'))
            else:
                self.model_entry.insert(0, DEFAULT_MODEL_NAME)
                self.model_var.set(DEFAULT_MODEL_NAME)

        def create_widgets(self) -> None:
            # Radio buttons for model selection
            ttk.Label(self, text='Select Model:', bootstyle="primary").pack(pady=10, padx=10)
            self.model_var = ttk.StringVar(value='custom')  # default selection

            # Create a frame to hold the radio buttons
            radio_frame = ttk.Frame(self)
            radio_frame.pack(padx=20, pady=10)  # Add padding around the frame

            models = [
                ('GPT-4v (Most Accurate, Slowest)', 'gpt-4-vision-preview'),
                ('GPT-4o (Medium Accurate, Medium Fast)', 'gpt-4o'),
                ('GPT-4-Turbo (Least Accurate, Fastest)', 'gpt-4-turbo'),
                ('Custom (Specify Settings Below)', 'custom')
            ]
            for text, value in models:
                ttk.Radiobutton(radio_frame, text=text, value=value, variable=self.model_var, bootstyle="info").pack(
                    anchor=ttk.W)

            label_base_url = ttk.Label(self, text='Custom OpenAI-Like API Model Base URL', bootstyle="secondary")
            label_base_url.pack(pady=10)

            # Entry for Base URL
            self.base_url_entry = ttk.Entry(self, width=30)
            self.base_url_entry.pack()

            # Model Label
            label_model = ttk.Label(self, text='Custom Model Name:', bootstyle="secondary")
            label_model.pack(pady=10)

            # Entry for Model
            self.model_entry = ttk.Entry(self, width=30)
            self.model_entry.pack()

            # Save Button
            save_button = ttk.Button(self, text='Save Settings', bootstyle="success", command=self.save_button)
            save_button.pack(pady=20)

        def save_button(self) -> None:
            base_url = self.base_url_entry.get().strip()
            model = self.model_var.get() if self.model_var.get() != 'custom' else self.model_entry.get().strip()
            settings_dict = {
                'base_url': base_url,
                'model': model,
            }

            self.settings.save_settings_to_file(settings_dict)
            self.destroy()

    class SettingsWindow(ttk.Toplevel):
        """
        Self-contained settings sub-window for the UI
        """

        def __init__(self, parent):
            super().__init__(parent)
            self.title('Settings')
            self.minsize(300, 450)
            self.available_themes = ['darkly', 'cyborg', 'journal', 'solar', 'superhero']
            self.create_widgets()

            self.settings = Settings()

            # Populate UI
            settings_dict = self.settings.get_dict()

            if 'api_key' in settings_dict:
                self.api_key_entry.insert(0, settings_dict['api_key'])
            if 'default_browser' in settings_dict:
                self.browser_combobox.set(settings_dict['default_browser'])
            if 'play_ding_on_completion' in settings_dict:
                self.play_ding.set(1 if settings_dict['play_ding_on_completion'] else 0)
            if 'custom_llm_instructions':
                self.llm_instructions_text.insert('1.0', settings_dict['custom_llm_instructions'])
            self.theme_combobox.set(settings_dict.get('theme', 'superhero'))

        def create_widgets(self) -> None:
            # API Key Widgets
            label_api = ttk.Label(self, text='GitHub Token:', bootstyle="info")
            label_api.pack(pady=10)
            self.api_key_entry = ttk.Entry(self, width=30)
            self.api_key_entry.pack()

            # Add helper text
            helper_text = ttk.Label(self, text='No permissions needed for token', bootstyle="secondary")
            helper_text.pack(pady=2)

            # Label for Browser Choice
            label_browser = ttk.Label(self, text='Choose Default Browser:', bootstyle="info")
            label_browser.pack(pady=10)

            # Dropdown for Browser Choice
            self.browser_var = ttk.StringVar()
            self.browser_combobox = ttk.Combobox(self, textvariable=self.browser_var,
                                                 values=['Safari', 'Firefox', 'Chrome', 'Microsoft Edge'])
            self.browser_combobox.pack(pady=5)
            self.browser_combobox.set('Choose Browser')

            # Label for Custom LLM Instructions
            label_llm = ttk.Label(self, text='Custom LLM Instructions:', bootstyle="info")
            label_llm.pack(pady=10)

            # Text Box for Custom LLM Instructions
            self.llm_instructions_text = ttk.Text(self, height=10, width=50)
            self.llm_instructions_text.pack(padx=(10, 10), pady=(0, 10))

            # Checkbox for "Play Ding" option
            self.play_ding = ttk.IntVar()
            play_ding_checkbox = ttk.Checkbutton(self, text="Play Ding on Completion", variable=self.play_ding,
                                                 bootstyle="round-toggle")
            play_ding_checkbox.pack(pady=10)

            # Theme Selection Widgets
            label_theme = ttk.Label(self, text='UI Theme:', bootstyle="info")
            label_theme.pack()
            self.theme_var = ttk.StringVar()
            self.theme_combobox = ttk.Combobox(self, textvariable=self.theme_var, values=self.available_themes,
                                               state="readonly")
            self.theme_combobox.pack(pady=5)
            self.theme_combobox.set('superhero')
            # Add binding for immediate theme change
            self.theme_combobox.bind('<<ComboboxSelected>>', self.on_theme_change)

            # Save Button
            save_button = ttk.Button(self, text='Save Settings', bootstyle="success", command=self.save_button)
            save_button.pack(pady=(10, 5))

            # Button to open Advanced Settings
            advanced_settings_button = ttk.Button(self, text='Advanced Settings', bootstyle="info",
                                                  command=self.open_advanced_settings)
            advanced_settings_button.pack(pady=(0, 10))

            # Hyperlink Label
            link_label = ttk.Label(self, text='Instructions', bootstyle="primary")
            link_label.pack()
            link_label.bind('<Button-1>', lambda e: open_link(
                'https://github.com/AmberSahdev/Jarjit?tab=readme-ov-file#setup-%EF%B8%8F'))

            # Check for updates Label
            update_label = ttk.Label(self, text='Check for Updates', bootstyle="primary")
            update_label.pack()
            update_label.bind('<Button-1>', lambda e: open_link(
                'https://github.com/AmberSahdev/Jarjit/releases/latest'))

            # Version Label
            version_label = ttk.Label(self, text=f'Version: {str(version)}', font=('Helvetica', 10))
            version_label.pack(side="bottom", pady=10)

        def on_theme_change(self, event=None) -> None:
            # Apply theme immediately when selected
            theme = self.theme_var.get()
            self.master.change_theme(theme)

        def save_button(self) -> None:
            theme = self.theme_var.get()
            api_key = self.api_key_entry.get().strip()
            default_browser = self.browser_var.get()
            settings_dict = {
                'api_key': api_key,
                'default_browser': default_browser,
                'play_ding_on_completion': bool(self.play_ding.get()),
                'custom_llm_instructions': self.llm_instructions_text.get("1.0", "end-1c").strip(),
                'theme': theme
            }

            # Remove redundant theme change since it's already applied
            self.settings.save_settings_to_file(settings_dict)
            self.destroy()

        def open_advanced_settings(self):
            # Open the advanced settings window
            UI.AdvancedSettingsWindow(self)

    class MainWindow(ttk.Window):
        def __init__(self):
            # Initialize với theme tối màu
            super().__init__(themename="darkly")  # Thay đổi theme sang tối
            
            # Load settings
            settings = Settings()
            settings_dict = settings.get_dict()
            self._current_theme = settings_dict.get('theme', 'darkly')
            
            # Set window properties với background trong suốt
            self.title('J.A.R.J.I.T')  # Thêm dấu chấm để giống AI
            self.attributes('-alpha', 0.95)  # Làm trong suốt nhẹ
            
            # Tạo gradient background
            self.configure(bg='#1a1a2e')  # Deep blue background

            # Custom styles
            style = ttk.Style()
            style.configure('Custom.TEntry', 
                padding=12,
                font=('Consolas', 14),  # Font monospace
                background='#0f3460',  # Deep blue
                foreground='#00ff00'  # Matrix green
            )
            
            style.configure('Title.TLabel',
                font=('Orbitron', 28, 'bold'),  # Futuristic font
                foreground='#16c79a',  # Cyber mint
                padding=20
            )

            # Load resources with larger icons
            path_to_icon_png = Path(__file__).resolve().parent.joinpath('resources', 'icon.png')
            path_to_microphone_png = Path(__file__).resolve().parent.joinpath('resources', 'microphone.png')
            self.logo_img = ImageTk.PhotoImage(Image.open(path_to_icon_png).resize((64, 64)))  # Larger icon
            self.mic_icon = ImageTk.PhotoImage(Image.open(path_to_microphone_png).resize((24, 24)))  # Larger mic icon

            # Set app icon
            self.iconphoto(True, self.logo_img)

            # Initialize queue
            self.user_request_queue = Queue()

            # Create widgets
            self.create_widgets()

            # Thêm vào phần __init__ hiện có
            self.thinking_animation = None
            self.dots_count = 0

            # Thêm styles cho thinking animation
            style.configure('Processing.TLabel',
                font=('Consolas', 14),  # Font monospace cho hiệu ứng máy tính
                foreground='#16c79a',  # Màu cyber mint
                background='#1a1a2e'  # Match với background
            )
            
            # Thêm styles cho message display
            style.configure('Message.TLabel', 
                font=('Consolas', 14),
                foreground='#e2e2e2',  # Màu sáng cho text thường
                background='#1a1a2e'
            )

        def change_theme(self, theme: str) -> None:
            """Change the application theme"""
            if theme != self._current_theme:
                style = ttk.Style()
                style.theme_use(theme)
                self._current_theme = theme

        def create_widgets(self) -> None:
            # Tạo circular frame cho logo
            self.logo_frame = ttk.Frame(self, style='Logo.TFrame')
            self.logo_frame.place(relx=0.1, rely=0.1)
            
            # Load và resize logo với glow effect
            self.logo_img = self.create_glowing_logo()
            self.logo_label = ttk.Label(self.logo_frame, image=self.logo_img)
            self.logo_label.pack()
            
            # Start pulse animation
            self.animate_logo()

            # Main container with more padding
            frame = ttk.Frame(self, padding='30 30 30 30')  # Increased padding
            frame.grid(column=0, row=0, sticky=(ttk.W, ttk.E, ttk.N, ttk.S))
            frame.columnconfigure(0, weight=1)
            
            # Top section with logo and title
            top_frame = ttk.Frame(frame)
            top_frame.grid(column=0, row=0, sticky=(ttk.W, ttk.E), pady=(0, 30))  # Increased spacing
            
            logo_label = ttk.Label(top_frame, image=self.logo_img)
            logo_label.pack(side='left', padx=(0, 20))  # Increased spacing
            
            heading_label = ttk.Label(
                top_frame, 
                text='What would you like me to do?',
                style='Title.TLabel'
            )
            heading_label.pack(side='left', fill='x', expand=True)

            # Input section with larger wraplength
            input_frame = ttk.Frame(frame)
            input_frame.grid(column=0, row=1, sticky=(ttk.W, ttk.E), pady=15)
            input_frame.columnconfigure(0, weight=1)

            self.entry = ttk.Entry(
                input_frame, 
                style='Custom.TEntry',
                font=('Helvetica', 14)  # Larger font
            )
            self.entry.grid(column=0, row=0, sticky=(ttk.W, ttk.E))
            
            mic_button = ttk.Button(
                input_frame,
                image=self.mic_icon,
                bootstyle="link-outline",
                command=self.start_voice_input_thread
            )
            mic_button.grid(column=1, row=0, padx=8)  # Increased spacing
            
            submit_button = ttk.Button(
                input_frame,
                text='Submit',
                style='Custom.TButton',
                bootstyle="success",
                command=self.execute_user_request
            )
            submit_button.grid(column=2, row=0, padx=(8, 0))  # Increased spacing

            # Status displays with larger wraplength
            self.input_display = ttk.Label(
                frame,
                text='',
                style='Status.TLabel',
                wraplength=700  # Increased from 440
            )
            self.input_display.grid(column=0, row=2, sticky=(ttk.W, ttk.E), pady=15)
            
            self.message_display = ttk.Label(
                frame,
                text='',
                style='Status.TLabel',
                wraplength=700  # Increased from 440
            )
            self.message_display.grid(column=0, row=3, sticky=(ttk.W, ttk.E))

            # Control buttons with more spacing
            button_frame = ttk.Frame(frame)
            button_frame.grid(column=0, row=4, sticky=(ttk.E), pady=30)  # Increased spacing
            
            settings_button = ttk.Button(
                button_frame,
                text='Settings',
                style='Custom.TButton',
                bootstyle="info-outline",
                command=self.open_settings
            )
            settings_button.pack(side='left', padx=8)  # Increased spacing
            
            stop_button = ttk.Button(
                button_frame,
                text='Stop',
                style='Custom.TButton',
                bootstyle="danger-outline",
                command=self.stop_previous_request
            )
            stop_button.pack(side='left', padx=8)  # Increased spacing

            # Bind keyboard shortcuts
            self.entry.bind("<Return>", lambda e: self.execute_user_request())
            self.entry.bind("<KP_Enter>", lambda e: self.execute_user_request())
            self.entry.focus_set()  # Set focus to entry by default

        def open_settings(self) -> None:
            UI.SettingsWindow(self)

        def stop_previous_request(self) -> None:
            # Interrupt currently running request by queueing a stop signal.
            self.user_request_queue.put('stop')

        def display_input(self) -> str:
            # Get the entry and update the input display
            user_input = self.entry.get()
            self.input_display['text'] = f'{user_input}'

            # Clear the entry widget
            self.entry.delete(0, ttk.END)

            return user_input.strip()

        def execute_user_request(self) -> None:
            user_request = self.display_input()

            if user_request == '' or user_request is None:
                return

            # Bắt đầu animation
            self.start_thinking_animation()
            
            # Remove focus from entry field 
            self.focus_set()
            
            self.user_request_queue.put(user_request)

        def start_voice_input_thread(self) -> None:
            # Start voice input in a separate thread
            threading.Thread(target=self.voice_input, daemon=True).start()

        def voice_input(self) -> None:
            # Function to handle voice input
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.update_message('Đang lắng nghe...')  # "Listening..." in Vietnamese
                # This might also help with asking for mic permissions on Macs
                recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = recognizer.listen(source, timeout=4)
                    try:
                        # Added language code 'vi-VN' for Vietnamese
                        text = recognizer.recognize_google(audio, language='vi-VN')
                        self.entry.delete(0, ttk.END)
                        self.entry.insert(0, text)
                        self.update_message('')
                    except sr.UnknownValueError:
                        self.update_message('Không thể nhận dạng giọng nói')  # "Could not understand audio" in Vietnamese
                    except sr.RequestError as e:
                        self.update_message(f'Lỗi kết nối - {e}')  # "Connection error" in Vietnamese
                except sr.WaitTimeoutError:
                    self.update_message('Không nghe thấy gì')  # "Didn't hear anything" in Vietnamese

        def update_message(self, message: str) -> None:
            # Dừng animation nếu đang chạy
            self.stop_thinking_animation()
            
            # Update message với style thường
            if threading.current_thread() is threading.main_thread():
                self.message_display.configure(
                    text=message,
                    style='Message.TLabel'
                )
            else:
                self.message_display.after(0, lambda: self.message_display.configure(
                    text=message,
                    style='Message.TLabel'
                ))

        def animate_thinking(self):
            if self.thinking_animation:
                self.dots_count = (self.dots_count + 1) % 4
                dots = "." * self.dots_count
                
                # Tạo hiệu ứng nhấp nháy với ký tự đặc biệt
                frames = [
                    "▌ Processing" + dots,  # Frame 1
                    "▐ Processing" + dots,  # Frame 2
                ]
                
                current_frame = frames[self.dots_count % 2]
                
                # Cập nhật label với style riêng
                self.message_display.configure(
                    text=current_frame,
                    style='Processing.TLabel'
                )
                
                # Tốc độ animation nhanh hơn
                self.thinking_animation = self.after(200, self.animate_thinking)

        def start_thinking_animation(self):
            self.dots_count = 0
            self.thinking_animation = self.after(0, self.animate_thinking)
            
        def stop_thinking_animation(self):
            if self.thinking_animation:
                self.after_cancel(self.thinking_animation)
                self.thinking_animation = None

        def create_glowing_logo(self):
            # Load original image
            path_to_icon = Path(__file__).resolve().parent.joinpath('resources', 'icon.png')
            original = Image.open(path_to_icon).resize((80, 80))
            
            # Add glow effect
            glow = original.filter(ImageFilter.GaussianBlur(radius=5))
            glow = ImageEnhance.Brightness(glow).enhance(1.5)
            
            # Combine original and glow
            result = Image.new('RGBA', glow.size, (0, 0, 0, 0))
            result.paste(glow, (0, 0))
            result.paste(original, (0, 0), original)
            
            return ImageTk.PhotoImage(result)

        def animate_logo(self):
            # Pulse animation
            def pulse():
                scale = 1.0
                def _pulse():
                    nonlocal scale
                    scale += 0.05 if scale < 1.1 else -0.05
                    if scale < 1.0: scale = 1.0
                    
                    self.logo_label.configure(image=self.create_glowing_logo())
                    self.after(50, _pulse)
                _pulse()
            pulse()

        def create_title(self):
            self.title_label = ttk.Label(
                self, 
                text="",
                style='Title.TLabel'
            )
            self.title_label.pack(pady=20)
            
            # Typing animation
            self.type_text("What would you like me to do?", self.title_label)

        def type_text(self, text, label, delay=100):
            def _type(index=0):
                if index < len(text):
                    current = label.cget("text") + text[index]
                    label.configure(text=current)
                    self.after(delay, lambda: _type(index + 1))
            _type()

        def create_ripple(self, event):
            # Create ripple effect on click
            x = event.x_root - self.winfo_rootx()
            y = event.y_root - self.winfo_rooty()
            
            ripple = ttk.Label(self, text="", style="Ripple.TLabel")
            ripple.place(x=x, y=y)
            
            def _animate_ripple(size=0, opacity=1.0):
                if size < 100:  # Max ripple size
                    ripple.configure(width=size, height=size)
                    ripple.place(x=x-size//2, y=y-size//2)
                    
                    self.after(10, lambda: _animate_ripple(size+4, opacity-0.02))
                else:
                    ripple.destroy()
                    
            _animate_ripple()
