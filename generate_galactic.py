"""
B2S Badge Generator — ULTRA RARE GALACTIC SERIES
Style: Orbes lumineux rebondissants, fond galactique, néons cosmiques
Thèmes: Base, Degen, Stack, Cosmic, Galactic

Usage:
  export PINATA_JWT=eyJ...
  python generate_galactic.py

Output: output/galactic/images/ + output/galactic/cids.json
"""

import os, sys, json, time, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import requests

# ─── CONFIG ───────────────────────────────────────────────────
PINATA_JWT   = os.environ.get("PINATA_JWT", "PASTE_YOUR_JWT_HERE")
OUTPUT_DIR   = "output/galactic/images"
CID_FILE     = "output/galactic/cids.json"
START_ID     = 501
END_ID       = 600   # 100 Ultra Rare Galactic
SIZE         = 512
UPLOAD_DELAY = 1.2

# ─── TRAITS GALACTIC / DEGEN / BASE / STACK ───────────────────
TRAITS = [
    # Galactic
    "Galactic Degen", "Cosmic Staker", "Nebula Farmer", "Star Chain Surfer",
    "Void Trader", "Pulsar Validator", "Dark Matter Dev", "Quasar Flipper",
    "Supernova Yield", "Black Hole Liquidity",
    # Base
    "Base OG", "Base Deployer", "Base Native", "L2 Pioneer",
    "Base Chain God", "Onchain Summer", "Base Maxi", "Coinbase Alumni",
    # Degen
    "Full Degen", "Ape In", "Diamond Hands", "Paper Hands Killer",
    "CT Alpha Caller", "Degen Yield Farmer", "100x Degen", "Rugged Survivor",
    # Stack
    "Stack Maxi", "STX OG", "Clarity Wizard", "Stacks Native",
    "BTC L2 Builder", "sBTC Pioneer", "Stack DeFi God", "Nakamoto Upgrade",
    # Cosmic Mix
    "Interplanetary Node", "Zero Gravity Staker", "Cosmic Bridge Runner",
    "Galaxy Brain Trader", "Multichain Astronaut", "DeFi Cosmonaut",
]

# Toujours ultra rare ou legendary
RARITIES = [
    ("rare",      0.25),
    ("epic",      0.40),
    ("legendary", 0.35),
]

# Palettes cosmiques par thème
PALETTES = {
    "galactic": {
        "bg":      [(2, 0, 15), (5, 0, 25), (8, 2, 35)],
        "orbs":    [(120, 0, 255), (0, 200, 255), (255, 0, 180), (255, 200, 0), (0, 255, 150)],
        "glow":    [(180, 50, 255), (50, 220, 255), (255, 50, 200)],
        "stars":   (255, 255, 255),
        "nebula":  [(80, 0, 120), (0, 60, 120), (120, 40, 0)],
    },
    "base": {
        "bg":      [(0, 5, 20), (0, 10, 35), (0, 15, 50)],
        "orbs":    [(0, 100, 255), (50, 150, 255), (100, 200, 255), (255, 255, 255), (0, 200, 255)],
        "glow":    [(0, 120, 255), (50, 170, 255), (100, 220, 255)],
        "stars":   (200, 220, 255),
        "nebula":  [(0, 30, 80), (0, 50, 100), (10, 40, 90)],
    },
    "degen": {
        "bg":      [(15, 0, 5), (25, 0, 10), (35, 5, 0)],
        "orbs":    [(255, 50, 0), (255, 150, 0), (255, 0, 100), (200, 0, 255), (255, 220, 0)],
        "glow":    [(255, 80, 0), (255, 180, 0), (255, 30, 120)],
        "stars":   (255, 200, 150),
        "nebula":  [(80, 20, 0), (60, 10, 20), (80, 40, 0)],
    },
    "stack": {
        "bg":      [(0, 10, 5), (0, 20, 10), (5, 30, 15)],
        "orbs":    [(0, 255, 150), (0, 200, 100), (150, 255, 0), (0, 255, 255), (255, 200, 0)],
        "glow":    [(0, 220, 120), (100, 255, 50), (0, 200, 200)],
        "stars":   (200, 255, 220),
        "nebula":  [(0, 50, 25), (10, 40, 20), (0, 60, 30)],
    },
}

