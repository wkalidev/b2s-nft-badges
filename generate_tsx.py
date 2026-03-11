"""
generate_tsx.py — Génère les lignes IPFS_BADGES à ajouter dans NFTMarketplace.tsx
Lance après generate_and_upload.py

Usage: python generate_tsx.py
Output: output/new_badges.tsx  ← copie ces lignes dans IPFS_BADGES
"""

import json, os

CID_FILE   = "output/cids.json"
OUT_FILE   = "output/new_badges.tsx"
GATEWAY    = "https://gateway.pinata.cloud/ipfs/"

def main():
    if not os.path.exists(CID_FILE):
        print(f"❌ {CID_FILE} not found — run generate_and_upload.py first")
        return

    with open(CID_FILE) as f:
        data = json.load(f)

    lines = []
    for key in sorted(data.keys(), key=lambda x: int(x)):
        b = data[key]
        tid     = b["tokenId"]
        rarity  = b["rarity"]
        trait   = b["trait"]
        cid     = b["cid"]
        url     = f"{GATEWAY}{cid}"

        # Padding pour alignement
        name_str    = f"'B2S Badge #{tid}'"
        trait_str   = f"'{trait}'"
        rarity_str  = f"'{rarity}'"

        line = (
            f"  {{ tokenId:{tid:<4} name:{name_str:<18} "
            f"trait:{trait_str:<28} "
            f"rarity:{rarity_str:<13} as const, "
            f"imageUrl:'{url}' }},"
        )
        lines.append(line)

    os.makedirs("output", exist_ok=True)
    with open(OUT_FILE, "w") as f:
        f.write("// ─── SÉRIE #201-500 — GLITCH ART ───────────────────────────\n")
        f.write(f"// {len(lines)} badges générés\n\n")
        f.write("\n".join(lines))
        f.write("\n")

    print(f"✅ {len(lines)} entries written to {OUT_FILE}")
    print(f"\n📋 Copy the content of {OUT_FILE} into IPFS_BADGES[] in NFTMarketplace.tsx")
    print(f"   (add after the last badge entry, before the closing ']')")

if __name__ == "__main__":
    main()
