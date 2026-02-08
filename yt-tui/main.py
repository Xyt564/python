#!/usr/bin/env python3
"""
Simple YouTube Terminal Player
Clean interface with working search, download, and playback
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich import box
    from rich.progress import Progress, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, BarColumn
    import yt_dlp
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "rich", "yt-dlp", "--break-system-packages"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich import box
    from rich.progress import Progress, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, BarColumn
    import yt_dlp


class YouTubePlayer:
    def __init__(self):
        self.console = Console()
        # Single downloads folder - no subfolders, keep it simple
        self.downloads_dir = Path.cwd() / "downloads"
        self.downloads_dir.mkdir(exist_ok=True)
        self.current_results = []
        self.last_query = ""
        
    def format_duration(self, seconds):
        """Convert seconds to readable format"""
        if not seconds:
            return "N/A"
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
        if hours:
            return f"{hours}h {mins}m"
        return f"{mins}m {secs}s"
    
    def format_views(self, views):
        """Format view count"""
        if not views:
            return "N/A"
        if views >= 1_000_000:
            return f"{views/1_000_000:.1f}M"
        if views >= 1_000:
            return f"{views/1_000:.1f}K"
        return str(views)
    
    def show_command_bar(self):
        """Display command bar at bottom"""
        downloads_path = str(self.downloads_dir.absolute())
        commands = (
            "[cyan]S[/cyan]=Search  "
            "[cyan]#[/cyan]=Play  "
            "[cyan]D#[/cyan]=Download  "
            "[cyan]A#[/cyan]=Audio  "
            "[cyan]C[/cyan]=Clear  "
            "[red]Q[/red]=Quit  "
            f"[dim]│ 📁 {downloads_path}[/dim]"
        )
        self.console.print(Panel(commands, box=box.HEAVY, style="bold white on blue"))
    
    def display_results(self):
        """Display search results in the middle"""
        if not self.current_results:
            self.console.print(Panel(
                "[yellow]No results yet. Press 'S' to search![/yellow]",
                title="Results",
                box=box.ROUNDED,
                style="yellow"
            ))
            return
        
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("#", style="yellow", width=3, justify="center")
        table.add_column("Title", style="white", min_width=40)
        table.add_column("Channel", style="green", width=20)
        table.add_column("Duration", style="magenta", width=10, justify="right")
        table.add_column("Views", style="blue", width=10, justify="right")
        
        for idx, video in enumerate(self.current_results[:15], 1):
            table.add_row(
                str(idx),
                video['title'][:60] + "..." if len(video['title']) > 60 else video['title'],
                video['uploader'][:20] if video['uploader'] else "Unknown",
                self.format_duration(video.get('duration')),
                self.format_views(video.get('view_count'))
            )
        
        self.console.print(Panel(
            table,
            title=f"[bold cyan]Search Results ({len(self.current_results)} videos)[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE
        ))
    
    def search(self, query: str, max_results: int = 15):
        """Search YouTube"""
        self.last_query = query
        self.console.print(f"\n[yellow]Searching for: {query}...[/yellow]")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'skip_download': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
                
                self.current_results = []
                if 'entries' in result:
                    for entry in result['entries']:
                        if entry:
                            self.current_results.append({
                                'title': entry.get('title', 'Unknown'),
                                'url': f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                                'duration': entry.get('duration', 0),
                                'uploader': entry.get('uploader', 'Unknown'),
                                'view_count': entry.get('view_count', 0),
                                'id': entry.get('id', '')
                            })
                
                self.console.print(f"[green]✓ Found {len(self.current_results)} results[/green]")
                
        except Exception as e:
            self.console.print(f"[red]✗ Search failed: {str(e)}[/red]")
            self.current_results = []
    
    def play_video(self, video_index: int):
        """Play video using mpv with yt-dlp integration"""
        if video_index < 1 or video_index > len(self.current_results):
            self.console.print("[red]Invalid video number![/red]")
            return
        
        video = self.current_results[video_index - 1]
        url = video['url']
        
        self.console.print(f"\n[green]▶ Playing: {video['title']}[/green]")
        self.console.print("[yellow]Loading video... (may buffer initially)[/yellow]")
        
        # mpv options for 1080p with anti-buffering settings
        mpv_opts = [
            'mpv',
            '--hwdec=auto',  # Use hardware decoding when available (faster)
            '--cache=yes',  # Enable caching
            '--demuxer-max-bytes=150M',  # Large buffer (150MB)
            '--demuxer-readahead-secs=30',  # 30 seconds of readahead
            '--cache-secs=30',  # 30 second cache
            '--ytdl-format=bestvideo[height<=1080][vcodec^=avc]+bestaudio/bestvideo[height<=1080]+bestaudio/best',  # 1080p H.264 preferred
            url
        ]
        
        # Try different players
        players = [
            mpv_opts,
            # Fallback with different settings
            ['mpv', '--cache=yes', '--ytdl-format=best[height<=1080]', url],
            # Other players
            ['vlc', url],
            # For macOS
            ['open', '-a', 'IINA', url],
        ]
        
        played = False
        for player_cmd in players:
            try:
                # Run in foreground so user can see if it works
                result = subprocess.run(
                    player_cmd,
                    check=False,
                    capture_output=False
                )
                played = True
                self.console.print(f"[green]✓ Playback finished[/green]")
                break
            except FileNotFoundError:
                continue
            except Exception as e:
                continue
        
        if not played:
            # Fallback to browser
            self.console.print("[yellow]No video player found (install mpv, vlc, or ffplay)[/yellow]")
            self.console.print("[yellow]Opening in browser instead...[/yellow]")
            import webbrowser
            webbrowser.open(url)
    
    def download_video(self, video_index: int, audio_only: bool = False):
        """Download video or audio"""
        if video_index < 1 or video_index > len(self.current_results):
            self.console.print("[red]Invalid video number![/red]")
            return
        
        video = self.current_results[video_index - 1]
        url = video['url']
        
        # Sanitize filename - make it cleaner
        safe_title = "".join(c for c in video['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace('  ', ' ')  # Remove double spaces
        safe_title = safe_title[:80]  # Shorter limit
        
        # Everything goes to downloads/ folder - simple!
        if audio_only:
            filename = f"[AUDIO] {safe_title}.%(ext)s"
            output_template = str(self.downloads_dir / filename)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'keepvideo': False,
            }
            self.console.print(f"\n[cyan]⬇ Downloading audio: {video['title']}[/cyan]")
        else:
            filename = f"{safe_title}.%(ext)s"
            output_template = str(self.downloads_dir / filename)
            ydl_opts = {
                'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best',
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
            }
            self.console.print(f"\n[cyan]⬇ Downloading video (1080p): {video['title']}[/cyan]")
        
        self.console.print(f"[dim]📁 Saving to: {self.downloads_dir.absolute()}/[/dim]\n")
        
        # Add options to bypass YouTube restrictions
        ydl_opts.update({
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'quiet': False,
            'no_warnings': False,
        })
        
        # Progress hook
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = d.get('_percent_str', 'N/A')
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    self.console.print(f"\r[yellow]⬇ {percent} | {speed} | ETA: {eta}[/yellow]", end='')
                except:
                    pass
            elif d['status'] == 'finished':
                self.console.print(f"\n[green]✓ Download complete! Processing...[/green]")
        
        ydl_opts['progress_hooks'] = [progress_hook]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
            
            # Find the downloaded file
            if audio_only:
                # Look for audio file
                pattern = f"[AUDIO] {safe_title}.*"
            else:
                # Look for video file
                pattern = f"{safe_title}.*"
            
            matching_files = list(self.downloads_dir.glob(pattern))
            
            if matching_files:
                actual_file = matching_files[0]
                file_size = actual_file.stat().st_size / (1024*1024)  # MB
                self.console.print(f"\n[bold green]✅ SUCCESS![/bold green]")
                self.console.print(f"[green]📁 File: {actual_file.name}[/green]")
                self.console.print(f"[green]💾 Size: {file_size:.1f} MB[/green]")
                self.console.print(f"[green]📂 Location: {actual_file.absolute()}[/green]")
            else:
                self.console.print(f"\n[yellow]⚠ Download complete but file not found in expected location[/yellow]")
                self.console.print(f"[yellow]Check: {self.downloads_dir.absolute()}[/yellow]")
            
        except Exception as e:
            self.console.print(f"\n[red]✗ Download failed: {str(e)}[/red]")
            self.console.print(f"[yellow]💡 Try: pip install -U yt-dlp --break-system-packages[/yellow]")
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                # Clear and show interface
                self.console.clear()
                
                # Top: Last search query
                if self.last_query:
                    self.console.print(Panel(
                        f"[bold cyan]🔍 {self.last_query}[/bold cyan]",
                        box=box.HEAVY,
                        style="cyan"
                    ))
                else:
                    self.console.print(Panel(
                        "[bold cyan]🎬 YouTube Terminal Player[/bold cyan]",
                        box=box.HEAVY,
                        style="cyan"
                    ))
                
                self.console.print()
                
                # Middle: Results
                self.display_results()
                
                self.console.print()
                
                # Bottom: Command bar
                self.show_command_bar()
                
                # Get command
                command = Prompt.ask("\n[bold yellow]Command[/bold yellow]").strip().upper()
                
                if command == 'Q':
                    self.console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                    break
                
                elif command == 'S':
                    query = Prompt.ask("\n[bold cyan]Search YouTube[/bold cyan]")
                    if query:
                        self.search(query)
                        Prompt.ask("\n[yellow]Press Enter to continue[/yellow]")
                
                elif command == 'C':
                    self.current_results = []
                    self.last_query = ""
                    self.console.print("\n[green]✓ Results cleared[/green]")
                
                elif command.isdigit():
                    # Play video
                    try:
                        idx = int(command)
                        self.play_video(idx)
                    except ValueError:
                        self.console.print("[red]Invalid number![/red]")
                
                elif command.startswith('D') and len(command) > 1:
                    # Download video
                    try:
                        idx = int(command[1:])
                        self.download_video(idx, audio_only=False)
                        Prompt.ask("\n[yellow]Press Enter to continue[/yellow]")
                    except ValueError:
                        self.console.print("[red]Invalid command! Use D1, D2, etc.[/red]")
                
                elif command.startswith('A') and len(command) > 1:
                    # Download audio
                    try:
                        idx = int(command[1:])
                        self.download_video(idx, audio_only=True)
                        Prompt.ask("\n[yellow]Press Enter to continue[/yellow]")
                    except ValueError:
                        self.console.print("[red]Invalid command! Use A1, A2, etc.[/red]")
                
                else:
                    self.console.print("[yellow]Unknown command. Check the command bar.[/yellow]")
                    
            except KeyboardInterrupt:
                self.console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                break
            
            except Exception as e:
                self.console.print(f"\n[red]Error: {str(e)}[/red]")
                Prompt.ask("\n[yellow]Press Enter to continue[/yellow]")


def main():
    """Entry point"""
    player = YouTubePlayer()
    player.run()


if __name__ == "__main__":
    main()