THEME_FOR_TRAIT = {}
for t in TRAITS:
    if any(k in t for k in ["Galactic","Cosmic","Nebula","Star","Void","Pulsar","Dark Matter","Quasar","Supernova","Black Hole","Interplanetary","Zero Gravity","Galaxy","Multichain","DeFi Cosmonaut"]):
        THEME_FOR_TRAIT[t] = "galactic"
    elif any(k in t for k in ["Base","L2","Onchain","Coinbase"]):
        THEME_FOR_TRAIT[t] = "base"
    elif any(k in t for k in ["Degen","Ape","Diamond","Paper","CT","Rugged","100x"]):
        THEME_FOR_TRAIT[t] = "degen"
    else:
        THEME_FOR_TRAIT[t] = "stack"

def pick_rarity(seed: int) -> str:
    random.seed(seed)
    r = random.random()
    cumul = 0
    for name, prob in RARITIES:
        cumul += prob
        if r < cumul:
            return name
    return "epic"

# ─── GÉNÉRATEURS VISUELS ──────────────────────────────────────

def make_galaxy_bg(size: int, palette: dict, seed: int) -> np.ndarray:
    """Fond galactique profond avec gradient radial."""
    rng = np.random.default_rng(seed)
    bg_colors = palette["bg"]
    arr = np.zeros((size, size, 3), dtype=np.float32)

    # Gradient radial depuis le centre
    Y, X = np.ogrid[:size, :size]
    cx, cy = size / 2, size / 2
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2) / (size * 0.7)
    dist = np.clip(dist, 0, 1)

    for c in range(3):
        c0 = bg_colors[2][c] / 255.0
        c1 = bg_colors[0][c] / 255.0
        arr[:, :, c] = c1 + (c0 - c1) * dist

    # Bruit galactique
    noise = rng.normal(0, 0.015, (size, size, 3))
    arr = np.clip(arr + noise, 0, 1)
    return (arr * 255).astype(np.uint8)

def add_nebula(arr: np.ndarray, palette: dict, seed: int) -> np.ndarray:
    """Nuages nébuleux colorés en arrière-plan."""
    rng = np.random.default_rng(seed + 1)
    h, w = arr.shape[:2]

    for _ in range(3):
        color = random.choice(palette["nebula"])
        cx = rng.integers(w // 4, 3 * w // 4)
        cy = rng.integers(h // 4, 3 * h // 4)
        rx = rng.integers(60, 180)
        ry = rng.integers(40, 140)

        Y, X = np.ogrid[:h, :w]
        ellipse = ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2
        mask = ellipse < 1
        intensity = np.clip(1 - ellipse, 0, 1) * 0.25

        for c in range(3):
            arr[:, :, c] = np.where(
                mask,
                np.clip(arr[:, :, c].astype(float) + color[c] * intensity, 0, 255),
                arr[:, :, c]
            ).astype(np.uint8)

    return arr

def add_stars(arr: np.ndarray, palette: dict, seed: int, n: int = 200) -> np.ndarray:
    """Étoiles scintillantes."""
    rng = np.random.default_rng(seed + 2)
    h, w = arr.shape[:2]
    star_color = palette["stars"]

    for _ in range(n):
        x = rng.integers(0, w)
        y = rng.integers(0, h)
        brightness = rng.uniform(0.3, 1.0)
        size = rng.integers(1, 3)

        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                if 0 <= y + dy < h and 0 <= x + dx < w:
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist <= size:
                        fade = brightness * (1 - dist / (size + 1))
                        for c in range(3):
                            arr[y + dy, x + dx, c] = min(255,
                                int(arr[y + dy, x + dx, c] * (1 - fade) + star_color[c] * fade))

    return arr

def draw_glowing_orb(img: Image.Image, cx: float, cy: float,
                     radius: float, color: tuple, intensity: float = 1.0) -> Image.Image:
    """Orbe lumineux avec glow multi-couches."""
    draw_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)

    # Glow externe (grande zone floue)
    for layer, (r_mult, alpha_mult) in enumerate([
        (3.5, 0.06), (2.8, 0.10), (2.2, 0.16), (1.7, 0.25),
        (1.3, 0.40), (1.0, 0.70), (0.6, 0.90), (0.3, 1.00),
    ]):
        r = radius * r_mult
        alpha = int(255 * alpha_mult * intensity)
        alpha = min(255, alpha)
        x0, y0 = cx - r, cy - r
        x1, y1 = cx + r, cy + r
        draw.ellipse([x0, y0, x1, y1], fill=(*color, alpha))

    # Highlight blanc au centre
    hr = radius * 0.25
    draw.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=(255, 255, 255, 180))

    # Blur pour le glow
    draw_layer = draw_layer.filter(ImageFilter.GaussianBlur(radius=radius * 0.8))
    img = Image.alpha_composite(img.convert('RGBA'), draw_layer)
    return img

