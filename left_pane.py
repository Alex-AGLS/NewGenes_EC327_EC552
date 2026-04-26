"""
left_pane.py contains File Upload and XML Viewer
============

A Tkinter Frame for the SBOL Protocol Generator GUI.

This module exposes a single class, ``LeftPane``, that handles:

  * uploading an SBOL XML file via a file-picker button
  * displaying its contents pretty-printed with light syntax coloring

It is meant to be the LEFT half of a horizontally-split main window. The
right half (handled by your teammates) consumes events emitted by this
pane via an optional callback.

PUBLIC API (everything teammates need to know):

    pane = LeftPane(parent)
    pane.pack(side="left", fill="both", expand=True)

    # Register to be notified when the user loads a new XML file:
    pane.set_on_file_loaded(lambda info: print(info))

    # The callback receives a dict like:
    #   {
    #       "xml_path":      "/path/to/file.xml",
    #       "circuit_id":    "demo_pBAD_GFP",
    #       "subcomponents": [
    #           {"DisplayId": "BBa_I0500", "About": "BBa_I0500", "Resource": "SO_0000167"},
    #           ...
    #       ],
    #       "nucleotides":   "ttatgacaa..."   # may be empty
    #   }
    # ...or None on a parse failure (an error message is shown in the pane).

    # Programmatic loading (useful for tests or right-pane-driven loads):
    pane.load_xml("/some/path.xml")

    # Read-only snapshot of what's currently loaded (or None):
    state = pane.get_loaded_state()

The pane is fully self-contained -- no global state, no module-level side
effects. Drop the file in your project folder and import the class.
"""

from __future__ import annotations

import os
import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, Optional, Dict, Any


# ---------------------------------------------------------------------------
# Color palette (kept here so teammates can theme without digging into widgets)
# ---------------------------------------------------------------------------
COLOR_BG          = "#1e1e2e"   # main background (dark)
COLOR_PANEL       = "#2a2a3e"   # secondary panels
COLOR_TEXT        = "#e0e0e0"   # primary text
COLOR_DIM         = "#888899"   # secondary text
COLOR_ACCENT      = "#7aa2f7"   # accent (blue)
COLOR_SUCCESS     = "#9ece6a"   # green (status: loaded OK)
COLOR_ERROR       = "#f7768e"   # red (status: parse error)

# Syntax-coloring palette for raw-XML mode
COLOR_XML_TAG     = "#7aa2f7"   # <DnaComponent>
COLOR_XML_ATTR    = "#bb9af7"   # rdf:about=
COLOR_XML_VALUE   = "#9ece6a"   # "the value"
COLOR_XML_COMMENT = "#565f89"   # <!-- -->


# ---------------------------------------------------------------------------
# SBOL parser (vendored copy of the logic in extract_xml.py so this module
# has no dependency on the teammates' file). The returned dict shape is
# intentionally compatible with extract_xml.parse() so teammates can swap in
# the real parser later without changing anything else.
# ---------------------------------------------------------------------------
SBOL_NS    = "http://sbols.org/v1#"
RDF_NS     = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NSMAP      = {"sbol": SBOL_NS, "rdf": RDF_NS}



