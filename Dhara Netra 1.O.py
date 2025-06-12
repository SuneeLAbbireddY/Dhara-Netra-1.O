'''#!/usr/bin/env python3'''
"""
Soil Classification Tool according to IS 1498:1970
Compatible with Python 3.11
Required packages:
- tkinter (comes with Python)
- matplotlib
- numpy
- reportlab
"""

import sys
import os
import platform
import subprocess
import site
import shutil
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import json
import csv
import io
import webbrowser
import tkinter as tk
from tkinter import (
    ttk, scrolledtext, filedialog, colorchooser, 
    messagebox, simpledialog, TclError
)
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import sqlite3

# Color themes
COLOR_THEMES = {
    'default': {
        'bg': '#f0f0f0',
        'fg': '#000000',
        'button_bg': '#e1e1e1',
        'button_fg': '#000000',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'highlight_bg': '#0078d7',
        'highlight_fg': '#ffffff',
        'error': '#ff0000',
        'success': '#00aa00',
        'warning': '#ffa500',
        'info': '#0078d7',
        'plot_bg': '#ffffff',
        'plot_fg': '#333333',
        'grid': '#cccccc'
    },
    'dark': {
        'bg': '#2d2d2d',
        'fg': '#ffffff',
        'button_bg': '#404040',
        'button_fg': '#ffffff',
        'entry_bg': '#404040',
        'entry_fg': '#ffffff',
        'highlight_bg': '#0078d7',
        'highlight_fg': '#ffffff',
        'error': '#ff6b6b',
        'success': '#4cd964',
        'warning': '#ffd60a',
        'info': '#5ac8fa',
        'plot_bg': '#2d2d2d',
        'plot_fg': '#ffffff',
        'grid': '#404040'
    },
    'blue': {
        'bg': '#e6f3ff',
        'fg': '#000000',
        'button_bg': '#0078d7',
        'button_fg': '#ffffff',
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'highlight_bg': '#005a9e',
        'highlight_fg': '#ffffff',
        'error': '#d83b01',
        'success': '#107c10',
        'warning': '#f7630c',
        'info': '#0078d7',
        'plot_bg': '#ffffff',
        'plot_fg': '#333333',
        'grid': '#e6f3ff'
    },
    'earth': {
        'bg': '#f5e6d3',
        'fg': '#2d2d2d',
        'button_bg': '#8b4513',
        'button_fg': '#ffffff',
        'entry_bg': '#ffffff',
        'entry_fg': '#2d2d2d',
        'highlight_bg': '#d2691e',
        'highlight_fg': '#ffffff',
        'error': '#8b0000',
        'success': '#556b2f',
        'warning': '#cd853f',
        'info': '#8b4513',
        'plot_bg': '#ffffff',
        'plot_fg': '#2d2d2d',
        'grid': '#deb887'
    }
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean_environment(force=False):
    """
    Clean up potentially conflicting packages.
    
    Args:
        force (bool): If True, forces cleanup even if environment seems clean
    
    Returns:
        bool: True if cleanup was successful or not needed, False if cleanup failed
    """
    try:
        # Get Python 3.10 site-packages path
        python310_path = os.path.join(site.USER_SITE.replace('Python311', 'Python310'))
        
        # Check if cleanup is needed
        if not os.path.exists(python310_path) and not force:
            logging.info("No conflicting packages found. Skipping cleanup.")
            return True
            
        logging.info(f"Attempting to clean up: {python310_path}")
        
        # Use Path object for better path handling
        path_obj = Path(python310_path)
        
        # Only attempt cleanup if directory exists
        if path_obj.exists():
            try:
                # Try to remove with ignore_errors=True to skip permission issues
                shutil.rmtree(str(path_obj), ignore_errors=True)
                if path_obj.exists():
                    logging.warning("Could not completely clean environment due to permissions - continuing anyway")
                    return True
                    
                logging.info("Environment cleanup completed successfully")
                return True
                
            except Exception as e:
                logging.warning(f"Non-critical error during cleanup: {e}")
                return True  # Continue anyway since this is not critical
        else:
            logging.info("No cleanup needed - directory does not exist")
            return True
            
    except Exception as e:
        logging.error(f"Environment cleanup failed: {e}")
        return True  # Continue anyway since this is not critical

def setup_environment():
    """Setup the Python environment and install required packages."""
    # Clean environment first
    if not clean_environment():
        logging.warning("Environment cleanup was not completely successful - proceeding with caution")
    
    try:
        import matplotlib
        import numpy
        import reportlab
        logging.info("Required packages are already installed")
    except ImportError:
        logging.info("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib', 'numpy', 'reportlab'])
            logging.info("Successfully installed required packages")
        except Exception as e:
            logging.error(f"Error installing packages: {e}")
            print("\nPlease run these commands manually:")
            print("pip install matplotlib numpy reportlab")
            sys.exit(1)

def main():
    """Main entry point with environment checks."""
    try:
        # Check Python version
        if sys.version_info < (3, 11):
            logging.warning(f"This version is optimized for Python 3.11+")
            logging.warning(f"Current Python version: {platform.python_version()}")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)

        # Setup environment
        setup_environment()

        # Import required packages
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox, Text, filedialog
        except ImportError as e:
            logging.error(f"Error importing tkinter: {e}")
            print("\nPlease ensure tkinter is installed with your Python distribution")
            sys.exit(1)

        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
            import numpy as np
        except ImportError as e:
            logging.error(f"Error importing matplotlib or numpy: {e}")
            print("\nPlease ensure matplotlib and numpy are installed:")
            print("pip install matplotlib numpy")
            sys.exit(1)

        # Continue with the rest of the imports
        import json
        import csv

        class SoilClassificationApp:
            def __init__(self, root):
                """Initialize the application."""
                try:
                    self.root = root
                    self.root.title('Dhara Netra 1.0')
                    
                    # Set up logging
                    logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='soil_classification.log'
                    )
                    
                    # Initialize style first
                    self.style = ttk.Style()
                    
                    # Load custom themes
                    self.load_custom_themes()
                    
                    # Load color theme
                    self.current_theme = 'default'
                    
                    # Configure styles before applying theme
                    try:
                        self.configure_styles()
                    except Exception as e:
                        logging.error(f"Failed initial style configuration: {e}")
                        # Continue anyway as we'll retry in load_theme
                    
                    # Now load the theme
                    self.load_theme(self.current_theme)
                    
                    # Configure exception handling
                    self.root.report_callback_exception = self.handle_exception
                    
                    # Initialize data storage
                    self.history = []
                    self.current_data = {}
                    
                    # Initialize plot
                    self.soil_plot = None
                    self.fig = None
                    self.canvas = None
                    
                    # Create menu
                    self.create_menu()
                    
                    # Initialize UI
                    self.create_widgets()
                    self.initialize_plot()
                    
                    # Set up window close protocol
                    self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                    
                    # Load last session if exists
                    self.load_last_session()
                    
                except Exception as e:
                    logging.critical(f"Failed to initialize application: {e}")
                    messagebox.showerror("Critical Error", 
                                       "Failed to initialize application. Please check the log file.")
                    raise

            def configure_styles(self):
                """Configure ttk styles with current theme."""
                try:
                    if not hasattr(self, 'style'):
                        self.style = ttk.Style()
                        logging.info("Style object created in configure_styles")
                    
                    theme = COLOR_THEMES[self.current_theme]
                    
                    # Configure ttk styles
                    style_configs = {
                        'TFrame': {'background': theme['bg']},
                        'TLabel': {
                            'background': theme['bg'],
                            'foreground': theme['fg']
                        },
                        'TButton': {
                            'background': theme['button_bg'],
                            'foreground': theme['button_fg']
                        },
                        'TEntry': {
                            'fieldbackground': theme['entry_bg'],
                            'foreground': theme['entry_fg']
                        },
                        'Treeview': {
                            'background': theme['entry_bg'],
                            'foreground': theme['entry_fg'],
                            'fieldbackground': theme['entry_bg']
                        },
                        'TNotebook': {'background': theme['bg']},
                        'TNotebook.Tab': {
                            'background': theme['button_bg'],
                            'foreground': theme['button_fg']
                        }
                    }
                    
                    # Apply configurations
                    for style_name, config in style_configs.items():
                        try:
                            self.style.configure(style_name, **config)
                        except TclError as e:
                            logging.warning(f"Failed to configure {style_name}: {e}")
                    
                    # Configure custom button styles
                    custom_styles = {
                        'Success.TButton': {
                            'background': theme['success'],
                            'foreground': theme['highlight_fg']
                        },
                        'Warning.TButton': {
                            'background': theme['warning'],
                            'foreground': theme['highlight_fg']
                        },
                        'Info.TButton': {
                            'background': theme['info'],
                            'foreground': theme['highlight_fg']
                        },
                        'Error.TButton': {
                            'background': theme['error'],
                            'foreground': theme['highlight_fg']
                        }
                    }
                    
                    for style_name, config in custom_styles.items():
                        try:
                            self.style.configure(style_name, **config)
                        except TclError as e:
                            logging.warning(f"Failed to configure {style_name}: {e}")
                            
                except Exception as e:
                    logging.error(f"Failed to configure styles: {e}")
                    if not hasattr(self, 'style'):
                        logging.error("Style attribute is missing")
                    messagebox.showwarning("Warning", 
                                         "Failed to configure some styles. The application will continue with default styles.")

            def load_theme(self, theme_name):
                """Load and apply color theme."""
                try:
                    if not hasattr(self, 'style'):
                        self.style = ttk.Style()
                        logging.info("Style object created in load_theme")
                    
                    if theme_name not in COLOR_THEMES:
                        logging.warning(f"Theme {theme_name} not found, using default")
                        theme_name = 'default'
                    
                    theme = COLOR_THEMES[theme_name]
                    self.current_theme = theme_name
                    
                    # Configure root window
                    try:
                        self.root.configure(bg=theme['bg'])
                    except TclError as e:
                        logging.error(f"Failed to set root background: {e}")
                    
                    # Update style configuration
                    try:
                        self.configure_styles()
                    except Exception as e:
                        logging.error(f"Failed to configure styles in load_theme: {e}")
                    
                    # Update plot colors if exists
                    if hasattr(self, 'fig') and self.fig is not None:
                        try:
                            self.fig.set_facecolor(theme['plot_bg'])
                            if hasattr(self, 'soil_plot') and self.soil_plot is not None:
                                self.soil_plot.set_facecolor(theme['plot_bg'])
                                self.soil_plot.grid(color=theme['grid'])
                                self.soil_plot.tick_params(colors=theme['plot_fg'])
                                self.soil_plot.set_xlabel(self.soil_plot.get_xlabel(), color=theme['plot_fg'])
                                self.soil_plot.set_ylabel(self.soil_plot.get_ylabel(), color=theme['plot_fg'])
                                if hasattr(self, 'canvas') and self.canvas is not None:
                                    self.canvas.draw()
                        except Exception as e:
                            logging.error(f"Failed to update plot colors: {e}")
                except Exception as e:
                    logging.error(f"Failed to load theme: {e}")
                    messagebox.showwarning("Warning", 
                                         "Failed to load theme. The application will continue with default styles.")

            def handle_exception(self, exc_type, exc_value, exc_traceback):
                """Handle uncaught exceptions."""
                error_msg = f"An error occurred:\n{exc_type.__name__}: {exc_value}"
                messagebox.showerror("Error", error_msg)
                print("Exception:", error_msg)

            def create_menu(self):
                menubar = tk.Menu(self.root)
                self.root.config(menu=menubar)
                
                # File menu
                file_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="File", menu=file_menu)
                file_menu.add_command(label="New", command=self.new_session)
                file_menu.add_command(label="Save", command=self.save_data)
                file_menu.add_command(label="Load", command=self.load_data)
                file_menu.add_separator()
                file_menu.add_command(label="Export Results", command=self.export_results)
                file_menu.add_command(label="Import Data", command=self.import_data)
                file_menu.add_separator()
                file_menu.add_command(label="Exit", command=self.on_closing)
                
                # Tools menu
                tools_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Tools", menu=tools_menu)
                tools_menu.add_command(label="Clear All", command=self.clear_all)
                tools_menu.add_command(label="View History", command=self.view_history)
                tools_menu.add_command(label="Generate Report", command=self.generate_report)
                tools_menu.add_separator()
                tools_menu.add_command(label="Compare Samples", command=self.compare_samples)
                tools_menu.add_command(label="Statistical Analysis", command=self.statistical_analysis)
                tools_menu.add_command(label="Batch Processing", command=self.batch_processing)
                
                # Analysis menu
                analysis_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Analysis", menu=analysis_menu)
                analysis_menu.add_command(label="Soil Properties Guide", command=self.show_soil_properties)
                analysis_menu.add_command(label="Engineering Applications", command=self.show_engineering_applications)
                analysis_menu.add_command(label="Correlation Analysis", command=self.show_correlations)
                analysis_menu.add_command(label="Trend Analysis", command=self.show_trend_analysis)
                analysis_menu.add_command(label="Project Database", command=self.show_project_database)
                
                # Visualization menu
                visual_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Visualization", menu=visual_menu)
                visual_menu.add_command(label="Customize Plot", command=self.customize_plot)
                visual_menu.add_command(label="3D Visualization", command=self.show_3d_visualization)
                visual_menu.add_command(label="Export Plot", command=self.export_plot)
                
                # Settings menu
                settings_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Settings", menu=settings_menu)
                settings_menu.add_command(label="Preferences", command=self.show_preferences)
                settings_menu.add_command(label="Theme Settings", command=self.theme_settings)
                settings_menu.add_command(label="Export Settings", command=self.export_settings)
                
                # Help menu
                help_menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label="Help", menu=help_menu)
                help_menu.add_command(label="User Guide", command=self.show_user_guide)
                help_menu.add_command(label="IS Code Reference", command=self.show_is_code)
                help_menu.add_command(label="Video Tutorials", command=self.show_tutorials)
                help_menu.add_command(label="Check Updates", command=self.check_updates)
                help_menu.add_command(label="About", command=self.show_about)

            def new_session(self):
                if messagebox.askyesno("New Session", "Clear all current data?"):
                    self.clear_all()

            def save_data(self):
                try:
                    data = {
                        'entries': {key: entry.get() for key, entry in self.entries.items()},
                        'current_data': self.current_data,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".json",
                        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                    )
                    
                    if file_path:
                        with open(file_path, 'w') as f:
                            json.dump(data, f, indent=4)
                        messagebox.showinfo("Success", "Data saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save data: {str(e)}")

            def load_data(self):
                try:
                    file_path = filedialog.askopenfilename(
                        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                    )
                    
                    if file_path:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        # Clear existing entries
                        self.clear_all()
                        
                        # Load entries
                        for key, value in data['entries'].items():
                            if key in self.entries:
                                self.entries[key].delete(0, tk.END)
                                self.entries[key].insert(0, value)
                        
                        # Load current data if available
                        if 'current_data' in data:
                            self.current_data = data['current_data']
                        
                        # Determine soil type and classify
                        if 'gravel_fraction' in data['entries']:
                            self.classify_soil('coarse')
                        else:
                            self.classify_soil('fine')
                            
                        messagebox.showinfo("Success", "Data loaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load data: {str(e)}")

            def export_results(self):
                try:
                    if not self.current_data:
                        messagebox.showwarning("Warning", "No results to export!")
                        return
                        
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf")]
                    )
                    
                    if file_path:
                        self.export_to_pdf(file_path)
                        messagebox.showinfo("Success", "Results exported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export results: {str(e)}")

            def export_to_pdf(self, file_path):
                """Export results to PDF with A4 size including plot."""
                # Save current plot to bytes
                plot_buffer = io.BytesIO()
                self.fig.savefig(plot_buffer, format='png', dpi=300, bbox_inches='tight')
                plot_buffer.seek(0)

                # Create PDF document
                doc = SimpleDocTemplate(
                    file_path,
                    pagesize=A4,
                    rightMargin=72,
                    leftMargin=72,
                    topMargin=72,
                    bottomMargin=72
                )

                # Create styles
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=TA_CENTER
                )
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=12,
                    spaceAfter=12
                )
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontSize=10,
                    spaceAfter=12
                )

                # Build content
                elements = []
                
                # Add title
                title = "Soil Classification Report"
                elements.append(Paragraph(title, title_style))
                
                # Add date
                date_str = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                elements.append(Paragraph(date_str, normal_style))
                elements.append(Spacer(1, 20))

                # Add soil type heading
                if 'Gravel Fraction' in self.current_data:
                    soil_type = "Coarse-Grained Soil Analysis"
                else:
                    soil_type = "Fine-Grained Soil Analysis"
                elements.append(Paragraph(soil_type, heading_style))
                elements.append(Spacer(1, 12))

                # Add input parameters
                elements.append(Paragraph("Input Parameters:", heading_style))
                for key, value in self.current_data.items():
                    if isinstance(value, float):
                        param_text = f"{key}: {value:.2f}"
                    else:
                        param_text = f"{key}: {value}"
                    elements.append(Paragraph(param_text, normal_style))
                elements.append(Spacer(1, 12))

                # Add classification results
                elements.append(Paragraph("Classification Results:", heading_style))
                results_text = self.results_text.get(1.0, tk.END).strip()
                for line in results_text.split('\n'):
                    if line.strip():
                        elements.append(Paragraph(line, normal_style))
                elements.append(Spacer(1, 20))

                # Add plot
                # Calculate image size to fit A4 while maintaining aspect ratio
                img_width = 6 * inch  # 6 inches width
                img = Image(plot_buffer, width=img_width, height=img_width)
                elements.append(img)

                # Build PDF
                doc.build(elements)

            def clear_all(self):
                try:
                    for entry in self.entries.values():
                        entry.delete(0, tk.END)
                    self.results_text.delete(1.0, tk.END)
                    self.initialize_plot()
                    self.current_data = {}
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to clear data: {str(e)}")

            def view_history(self):
                if not self.history:
                    messagebox.showinfo("History", "No history available")
                    return
                
                history_window = tk.Toplevel(self.root)
                history_window.title("Classification History")
                
                text = Text(history_window, wrap=tk.WORD, height=20, width=50)
                text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                for item in self.history:
                    text.insert(tk.END, f"Date: {item['timestamp']}\n")
                    text.insert(tk.END, f"Results:\n{item['results']}\n")
                    text.insert(tk.END, "-" * 50 + "\n")

            def generate_report(self):
                try:
                    if not self.current_data:
                        messagebox.showwarning("Warning", "No data to generate report!")
                        return
                        
                    file_path = filedialog.asksaveasfilename(
                        defaultextension=".txt",
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                    )
                    
                    if file_path:
                        with open(file_path, 'w') as f:
                            f.write("SOIL CLASSIFICATION REPORT\n")
                            f.write("=" * 50 + "\n\n")
                            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                            f.write("Input Parameters:\n")
                            f.write("-" * 20 + "\n")
                            for key, entry in self.entries.items():
                                value = entry.get()
                                if value:
                                    f.write(f"{key.replace('_', ' ').title()}: {value}%\n")
                            f.write("\nClassification Results:\n")
                            f.write("-" * 20 + "\n")
                            f.write(self.results_text.get(1.0, tk.END))
                        
                        messagebox.showinfo("Success", "Report generated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

            def load_last_session(self):
                try:
                    if os.path.exists('last_session.json'):
                        with open('last_session.json', 'r') as f:
                            data = json.load(f)
                        for key, value in data['entries'].items():
                            if key in self.entries:
                                self.entries[key].insert(0, value)
                except Exception:
                    pass  # Silently fail if last session can't be loaded

            def save_last_session(self):
                try:
                    data = {
                        'entries': {key: entry.get() for key, entry in self.entries.items()},
                        'timestamp': datetime.now().isoformat()
                    }
                    with open('last_session.json', 'w') as f:
                        json.dump(data, f)
                except Exception:
                    pass  # Silently fail if session can't be saved

            def create_widgets(self):
                """Create and arrange widgets with error handling."""
                try:
                    # Create main container frame with theme colors
                    main_frame = ttk.Frame(self.root)
                    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                    
                    # Create theme selector
                    theme_frame = ttk.Frame(main_frame)
                    theme_frame.pack(fill=tk.X, pady=(0, 10))
                    
                    ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
                    theme_combo = ttk.Combobox(theme_frame, 
                                             values=list(COLOR_THEMES.keys()),
                                             state='readonly')
                    theme_combo.set(self.current_theme)
                    theme_combo.pack(side=tk.LEFT, padx=5)
                    
                    def on_theme_change(event):
                        try:
                            new_theme = theme_combo.get()
                            if new_theme != self.current_theme:
                                self.load_theme(new_theme)
                        except Exception as e:
                            logging.error(f"Failed to change theme: {e}")
                            messagebox.showerror("Error", f"Failed to change theme: {str(e)}")
                    
                    theme_combo.bind('<<ComboboxSelected>>', on_theme_change)
                    
                    # Create left frame for inputs and results
                    left_frame = ttk.Frame(main_frame)
                    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
                    
                    # Create right frame for plot
                    right_frame = ttk.Frame(main_frame)
                    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    
                    # Create and arrange input elements in the left frame
                    self.create_input_frame(left_frame)
                    self.create_results_frame(left_frame)
                    self.create_plot_frame(right_frame)
                    
                except Exception as e:
                    logging.error(f"Failed to create widgets: {e}")
                    messagebox.showerror("Error", f"Failed to create widgets: {str(e)}")
                    raise

            def theme_settings(self):
                """Show theme settings dialog with error handling."""
                self.show_preferences()

            def create_input_frame(self, parent):
                frame_input = ttk.LabelFrame(parent, text='Soil Properties', padding=10)
                frame_input.pack(fill=tk.X)

                # Create notebook for different soil types
                self.notebook = ttk.Notebook(frame_input)
                self.notebook.pack(fill=tk.X, pady=5)

                # Fine-grained soil tab
                fine_frame = ttk.Frame(self.notebook)
                self.notebook.add(fine_frame, text='Fine-Grained')

                # Coarse-grained soil tab
                coarse_frame = ttk.Frame(self.notebook)
                self.notebook.add(coarse_frame, text='Coarse-Grained')

                # Create dictionary to store entry widgets
                self.entries = {}

                # Fine-grained properties
                ttk.Label(fine_frame, text='Basic Properties:', font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w')

                basic_props = [
                    ('liquid_limit', 'Liquid Limit (%)', 1),
                    ('plastic_limit', 'Plastic Limit (%)', 2)
                ]

                for key, label, row in basic_props:
                    ttk.Label(fine_frame, text=label).grid(row=row, column=0, sticky='w')
                    self.entries[key] = ttk.Entry(fine_frame, width=15)
                    self.entries[key].grid(row=row, column=1, padx=5)

                # Additional fine-grained properties
                ttk.Label(fine_frame, text='Additional Properties:', font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, sticky='w', pady=(10,0))

                additional_props = [
                    ('water_content', 'Natural Water Content (%)', 4),
                    ('shrinkage_limit', 'Shrinkage Limit (%)', 5),
                    ('clay_fraction', 'Clay Fraction (%)', 6)
                ]

                for key, label, row in additional_props:
                    ttk.Label(fine_frame, text=label).grid(row=row, column=0, sticky='w')
                    self.entries[key] = ttk.Entry(fine_frame, width=15)
                    self.entries[key].grid(row=row, column=1, padx=5)

                # Coarse-grained properties
                ttk.Label(coarse_frame, text='Grain Size Distribution:', font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w')

                grain_props = [
                    ('gravel_fraction', 'Gravel (>4.75mm) (%)', 1),
                    ('sand_fraction', 'Sand (4.75-0.075mm) (%)', 2),
                    ('fines_fraction', 'Fines (<0.075mm) (%)', 3),
                    ('cu', 'Coefficient of Uniformity (Cu)', 4),
                    ('cc', 'Coefficient of Curvature (Cc)', 5)
                ]

                for key, label, row in grain_props:
                    ttk.Label(coarse_frame, text=label).grid(row=row, column=0, sticky='w')
                    self.entries[key] = ttk.Entry(coarse_frame, width=15)
                    self.entries[key].grid(row=row, column=1, padx=5)

                # Add classify buttons to both tabs
                classify_fine = ttk.Button(fine_frame, text='Classify Fine-Grained Soil', command=lambda: self.classify_soil('fine'))
                classify_fine.grid(row=7, column=0, columnspan=2, pady=10)

                classify_coarse = ttk.Button(coarse_frame, text='Classify Coarse-Grained Soil', command=lambda: self.classify_soil('coarse'))
                classify_coarse.grid(row=6, column=0, columnspan=2, pady=10)

            def create_results_frame(self, parent):
                results_frame = ttk.LabelFrame(parent, text='Classification Results', padding=10)
                results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

                self.results_text = Text(results_frame, wrap=tk.WORD, height=15, width=40)
                self.results_text.pack(fill=tk.BOTH, expand=True)

            def create_plot_frame(self, parent):
                # Create Matplotlib figure
                self.fig = plt.figure(figsize=(8, 8))
                self.soil_plot = self.fig.add_subplot(111)

                # Create canvas
                self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

                # Add toolbar
                toolbar = NavigationToolbar2Tk(self.canvas, parent)
                toolbar.update()

            def initialize_plot(self):
                if self.soil_plot:
                    self.soil_plot.clear()
                    self.soil_plot.set_xlabel('Liquid Limit (%)')
                    self.soil_plot.set_ylabel('Plasticity Index (%)')
                    self.soil_plot.set_xlim(0, 100)
                    self.soil_plot.set_ylim(0, 60)
                    self.soil_plot.grid(True)
                    self.canvas.draw()

            def update_results(self, text):
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, text)

            def validate_input(self, value):
                try:
                    float_value = float(value)
                    # Extended validation rules
                    if float_value < 0:
                        messagebox.showwarning("Warning", "Value cannot be negative")
                        return False
                    if float_value > 100:
                        messagebox.showwarning("Warning", "Value cannot exceed 100%")
                        return False
                    return True
                except ValueError:
                    messagebox.showwarning("Warning", "Please enter a valid number")
                    return False

            def get_entry_value(self, key):
                try:
                    value = float(self.entries[key].get())
                    if self.validate_input(str(value)):
                        return value
                    return None
                except:
                    return None

            def calculate_indices(self):
                ll = self.get_entry_value('liquid_limit')
                pl = self.get_entry_value('plastic_limit')
                wc = self.get_entry_value('water_content')
                sl = self.get_entry_value('shrinkage_limit')

                indices = {'shrinkage_index': None, 'liquidity_index': None, 'consistency_index': None}
                
                if ll is not None and sl is not None:
                    indices['shrinkage_index'] = ll - sl
                    
                if ll is not None and pl is not None and wc is not None:
                    try:
                        indices['liquidity_index'] = (wc - pl) / (ll - pl)
                        indices['consistency_index'] = (ll - wc) / (ll - pl)
                    except:
                        pass
                    
                return indices

            def get_soil_consistency(self, ci):
                if ci is None:
                    return "Not available"
                if ci <= 0:
                    return "Very Soft"
                elif ci <= 0.25:
                    return "Soft"
                elif ci <= 0.50:
                    return "Medium Soft"
                elif ci <= 0.75:
                    return "Stiff"
                elif ci <= 1.00:
                    return "Very Stiff"
                else:
                    return "Hard"

            def classify_soil(self, soil_type='fine'):
                """Classify soil based on its properties."""
                try:
                    if soil_type == 'fine':
                        self._classify_fine_grained()
                    else:
                        self._classify_coarse_grained()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

            def _classify_coarse_grained(self):
                """Classify coarse-grained soil according to IS 1498:1970."""
                try:
                    # Get input values
                    gravel = self.get_entry_value('gravel_fraction')
                    sand = self.get_entry_value('sand_fraction')
                    fines = self.get_entry_value('fines_fraction')
                    cu = self.get_entry_value('cu')
                    cc = self.get_entry_value('cc')

                    # Validate inputs
                    if None in [gravel, sand, fines]:
                        messagebox.showerror("Error", "Please enter valid percentages for grain size distribution")
                        return

                    # Check if percentages sum to approximately 100%
                    total = gravel + sand + fines
                    if not (98 <= total <= 102):
                        messagebox.showerror("Error", f"Grain size percentages sum to {total}%. Should be close to 100%")
                        return

                    # Store current data
                    self.current_data = {
                        'Gravel Fraction': gravel,
                        'Sand Fraction': sand,
                        'Fines Fraction': fines,
                        'Coefficient of Uniformity (Cu)': cu if cu is not None else 'N/A',
                        'Coefficient of Curvature (Cc)': cc if cc is not None else 'N/A'
                    }

                    # Determine primary soil type
                    if gravel > sand:
                        primary_type = "G (Gravel)"
                        secondary_fraction = sand
                    else:
                        primary_type = "S (Sand)"
                        secondary_fraction = gravel

                    # Determine gradation and secondary characteristics
                    if fines < 5:  # Clean gravel/sand
                        if cu is None or cc is None:
                            messagebox.showerror("Error", "Please enter Cu and Cc values for clean coarse soil")
                            return
                            
                        if cu >= 4 and (1 <= cc <= 3):
                            gradation = "W (Well graded)"
                        else:
                            gradation = "P (Poorly graded)"
                        
                        classification = f"{primary_type[0]}{gradation}"
                        
                    elif 5 <= fines <= 12:  # With fines
                        if cu is None or cc is None:
                            messagebox.showerror("Error", "Please enter Cu and Cc values")
                            return
                            
                        if cu >= 4 and (1 <= cc <= 3):
                            gradation = "W"
                        else:
                            gradation = "P"
                            
                        # Get fine-grained properties for classification
                        ll = self.get_entry_value('liquid_limit')
                        pl = self.get_entry_value('plastic_limit')
                        
                        if ll is not None and pl is not None:
                            pi = ll - pl
                            if pi < 4 or (ll < 25.5 and pi < 0.73 * (ll - 20)):
                                suffix = "M"
                            else:
                                suffix = "C"
                        else:
                            suffix = "M"  # Default to M if no plasticity data
                            
                        classification = f"{primary_type[0]}{gradation}-{suffix}"
                        
                    else:  # More than 12% fines
                        # Need plasticity data
                        ll = self.get_entry_value('liquid_limit')
                        pl = self.get_entry_value('plastic_limit')
                        
                        if ll is None or pl is None:
                            messagebox.showerror("Error", "Please enter Liquid Limit and Plastic Limit for soil with >12% fines")
                            return
                            
                        pi = ll - pl
                        if pi < 4 or (ll < 25.5 and pi < 0.73 * (ll - 20)):
                            suffix = "M"
                        else:
                            suffix = "C"
                            
                        classification = f"{primary_type[0]}{suffix}"

                    # Prepare detailed description
                    description = f"Primary Soil Type: {primary_type}\n"
                    description += f"Secondary Fraction: {secondary_fraction:.1f}%\n"
                    description += f"Fines Content: {fines:.1f}%\n"
                    
                    if cu is not None:
                        description += f"Coefficient of Uniformity (Cu): {cu:.2f}\n"
                    if cc is not None:
                        description += f"Coefficient of Curvature (Cc): {cc:.2f}\n"
                        
                    description += f"\nClassification: {classification}\n"
                    
                    if "W" in classification:
                        description += "\nWell graded soil with good particle size distribution"
                    elif "P" in classification:
                        description += "\nPoorly graded soil with uniform particle size distribution"
                        
                    if "M" in classification:
                        description += "\nWith non-plastic or low plasticity fines"
                    elif "C" in classification:
                        description += "\nWith plastic fines"

                    # Update results
                    self.update_results(description)
                    
                    # Update plot with grain size distribution
                    self._plot_grain_size_distribution(gravel, sand, fines)

                    # Add to history
                    history_item = {
                        'timestamp': datetime.now().isoformat(),
                        'results': description,
                        'data': self.current_data.copy()
                    }
                    self.history.append(history_item)

                    # Save last session
                    self.save_last_session()

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

            def _plot_grain_size_distribution(self, gravel, sand, fines):
                """Plot grain size distribution chart."""
                try:
                    self.soil_plot.clear()
                    
                    # Create bar chart
                    categories = ['Gravel\n>4.75mm', 'Sand\n4.75-0.075mm', 'Fines\n<0.075mm']
                    values = [gravel, sand, fines]
                    colors = ['#8B4513', '#DAA520', '#F4A460']
                    
                    bars = self.soil_plot.bar(categories, values, color=colors)
                    
                    # Customize the plot
                    self.soil_plot.set_ylabel('Percentage (%)')
                    self.soil_plot.set_title('Grain Size Distribution')
                    
                    # Add value labels on top of bars
                    for bar in bars:
                        height = bar.get_height()
                        self.soil_plot.text(bar.get_x() + bar.get_width()/2., height,
                                          f'{height:.1f}%',
                                          ha='center', va='bottom')
                    
                    # Set y-axis limit to 100%
                    self.soil_plot.set_ylim(0, 100)
                    
                    # Add grid
                    self.soil_plot.grid(True, axis='y', linestyle='--', alpha=0.7)
                    
                    # Update canvas
                    self.canvas.draw()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to plot grain size distribution: {str(e)}")

            def _classify_fine_grained(self):
                """Classify fine-grained soil according to IS 1498:1970."""
                try:
                    # Validate required inputs
                    ll = self.get_entry_value('liquid_limit')
                    pl = self.get_entry_value('plastic_limit')
                    
                    if ll is None or pl is None:
                        messagebox.showerror("Error", "Please enter valid values (0-100) for Liquid Limit and Plastic Limit")
                        return

                    if pl >= ll:
                        messagebox.showerror("Error", "Plastic Limit must be less than Liquid Limit")
                        return

                    plastic_index = ll - pl
                    
                    # Store current data
                    self.current_data = {
                        'Liquid Limit': ll,
                        'Plastic Limit': pl,
                        'Plasticity Index': plastic_index
                    }

                    # A-line equation according to IS 1498:1970
                    a_line = 0.73 * (ll - 20)
                    
                    # Clear and update plot
                    self.soil_plot.clear()
                    
                    # Plot A-line and U-line
                    self.soil_plot.plot(range(0, 101), [0.73 * (x - 20) for x in range(0, 101)], label='A-line')
                    self.soil_plot.plot(range(0, 101), [0.9 * (x - 8) for x in range(0, 101)], label='U-line')
                    
                    # Plot vertical lines
                    self.soil_plot.axvline(x=35, color='gray', linestyle='--', label='LL=35')
                    self.soil_plot.axvline(x=50, color='gray', linestyle='--', label='LL=50')
                    
                    # Plot sample point
                    self.soil_plot.scatter([ll], [plastic_index], c='red', marker='o', label='Sample Point')
                    
                    # Draw horizontal lines
                    self.soil_plot.axhline(y=4, xmin=0.12, xmax=0.25, color='gray', linestyle='--')
                    self.soil_plot.axhline(y=7, xmin=0, xmax=0.3, color='gray', linestyle='--')
                    
                    # Add labels
                    self.soil_plot.text(10, 25, 'CL', fontsize=12, ha='center', va='center')
                    self.soil_plot.text(40, 35, 'CI', fontsize=12, ha='center', va='center')
                    self.soil_plot.text(55, 55, 'CH', fontsize=12, ha='center', va='center')
                    self.soil_plot.text(2, 2, 'ML', fontsize=10, ha='center', va='center')
                    self.soil_plot.text(20, 5.5, 'CL-ML', fontsize=10, ha='center', va='center')
                    self.soil_plot.text(30, 2, 'ML or OL', fontsize=10, ha='center', va='center')
                    self.soil_plot.text(43, 4, 'MI or OI', fontsize=12, ha='center', va='center')
                    self.soil_plot.text(60, 10, 'MH or OH', fontsize=12, ha='center', va='center')
                    
                    # Update plot settings
                    self.soil_plot.set_xlabel('Liquid Limit (%)')
                    self.soil_plot.set_ylabel('Plasticity Index (%)')
                    self.soil_plot.set_xlim(0, 100)
                    self.soil_plot.set_ylim(0, 60)
                    self.soil_plot.grid(True)
                    self.soil_plot.legend()
                    
                    # Update canvas
                    self.canvas.draw()

                    # Classify soil
                    if ll < 35:
                        compressibility = 'Low -[L]'
                    elif ll <= 50:
                        compressibility = 'Intermediate -[I]'
                    else:
                        compressibility = 'High -[H]'
                    
                    if plastic_index > a_line:
                        soil_type = f'Clay -[C] (Inorganic)'
                    else:
                        soil_type = f'Silt -[M] or Organic soil -[O]'

                    if ll < 35 and plastic_index < 12:
                        expansion = "Low (Non-critical)"
                    elif ll <= 50 and plastic_index <= 23:
                        expansion = "Medium (Marginal)"
                    elif ll <= 70 and plastic_index <= 32:
                        expansion = "High (Critical)"
                    else:
                        expansion = "Very High (Severe)"

                    # Calculate indices
                    indices = self.calculate_indices()
                    consistency = self.get_soil_consistency(indices['consistency_index'])

                    if plastic_index < 7:
                        toughness = "Low toughness"
                    elif plastic_index <= 17:
                        toughness = "Medium toughness"
                    else:
                        toughness = "High toughness"

                    # Calculate activity
                    clay_fraction = self.get_entry_value('clay_fraction')
                    if clay_fraction is not None:
                        activity = plastic_index / clay_fraction
                        if activity < 0.75:
                            activity_class = "Inactive"
                        elif activity <= 1.25:
                            activity_class = "Normal"
                        else:
                            activity_class = "Active"
                    else:
                        activity = None
                        activity_class = "Not available"

                    # Prepare results
                    result = f'Plasticity Index: {plastic_index:.2f}\n' \
                            f'A-line Value: {a_line:.2f}\n' \
                            f'Soil Classification: {soil_type}\n' \
                            f'Compressibility: {compressibility}\n' \
                            f'Degree of Expansion: {expansion}\n' \
                            f'Toughness: {toughness}\n'
                    
                    if indices['shrinkage_index'] is not None:
                        result += f'Shrinkage Index: {indices["shrinkage_index"]:.2f}\n'
                    
                    if indices['liquidity_index'] is not None:
                        result += f'Liquidity Index: {indices["liquidity_index"]:.2f}\n'
                    
                    if indices['consistency_index'] is not None:
                        result += f'Consistency Index: {indices["consistency_index"]:.2f}\n' \
                                 f'Soil Consistency: {consistency}\n'
                    
                    if activity is not None:
                        result += f'Activity: {activity:.2f}\n' \
                                 f'Activity Classification: {activity_class}\n'

                    # Add to history
                    history_item = {
                        'timestamp': datetime.now().isoformat(),
                        'results': result,
                        'data': self.current_data.copy()
                    }
                    self.history.append(history_item)

                    # Save last session
                    self.save_last_session()

                    self.update_results(result)

                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {str(e)}")

            def on_closing(self):
                """Clean up resources and close the application."""
                try:
                    self.save_last_session()
                    if hasattr(self, 'fig') and self.fig is not None:
                        plt.close(self.fig)
                    if hasattr(self, 'root') and self.root is not None:
                        self.root.destroy()
                except Exception as e:
                    print(f"Error during cleanup: {str(e)}")
                    try:
                        if hasattr(self, 'root') and self.root is not None:
                            self.root.destroy()
                    except:
                        sys.exit(1)

            def compare_samples(self):
                """Compare multiple soil samples."""
                if not self.history:
                    messagebox.showwarning("Warning", "No samples in history to compare!")
                    return
                
                compare_window = tk.Toplevel(self.root)
                compare_window.title("Compare Soil Samples")
                compare_window.geometry("800x600")
                
                # Create comparison table
                columns = ("Timestamp", "Type", "Classification", "Key Properties")
                tree = ttk.Treeview(compare_window, columns=columns, show='headings')
                
                # Set column headings
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                
                # Add data
                for item in self.history:
                    soil_type = "Coarse-grained" if 'Gravel Fraction' in item['data'] else "Fine-grained"
                    classification = item['results'].split('\n')[0] if item['results'] else "N/A"
                    key_props = []
                    if 'Gravel Fraction' in item['data']:
                        key_props.append(f"Gravel: {item['data']['Gravel Fraction']:.1f}%")
                    if 'Liquid Limit' in item['data']:
                        key_props.append(f"LL: {item['data']['Liquid Limit']:.1f}")
                    
                    tree.insert('', tk.END, values=(
                        item['timestamp'].split('T')[0],
                        soil_type,
                        classification,
                        ', '.join(key_props)
                    ))
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(compare_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                # Pack widgets
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Add export button
                ttk.Button(compare_window, text="Export Comparison", 
                          command=lambda: self.export_comparison(tree)).pack(pady=10)

            def statistical_analysis(self):
                """Perform statistical analysis on soil samples."""
                if not self.history:
                    messagebox.showwarning("Warning", "No samples to analyze!")
                    return
                
                stats_window = tk.Toplevel(self.root)
                stats_window.title("Statistical Analysis")
                stats_window.geometry("600x400")
                
                # Create text widget for results
                text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD, width=70, height=20)
                text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                # Separate fine and coarse-grained samples
                fine_samples = []
                coarse_samples = []
                
                for item in self.history:
                    if 'Gravel Fraction' in item['data']:
                        coarse_samples.append(item['data'])
                    else:
                        fine_samples.append(item['data'])
                
                # Analyze fine-grained samples
                if fine_samples:
                    text.insert(tk.END, "Fine-Grained Soil Statistics:\n")
                    text.insert(tk.END, "=" * 40 + "\n\n")
                    
                    ll_values = [sample['Liquid Limit'] for sample in fine_samples]
                    pi_values = [sample['Plasticity Index'] for sample in fine_samples]
                    
                    text.insert(tk.END, f"Number of Samples: {len(fine_samples)}\n\n")
                    text.insert(tk.END, "Liquid Limit Statistics:\n")
                    text.insert(tk.END, f"Mean: {np.mean(ll_values):.2f}\n")
                    text.insert(tk.END, f"Standard Deviation: {np.std(ll_values):.2f}\n")
                    text.insert(tk.END, f"Range: {max(ll_values) - min(ll_values):.2f}\n\n")
                    
                    text.insert(tk.END, "Plasticity Index Statistics:\n")
                    text.insert(tk.END, f"Mean: {np.mean(pi_values):.2f}\n")
                    text.insert(tk.END, f"Standard Deviation: {np.std(pi_values):.2f}\n")
                    text.insert(tk.END, f"Range: {max(pi_values) - min(pi_values):.2f}\n\n")
                
                # Analyze coarse-grained samples
                if coarse_samples:
                    text.insert(tk.END, "Coarse-Grained Soil Statistics:\n")
                    text.insert(tk.END, "=" * 40 + "\n\n")
                    
                    gravel_values = [sample['Gravel Fraction'] for sample in coarse_samples]
                    sand_values = [sample['Sand Fraction'] for sample in coarse_samples]
                    fines_values = [sample['Fines Fraction'] for sample in coarse_samples]
                    
                    text.insert(tk.END, f"Number of Samples: {len(coarse_samples)}\n\n")
                    text.insert(tk.END, "Gravel Content Statistics:\n")
                    text.insert(tk.END, f"Mean: {np.mean(gravel_values):.2f}%\n")
                    text.insert(tk.END, f"Standard Deviation: {np.std(gravel_values):.2f}%\n")
                    text.insert(tk.END, f"Range: {max(gravel_values) - min(gravel_values):.2f}%\n\n")
                    
                    text.insert(tk.END, "Sand Content Statistics:\n")
                    text.insert(tk.END, f"Mean: {np.mean(sand_values):.2f}%\n")
                    text.insert(tk.END, f"Standard Deviation: {np.std(sand_values):.2f}%\n")
                    text.insert(tk.END, f"Range: {max(sand_values) - min(sand_values):.2f}%\n\n")
                    
                    text.insert(tk.END, "Fines Content Statistics:\n")
                    text.insert(tk.END, f"Mean: {np.mean(fines_values):.2f}%\n")
                    text.insert(tk.END, f"Standard Deviation: {np.std(fines_values):.2f}%\n")
                    text.insert(tk.END, f"Range: {max(fines_values) - min(fines_values):.2f}%\n")

            def show_soil_properties(self):
                """Show comprehensive soil properties guide."""
                guide_window = tk.Toplevel(self.root)
                guide_window.title("Soil Properties Guide")
                guide_window.geometry("800x600")
                
                # Create notebook for different property categories
                notebook = ttk.Notebook(guide_window)
                notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Physical properties tab
                physical_frame = ttk.Frame(notebook)
                notebook.add(physical_frame, text='Physical Properties')
                
                physical_text = scrolledtext.ScrolledText(physical_frame, wrap=tk.WORD)
                physical_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                physical_text.insert(tk.END, "Physical Properties of Soils\n\n")
                physical_text.insert(tk.END, "1. Particle Size Distribution\n")
                physical_text.insert(tk.END, "   - Gravel: >4.75mm\n")
                physical_text.insert(tk.END, "   - Sand: 4.75mm - 0.075mm\n")
                physical_text.insert(tk.END, "   - Silt: 0.075mm - 0.002mm\n")
                physical_text.insert(tk.END, "   - Clay: <0.002mm\n\n")
                physical_text.insert(tk.END, "2. Atterberg Limits\n")
                physical_text.insert(tk.END, "   - Liquid Limit (LL)\n")
                physical_text.insert(tk.END, "   - Plastic Limit (PL)\n")
                physical_text.insert(tk.END, "   - Shrinkage Limit (SL)\n")
                physical_text.insert(tk.END, "   - Plasticity Index (PI) = LL - PL\n\n")
                
                # Engineering properties tab
                engineering_frame = ttk.Frame(notebook)
                notebook.add(engineering_frame, text='Engineering Properties')
                
                engineering_text = scrolledtext.ScrolledText(engineering_frame, wrap=tk.WORD)
                engineering_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                engineering_text.insert(tk.END, "Engineering Properties\n\n")
                engineering_text.insert(tk.END, "1. Shear Strength\n")
                engineering_text.insert(tk.END, "2. Compressibility\n")
                engineering_text.insert(tk.END, "3. Permeability\n")
                engineering_text.insert(tk.END, "4. Compaction Characteristics\n")
                
                # Classification systems tab
                classification_frame = ttk.Frame(notebook)
                notebook.add(classification_frame, text='Classification Systems')
                
                classification_text = scrolledtext.ScrolledText(classification_frame, wrap=tk.WORD)
                classification_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                classification_text.insert(tk.END, "Soil Classification Systems\n\n")
                classification_text.insert(tk.END, "1. IS Classification (IS 1498:1970)\n")
                classification_text.insert(tk.END, "2. Unified Soil Classification System (USCS)\n")
                classification_text.insert(tk.END, "3. AASHTO Classification System\n")

            def show_engineering_applications(self):
                """Show engineering applications of different soil types."""
                apps_window = tk.Toplevel(self.root)
                apps_window.title("Engineering Applications")
                apps_window.geometry("800x600")
                
                text = scrolledtext.ScrolledText(apps_window, wrap=tk.WORD)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                text.insert(tk.END, "Engineering Applications of Different Soil Types\n\n")
                text.insert(tk.END, "1. Coarse-Grained Soils (GW, GP, SW, SP)\n")
                text.insert(tk.END, "   - Excellent drainage characteristics\n")
                text.insert(tk.END, "   - High strength and stability\n")
                text.insert(tk.END, "   - Suitable for:\n")
                text.insert(tk.END, "     * Road base and sub-base\n")
                text.insert(tk.END, "     * Dam construction (filters)\n")
                text.insert(tk.END, "     * Foundation support\n\n")
                
                text.insert(tk.END, "2. Fine-Grained Soils (CL, CH, ML, MH)\n")
                text.insert(tk.END, "   - Low permeability\n")
                text.insert(tk.END, "   - Compressible nature\n")
                text.insert(tk.END, "   - Applications:\n")
                text.insert(tk.END, "     * Clay liners\n")
                text.insert(tk.END, "     * Earth dams (core)\n")
                text.insert(tk.END, "     * Impervious barriers\n\n")
                
                text.insert(tk.END, "3. Special Considerations\n")
                text.insert(tk.END, "   - Expansive soils (CH)\n")
                text.insert(tk.END, "   - Collapsible soils\n")
                text.insert(tk.END, "   - Organic soils\n")

            def show_correlations(self):
                """Show correlations between soil properties."""
                if len(self.history) < 2:
                    messagebox.showwarning("Warning", "Need at least 2 samples for correlation analysis!")
                    return
                
                corr_window = tk.Toplevel(self.root)
                corr_window.title("Correlation Analysis")
                corr_window.geometry("600x400")
                
                # Create figure for correlation plots
                fig = Figure(figsize=(8, 6))
                ax = fig.add_subplot(111)
                
                # Separate fine and coarse-grained samples
                fine_samples = [item['data'] for item in self.history if 'Liquid Limit' in item['data']]
                coarse_samples = [item['data'] for item in self.history if 'Gravel Fraction' in item['data']]
                
                if fine_samples:
                    # Plot LL vs PI correlation
                    ll_values = [sample['Liquid Limit'] for sample in fine_samples]
                    pi_values = [sample['Plasticity Index'] for sample in fine_samples]
                    
                    ax.scatter(ll_values, pi_values, alpha=0.6)
                    ax.set_xlabel('Liquid Limit (%)')
                    ax.set_ylabel('Plasticity Index (%)')
                    ax.set_title('Liquid Limit vs Plasticity Index')
                    
                    # Add A-line
                    x = np.array([0, 100])
                    ax.plot(x, 0.73 * (x - 20), 'r--', label='A-line')
                    ax.legend()
                
                elif coarse_samples:
                    # Plot gravel vs sand content
                    gravel_values = [sample['Gravel Fraction'] for sample in coarse_samples]
                    sand_values = [sample['Sand Fraction'] for sample in coarse_samples]
                    
                    ax.scatter(gravel_values, sand_values, alpha=0.6)
                    ax.set_xlabel('Gravel Content (%)')
                    ax.set_ylabel('Sand Content (%)')
                    ax.set_title('Gravel vs Sand Content')
                
                # Create canvas
                canvas = FigureCanvasTkAgg(fig, master=corr_window)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            def show_user_guide(self):
                """Show user guide in a new window."""
                guide_window = tk.Toplevel(self.root)
                guide_window.title("User Guide")
                guide_window.geometry("800x600")
                
                text = scrolledtext.ScrolledText(guide_window, wrap=tk.WORD)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                text.insert(tk.END, "Soil Classification Tool - User Guide\n\n")
                text.insert(tk.END, "1. Getting Started\n")
                text.insert(tk.END, "   - Choose soil type (Fine-grained or Coarse-grained)\n")
                text.insert(tk.END, "   - Enter required parameters\n")
                text.insert(tk.END, "   - Click 'Classify' button\n\n")
                
                text.insert(tk.END, "2. Fine-grained Soils\n")
                text.insert(tk.END, "   Required parameters:\n")
                text.insert(tk.END, "   - Liquid Limit (LL)\n")
                text.insert(tk.END, "   - Plastic Limit (PL)\n")
                text.insert(tk.END, "   Optional parameters:\n")
                text.insert(tk.END, "   - Natural Water Content\n")
                text.insert(tk.END, "   - Shrinkage Limit\n")
                text.insert(tk.END, "   - Clay Fraction\n\n")
                
                text.insert(tk.END, "3. Coarse-grained Soils\n")
                text.insert(tk.END, "   Required parameters:\n")
                text.insert(tk.END, "   - Gravel Fraction\n")
                text.insert(tk.END, "   - Sand Fraction\n")
                text.insert(tk.END, "   - Fines Fraction\n")
                text.insert(tk.END, "   Additional parameters (if fines ≤12%):\n")
                text.insert(tk.END, "   - Coefficient of Uniformity (Cu)\n")
                text.insert(tk.END, "   - Coefficient of Curvature (Cc)\n\n")
                
                text.insert(tk.END, "4. Tools and Features\n")
                text.insert(tk.END, "   - Save/Load: Save current data or load previous data\n")
                text.insert(tk.END, "   - Export: Generate PDF report with results\n")
                text.insert(tk.END, "   - Compare: Compare multiple soil samples\n")
                text.insert(tk.END, "   - Statistics: View statistical analysis of samples\n")
                text.insert(tk.END, "   - Correlations: Analyze relationships between properties\n")

            def show_is_code(self):
                """Show IS Code reference."""
                code_window = tk.Toplevel(self.root)
                code_window.title("IS Code Reference")
                code_window.geometry("800x600")
                
                text = scrolledtext.ScrolledText(code_window, wrap=tk.WORD)
                text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                text.insert(tk.END, "IS 1498:1970 - Classification and Identification of Soils\n\n")
                text.insert(tk.END, "1. Scope\n")
                text.insert(tk.END, "   This standard covers the classification and identification of soils for\n")
                text.insert(tk.END, "   general engineering purposes based on laboratory determination of particle\n")
                text.insert(tk.END, "   size characteristics, liquid limit, and plasticity index.\n\n")
                
                text.insert(tk.END, "2. Classification System\n")
                text.insert(tk.END, "   2.1 Coarse-grained Soils (>50% retained on 75-micron IS Sieve)\n")
                text.insert(tk.END, "       - Gravels (G): >50% of coarse fraction retained on 4.75mm sieve\n")
                text.insert(tk.END, "       - Sands (S): >50% of coarse fraction passing 4.75mm sieve\n\n")
                
                text.insert(tk.END, "   2.2 Fine-grained Soils (>50% passing 75-micron IS Sieve)\n")
                text.insert(tk.END, "       - Silts (M)\n")
                text.insert(tk.END, "       - Clays (C)\n")
                text.insert(tk.END, "       - Organic Soils (O)\n\n")
                
                text.insert(tk.END, "3. Plasticity Characteristics\n")
                text.insert(tk.END, "   - Low Plasticity (L): LL < 35\n")
                text.insert(tk.END, "   - Intermediate Plasticity (I): 35 ≤ LL ≤ 50\n")
                text.insert(tk.END, "   - High Plasticity (H): LL > 50\n\n")
                
                text.insert(tk.END, "4. Gradation Characteristics\n")
                text.insert(tk.END, "   Well Graded (W):\n")
                text.insert(tk.END, "   - Cu > 4 for gravels, Cu > 6 for sands\n")
                text.insert(tk.END, "   - 1 < Cc < 3\n")
                text.insert(tk.END, "   Poorly Graded (P): Not meeting above criteria\n")

            def show_about(self):
                """Show about dialog."""
                about_text = """Dhara Netra v1.0

Based on IS 1498:1970
Indian Standard Classification and Identification of Soils
for General Engineering Purposes

Features:
- Fine and coarse-grained soil classification
- Plasticity chart plotting
- Grain size distribution analysis
- Statistical analysis
- Sample comparison
- PDF report generation

Created using Python with tkinter, matplotlib, and reportlab
"""
                messagebox.showinfo("About", about_text)

            def export_comparison(self, tree):
                """Export comparison data to PDF."""
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")]
                )
                
                if not file_path:
                    return
                
                # Create PDF
                doc = SimpleDocTemplate(file_path, pagesize=A4)
                elements = []
                
                # Title
                styles = getSampleStyleSheet()
                elements.append(Paragraph("Soil Sample Comparison", styles['Title']))
                elements.append(Spacer(1, 20))
                
                # Create table data
                data = [["Timestamp", "Type", "Classification", "Key Properties"]]
                for item in tree.get_children():
                    data.append(list(tree.item(item)['values']))
                
                # Create table
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(table)
                
                # Build PDF
                doc.build(elements)
                messagebox.showinfo("Success", "Comparison exported successfully!")

            def import_data(self, file_path=None):
                """Import data from CSV or Excel files."""
                if not file_path:
                    file_path = filedialog.askopenfilename(
                        filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")]
                    )
                if not file_path:
                    return
                
                try:
                    if file_path.endswith('.csv'):
                        with open(file_path, 'r') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                # Convert string values to float
                                data = {k: float(v) if v.replace('.','',1).isdigit() else v 
                                       for k, v in row.items()}
                                self.history.append({
                                    'timestamp': datetime.now().isoformat(),
                                    'data': data,
                                    'results': self.classify_from_data(data)
                                })
                    else:
                        messagebox.showinfo("Info", "Excel import requires pandas library")
                    
                    messagebox.showinfo("Success", "Data imported successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to import data: {str(e)}")

            def batch_processing(self):
                """Process multiple samples from a file."""
                file_paths = filedialog.askopenfilenames(
                    filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")]
                )
                if not file_paths:
                    return
                
                batch_window = tk.Toplevel(self.root)
                batch_window.title("Batch Processing")
                batch_window.geometry("800x600")
                
                # Create progress frame
                progress_frame = ttk.LabelFrame(batch_window, text="Progress")
                progress_frame.pack(fill=tk.X, padx=10, pady=5)
                
                progress_var = tk.DoubleVar()
                progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
                progress_bar.pack(fill=tk.X, padx=5, pady=5)
                
                # Create results text
                results_text = scrolledtext.ScrolledText(batch_window, wrap=tk.WORD)
                results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Process files
                total_files = len(file_paths)
                for i, file_path in enumerate(file_paths):
                    try:
                        results_text.insert(tk.END, f"\nProcessing {os.path.basename(file_path)}...\n")
                        # Process file
                        self.import_data(file_path)
                        results_text.insert(tk.END, "Successfully processed\n")
                        progress_var.set((i + 1) / total_files * 100)
                        batch_window.update()
                    except Exception as e:
                        results_text.insert(tk.END, f"Error: {str(e)}\n")
                
                ttk.Button(batch_window, text="Export Results", 
                          command=lambda: self.export_batch_results(results_text.get(1.0, tk.END))).pack(pady=5)

            def show_trend_analysis(self):
                """Show trends in soil properties over time."""
                if len(self.history) < 2:
                    messagebox.showwarning("Warning", "Need at least 2 samples for trend analysis!")
                    return
                
                trend_window = tk.Toplevel(self.root)
                trend_window.title("Trend Analysis")
                trend_window.geometry("800x600")
                
                # Create figure
                fig = Figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                
                # Get data
                dates = [datetime.fromisoformat(item['timestamp']) for item in self.history]
                
                # Plot different properties based on soil type
                if 'Liquid Limit' in self.history[0]['data']:
                    values = [item['data']['Liquid Limit'] for item in self.history]
                    property_name = 'Liquid Limit'
                else:
                    values = [item['data']['Gravel Fraction'] for item in self.history]
                    property_name = 'Gravel Content'
                
                # Plot trend
                ax.plot(dates, values, 'o-')
                ax.set_xlabel('Date')
                ax.set_ylabel(property_name)
                ax.set_title(f'{property_name} Trend Over Time')
                fig.autofmt_xdate()
                
                # Create canvas
                canvas = FigureCanvasTkAgg(fig, master=trend_window)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Add toolbar
                toolbar = NavigationToolbar2Tk(canvas, trend_window)
                toolbar.update()

            def show_project_database(self):
                """Show and manage project database."""
                db_window = tk.Toplevel(self.root)
                db_window.title("Project Database")
                db_window.geometry("1000x600")
                
                # Create database if not exists
                conn = sqlite3.connect('soil_projects.db')
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS projects
                           (id INTEGER PRIMARY KEY,
                            project_name TEXT,
                            location TEXT,
                            date TEXT,
                            soil_type TEXT,
                            properties TEXT,
                            notes TEXT)''')
                conn.commit()
                
                # Create frames
                control_frame = ttk.Frame(db_window)
                control_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Add project button
                ttk.Button(control_frame, text="Add Project", 
                          command=self.add_project).pack(side=tk.LEFT, padx=5)
                
                # Search frame
                search_frame = ttk.LabelFrame(control_frame, text="Search")
                search_frame.pack(side=tk.LEFT, padx=5)
                
                ttk.Entry(search_frame).pack(side=tk.LEFT, padx=5)
                ttk.Button(search_frame, text="Search").pack(side=tk.LEFT, padx=5)
                
                # Create treeview
                columns = ("Project", "Location", "Date", "Soil Type", "Properties")
                tree = ttk.Treeview(db_window, columns=columns, show='headings')
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                
                tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(db_window, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            def add_project(self):
                """Add new project to database."""
                project_window = tk.Toplevel(self.root)
                project_window.title("Add Project")
                project_window.geometry("400x500")
                
                # Create form
                ttk.Label(project_window, text="Project Name:").pack(padx=10, pady=5)
                name_entry = ttk.Entry(project_window)
                name_entry.pack(fill=tk.X, padx=10)
                
                ttk.Label(project_window, text="Location:").pack(padx=10, pady=5)
                location_entry = ttk.Entry(project_window)
                location_entry.pack(fill=tk.X, padx=10)
                
                ttk.Label(project_window, text="Date:").pack(padx=10, pady=5)
                date_entry = ttk.Entry(project_window)
                date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                date_entry.pack(fill=tk.X, padx=10)
                
                ttk.Label(project_window, text="Soil Type:").pack(padx=10, pady=5)
                soil_type = ttk.Combobox(project_window, 
                                       values=['Fine-grained', 'Coarse-grained'])
                soil_type.pack(fill=tk.X, padx=10)
                
                ttk.Label(project_window, text="Notes:").pack(padx=10, pady=5)
                notes_text = scrolledtext.ScrolledText(project_window, height=6)
                notes_text.pack(fill=tk.X, padx=10)
                
                def save_project():
                    conn = sqlite3.connect('soil_projects.db')
                    c = conn.cursor()
                    c.execute('''INSERT INTO projects 
                               (project_name, location, date, soil_type, notes)
                               VALUES (?, ?, ?, ?, ?)''',
                             (name_entry.get(), location_entry.get(), 
                              date_entry.get(), soil_type.get(), 
                              notes_text.get(1.0, tk.END)))
                    conn.commit()
                    conn.close()
                    project_window.destroy()
                    messagebox.showinfo("Success", "Project added successfully!")
                
                ttk.Button(project_window, text="Save Project", 
                          command=save_project).pack(pady=10)

            def customize_plot(self):
                """Customize plot appearance."""
                custom_window = tk.Toplevel(self.root)
                custom_window.title("Customize Plot")
                custom_window.geometry("400x500")
                
                # Style frame
                style_frame = ttk.LabelFrame(custom_window, text="Style Settings")
                style_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Title settings
                ttk.Label(style_frame, text="Title:").pack(padx=5, pady=2)
                title_entry = ttk.Entry(style_frame)
                title_entry.pack(fill=tk.X, padx=5)
                
                # Font size
                ttk.Label(style_frame, text="Font Size:").pack(padx=5, pady=2)
                font_size = ttk.Spinbox(style_frame, from_=8, to=24)
                font_size.pack(fill=tk.X, padx=5)
                
                # Color settings
                color_frame = ttk.LabelFrame(custom_window, text="Colors")
                color_frame.pack(fill=tk.X, padx=10, pady=5)
                
                def choose_color(button):
                    color = colorchooser.askcolor(title="Choose Color")[1]
                    if color:
                        button.configure(bg=color)
                
                ttk.Label(color_frame, text="Background:").pack(side=tk.LEFT, padx=5)
                bg_button = tk.Button(color_frame, text="Pick Color", 
                                    command=lambda: choose_color(bg_button))
                bg_button.pack(side=tk.LEFT, padx=5)
                
                # Grid settings
                grid_frame = ttk.LabelFrame(custom_window, text="Grid")
                grid_frame.pack(fill=tk.X, padx=10, pady=5)
                
                grid_var = tk.BooleanVar(value=True)
                ttk.Checkbutton(grid_frame, text="Show Grid", 
                               variable=grid_var).pack(padx=5)
                
                def apply_settings():
                    try:
                        self.soil_plot.set_title(title_entry.get())
                        plt.rcParams['font.size'] = int(font_size.get())
                        self.soil_plot.grid(grid_var.get())
                        self.canvas.draw()
                        custom_window.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
                
                ttk.Button(custom_window, text="Apply", 
                          command=apply_settings).pack(pady=10)

            def show_3d_visualization(self):
                """Show 3D visualization of soil properties."""
                if len(self.history) < 3:
                    messagebox.showwarning("Warning", "Need at least 3 samples for 3D visualization!")
                    return
                
                viz_window = tk.Toplevel(self.root)
                viz_window.title("3D Visualization")
                viz_window.geometry("800x600")
                
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                
                if 'Liquid Limit' in self.history[0]['data']:
                    # Fine-grained soil
                    x = [item['data']['Liquid Limit'] for item in self.history]
                    y = [item['data']['Plastic Limit'] for item in self.history]
                    z = [item['data'].get('Clay Fraction', 0) for item in self.history]
                    ax.set_xlabel('Liquid Limit (%)')
                    ax.set_ylabel('Plastic Limit (%)')
                    ax.set_zlabel('Clay Fraction (%)')
                else:
                    # Coarse-grained soil
                    x = [item['data']['Gravel Fraction'] for item in self.history]
                    y = [item['data']['Sand Fraction'] for item in self.history]
                    z = [item['data']['Fines Fraction'] for item in self.history]
                    ax.set_xlabel('Gravel (%)')
                    ax.set_ylabel('Sand (%)')
                    ax.set_zlabel('Fines (%)')
                
                ax.scatter(x, y, z)
                
                canvas = FigureCanvasTkAgg(fig, master=viz_window)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                toolbar = NavigationToolbar2Tk(canvas, viz_window)
                toolbar.update()

            def export_plot(self):
                """Export current plot to various formats."""
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"),
                              ("PDF files", "*.pdf"),
                              ("SVG files", "*.svg")]
                )
                
                if file_path:
                    try:
                        self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                        messagebox.showinfo("Success", "Plot exported successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export plot: {str(e)}")

            def show_preferences(self):
                """Show and edit application preferences."""
                pref_window = tk.Toplevel(self.root)
                pref_window.title("Preferences")
                pref_window.geometry("600x700")
                
                # Configure theme window with current theme
                pref_window.configure(bg=COLOR_THEMES[self.current_theme]['bg'])
                
                # Theme selection
                select_frame = ttk.LabelFrame(pref_window, text="Select Theme")
                select_frame.pack(fill=tk.X, padx=10, pady=5)
                
                themes = list(COLOR_THEMES.keys())
                theme_combo = ttk.Combobox(select_frame, values=themes, state='readonly')
                theme_combo.set(self.current_theme)
                theme_combo.pack(padx=10, pady=5)
                
                # Preview frame
                preview_frame = ttk.LabelFrame(pref_window, text="Preview")
                preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Sample widgets for preview
                ttk.Label(preview_frame, text="Sample Label").pack(pady=5)
                ttk.Entry(preview_frame).pack(pady=5)
                ttk.Button(preview_frame, text="Sample Button").pack(pady=5)
                
                # Create color customization frames for each theme element
                color_frame = ttk.LabelFrame(pref_window, text="Customize Colors")
                color_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Create scrolled frame for color options
                canvas = tk.Canvas(color_frame)
                scrollbar = ttk.Scrollbar(color_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Color picker buttons for each element
                color_buttons = {}
                for element, color in COLOR_THEMES[self.current_theme].items():
                    row = ttk.Frame(scrollable_frame)
                    row.pack(fill=tk.X, padx=5, pady=2)
                    
                    ttk.Label(row, text=f"{element}:").pack(side=tk.LEFT, padx=5)
                    color_buttons[element] = tk.Button(
                        row, 
                        width=10, 
                        bg=color,
                        command=lambda e=element: self.pick_color(e, color_buttons)
                    )
                    color_buttons[element].pack(side=tk.LEFT, padx=5)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
                # Apply and Save buttons
                button_frame = ttk.Frame(pref_window)
                button_frame.pack(fill=tk.X, padx=10, pady=5)
                
                ttk.Button(button_frame, text="Apply Theme",
                          command=lambda: self.apply_theme_changes(theme_combo.get(), color_buttons)
                          ).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(button_frame, text="Save as Custom Theme",
                          command=lambda: self.save_custom_theme(color_buttons)
                          ).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(button_frame, text="Reset to Default",
                          command=lambda: self.reset_theme(theme_combo.get(), color_buttons)
                          ).pack(side=tk.LEFT, padx=5)

            def pick_color(self, element, color_buttons):
                """Open color picker and update button color with error handling."""
                try:
                    color = colorchooser.askcolor(
                        title=f"Choose {element} color",
                        color=color_buttons[element].cget('bg')
                    )[1]
                    if color:
                        color_buttons[element].configure(bg=color)
                except Exception as e:
                    logging.error(f"Failed to pick color for {element}: {e}")
                    messagebox.showerror("Error", f"Failed to pick color: {str(e)}")

            def apply_theme_changes(self, theme_name, color_buttons):
                """Apply theme changes from color buttons with error handling."""
                try:
                    if not theme_name:
                        raise ValueError("No theme selected")
                        
                    new_theme = {}
                    for element, button in color_buttons.items():
                        try:
                            new_theme[element] = button.cget('bg')
                        except TclError as e:
                            logging.warning(f"Failed to get color for {element}: {e}")
                            new_theme[element] = COLOR_THEMES['default'][element]
                    
                    COLOR_THEMES[theme_name] = new_theme
                    self.load_theme(theme_name)
                    messagebox.showinfo("Success", "Theme applied successfully!")
                except Exception as e:
                    logging.error(f"Failed to apply theme changes: {e}")
                    messagebox.showerror("Error", f"Failed to apply theme changes: {str(e)}")

            def save_custom_theme(self, color_buttons):
                """Save current color settings as a custom theme with error handling."""
                try:
                    name = simpledialog.askstring("Save Theme", 
                                                "Enter name for custom theme:")
                    if name:
                        if name in COLOR_THEMES:
                            if not messagebox.askyesno("Warning", 
                                                     f"Theme '{name}' already exists. Overwrite?"):
                                return
                        
                        new_theme = {}
                        for element, button in color_buttons.items():
                            try:
                                new_theme[element] = button.cget('bg')
                            except TclError as e:
                                logging.warning(f"Failed to get color for {element}: {e}")
                                new_theme[element] = COLOR_THEMES['default'][element]
                        
                        COLOR_THEMES[name] = new_theme
                        
                        # Save themes to file
                        try:
                            with open('custom_themes.json', 'w') as f:
                                json.dump(COLOR_THEMES, f, indent=4)
                        except Exception as e:
                            logging.warning(f"Failed to save themes to file: {e}")
                        
                        messagebox.showinfo("Success", f"Custom theme '{name}' saved!")
                except Exception as e:
                    logging.error(f"Failed to save custom theme: {e}")
                    messagebox.showerror("Error", f"Failed to save custom theme: {str(e)}")

            def reset_theme(self, theme_name, color_buttons):
                """Reset theme to default colors with error handling."""
                try:
                    if not theme_name:
                        raise ValueError("No theme selected")
                        
                    if theme_name not in COLOR_THEMES:
                        raise ValueError(f"Theme '{theme_name}' not found")
                        
                    # Get default theme colors
                    default_colors = COLOR_THEMES[theme_name].copy()
                    
                    # Update color buttons
                    for element, color in default_colors.items():
                        if element in color_buttons:
                            try:
                                color_buttons[element].configure(bg=color)
                            except TclError as e:
                                logging.warning(f"Failed to reset color for {element}: {e}")
                    
                    # Apply theme
                    self.load_theme(theme_name)
                    messagebox.showinfo("Success", "Theme reset to default!")
                except Exception as e:
                    logging.error(f"Failed to reset theme: {e}")
                    messagebox.showerror("Error", f"Failed to reset theme: {str(e)}")

            def load_custom_themes(self):
                """Load custom themes from file with error handling."""
                try:
                    if os.path.exists('custom_themes.json'):
                        with open('custom_themes.json', 'r') as f:
                            custom_themes = json.load(f)
                            
                        # Validate and merge themes
                        for name, theme in custom_themes.items():
                            if all(key in theme for key in COLOR_THEMES['default'].keys()):
                                COLOR_THEMES[name] = theme
                            else:
                                logging.warning(f"Invalid theme format for '{name}', skipping")
                except Exception as e:
                    logging.error(f"Failed to load custom themes: {e}")
                    # Don't show error to user as this is a background operation

            def export_settings(self):
                """Export current application settings."""
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json")]
                )
                
                if file_path:
                    try:
                        settings = {
                            'theme': self.current_theme,
                            'window_size': self.root.geometry(),
                            'plot_settings': {
                                'show_grid': True,
                                'font_size': plt.rcParams['font.size']
                            }
                        }
                        with open(file_path, 'w') as f:
                            json.dump(settings, f, indent=4)
                        messagebox.showinfo("Success", "Settings exported successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to export settings: {str(e)}")

            def show_tutorials(self):
                """Show video tutorials."""
                tutorial_window = tk.Toplevel(self.root)
                tutorial_window.title("Video Tutorials")
                tutorial_window.geometry("800x600")
                
                # Create notebook for different tutorials
                notebook = ttk.Notebook(tutorial_window)
                notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                
                # Basic usage
                basic_frame = ttk.Frame(notebook)
                notebook.add(basic_frame, text='Basic Usage')
                
                ttk.Label(basic_frame, 
                         text="Basic Soil Classification Tutorial",
                         font=('Arial', 12, 'bold')).pack(pady=10)
                
                def open_tutorial(url):
                    webbrowser.open(url)
                
                ttk.Button(basic_frame, text="Watch Tutorial", 
                          command=lambda: open_tutorial("https://example.com/tutorial1")).pack()
                
                # Advanced features
                advanced_frame = ttk.Frame(notebook)
                notebook.add(advanced_frame, text='Advanced Features')
                
                ttk.Label(advanced_frame,
                         text="Advanced Analysis Tutorial",
                         font=('Arial', 12, 'bold')).pack(pady=10)
                
                ttk.Button(advanced_frame, text="Watch Tutorial",
                          command=lambda: open_tutorial("https://example.com/tutorial2")).pack()

            def check_updates(self):
                """Check for software updates."""
                update_window = tk.Toplevel(self.root)
                update_window.title("Check for Updates")
                update_window.geometry("400x300")
                
                current_version = "1.0"  # Replace with actual version
                
                ttk.Label(update_window,
                         text=f"Current Version: {current_version}",
                         font=('Arial', 10, 'bold')).pack(pady=10)
                
                progress_var = tk.DoubleVar()
                progress_bar = ttk.Progressbar(update_window, 
                                             variable=progress_var,
                                             maximum=100)
                progress_bar.pack(fill=tk.X, padx=10, pady=5)
                
                status_label = ttk.Label(update_window, text="Checking for updates...")
                status_label.pack(pady=5)
                
                def check_update():
                    try:
                        # Simulate update check
                        for i in range(100):
                            progress_var.set(i + 1)
                            update_window.update()
                            time.sleep(0.02)
                        
                        status_label.config(text="You have the latest version!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to check updates: {str(e)}")
                
                update_window.after(500, check_update)

        # Create and run the application
        try:
            root = tk.Tk()
            
            # Configure exception handling for the main window
            def show_error(exc_type, exc_value, exc_traceback):
                error_msg = f"An error occurred:\n{exc_type.__name__}: {exc_value}"
                messagebox.showerror("Error", error_msg)
                print("Exception:", error_msg)
            
            root.report_callback_exception = show_error
            
            # Create the application
            app = SoilClassificationApp(root)
            
            # Configure window
            root.minsize(1000, 600)
            
            # Center window on screen
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width - 1000) // 2
            y = (screen_height - 600) // 2
            root.geometry(f'1000x600+{x}+{y}')
            
            # Start the application
            root.mainloop()
        except Exception as e:
            print(f"Critical Error: {e}")
            messagebox.showerror("Critical Error", f"Application failed to start: {str(e)}")
            sys.exit(1)

    except Exception as e:
        print(f"Critical Error: {e}")
        messagebox.showerror("Critical Error", f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
