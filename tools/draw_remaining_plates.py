"""Original CAD plates for remaining zip overlays. Bold strokes. Live copy."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "drawings"
OUT.mkdir(parents=True, exist_ok=True)

C = "#47b1dc"
C2 = "#5cb9e9"
INK = "#eef4f8"
MUTED = "#9ec9dc"
BG = "#010d1d"
SEAL = "../signet7-circle-logo-official-v2.png"


def t(x, y, s, size=12, fill=C2, anchor="start", family="Consolas, monospace", ls="1.4", weight="400"):
    s = (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-family="{family}" '
        f'text-anchor="{anchor}" letter-spacing="{ls}" font-weight="{weight}">{s}</text>'
    )


def rect(x, y, w, h, sw=2.4, fill="none", stroke=C):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def chrome(title, dwg):
    return "\n".join(
        [
            f'<rect width="1920" height="1080" fill="{BG}"/>',
            '<rect width="1920" height="1080" fill="url(#grid)"/>',
            rect(18, 18, 1884, 1044, 3.0, "none", C),
            rect(28, 28, 1864, 1024, 1.6, "none", C),
            f'<path d="M6 18 H30 M18 6 V30" stroke="{C2}" stroke-width="2.6"/>',
            f'<path d="M1890 18 H1914 M1902 6 V30" stroke="{C2}" stroke-width="2.6"/>',
            f'<path d="M6 1062 H30 M18 1050 V1074" stroke="{C2}" stroke-width="2.6"/>',
            f'<path d="M1890 1062 H1914 M1902 1050 V1074" stroke="{C2}" stroke-width="2.6"/>',
            rect(40, 40, 1840, 88, 2.2, "none", C),
            f'<image href="{SEAL}" x="52" y="52" width="64" height="64"/>',
            t(128, 78, "SIGNET7.IO", 22, INK, family="Segoe UI, Arial, sans-serif", ls="3", weight="600"),
            t(128, 102, "VERIFY  ·  SEAL  ·  TRUST", 10, MUTED, ls="2.4"),
            t(430, 90, title, 18, INK, family="Segoe UI, Arial, sans-serif", ls="1.4", weight="600"),
            t(1180, 70, f"DRAWING  {dwg}", 10, MUTED),
            t(1180, 88, "DATE  17 SEP 26   REV E   SCALE NTS", 10, MUTED),
            t(1180, 106, "DRAWN  S7 SYSTEMS", 10, MUTED),
            f'<rect x="1660" y="58" width="200" height="52" fill="{C2}" stroke="{C2}" stroke-width="2.6"/>'
            + t(1760, 90, "LIVE CHECK", 12, BG, "middle", ls="1.8"),
        ]
    )


def foot(title):
    return "\n".join(
        [
            rect(40, 930, 1840, 110, 2.4, "none", C),
            t(60, 972, "SCALE 1:1 NTS", 12, MUTED),
            f'<line x1="240" y1="968" x2="560" y2="968" stroke="{C2}" stroke-width="3.6"/>',
            *[
                f'<line x1="{240 + i * 80}" y1="958" x2="{240 + i * 80}" y2="978" stroke="{C2}" stroke-width="2.2"/>'
                + t(240 + i * 80, 1000, lab, 10, MUTED, "middle")
                for i, lab in enumerate(["0", "50", "100", "150", "200"])
            ],
            t(620, 968, "GRID ON · SNAP ON · ORTHO ON · UNITS mm · THIRD ANGLE", 11, MUTED, ls="1.1"),
            t(620, 996, title, 14, INK, family="Segoe UI, Arial, sans-serif", ls="0.6", weight="600"),
            f'<image href="{SEAL}" x="1788" y="948" width="72" height="72"/>',
        ]
    )


DEFS = f"""
  <defs>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0 H0 V32" fill="none" stroke="{C}" stroke-width="0.85" opacity="0.28"/>
    </pattern>
    <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="{C}" stroke-width="1.5" opacity="0.7"/>
    </pattern>
  </defs>
