# Badge System
## Tiers
- Bronze, Silver, Gold, Diamond
# 🎖️ B2S Badge System

Complete reference for all NFT achievement badges in the Base2Stacks ecosystem.

**Standard**: SIP-009 · **Network**: Stacks Mainnet · **Total Supply**: 200  
**IPFS Status**: 167/200 uploaded · Seeds 171-200 pending  
**Contract**: `SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-airdrop-v2`

---

## 🏆 Rarity Tiers

| Tier | Color | Drop Rate | Leaderboard Points | Count |
|---|---|---|---|---|
| Common | ⬜ Gray | 50% | +10 | 100 |
| Uncommon | 🟩 Green | 30% | +25 | 60 |
| Rare | 🟦 Blue | 15% | +50 | 30 |
| Epic | 🟪 Purple | 4% | +100 | 7 |
| Legendary | 🟧 Gold | 1% | +250 | 3 |

---

## 🔒 Staking Badges

Earned by reaching $B2S staking thresholds in `b2s-staking-vault-v2`.

| ID | Badge | Requirement | Rarity |
|---|---|---|---|
| #001 | 🥉 Bronze Staker | Stake 100+ $B2S | Common |
| #002 | 🥈 Silver Staker | Stake 1,000+ $B2S | Uncommon |
| #003 | 🥇 Gold Staker | Stake 10,000+ $B2S | Rare |
| #004 | 💎 Diamond Staker | Stake 100,000+ $B2S | Epic |
| #005 | 👑 Legendary Staker | Stake 1,000,000+ $B2S | Legendary |

**Award type**: Automatic — triggered when staking threshold is met.

---

## ⚡ Activity Badges

Earned by transaction volume and on-chain activity.

| ID | Badge | Requirement | Rarity |
|---|---|---|---|
| #010 | 🔥 Early Adopter | First 100 users | Legendary |
| #011 | 🎯 First Stake | Complete first stake | Common |
| #012 | ⚡ Active Trader | 100+ transactions | Rare |
| #013 | 🎯 Consistent Claimer | 30-day streak | Uncommon |
| #014 | 💪 Power User | 1,000+ transactions | Epic |
| #015 | 🌟 Community Leader | Top 10 leaderboard | Legendary |
| #016 | 🔄 Bridge Pioneer | First bridge transaction | Common |
| #017 | 🌉 Bridge Master | 10+ bridge transactions | Rare |

**Award type**: Automatic — checked every 24h via indexer.

---

## 🛡️ Infosec Legendary Badges

Special cybersecurity-themed badges — manually awarded by team.

| ID | Badge | Description | Rarity |
|---|---|---|---|
| #038 | 🕵️ OSINT Master | Open-source intelligence achievement | Legendary |
| #076 | 🐛 Bug Bounty | Reported and verified critical bug | Legendary |
| #114 | 🔓 Pen Tester | Ethical hacking contribution | Legendary |

**Award type**: Manual — verified and signed by deployer `SP936Y...ARQ96`.

---

## 🤝 Community Badges

Earned by contributing to the ecosystem.

| ID | Badge | Requirement | Rarity |
|---|---|---|---|
| #020 | 🐛 Bug Hunter | Report a confirmed bug | Epic |
| #021 | 💡 Feature Contributor | Suggest an implemented feature | Rare |
| #022 | 📚 Documentation Master | Contribute to docs | Uncommon |
| #023 | 🎨 Design Wizard | Create official artwork | Epic |
| #024 | 🚀 Launch Hero | Participated at launch | Legendary |

**Award type**: Manual — submit via GitHub Issues.

---

## 🎖️ Trader Badges *(Q2 2026)*

| Badge | Requirement | Rarity |
|---|---|---|
| 🥉 Bronze Trader | 10 marketplace sales | Common |
| 🥈 Silver Trader | 50 marketplace sales | Uncommon |
| 🥇 Gold Trader | 100 marketplace sales | Rare |
| 💎 Diamond Trader | 500 marketplace sales | Epic |

---

## 🎨 Badge Artwork

All badge artwork:
- **Format**: 512×512px PNG
- **Style**: Neon punk / cyberpunk infosec
- **Storage**: IPFS via Pinata
- **Animated**: Special glow effects for Rare+ badges
- **Gateway order**: `ipfs.io → dweb.link → gateway.pinata.cloud`

```json
{
  "name": "Gold Staker Badge",
  "description": "Awarded for staking 10,000+ $B2S tokens on Stacks mainnet",
  "image": "ipfs://QmXxxx/gold-staker.png",
  "attributes": [
    { "trait_type": "Type", "value": "Staking" },
    { "trait_type": "Rarity", "value": "Rare" },
    { "trait_type": "Network", "value": "Stacks Mainnet" },
    { "trait_type": "Contract", "value": "b2s-airdrop-v2" }
  ]
}
```

---

## 🔧 Earning & Claiming

### Automatic Badges
Staking and activity badges mint automatically when conditions are met:
```clarity
(define-public (check-and-mint (user principal))
  (let ((staked (get-staked-amount user)))
    (if (>= staked u10000000000)  ;; 10,000 $B2S
      (nft-mint? b2s-badge GOLD-STAKER-ID user)
      (err u1)
    )
  )
)
```

### Manual Badges
For community and infosec badges — open an issue:
1. Go to [github.com/wkalidev/b2s-nft-badges/issues](https://github.com/wkalidev/b2s-nft-badges/issues)
2. Use template **"Badge Claim Request"**
3. Provide proof of achievement
4. Team verifies and mints within 48h

---

## 🔮 Future Badges (Q3 2026)

- 🎮 Gaming achievement badges
- 🤝 Referral reward badges
- 📈 Trading milestone badges
- 🌍 Community event badges (seasonal)
- sBTC bridge pioneer badge

---

## 🔗 Related

- [README.md](../README.md) — Project overview
- [MARKETPLACE.md](./MARKETPLACE.md) — Buy & sell badges
- [Live App](https://base2stacks-tracker.vercel.app) — View your badges
- [b2s-token-contract](https://github.com/wkalidev/b2s-token-contract) — Smart contracts

---

**Version**: 1.1.0 · **Updated**: March 2026 · **Network**: Stacks Mainnet