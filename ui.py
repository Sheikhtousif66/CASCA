"""
CASCA AI Assistant - Futuristic Desktop UI
A premium, cinematic interface with fluid orb animations
"""

import customtkinter as ctk
import math
import random
import time
import threading
from typing import Callable, Optional
from dataclasses import dataclass
from enum import Enum


class OrbState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"


@dataclass
class Message:
    content: str
    is_user: bool
    timestamp: float


class AnimatedOrb(ctk.CTkCanvas):
    """A living, breathing fluid orb with multiple animation states"""
    
    def __init__(self, master, size: int = 200, **kwargs):
        super().__init__(
            master,
            width=size,
            height=size,
            bg="#05010A",
            highlightthickness=0,
            **kwargs
        )
        
        self.size = size
        self.center = size // 2
        self.base_radius = size // 4
        self.state = OrbState.IDLE
        
        # Animation parameters
        self.time = 0
        self.blob_points = 12
        self.noise_offsets = [random.uniform(0, 2 * math.pi) for _ in range(self.blob_points)]
        self.target_scale = 1.0
        self.current_scale = 1.0
        self.target_brightness = 1.0
        self.current_brightness = 1.0
        self.rotation = 0
        self.pulse_phase = 0
        
        # Colors
        self.primary_color = "#B884FF"
        self.glow_color = "#B884FF"
        
        self._animate()
    
    def set_state(self, state: OrbState):
        """Change the orb's animation state"""
        self.state = state
        
        if state == OrbState.IDLE:
            self.target_scale = 1.0
            self.target_brightness = 1.0
        elif state == OrbState.LISTENING:
            self.target_scale = 1.15
            self.target_brightness = 1.4
        elif state == OrbState.THINKING:
            self.target_scale = 1.05
            self.target_brightness = 1.2
        elif state == OrbState.SPEAKING:
            self.target_scale = 1.1
            self.target_brightness = 1.3
    
    def _lerp(self, current: float, target: float, speed: float = 0.08) -> float:
        return current + (target - current) * speed
    
    def _get_blob_points(self) -> list:
        """Generate fluid blob points with organic movement"""
        points = []
        
        for i in range(self.blob_points):
            angle = (2 * math.pi * i) / self.blob_points
            
            # Base noise for organic shape
            noise = 0
            noise += math.sin(self.time * 1.5 + self.noise_offsets[i]) * 0.15
            noise += math.sin(self.time * 2.3 + self.noise_offsets[i] * 2) * 0.1
            noise += math.sin(self.time * 0.7 + self.noise_offsets[i] * 0.5) * 0.08
            
            # State-specific modifications
            if self.state == OrbState.THINKING:
                # Swirling motion
                swirl = math.sin(self.time * 4 + angle * 3) * 0.12
                noise += swirl
                angle += self.rotation
            elif self.state == OrbState.SPEAKING:
                # Pulsing motion
                pulse = math.sin(self.time * 8 + self.pulse_phase) * 0.15
                pulse += math.sin(self.time * 12 + angle * 2) * 0.08
                noise += pulse
            elif self.state == OrbState.LISTENING:
                # Expanded, alert state
                noise += math.sin(self.time * 3 + angle * 4) * 0.08
            
            radius = self.base_radius * self.current_scale * (1 + noise)
            
            x = self.center + radius * math.cos(angle)
            y = self.center + radius * math.sin(angle)
            points.extend([x, y])
        
        return points
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb: tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(
            max(0, min(255, int(rgb[0]))),
            max(0, min(255, int(rgb[1]))),
            max(0, min(255, int(rgb[2])))
        )
    
    def _get_glow_color(self, intensity: float) -> str:
        base_rgb = self._hex_to_rgb(self.primary_color)
        adjusted = tuple(min(255, int(c * intensity * self.current_brightness)) for c in base_rgb)
        return self._rgb_to_hex(adjusted)
    
    def _draw_glow_layers(self):
        """Draw multiple glow layers for depth"""
        glow_layers = [
            (2.5, 0.08),
            (2.0, 0.12),
            (1.6, 0.18),
            (1.3, 0.25),
        ]
        
        for scale_mult, intensity in glow_layers:
            points = []
            for i in range(self.blob_points):
                angle = (2 * math.pi * i) / self.blob_points
                
                noise = math.sin(self.time * 1.2 + self.noise_offsets[i]) * 0.1
                radius = self.base_radius * self.current_scale * scale_mult * (1 + noise)
                
                if self.state == OrbState.THINKING:
                    angle += self.rotation * 0.5
                
                x = self.center + radius * math.cos(angle)
                y = self.center + radius * math.sin(angle)
                points.extend([x, y])
            
            if len(points) >= 6:
                color = self._get_glow_color(intensity)
                self.create_polygon(
                    points,
                    fill=color,
                    outline="",
                    smooth=True,
                    splinesteps=32
                )
    
    def _animate(self):
        """Main animation loop"""
        self.delete("all")
        
        # Update animation parameters
        self.time += 0.016
        self.current_scale = self._lerp(self.current_scale, self.target_scale)
        self.current_brightness = self._lerp(self.current_brightness, self.target_brightness)
        
        if self.state == OrbState.THINKING:
            self.rotation += 0.03
        elif self.state == OrbState.SPEAKING:
            self.pulse_phase += 0.2
        
        # Draw glow layers
        self._draw_glow_layers()
        
        # Draw main blob
        points = self._get_blob_points()
        if len(points) >= 6:
            # Inner gradient effect
            inner_color = self._get_glow_color(0.6)
            self.create_polygon(
                points,
                fill=inner_color,
                outline="",
                smooth=True,
                splinesteps=32
            )
            
            # Core highlight
            core_points = []
            for i in range(self.blob_points):
                angle = (2 * math.pi * i) / self.blob_points
                noise = math.sin(self.time * 2 + self.noise_offsets[i]) * 0.1
                radius = self.base_radius * self.current_scale * 0.6 * (1 + noise)
                
                if self.state == OrbState.THINKING:
                    angle += self.rotation
                
                x = self.center + radius * math.cos(angle)
                y = self.center + radius * math.sin(angle)
                core_points.extend([x, y])
            
            if len(core_points) >= 6:
                core_color = self._get_glow_color(0.9)
                self.create_polygon(
                    core_points,
                    fill=core_color,
                    outline="",
                    smooth=True,
                    splinesteps=32
                )
        
        self.after(16, self._animate)