"""


def wrap(name, title, dwg, body, footer):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
{DEFS}
{chrome(title, dwg)}
{body}
{foot(footer)}
</svg>
'''
    path = OUT / name
    path.write_text(svg, encoding="utf-8")
    print("wrote", path.name, path.stat().st_size)


# ABOUT — founding team
people = [
    (80, 180, "S7-P-01", "SAMUEL J. SANDERSON", "Founder"),
    (520, 180, "S7-P-02", "JUSTIN D. DAINES", "CO-Founder"),
    (960, 180, "S7-P-03", "JOSH S. RILEY", "Founding Team Member"),
    (1400, 180, "S7-P-04", "GEORGE TERRIS", "Founding Team Member · marketing"),
]
boxes = []
for x, y, pid, name, role in people:
    boxes.append(rect(x, y, 400, 160, 2.6, "none", C))
    boxes.append(t(x + 20, y + 40, pid, 11, MUTED, ls="2"))
    boxes.append(t(x + 20, y + 78, name, 16, INK, family="Segoe UI, Arial, sans-serif", ls="0.8", weight="600"))
    boxes.append(t(x + 20, y + 108, role, 13, C2, family="Segoe UI, Arial, sans-serif", ls="0.4"))
    boxes.append(t(x + 20, y + 136, "Working role. Not an officer title.", 11, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2"))
env = f'''
<g fill="none" stroke="{C2}" stroke-width="4.2">
  <rect x="620" y="400" width="680" height="430"/>
  <path d="M620 400 L960 620 L1300 400"/>
  <rect x="924" y="560" width="72" height="58" rx="4" fill="{BG}" stroke-width="4"/>
  <path d="M940 560 V538 A16 16 0 0 1 980 538 V560"/>
  <circle cx="960" cy="588" r="54" stroke="{C}" stroke-width="2.4"/>
</g>
'''
wrap(
    "about-sheet.svg",
    "FOUNDING TEAM",
    "S7-AB-001",
    "\n".join(boxes)
    + env
    + t(80, 390, "Important mail should be sealed.", 28, INK, family="Segoe UI, Arial, sans-serif", ls="-0.2", weight="600")
    + t(80, 430, "Pre-formation project. Checkout is not live. Recipients never install.", 14, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2"),
    "ABOUT  ·  FOUNDING TEAM  ·  NOT OFFICER TITLES",
)

# ABOUT cyber variant — isometric envelope + same four names as callouts
wrap(
    "about-cyber-sheet.svg",
    "ABOUT  ·  CYBER VARIANT",
    "S7-AB-002",
    f'''
{t(80, 200, "Same facts. Different sheet.", 36, INK, family="Segoe UI, Arial, sans-serif", ls="-0.3", weight="600")}
{t(80, 240, "Recipients never install. Company Signet7 is free for 3 months.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
<g fill="none" stroke="{C2}" stroke-width="4" transform="translate(520,260)">
  <polygon points="80,360 560,360 760,200 280,200"/>
  <polygon points="280,200 760,200 760,40 280,40"/>
  <polygon points="560,360 760,200 760,40 560,200"/>
  <path d="M280 40 L520 140 L760 40" stroke-width="3.6"/>
  <rect x="488" y="100" width="64" height="50" rx="3" fill="{BG}"/>
  <circle cx="520" cy="124" r="42" stroke="{C}" stroke-width="2.6"/>
</g>
{rect(80, 640, 400, 120, 2.6)}{t(100, 690, "SANDERSON  ·  FOUNDER", 14, INK, family="Segoe UI, Arial, sans-serif", ls="0.8", weight="600")}
{rect(520, 640, 400, 120, 2.6)}{t(540, 690, "DAINES  ·  CO-FOUNDER", 14, INK, family="Segoe UI, Arial, sans-serif", ls="0.8", weight="600")}
{rect(960, 640, 400, 120, 2.6)}{t(980, 690, "RILEY  ·  FOUNDING TEAM", 14, INK, family="Segoe UI, Arial, sans-serif", ls="0.8", weight="600")}
{rect(1400, 640, 400, 120, 2.6)}{t(1420, 690, "TERRIS  ·  MARKETING", 14, INK, family="Segoe UI, Arial, sans-serif", ls="0.8", weight="600")}
''',
    "ABOUT  ·  CYBER VARIANT  ·  SAME FACTS",
)

# ARCHITECTURE — two companies
wrap(
    "architecture-sheet.svg",
    "TWO COMPANIES  ·  LISTING",
    "S7-AR-001",
    f'''
{t(80, 200, "Two companies. Two listings.", 36, INK, family="Segoe UI, Arial, sans-serif", ls="-0.3", weight="600")}
{t(80, 240, "Mail in between can be checked. Not a phone book of every company.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(200, 320, 520, 420, 3.2)}
{t(460, 380, "COMPANY A", 18, C2, "middle", ls="2", weight="600")}
{t(460, 430, "Named work email", 16, INK, "middle", family="Segoe UI, Arial, sans-serif")}
{t(460, 470, "Own key  ·  listed or not", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
{rect(1200, 320, 520, 420, 3.2)}
{t(1460, 380, "COMPANY B", 18, C2, "middle", ls="2", weight="600")}
{t(1460, 430, "Named work email", 16, INK, "middle", family="Segoe UI, Arial, sans-serif")}
{t(1460, 470, "Own key  ·  listed or not", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
<line x1="720" y1="530" x2="1200" y2="530" stroke="{C2}" stroke-width="4.2"/>
<polygon points="1200,530 1178,518 1178,542" fill="{C2}"/>
<polygon points="720,530 742,518 742,542" fill="{C2}"/>
{t(960, 510, "CHECKED MAIL", 13, C2, "middle", ls="2")}
{t(960, 580, "Live check  ·  two facts", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
''',
    "ARCHITECTURE  ·  TWO LISTINGS  ·  NOT A DIRECTORY",
)

# DESK — register
wrap(
    "desk-sheet.svg",
    "COMPANY DESK  ·  REGISTER",
    "S7-DK-001",
    f'''
{t(80, 200, "Register the company.", 40, INK, family="Segoe UI, Arial, sans-serif", ls="-0.3", weight="600")}
{t(80, 250, "Then name the work emails in Signet7 desktop. Recipients never install.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(120, 320, 780, 480, 3.2)}
{t(160, 380, "ITEM 01  ACCOUNT", 14, MUTED, ls="2")}
{t(160, 430, "Company login", 28, INK, family="Segoe UI, Arial, sans-serif", ls="0.4", weight="600")}
{t(160, 480, "Not the desktop app. Not every laptop.", 16, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(1020, 320, 780, 220, 3.2)}
{t(1060, 380, "ITEM 02  DESK", 14, MUTED, ls="2")}
{t(1060, 430, "Download after sign-in", 22, INK, family="Segoe UI, Arial, sans-serif", ls="0.3", weight="600")}
{rect(1020, 580, 780, 220, 3.2)}
{t(1060, 640, "ITEM 03  LIVE CHECK", 14, MUTED, ls="2")}
{t(1060, 690, "Anyone. No account.", 22, INK, family="Segoe UI, Arial, sans-serif", ls="0.3", weight="600")}
''',
    "REGISTER  ·  COMPANY DESK  ·  ZIP AFTER SIGN-IN",
)

# DESKTOP
wrap(
    "desktop-sheet.svg",
    "SIGNET7 DESKTOP",
    "S7-DT-001",
    f'''
{t(80, 200, "Named work emails. Company computers only.", 32, INK, family="Segoe UI, Arial, sans-serif", ls="-0.2", weight="600")}
{t(80, 248, "Not the desktop app on every staff laptop. Recipients never install.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(120, 300, 1680, 520, 3.4)}
{rect(160, 340, 520, 440, 2.8)}
{t(180, 390, "INBOX A", 14, MUTED, ls="2")}
{t(180, 440, "Purchasing", 24, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(180, 490, "Own listing  ·  own key", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(700, 340, 520, 440, 2.8)}
{t(720, 390, "INBOX B", 14, MUTED, ls="2")}
{t(720, 440, "Billing", 24, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(720, 490, "Own listing  ·  own key", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(1240, 340, 520, 440, 2.8)}
{t(1260, 390, "INBOX C", 14, MUTED, ls="2")}
{t(1260, 440, "Trust / intake", 24, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1260, 490, "Own listing  ·  own key", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
''',
    "DESKTOP  ·  NAMED WORK EMAILS  ·  NOT EVERY LAPTOP",
)

# DOWNLOAD
wrap(
    "download-sheet.svg",
    "SIGNET7 DESKTOP  ·  DOWNLOAD",
    "S7-DL-001",
    f'''
{t(80, 200, "Register first. Then the zip.", 40, INK, family="Segoe UI, Arial, sans-serif", ls="-0.3", weight="600")}
{t(80, 250, "Windows, Mac, and Linux. Recipients never download this.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(120, 320, 520, 480, 3.2)}{t(380, 520, "WINDOWS", 22, INK, "middle", family="Segoe UI, Arial, sans-serif", weight="600")}{t(380, 560, "Office computer", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
{rect(700, 320, 520, 480, 3.2)}{t(960, 520, "MAC", 22, INK, "middle", family="Segoe UI, Arial, sans-serif", weight="600")}{t(960, 560, "Office computer", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
{rect(1280, 320, 520, 480, 3.2)}{t(1540, 520, "LINUX", 22, INK, "middle", family="Segoe UI, Arial, sans-serif", weight="600")}{t(1540, 560, "Office computer", 14, MUTED, "middle", family="Segoe UI, Arial, sans-serif")}
''',
    "DOWNLOAD  ·  REGISTER FIRST  ·  UNSIGNED PREVIEW",
)

# FAQ
wrap(
    "faq-sheet.svg",
    "FAQ  ·  THE SHORT ANSWERS",
    "S7-FQ-001",
    f'''
{rect(80, 170, 860, 220, 2.8)}
{t(110, 220, "FAQ-001", 12, MUTED, ls="2")}
{t(110, 260, "I got an important email. What do I do?", 18, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(110, 300, "Keep the original. Open the live check. Recipients never install.", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(980, 170, 860, 220, 2.8)}
{t(1010, 220, "FAQ-002", 12, MUTED, ls="2")}
{t(1010, 260, "Do recipients install?", 18, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1010, 300, "No. They use the website check. No app, plugin, or account.", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(80, 430, 860, 220, 2.8)}
{t(110, 480, "FAQ-003", 12, MUTED, ls="2")}
{t(110, 520, "What does no seal mean?", 18, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(110, 560, "Ordinary mail. Unknown is not fraud.", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(980, 430, 860, 220, 2.8)}
{t(1010, 480, "FAQ-004", 12, MUTED, ls="2")}
{t(1010, 520, "Does a match mean pay?", 18, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1010, 560, "No. Match is not advice to pay. Checkout is not live.", 14, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(80, 690, 1760, 180, 2.8)}
{t(110, 750, "READY  ·  live check", 16, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(620, 750, "PREVIEW  ·  desktop unsigned", 16, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1180, 750, "NOT YET  ·  checkout not live", 16, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
''',
    "FAQ  ·  SHORT ANSWERS  ·  MATCH IS NOT PAY",
)

# HOW
wrap(
    "how-sheet.svg",
    "HOW IT WORKS",
    "S7-HW-001",
    f'''
{t(80, 200, "Seal the email. Then anyone can verify.", 32, INK, family="Segoe UI, Arial, sans-serif", ls="-0.2", weight="600")}
{rect(80, 280, 540, 520, 3.2)}
{t(110, 340, "01", 14, MUTED, ls="2")}
{t(110, 400, "WRITE", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(110, 450, "In the mail you already use.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{t(110, 490, "Signet7 is not a composer.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(690, 280, 540, 520, 3.2)}
{t(720, 340, "02", 14, MUTED, ls="2")}
{t(720, 400, "SEAL", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(720, 450, "Optional cryptographic stamp", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{t(720, 490, "on the outgoing message.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(1300, 280, 540, 520, 3.2)}
{t(1330, 340, "03", 14, MUTED, ls="2")}
{t(1330, 400, "CHECK", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1330, 450, "Two facts. Signed file you keep.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{t(1330, 490, "Recipients never install.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
''',
    "HOW  ·  WRITE / SEAL / CHECK",
)

# OUTLOOK — optional
wrap(
    "outlook-sheet.svg",
    "OUTLOOK  ·  OPTIONAL PANE",
    "S7-OL-001",
    f'''
{t(80, 200, "Name the work emails that can move money.", 30, INK, family="Segoe UI, Arial, sans-serif", ls="-0.2", weight="600")}
{t(80, 246, "Outlook XML is optional. Recipients never install. The website check is the door.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(120, 300, 1000, 520, 3.4)}
{t(160, 360, "MESSAGE", 14, MUTED, ls="2")}
{rect(160, 390, 920, 380, 2.6, "none", C2)}
{t(200, 460, "From: named work email", 18, INK, family="Segoe UI, Arial, sans-serif")}
{t(200, 510, "Seal present or not", 18, INK, family="Segoe UI, Arial, sans-serif")}
{rect(1180, 300, 640, 520, 3.4)}
{t(1220, 360, "OPTIONAL PANE", 14, MUTED, ls="2")}
{t(1220, 430, "IT can add from file.", 18, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1220, 480, "Not AppSource.", 16, MUTED, family="Segoe UI, Arial, sans-serif")}
{t(1220, 530, "Not required to check.", 16, MUTED, family="Segoe UI, Arial, sans-serif")}
''',
    "OUTLOOK  ·  OPTIONAL  ·  WEBSITE CHECK REMAINS",
)

# PROGRAMS
wrap(
    "programs-sheet.svg",
    "PROGRAMS  ·  CHECKOUT NOT LIVE",
    "S7-PG-001",
    f'''
{t(80, 200, "Seal. Check for free. Desktop for named emails.", 28, INK, family="Segoe UI, Arial, sans-serif", ls="-0.2", weight="600")}
{t(80, 244, "Checkout is not live. Amounts are not a public offer.", 16, MUTED, family="Segoe UI, Arial, sans-serif", ls="0.2")}
{rect(80, 300, 560, 500, 3.2)}
{t(110, 360, "S7-F-01", 12, MUTED, ls="2")}
{t(110, 420, "SEAL", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(110, 470, "Outgoing mail you already write.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(680, 300, 560, 500, 3.2)}
{t(710, 360, "S7-F-02", 12, MUTED, ls="2")}
{t(710, 420, "CHECK", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(710, 470, "Free. No account. Two facts.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
{rect(1280, 300, 560, 500, 3.2)}
{t(1310, 360, "S7-F-03", 12, MUTED, ls="2")}
{t(1310, 420, "DESKTOP", 26, INK, family="Segoe UI, Arial, sans-serif", weight="600")}
{t(1310, 470, "Several work emails. Not every laptop.", 15, MUTED, family="Segoe UI, Arial, sans-serif")}
''',
    "PROGRAMS  ·  CHECKOUT NOT LIVE  ·  NO PUBLIC PRICE",
)

print("done", list(OUT.glob("*-sheet.svg")))
