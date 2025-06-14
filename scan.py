import socket
import ssl
import argparse
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import sys

console = Console()

def print_banner():
    banner = """

░██████╗░█████╗░░█████╗░███╗░░██╗  ░██████╗░█████╗░██╗░░░██╗██████╗░░█████╗░██████╗░██╗░░██╗
██╔════╝██╔══██╗██╔══██╗████╗░██║  ██╔════╝██╔══██╗██║░░░██║██╔══██╗██╔══██╗██╔══██╗██║░░██║
╚█████╗░██║░░╚═╝███████║██╔██╗██║  ╚█████╗░███████║██║░░░██║██████╔╝███████║██████╦╝███████║
░╚═══██╗██║░░██╗██╔══██║██║╚████║  ░╚═══██╗██╔══██║██║░░░██║██╔══██╗██╔══██║██╔══██╗██╔══██║
██████╔╝╚█████╔╝██║░░██║██║░╚███║  ██████╔╝██║░░██║╚██████╔╝██║░░██║██║░░██║██████╦╝██║░░██║
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝  ╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝

                        [bold green]Smart Scan Mode Activated[/bold green]
    """
    print(Panel.fit(banner, title="[bold red]Scan Saurabh[/bold red]", border_style="green"))

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print_banner()
        console.print(f"[bold red]❌ Argument Error:[/bold red] {message}")
        self.print_help()
        sys.exit(2)

def ping_host(ip):
    try:
        socket.gethostbyname(ip)
        return True
    except socket.error:
        return False

def detect_ssl(target, port=443):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((target, port), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                print(f"[blue]🔒 SSL Certificate Detected[/blue] - Issuer: {cert.get('issuer')}")
                print(f"[blue]🔐 Protocol:[/blue] {ssock.version()}")
                return True
    except Exception:
        return False

def grab_banner(ip, port):
    try:
        with socket.socket() as sock:
            sock.settimeout(1)
            sock.connect((ip, port))
            sock.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore")
            if banner:
                print(f"[magenta]📡 Banner on port {port}:[/magenta] {banner.strip().splitlines()[0]}")
    except Exception:
        pass

def scan_ports(target, ports):
    print(f"\n[cyan]🎯 Scanning Target:[/cyan] [bold]{target}[/bold]")
    for port in track(ports, description="[bold green]🔍 Scanning ports...[/bold green]"):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"[green]✅ Port {port} is OPEN[/green]")
                    grab_banner(target, port)
                    if port == 443:
                        detect_ssl(target)
                else:
                    print(f"[red]⛔ Port {port} is CLOSED[/red]")
            except Exception:
                print(f"[yellow]⚠️ Skipped port {port} due to error[/yellow]")

def smart_port_list(target):
    print("[bold yellow]⚙️ Analyzing target for smart scan strategy...[/bold yellow]")
    if detect_ssl(target):
        print("[cyan]🔁 Switching to web-focused port scan.[/cyan]")
        return [80, 443, 8080, 8443]
    else:
        return [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306]

if __name__ == "__main__":
    parser = CustomArgumentParser(
        description="📡 Scan Saurabh - A Smart and Stylish Port Scanner",
        epilog="🛠 Example: python3 scan_saurabh.py example.com --smart\n"
               "🔧 Or: python3 scan_saurabh.py 192.168.1.1 -p 22 80 443",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("target", help="Target IP address or hostname (e.g. 192.168.1.1 or example.com)")
    parser.add_argument(
        "-s", "--smart",
        action="store_true",
        help="Enable smart scan (auto-select ports based on target's behavior)"
    )
    parser.add_argument(
        "-p", "--ports",
        nargs="+",
        type=int,
        help="Custom list of ports to scan (e.g., -p 22 80 443)"
    )

    args = parser.parse_args()

    print_banner()

    try:
        target_ip = socket.gethostbyname(args.target)
        if not ping_host(args.target):
            print("[bold red]❌ Host appears unreachable or down.[/bold red]")
        else:
            if args.smart:
                ports = smart_port_list(args.target)
            elif args.ports:
                ports = args.ports
            else:
                ports = [21, 22, 80, 443, 8080]
            scan_ports(target_ip, ports)
    except socket.gaierror:
        print("[bold red]❌ Error: Invalid hostname or target could not be resolved.[/bold red]")