class ChatBubble(ctk.CTkFrame):
    """Floating chat bubble with smooth appearance"""
    
    def __init__(self, master, message: Message, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color="transparent")
        
        # Bubble styling based on sender
        if message.is_user:
            bubble_color = "#1a1520"
            text_color = "#ffffff"
            anchor = "e"
            padx = (50, 0)
        else:
            bubble_color = "#12101a"
            text_color = "#e0d4f7"
            anchor = "w"
            padx = (0, 50)
        
        # Container for alignment
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=padx, pady=4)
        
        # Bubble
        bubble = ctk.CTkFrame(
            container,
            fg_color=bubble_color,
            corner_radius=16,
            border_width=1,
            border_color="#2a2235"
        )
        
        if message.is_user:
            bubble.pack(side="right")
        else:
            bubble.pack(side="left")
        
        # Message text
        label = ctk.CTkLabel(
            bubble,
            text=message.content,
            text_color=text_color,
            font=("SF Pro Display", 14),
            wraplength=280,
            justify="left" if not message.is_user else "right",
            padx=16,
            pady=12
        )
        label.pack()
        
        # Fade in animation
        self.alpha = 0
        self._fade_in()
    
    def _fade_in(self):
        if self.alpha < 1:
            self.alpha += 0.1
            self.after(20, self._fade_in)