def compute_orb_positions(token_id: int, n_orbs: int, size: int, frame: int = 0) -> list:
    """Calcule les positions des orbes — effet rebond déterministe."""
    positions = []
    rng = random.Random(token_id * 7919)

    for i in range(n_orbs):
        # Position de base
        base_x = rng.uniform(0.15, 0.85) * size
        base_y = rng.uniform(0.15, 0.85) * size

        # Vitesse de rebond unique par orbe
        vx = rng.uniform(0.8, 2.5) * (1 if rng.random() > 0.5 else -1)
        vy = rng.uniform(0.8, 2.5) * (1 if rng.random() > 0.5 else -1)

        # Calcul position au frame donné (freeze pour image statique)
        t = frame + i * 47
        x = base_x + math.sin(t * vx * 0.05) * size * 0.25
        y = base_y + math.cos(t * vy * 0.05) * size * 0.25
        x = max(40, min(size - 40, x))
        y = max(40, min(size - 40, y))

        radius = rng.uniform(18, 45)
        positions.append((x, y, radius))

    return positions

def draw_orb_trails(img: Image.Image, token_id: int, n_orbs: int,
                    size: int, palette: dict) -> Image.Image:
    """Traînes lumineuses des orbes."""
    draw = ImageDraw.Draw(img, 'RGBA')
    rng = random.Random(token_id * 3141)

    for i in range(n_orbs):
        color = palette["orbs"][i % len(palette["orbs"])]
        # 5 positions passées pour la traîne
        for t_back in range(5, 0, -1):
            positions = compute_orb_positions(token_id, n_orbs, size, frame=-t_back * 3)
            if i < len(positions):
                x, y, r = positions[i]
                alpha = int(30 * (1 - t_back / 6))
                sr = max(2, r * 0.3 * (1 - t_back / 6))
                draw.ellipse([x-sr, y-sr, x+sr, y+sr], fill=(*color, alpha))

    return img

def draw_connection_lines(img: Image.Image, positions: list, palette: dict,
                           token_id: int) -> Image.Image:
    """Lignes de connexion entre orbes proches."""
    draw = ImageDraw.Draw(img, 'RGBA')
    rng = random.Random(token_id)
    color = rng.choice(palette["glow"])

    for i, (x1, y1, r1) in enumerate(positions):
        for j, (x2, y2, r2) in enumerate(positions):
            if j <= i:
                continue
            dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if dist < 180:
                alpha = int(60 * (1 - dist / 180))
                draw.line([(x1, y1), (x2, y2)], fill=(*color, alpha), width=1)

    return img

