"""
generate_galactic_tsx.py - Genere les entrees TSX pour la serie Galactic #501-600
Lance apres generate_galactic.py

Usage: python generate_galactic_tsx.py
Output: output/galactic/new_badges_galactic.tsx
"""

import json, os

CID_FILE = "output/galactic/cids.json"
OUT_FILE = "output/galactic/new_badges_galactic.tsx"
GATEWAY  = "https://gateway.pinata.cloud/ipfs/"

def main():
    if not os.path.exists(CID_FILE):
        print("ERROR: " + CID_FILE + " not found - run generate_galactic.py first")
        return

    with open(CID_FILE) as f:
        data = json.load(f)

    lines = []
    for key in sorted(data.keys(), key=lambda x: int(x)):
        b = data[key]
        tid    = b["tokenId"]
        rarity = b["rarity"]
        trait  = b["trait"]
        cid    = b["cid"]
        url    = GATEWAY + cid

        line = (
            "  { tokenId:" + str(tid) + ", name:'B2S Badge #" + str(tid) + "',"
            " trait:'" + trait + "',"
            " rarity:'" + rarity + "' as const,"
            " imageUrl:'" + url + "' },"
        )
        lines.append(line)

    os.makedirs("output/galactic", exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("// SERIE GALACTIC #501-600 - ULTRA RARE\n")
        f.write("// Themes: Galactic / Base / Degen / Stack\n")
        f.write("// " + str(len(lines)) + " badges - Rare / Epic / Legendary\n\n")
        f.write("\n".join(lines))
        f.write("\n")

    print("OK " + str(len(lines)) + " entries written to " + OUT_FILE)

if __name__ == "__main__":
    main()