class GlassInputBar(ctk.CTkFrame):
    """Glassmorphic floating input bar"""
    
    def __init__(self, master, on_send: Callable[[str], None], on_mic: Callable[[], None], **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_send = on_send
        self.on_mic = on_mic
        
        self.configure(
            fg_color="#0d0a12",
            corner_radius=28,
            border_width=1,
            border_color="#2a2235"
        )
        
        # Inner container
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Microphone button
        self.mic_btn = ctk.CTkButton(
            inner,
            text="🎤",
            width=44,
            height=44,
            corner_radius=22,
            fg_color="#1a1520",
            hover_color="#2a2235",
            font=("SF Pro Display", 18),
            command=self._on_mic_click
        )
        self.mic_btn.pack(side="left", padx=(4, 8))
        
        # Text entry
        self.entry = ctk.CTkEntry(
            inner,
            placeholder_text="Type message...",
            placeholder_text_color="#6b5f7a",
            text_color="#ffffff",
            fg_color="transparent",
            border_width=0,
            font=("SF Pro Display", 15),
            height=44
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=8)
        self.entry.bind("<Return>", self._on_enter)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            inner,
            text="➤",
            width=44,
            height=44,
            corner_radius=22,
            fg_color="#B884FF",
            hover_color="#9966dd",
            text_color="#05010A",
            font=("SF Pro Display", 18),
            command=self._on_send_click
        )
        self.send_btn.pack(side="right", padx=(8, 4))
    
    def _on_enter(self, event):
        self._on_send_click()
    
    def _on_send_click(self):
        text = self.entry.get().strip()
        if text:
            self.entry.delete(0, "end")
            self.on_send(text)
    
    def _on_mic_click(self):
        self.on_mic()
    
    def get_text(self) -> str:
        return self.entry.get()
    
    def clear(self):
        self.entry.delete(0, "end")


