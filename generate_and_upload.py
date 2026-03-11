"""
B2S Badge Generator — Série #201-500 — Glitch Art / Distortion
Génère 300 images PNG 512x512 puis les upload sur Pinata IPFS.

Usage:
  1. Set PINATA_JWT dans le terminal ou dans ce fichier
  2. python generate_and_upload.py
  3. Les CIDs sont sauvés dans output/cids.json
"""

import os, sys, json, time, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import requests

# ─── CONFIG ───────────────────────────────────────────────────
PINATA_JWT   = os.environ.get("PINATA_JWT", "PASTE_YOUR_JWT_HERE")
OUTPUT_DIR   = "output/images"
CID_FILE     = "output/cids.json"
START_ID     = 201
END_ID       = 500   # inclus
SIZE         = 512
UPLOAD_DELAY = 1.2   # secondes entre uploads (évite rate-limit Pinata)

# ─── TRAITS MIX INFOSEC + WEB3 ────────────────────────────────
TRAITS = [
    # Infosec étendu
    "Social Engineer", "Malware Dev", "Exploit Writer", "Forensic Analyst",
    "Dark Web Scout", "Payload Crafter", "APT Operator", "Reverse Engineer",
    "Fuzzer", "Shellcoder", "Network Sniffer", "Steganographer",
    # Web3 / DeFi
    "DeFi Hacker", "Flash Loan Wizard", "MEV Hunter", "Smart Contract Auditor",
    "Bridge Exploiter", "Rug Detector", "Whale Watcher", "Liquidity Sniper",
    "On-Chain Analyst", "Governance Voter", "Yield Optimizer", "Cross-Chain Ranger",
    # Mix
    "Blockchain Forensic", "Crypto OSINT", "Web3 Red Team", "DAO Infiltrator",
    "Token Engineer", "ZK Prover", "Sandwich Botter", "Mempool Watcher",
]

RARITIES = [
    ("common",    0.45),
    ("uncommon",  0.28),
    ("rare",      0.17),
    ("epic",      0.07),
    ("legendary", 0.03),
]

# Palettes Glitch Art par rareté
PALETTES = {
    "common":    [(20,20,30), (0,255,150), (0,180,255), (30,30,50)],
    "uncommon":  [(10,10,25), (0,255,100), (100,0,255), (255,0,150)],
    "rare":      [(5,5,20),   (0,200,255), (255,50,200), (50,255,200)],
    "epic":      [(15,0,30),  (180,0,255), (255,0,100), (0,255,255)],
    "legendary": [(0,0,10),   (255,200,0), (255,50,0),  (255,255,100)],
}

def pick_rarity() -> str:
    r = random.random()
    cumul = 0
    for name, prob in RARITIES:
        cumul += prob
        if r < cumul:
            return name
    return "common"

# ─── GÉNÉRATEUR GLITCH ART ────────────────────────────────────

def make_base(size: int, palette: list) -> np.ndarray:
    """Fond dégradé sombre avec bruit."""
    bg, c1, c2, c3 = palette
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        t = y / size
        r = int(bg[0] + (c1[0] - bg[0]) * t * 0.3)
        g = int(bg[1] + (c1[1] - bg[1]) * t * 0.3)
        b = int(bg[2] + (c1[2] - bg[2]) * t * 0.3)
        arr[y] = [r, g, b]
    # Bruit subtil
    noise = np.random.randint(-8, 8, (size, size, 3))
    arr = np.clip(arr.astype(int) + noise, 0, 255).astype(np.uint8)
    return arr

def add_scanlines(arr: np.ndarray, intensity: float = 0.15) -> np.ndarray:
    """Lignes horizontales type CRT."""
    for y in range(0, arr.shape[0], 3):
        arr[y] = (arr[y] * (1 - intensity)).astype(np.uint8)
    return arr