# ---------------------------------------------------------------------------
# The widget itself
# ---------------------------------------------------------------------------
class XMLViewer(tk.Frame):
    """The left half of the main window: file upload + raw-XML viewer.

    Subclasses tk.Frame so it can be packed/gridded by the caller. All
    widgets are private (prefixed with _); only the public API documented
    in the module docstring should be relied on.
    """

    def __init__(self, master: tk.Misc, **kwargs):
        super().__init__(master, bg=COLOR_BG, **kwargs)

        # --- internal state ------------------------------------------------
        self._loaded_xml_path: Optional[str] = None
        self._loaded_state:    Optional[Dict[str, Any]] = None
        self._on_file_loaded:  Optional[Callable[[Optional[Dict[str, Any]]], None]] = None

        # --- build the UI --------------------------------------------------
        self._build_header()
        self._build_viewer()
        self._show_placeholder()

    def get_xml_path(self):
        return self._loaded_xml_path
    
    def refresh(self):
        print("refresh left pane")
        self._show_placeholder()
        self._filename_label.config(text="No file loaded")
        self._status_label.config(text="")
        self._loaded_xml_path = None
        self._loaded_state = None
        self._on_file_loaded = None

    # ----------------------------------------------------------------- build
    def _build_header(self) -> None:
        """Top strip: upload button + filename label + status."""
        header = tk.Frame(self, bg=COLOR_PANEL, padx=12, pady=10)
        header.pack(side="top", fill="x")

        self._filename_label = tk.Label(
            header,
            text="No file loaded",
            bg=COLOR_PANEL, fg=COLOR_DIM,
            font=("Helvetica", 10, "italic"),
            anchor="center",
        )
        self._filename_label.pack(side="left", padx=12, fill="x", expand=True)

        self._status_label = tk.Label(
            header, text="",
            bg=COLOR_PANEL, fg=COLOR_DIM,
            font=("Helvetica", 9),
        )
        self._status_label.pack(side="right")

    def _build_viewer(self) -> None:
        """The main content area: a scrollable, read-only Text widget."""
        viewer_holder = tk.Frame(self, bg=COLOR_BG)
        viewer_holder.pack(side="top", fill="both", expand=True,
                           padx=12, pady=12)

        scroll = tk.Scrollbar(viewer_holder, orient="vertical")
        scroll.pack(side="right", fill="y")

        self._raw_text = tk.Text(
            viewer_holder,
            wrap="none",
            bg=COLOR_PANEL, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            font=("Menlo", 10) if self._monospace_available() else ("Courier", 10),
            yscrollcommand=scroll.set,
            relief="flat",
            padx=10, pady=10,
        )
        self._raw_text.pack(side="left", fill="both", expand=True)
        scroll.config(command=self._raw_text.yview)

        # Configure tags for syntax coloring
        self._raw_text.tag_configure("xml_tag",     foreground=COLOR_XML_TAG)
        self._raw_text.tag_configure("xml_attr",    foreground=COLOR_XML_ATTR)
        self._raw_text.tag_configure("xml_value",   foreground=COLOR_XML_VALUE)
        self._raw_text.tag_configure(
            "xml_comment",
            foreground=COLOR_XML_COMMENT,
            font=("Menlo", 10, "italic"),
        )
        self._raw_text.tag_configure(
            "placeholder",
            foreground=COLOR_DIM,
            justify="center",
            spacing1=80,
        )

    @staticmethod
    def _monospace_available() -> bool:
        """Best-effort check for Mac's Menlo font; falls back to Courier."""
        try:
            from tkinter import font
            return "Menlo" in font.families()
        except Exception:
            return False

    # --------------------------------------------------------------- public
    def set_on_file_loaded(
        self,
        callback: Optional[Callable[[Optional[Dict[str, Any]]], None]],
    ) -> None:
        """Register a function to call whenever a file is loaded (or fails).

        The callback receives a state dict (see module docstring) on success,
        or None on failure.
        """
        self._on_file_loaded = callback

    def load_xml(self, xml_path: str) -> bool:
        """Programmatically load an XML file.

        Returns True on success, False on failure. Either way the pane
        updates its display and (if registered) fires the on_file_loaded
        callback. Useful for testing and for accepting drag-drop later.
        """
        return self._load_and_display(xml_path)

    def get_loaded_state(self) -> Optional[Dict[str, Any]]:
        """Snapshot of the currently-loaded state, or None if no file is
        loaded. The dict is a fresh copy -- mutating it is safe.
        """
        if self._loaded_state is None:
            return None
        return json.loads(json.dumps(self._loaded_state))

    # --------------------------------------------------------------- events

    def _load_and_display(self, xml_path: str) -> bool:
        """Core loader: parse, store state, render, fire callback.

        On error, displays a friendly message in the pane and a popup, and
        clears the loaded state.
        """


        # Save state
        self._loaded_xml_path = xml_path


        # Update header / status
        self._filename_label.config(
            text=os.path.basename(xml_path),
            fg=COLOR_TEXT,
        )
        self._status_label.config(
            text=f"Loaded OK",
            fg=COLOR_SUCCESS,
        )

        self._render_raw_xml()

        # Fire the callback last (after our own UI is up to date)
        if self._on_file_loaded is not None:
            try:
                self._on_file_loaded(self.get_loaded_state())
            except Exception as cb_err:
                print(f"[LeftPane] on_file_loaded callback raised: {cb_err}")

        return True

    def _show_error(self, xml_path: str, message: str) -> None:
        """Display an error in the pane and via a popup."""
        self._loaded_xml_path = None
        self._loaded_state = None

        self._filename_label.config(
            text=f"Failed: {os.path.basename(xml_path)}",
            fg=COLOR_ERROR,
        )
        self._status_label.config(text="Parse error", fg=COLOR_ERROR)

        self._raw_text.config(state="normal")
        self._raw_text.delete("1.0", "end")
        self._raw_text.insert(
            "end",
            f"Could not load {os.path.basename(xml_path)}.\n\n"
            f"{message}\n\n"
            "Make sure the file is valid SBOL 1.x XML."
        )
        self._raw_text.config(state="disabled")

        messagebox.showerror(
            "XML load error",
            f"Couldn't parse {os.path.basename(xml_path)}:\n\n{message}"
        )

    # ---------------------------------------------------------------- render
    def _render_raw_xml(self) -> None:
        """Read the file from disk, pretty-print it, apply syntax coloring."""
        if self._loaded_xml_path is None:
            return

        try:
            with open(self._loaded_xml_path, "r", encoding="utf-8", errors="replace") as f:
                raw = f.read()
        except OSError as e:
            raw = f"<Could not re-read file: {e}>"

        pretty = self._pretty_print_xml(raw)

        self._raw_text.config(state="normal")
        self._raw_text.delete("1.0", "end")
        self._raw_text.insert("end", pretty)
        self._apply_xml_syntax_coloring()
        self._raw_text.config(state="disabled")

    @staticmethod
    def _pretty_print_xml(raw: str) -> str:
        """Best-effort pretty-print. Falls back to raw on parse failure
        because we still want to show *something*.
        """
        try:
            tree = ET.ElementTree(ET.fromstring(raw))
            try:
                # ET.indent was added in Python 3.9; safe fallback if missing
                ET.indent(tree, space="  ", level=0)
            except AttributeError:
                pass
            body = ET.tostring(tree.getroot(), encoding="unicode")
            return '<?xml version="1.0" encoding="UTF-8"?>\n' + body
        except ET.ParseError:
            return raw

    def _apply_xml_syntax_coloring(self) -> None:
        """Apply tags to the Text widget so XML elements get colored.

        Intentionally simple: regex-style scanning, not a full XML parser.
        Good enough for highlighting at a glance.
        """
        import re
        text = self._raw_text.get("1.0", "end-1c")

        # Clear any existing tags first
        for tag in ("xml_tag", "xml_attr", "xml_value", "xml_comment"):
            self._raw_text.tag_remove(tag, "1.0", "end")

        # Comments first (so other patterns don't fire inside them)
        for m in re.finditer(r"<!--.*?-->", text, re.DOTALL):
            self._raw_text.tag_add(
                "xml_comment",
                f"1.0+{m.start()}c", f"1.0+{m.end()}c"
            )

        # Tag names: <foo or </foo or <foo:bar
        for m in re.finditer(r"</?([a-zA-Z_][\w:.-]*)", text):
            self._raw_text.tag_add(
                "xml_tag",
                f"1.0+{m.start(1)}c", f"1.0+{m.end(1)}c"
            )

        # Attribute names: name=
        for m in re.finditer(r"\b([a-zA-Z_:][\w:.-]*)=", text):
            self._raw_text.tag_add(
                "xml_attr",
                f"1.0+{m.start(1)}c", f"1.0+{m.end(1)}c"
            )

        # Quoted attribute values
        for m in re.finditer(r'"[^"]*"', text):
            self._raw_text.tag_add(
                "xml_value",
                f"1.0+{m.start()}c", f"1.0+{m.end()}c"
            )

    def _show_placeholder(self) -> None:
        """Initial state when nothing is loaded."""
        self._raw_text.config(state="normal")
        self._raw_text.delete("1.0", "end")
        self._raw_text.insert(
            "end",
            "\n"
            "No SBOL XML loaded.\n\n"
            "Click \"Upload SBOL XML...\" above to begin.",
            "placeholder",
        )
        self._raw_text.config(state="disabled")