def draw_badge_frame(img: Image.Image, token_id: int, rarity: str,
                     trait: str, palette: dict) -> Image.Image:
    """Cadre hexagonal + texte du badge."""
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    cx, cy = w // 2, h // 2

    # Couleur frame selon rareté
    frame_colors = {
        "rare":      (0, 200, 255),
        "epic":      (180, 0, 255),
        "legendary": (255, 200, 0),
    }
    fc = frame_colors.get(rarity, (255, 255, 255))

    # Hexagone externe
    r_hex = 200
    for thickness, alpha in [(6, 60), (3, 120), (1, 220)]:
        pts = [(cx + r_hex * math.cos(math.radians(60*i - 30)),
                cy + r_hex * math.sin(math.radians(60*i - 30))) for i in range(6)]
        draw.polygon(pts, outline=(*fc, alpha))

    # Hexagone interne
    r_hex2 = 185
    pts2 = [(cx + r_hex2 * math.cos(math.radians(60*i - 30)),
             cy + r_hex2 * math.sin(math.radians(60*i - 30))) for i in range(6)]
    draw.polygon(pts2, outline=(*fc, 80))

    # Coins décoratifs
    corner_len = 20
    corners = [(cx + r_hex * math.cos(math.radians(60*i - 30)),
                cy + r_hex * math.sin(math.radians(60*i - 30))) for i in range(6)]
    for cx2, cy2 in corners:
        draw.ellipse([cx2-4, cy2-4, cx2+4, cy2+4], fill=(*fc, 255))

    # Token ID en haut
    id_text = f"B2S #{token_id}"
    draw.text((cx - len(id_text)*4, 25), id_text, fill=(*fc, 240))

    # Trait en bas
    draw.text((cx - len(trait)*4, h - 40), trait, fill=(*fc, 200))

    # Rarity indicator
    rarity_icons = {"rare": "◆◆◆", "epic": "★★", "legendary": "🌟 LEGENDARY 🌟"}
    rarity_text = rarity_icons.get(rarity, "◆")
    draw.text((cx - len(rarity_text)*4, h - 25), rarity_text, fill=(*fc, 180))

    return img

def draw_central_symbol(img: Image.Image, token_id: int, trait: str,
                         palette: dict, rarity: str) -> Image.Image:
    """Symbole central selon le thème."""
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    cx, cy = w // 2, h // 2

    theme = THEME_FOR_TRAIT.get(trait, "galactic")
    color = palette["orbs"][0]

    symbols = {
        "galactic": "✦",
        "base":     "B",
        "degen":    "Ξ",
        "stack":    "S",
    }
    symbol = symbols.get(theme, "✦")

    # Cercle central
    r = 35
    draw.ellipse([cx-r, cy-r, cx+r, cy+r],
                 outline=(*color, 200), fill=(*color, 20), width=2)

    # Symbole
    draw.text((cx - 8, cy - 10), symbol, fill=(*color, 240))

    return img

def generate_galactic_badge(token_id: int, rarity: str, trait: str) -> Image.Image:
    """Pipeline complet — badge galactique avec orbes rebondissants."""
    seed = token_id * 2053 + hash(trait) % 10000

    theme = THEME_FOR_TRAIT.get(trait, "galactic")
    palette = PALETTES[theme]

    # Nombre d'orbes selon rareté
    n_orbs_map = {"rare": 4, "epic": 6, "legendary": 9}
    n_orbs = n_orbs_map.get(rarity, 5)

    # 1. Fond galactique
    arr = make_galaxy_bg(SIZE, palette, seed)

    # 2. Nébuleuses
    arr = add_nebula(arr, palette, seed)

    # 3. Étoiles
    n_stars = {"rare": 150, "epic": 220, "legendary": 350}.get(rarity, 200)
    arr = add_stars(arr, palette, seed, n=n_stars)

    # 4. Vers PIL RGBA
    img = Image.fromarray(arr, 'RGB').convert('RGBA')

    # 5. Traînes des orbes
    img = draw_orb_trails(img, token_id, n_orbs, SIZE, palette)

    # 6. Lignes de connexion
    positions = compute_orb_positions(token_id, n_orbs, SIZE, frame=token_id % 60)
    img = draw_connection_lines(img, positions, palette, token_id)

    # 7. Orbes lumineux
    for i, (ox, oy, radius) in enumerate(positions):
        color = palette["orbs"][i % len(palette["orbs"])]
        intensity = 1.0 if rarity == "legendary" else 0.8
        img = draw_glowing_orb(img, ox, oy, radius, color, intensity)

    # 8. Cadre hexagonal + texte
    img = draw_badge_frame(img, token_id, rarity, trait, palette)

    # 9. Symbole central
    img = draw_central_symbol(img, token_id, trait, palette, rarity)

    # 10. Post-processing
    img = img.convert('RGB')
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    # Legendary : double glow blur
    if rarity == "legendary":
        img_blur = img.filter(ImageFilter.GaussianBlur(radius=1.5))
        img = Image.blend(img, img_blur, alpha=0.2)

    return img