def add_glitch_slices(arr: np.ndarray, palette: list, n: int = 12) -> np.ndarray:
    """Tranches horizontales décalées — effet glitch principal."""
    h, w = arr.shape[:2]
    for _ in range(n):
        y1 = random.randint(0, h - 20)
        h_slice = random.randint(2, 18)
        y2 = min(y1 + h_slice, h)
        shift = random.randint(-40, 40)
        slice_row = arr[y1:y2].copy()
        arr[y1:y2] = np.roll(slice_row, shift, axis=1)
        # Colorise la tranche avec couleur palette
        color = random.choice(palette[1:])
        mask = np.random.rand(y2-y1, w) > 0.7
        for c, val in enumerate(color):
            arr[y1:y2, :, c] = np.where(mask, np.clip(arr[y1:y2, :, c].astype(int) + val // 3, 0, 255), arr[y1:y2, :, c])
    return arr

def add_rgb_split(arr: np.ndarray, shift: int = 6) -> np.ndarray:
    """Séparation des canaux RGB — aberration chromatique."""
    r = np.roll(arr[:,:,0], shift, axis=1)
    b = np.roll(arr[:,:,2], -shift, axis=1)
    arr[:,:,0] = r
    arr[:,:,2] = b
    return arr

def add_neon_lines(img: Image.Image, palette: list, n: int = 8) -> Image.Image:
    """Lignes néon verticales/horizontales lumineuses."""
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    for _ in range(n):
        color = random.choice(palette[1:])
        alpha = random.randint(80, 200)
        thickness = random.randint(1, 3)
        if random.random() > 0.5:
            x = random.randint(0, w)
            draw.line([(x, 0), (x, h)], fill=(*color, alpha), width=thickness)
        else:
            y = random.randint(0, h)
            draw.line([(0, y), (w, y)], fill=(*color, alpha), width=thickness)
    return img

def add_hex_grid(img: Image.Image, palette: list, opacity: int = 40) -> Image.Image:
    """Grille hexagonale subtile en overlay."""
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    color = random.choice(palette[1:])
    step = random.randint(30, 60)
    for x in range(0, w, step):
        for y in range(0, h, step):
            r = step // 3
            pts = [(x + r*math.cos(math.radians(60*i)), y + r*math.sin(math.radians(60*i))) for i in range(6)]
            draw.polygon(pts, outline=(*color, opacity))
    return img

def add_data_corruption(arr: np.ndarray, palette: list, blocks: int = 6) -> np.ndarray:
    """Blocs de corruption de données — rectangles pixelisés."""
    h, w = arr.shape[:2]
    for _ in range(blocks):
        x1 = random.randint(0, w - 60)
        y1 = random.randint(0, h - 20)
        bw = random.randint(20, 80)
        bh = random.randint(4, 16)
        x2, y2 = min(x1+bw, w), min(y1+bh, h)
        color = random.choice(palette[1:])
        intensity = random.random()
        arr[y1:y2, x1:x2] = np.clip(
            arr[y1:y2, x1:x2].astype(int) * (1-intensity) + np.array(color) * intensity,
            0, 255
        ).astype(np.uint8)
    return arr

def add_vignette(arr: np.ndarray) -> np.ndarray:
    """Vignette sombre sur les bords."""
    h, w = arr.shape[:2]
    Y, X = np.ogrid[:h, :w]
    cx, cy = w/2, h/2
    dist = np.sqrt(((X-cx)/cx)**2 + ((Y-cy)/cy)**2)
    vignette = np.clip(1 - dist * 0.6, 0.3, 1.0)
    arr = (arr * vignette[:,:,np.newaxis]).astype(np.uint8)
    return arr

def draw_badge_symbol(img: Image.Image, token_id: int, palette: list, rarity: str) -> Image.Image:
    """Symbole central : hexagone + ID du badge."""
    draw = ImageDraw.Draw(img, 'RGBA')
    w, h = img.size
    cx, cy = w//2, h//2
    color = palette[1]

    # Hexagone externe
    r_outer = 90
    pts_outer = [(cx + r_outer*math.cos(math.radians(60*i - 30)),
                  cy + r_outer*math.sin(math.radians(60*i - 30))) for i in range(6)]
    draw.polygon(pts_outer, outline=(*color, 200), fill=(*color, 20))

    # Hexagone interne
    r_inner = 65
    pts_inner = [(cx + r_inner*math.cos(math.radians(60*i - 30)),
                  cy + r_inner*math.sin(math.radians(60*i - 30))) for i in range(6)]
    c2 = palette[2]
    draw.polygon(pts_inner, outline=(*c2, 160), fill=(*c2, 10))

    # Texte ID
    id_str = f"#{token_id}"
    # Taille manuelle (sans font TTF)
    char_w = 8
    text_x = cx - len(id_str) * char_w // 2
    draw.text((text_x, cy - 8), id_str, fill=(*color, 240))

    # Rarity dots
    rarity_map = {"common":1, "uncommon":2, "rare":3, "epic":4, "legendary":5}
    n_dots = rarity_map.get(rarity, 1)
    dot_r = 4
    spacing = 14
    start_x = cx - (n_dots-1)*spacing//2
    for i in range(n_dots):
        dx = start_x + i*spacing
        draw.ellipse([dx-dot_r, cy+30-dot_r, dx+dot_r, cy+30+dot_r], fill=(*color, 220))

    return img

def generate_badge(token_id: int, rarity: str, trait: str) -> Image.Image:
    """Pipeline complet de génération d'un badge Glitch Art."""
    random.seed(token_id * 137 + hash(trait) % 1000)
    np.random.seed(token_id % (2**31))

    palette = PALETTES[rarity]

    # 1. Base
    arr = make_base(SIZE, palette)

    # 2. Effets glitch numpy
    arr = add_glitch_slices(arr, palette, n=random.randint(8, 20))
    arr = add_data_corruption(arr, palette, blocks=random.randint(4, 10))
    arr = add_rgb_split(arr, shift=random.randint(3, 12))
    arr = add_scanlines(arr, intensity=0.12)
    arr = add_vignette(arr)

    # 3. Vers PIL
    img = Image.fromarray(arr, 'RGB').convert('RGBA')

    # 4. Effets PIL
    img = add_neon_lines(img, palette, n=random.randint(5, 15))
    img = add_hex_grid(img, palette, opacity=random.randint(20, 60))
    img = draw_badge_symbol(img, token_id, palette, rarity)

    # 5. Post-processing
    img = img.convert('RGB')
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.4)

    # Léger blur sur legendary pour effet glow
    if rarity == "legendary":
        img_blur = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = Image.blend(img, img_blur, alpha=0.3)

    return img

# ─── UPLOAD PINATA ────────────────────────────────────────────

def upload_to_pinata(filepath: str, name: str) -> str | None:
    """Upload un fichier sur Pinata, retourne le CID."""
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    with open(filepath, "rb") as f:
        files = {"file": (name, f, "image/png")}
        data  = {"pinataMetadata": json.dumps({"name": name})}
        try:
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)
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

    # Charge CIDs existants
    existing = {}
    if os.path.exists(CID_FILE):
        with open(CID_FILE) as f:
            existing = json.load(f)

    total = END_ID - START_ID + 1
    print(f"🎨 Generating & uploading {total} Glitch Art badges #{START_ID}-#{END_ID}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"🔑 Pinata JWT: {PINATA_JWT[:20]}...")
    print()

    results = dict(existing)

    for i, token_id in enumerate(range(START_ID, END_ID + 1)):
        key = str(token_id)

        # Skip si déjà uploadé
        if key in results:
            print(f"  ⏭  #{token_id} already uploaded: {results[key]['cid']}")
            continue

        # Choix rareté et trait déterministes
        random.seed(token_id * 31)
        rarity = pick_rarity()
        trait  = TRAITS[token_id % len(TRAITS)]

        # Génération
        print(f"  [{i+1}/{total}] #{token_id} {rarity:10s} {trait:25s}", end=" ", flush=True)
        img_path = os.path.join(OUTPUT_DIR, f"badge_{token_id}.png")

        if not os.path.exists(img_path):
            img = generate_badge(token_id, rarity, trait)
            img.save(img_path, "PNG", optimize=True)
            print(f"✏️  generated", end=" ", flush=True)
        else:
            print(f"📦 cached", end=" ", flush=True)

        # Upload
        cid = upload_to_pinata(img_path, f"b2s-badge-{token_id}.png")
        if cid:
            results[key] = {"tokenId": token_id, "cid": cid, "rarity": rarity, "trait": trait}
            print(f"✅ {cid}")
        else:
            print(f"❌ upload failed, will retry next run")

        # Sauvegarde progressive (reprend où on s'arrête)
        with open(CID_FILE, "w") as f:
            json.dump(results, f, indent=2)

        time.sleep(UPLOAD_DELAY)

    # Résumé
    print(f"\n✅ Done! {len(results)} badges uploaded")
    print(f"📄 CIDs saved to {CID_FILE}")
    print(f"\n🔧 Now run: python generate_tsx.py")

if __name__ == "__main__":
    main()