class CascaUI(ctk.CTk):
    """Main CASCA AI Assistant Interface"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("CASCA")
        self.geometry("420x780")
        self.minsize(380, 700)
        self.configure(fg_color="#05010A")
        
        # Chat history
        self.messages: list[Message] = []
        
        self._setup_ui()
        
        # Backend callbacks
        self.run_casca: Optional[Callable] = None
        self.listen: Optional[Callable] = None
        self.speak: Optional[Callable] = None
    
    def _setup_ui(self):
        """Build the complete UI"""
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=24, pady=24)
        
        # === TOP: Title ===
        title_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame,
            text="CASCA",
            font=("SF Pro Display", 28, "bold"),
            text_color="#B884FF"
        )
        title.pack()
        
        # Subtle tagline
        tagline = ctk.CTkLabel(
            title_frame,
            text="AI Assistant",
            font=("SF Pro Display", 12),
            text_color="#4a3f5a"
        )
        tagline.pack()
        
        # === CENTER: Animated Orb ===
        orb_container = ctk.CTkFrame(main_container, fg_color="transparent")
        orb_container.pack(fill="x", pady=20)
        
        self.orb = AnimatedOrb(orb_container, size=200)
        self.orb.pack()
        
        # Status text below orb
        self.status_label = ctk.CTkLabel(
            orb_container,
            text="How may I help today?",
            font=("SF Pro Display", 16),
            text_color="#8a7a9a"
        )
        self.status_label.pack(pady=(20, 0))
        
        # === MIDDLE: Chat Area ===
        chat_container = ctk.CTkFrame(main_container, fg_color="transparent")
        chat_container.pack(fill="both", expand=True, pady=20)
        
        # Scrollable chat frame
        self.chat_scroll = ctk.CTkScrollableFrame(
            chat_container,
            fg_color="transparent",
            scrollbar_button_color="#2a2235",
            scrollbar_button_hover_color="#3a3245"
        )
        self.chat_scroll.pack(fill="both", expand=True)
        
        # === BOTTOM: Input Bar ===
        self.input_bar = GlassInputBar(
            main_container,
            on_send=self._handle_send,
            on_mic=self._handle_mic
        )
        self.input_bar.pack(fill="x", pady=(10, 0))
        
        # Add welcome message and speak it directly (only place UI calls speak)
        GREETING = "Hello! I'm CASCA, your AI assistant. How can I help you today?"
        self._add_message(GREETING, is_user=False)
        self.after(500, lambda: threading.Thread(
            target=lambda: self.speak(GREETING) if self.speak else None,
            daemon=True
        ).start())
    
    def _add_message(self, content: str, is_user: bool):
        """Add a message to the chat"""
        message = Message(content=content, is_user=is_user, timestamp=time.time())
        self.messages.append(message)
        
        bubble = ChatBubble(self.chat_scroll, message)
        bubble.pack(fill="x", pady=2)
        
        # Scroll to bottom
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
    
    def _extract_reply(self, result) -> str:
        """Extract reply string from run_casca result"""
        if isinstance(result, dict):
            return result.get("response", str(result))
        return str(result)

    def _handle_send(self, text: str):
        """Handle sending a text message — runs backend in a thread"""
        # Show user bubble immediately
        self._add_message(text, is_user=True)

        # Update orb state on main thread
        self.set_orb_state(OrbState.THINKING)
        self.set_status("Thinking...")

        def worker():
            try:
                result = self.run_casca(text) if self.run_casca else {"response": "Backend not connected."}
                reply = self._extract_reply(result)
            except Exception as e:
                reply = f"Error: {e}"

            # All UI updates must happen on the main thread
            self.after(0, lambda: self._on_text_reply(reply))

        threading.Thread(target=worker, daemon=True).start()

    def _on_text_reply(self, reply: str):
        """Called on main thread after run_casca returns"""
        self._add_message(reply, is_user=False)
        self.set_orb_state(OrbState.SPEAKING)
        self.set_status("Speaking...")
        # speak() is handled by run_casca internally
        self.after(2000, self._return_to_idle)

    def _handle_mic(self):
        """Handle microphone button press — runs STT + backend in a thread"""
        if self.orb.state == OrbState.LISTENING:
            # Toggle off
            self._return_to_idle()
            return

        self.set_orb_state(OrbState.LISTENING)
        self.set_status("Listening...")

        def worker():
            try:
                user_text, audio = self.listen() if self.listen else (None, None)
            except Exception as e:
                self.after(0, self._return_to_idle)
                return

            if not user_text:
                self.after(0, self._return_to_idle)
                return

            # Show user bubble, switch to thinking
            self.after(0, lambda: self._add_message(user_text, is_user=True))
            self.after(0, lambda: self.set_orb_state(OrbState.THINKING))
            self.after(0, lambda: self.set_status("Thinking..."))

            try:
                result = self.run_casca(user_text) if self.run_casca else {"response": "Backend not connected."}
                reply = self._extract_reply(result)
            except Exception as e:
                reply = f"Error: {e}"

            self.after(0, lambda: self._on_voice_reply(reply))

        threading.Thread(target=worker, daemon=True).start()

    def _on_voice_reply(self, reply: str):
        """Called on main thread after voice pipeline completes"""
        self._add_message(reply, is_user=False)
        self.set_orb_state(OrbState.SPEAKING)
        self.set_status("Speaking...")
        # speak() is handled by run_casca internally
        self.after(2000, self._return_to_idle)

    def _return_to_idle(self):
        self.set_orb_state(OrbState.IDLE)
        self.set_status("How may I help today?")
    
    def set_orb_state(self, state: OrbState):
        """Change the orb animation state"""
        self.orb.set_state(state)
    
    def set_status(self, text: str):
        """Update the status text below the orb"""
        self.status_label.configure(text=text)
    
    def connect_backend(
        self,
        run_casca: Optional[Callable] = None,
        listen: Optional[Callable] = None,
        speak: Optional[Callable] = None
    ):
        """Connect backend functions"""
        self.run_casca = run_casca
        self.listen = listen
        self.speak = speak


def main():
    """Entry point for CASCA UI"""
    from main import run_casca
    from stt import listen
    from voice import speak

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = CascaUI()
    app.connect_backend(
        run_casca=run_casca,
        listen=listen,
        speak=speak
    )
    app.mainloop()


if __name__ == "__main__":
    main()