# ─── UPLOAD PINATA ────────────────────────────────────────────

def upload_to_pinata(filepath: str, name: str) -> str | None:
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    with open(filepath, "rb") as f:
        files = {"file": (name, f, "image/png")}
        data  = {"pinataMetadata": json.dumps({"name": name})}
        try:
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            resp.raise_for_status()
            return resp.json()["IpfsHash"]
        except Exception as e:
            print(f"  ❌ Upload failed: {e}")
            return None

# ─── MAIN ─────────────────────────────────────────────────────

def main():
    if PINATA_JWT == "PASTE_YOUR_JWT_HERE":
        print("❌ Set PINATA_JWT first!")
        print("   export PINATA_JWT=eyJ...")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs("output/galactic", exist_ok=True)

    existing = {}
    if os.path.exists(CID_FILE):
        with open(CID_FILE) as f:
            existing = json.load(f)

    total = END_ID - START_ID + 1
    print(f"🌌 Generating & uploading {total} ULTRA RARE GALACTIC badges #{START_ID}-#{END_ID}")
    print(f"🎨 Themes: Galactic / Base / Degen / Stack")
    print(f"⭐ Rarities: Rare / Epic / Legendary ONLY")
    print(f"🔑 Pinata JWT: {PINATA_JWT[:20]}...")
    print()

    results = dict(existing)

    for i, token_id in enumerate(range(START_ID, END_ID + 1)):
        key = str(token_id)

        if key in results:
            print(f"  ⏭  #{token_id} already uploaded: {results[key]['cid']}")
            continue

        rarity = pick_rarity(token_id * 31)
        trait  = TRAITS[token_id % len(TRAITS)]
        theme  = THEME_FOR_TRAIT.get(trait, "galactic")

        print(f"  [{i+1}/{total}] #{token_id} {rarity:10s} [{theme:8s}] {trait:30s}", end=" ", flush=True)

        img_path = os.path.join(OUTPUT_DIR, f"galactic_{token_id}.png")

        if not os.path.exists(img_path):
            img = generate_galactic_badge(token_id, rarity, trait)
            img.save(img_path, "PNG", optimize=True)
            print(f"✏️  generated", end=" ", flush=True)
        else:
            print(f"📦 cached", end=" ", flush=True)

        cid = upload_to_pinata(img_path, f"b2s-galactic-{token_id}.png")
        if cid:
            results[key] = {
                "tokenId": token_id,
                "cid": cid,
                "rarity": rarity,
                "trait": trait,
                "theme": theme,
                "series": "galactic"
            }
            print(f"✅ {cid}")
        else:
            print(f"❌ will retry next run")

        with open(CID_FILE, "w") as f:
            json.dump(results, f, indent=2)

        time.sleep(UPLOAD_DELAY)

    uploaded = len(results)
    print(f"\n🌌 Done! {uploaded}/{total} galactic badges uploaded")
    print(f"📄 CIDs saved to {CID_FILE}")
    print(f"\n🔧 Next: python generate_galactic_tsx.py")

if __name__ == "__main__":
    main()
