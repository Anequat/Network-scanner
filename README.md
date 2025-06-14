# Scan Saurabh - Smart & Stylish Port Scanner 🚀

**Scan Saurabh** is a Python-based port scanner that blends functionality with style. Designed for ethical hacking, bug bounty hunting, and network diagnostics, it provides smart scanning features, SSL detection, and colorful output using `rich`.

## 🌟 Features
- 🎨 Beautiful terminal output with [rich](https://github.com/Textualize/rich)
- 🔍 **Smart Scan Mode**: Automatically selects common or web-focused ports based on SSL detection
- ⚡ Fast scanning with progress tracking
- 📡 Grabs HTTP banners from open ports
- 🔒 Detects SSL certificates and protocol versions
- 🛠 Accepts custom port lists for flexible scanning
- 💡 Helpful CLI with clear error handling and usage examples

## 📦 Requirements
- Python 3.6+
- rich (`pip install rich`)

## 🚀 Installation
```bash
git clone https://github.com/yourusername/scan-saurabh.git
cd scan-saurabh
pip install rich

🛠 Usage

# Smart scan mode (auto port selection)
python3 scan.py example.com --smart

# Custom ports
python3 scan.py 192.168.1.1 -p 22 80 443

Options
Option	Description
target	Target IP address or hostname
-s, --smart	Enable smart scan (auto-select ports based on target's behavior)
-p, --ports	Specify custom ports to scan (e.g., -p 22 80 443)
📌 Example

python3 scan.py scanme.nmap.org --smart

⚠ Disclaimer

This tool is for educational purposes and authorized testing only. Use responsibly and ensure you have permission to scan the target.   
