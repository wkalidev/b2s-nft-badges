# B2S NFT Achievement Badges

[![Mainnet](https://img.shields.io/badge/Network-Stacks%20Mainnet-green)](https://explorer.hiro.so/?chain=mainnet)
[![SIP-009](https://img.shields.io/badge/Standard-SIP--009-blue)](https://github.com/stacksgov/sips)
[![Clarity](https://img.shields.io/badge/Clarity-55%25-purple)](https://docs.stacks.co/clarity)
[![TypeScript](https://img.shields.io/badge/TypeScript-44%25-blue)](https://typescriptlang.org/)
[![IPFS](https://img.shields.io/badge/Storage-IPFS%20Pinata-orange)](https://pinata.cloud/)
[![Builder Rewards](https://img.shields.io/badge/Stacks-Builder%20Rewards%20March%202026-orange)](https://stacks.org)

NFT badges system rewarding Base2Stacks ecosystem milestones — SIP-009 standard on Stacks mainnet.

**[https://base2stacks-tracker.vercel.app](https://base2stacks-tracker.vercel.app)**

---

## 🏅 Overview

Earn unique NFT badges by reaching milestones in the Base2Stacks ecosystem. Each badge is a collectible that proves your achievements on-chain. **167/200 badges uploaded** to IPFS via Pinata.

**Deployer**: `SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96`

---

## 🎖️ Badge Types

### Staking Badges

| Badge | Requirement | Rarity |
|---|---|---|
| 🥉 Bronze Staker | Stake 100+ $B2S | Common |
| 🥈 Silver Staker | Stake 1,000+ $B2S | Uncommon |
| 🥇 Gold Staker | Stake 10,000+ $B2S | Rare |
| 💎 Diamond Staker | Stake 100,000+ $B2S | Epic |
| 👑 Legendary Staker | Stake 1M+ $B2S | Legendary |

### Activity Badges

| Badge | Requirement | Rarity |
|---|---|---|
| 🔥 Early Adopter | First 100 users | Legendary |
| ⚡ Active Trader | 100+ transactions | Rare |
| 🎯 Consistent Claimer | 30-day streak | Uncommon |
| 💪 Power User | 1,000+ transactions | Epic |
| 🌟 Community Leader | Top 10 leaderboard | Legendary |

### Special Badges (Infosec Legendaries)

| Badge | ID | Rarity |
|---|---|---|
| 🕵️ OSINT Master | #38 | Legendary |
| 🐛 Bug Bounty | #76 | Legendary |
| 🔓 Pen Tester | #114 | Legendary |

---

## 🚀 Quick Start

### Installation
```bash
npm install @wkalidev/b2s-nft-badges
```

### Check Your Badges
```tsx
import { BadgeChecker } from '@wkalidev/b2s-nft-badges'

function MyBadges() {
  const { badges, loading } = useBadges(userAddress)

  return (
    <div>
      {badges.map(badge => (
        <BadgeCard key={badge.id} badge={badge} />
      ))}
    </div>
  )
}
```

### Mint Badge
```tsx
import { mintBadge } from '@wkalidev/b2s-nft-badges'

await mintBadge({
  userAddress: 'SP1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM',
  badgeType: 'gold-staker',
  contractAddress: 'SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-airdrop-v2'
})
```

---

## 📦 Components

### `BadgeGallery`
```tsx
<BadgeGallery
  userAddress={string}
  showRarity={true}
  filterByType?: 'staking' | 'activity' | 'special'
/>
```

### `BadgeCard`
```tsx
<BadgeCard badge={Badge} showDetails={true} size="medium" />
```

### `BadgeProgress`
```tsx
<BadgeProgress currentAmount={5000} nextBadge="gold-staker" requirement={10000} />
```

### `BadgeNotification`
```tsx
// In base2stacks-tracker
import { BadgeNotification } from '@wkalidev/b2s-nft-badges'

<BadgeNotification
  userAddress={address}
  onNewBadge={(badge) => toast.success(`🎉 New badge: ${badge.name}`)}
/>
```

---

## 🔧 Smart Contract (Clarity)

```clarity
;; Deployer: SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96
;; Contract: b2s-airdrop-v2

(define-public (mint-badge (recipient principal) (badge-id uint))
  (begin
    (asserts! (is-eligible recipient badge-id) err-not-eligible)
    (nft-mint? b2s-badge badge-id recipient)
  )
)

(define-read-only (is-eligible (user principal) (badge-id uint))
  (let ((staked-amount (get-staked-amount user)))
    (>= staked-amount (get-badge-requirement badge-id))
  )
)
```

---

## 📊 Badge Metadata (IPFS)

```json
{
  "name": "Gold Staker Badge",
  "description": "Awarded for staking 10,000+ $B2S tokens",
  "image": "ipfs://QmXxxx/gold-staker.png",
  "attributes": [
    { "trait_type": "Type", "value": "Staking" },
    { "trait_type": "Rarity", "value": "Rare" },
    { "trait_type": "Network", "value": "Stacks Mainnet" }
  ]
}
```

**IPFS Gateway order**: `ipfs.io → dweb.link → gateway.pinata.cloud`

**Status**: 167/200 badges uploaded · Seeds 171-200 pending (Pinata monthly limit)

---

## 🏆 Leaderboard Scoring

| Rarity | Points |
|---|---|
| Common | +10 |
| Uncommon | +25 |
| Rare | +50 |
| Epic | +100 |
| Legendary | +250 |

---

## 🛠️ Development

```bash
npm install

# Deploy to mainnet
clarinet deploy --mainnet

# Run tests
clarinet test
```

---

## 📖 API Reference

```typescript
interface Badge {
  id: number
  name: string
  description: string
  image: string
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic' | 'Legendary'
  earnedDate: Date
  metadata: Record<string, unknown>
}

const { badges, loading, refetch } = useBadges(userAddress)
```

---

## 🔗 Related Repos

| Repo | Description |
|---|---|
| [base2stacks-tracker](https://github.com/wkalidev/base2stacks-tracker) | Main frontend — [live app](https://base2stacks-tracker.vercel.app) |
| [b2s-token-contract](https://github.com/wkalidev/b2s-token-contract) | All Clarity smart contracts |
| [b2s-staking-interface](https://github.com/wkalidev/b2s-staking-interface) | Staking UI |

---

## 📜 License

MIT — See [LICENSE](./LICENSE)

## 👨‍💻 Author

**wkalidev (zcodebase)** · [Twitter](https://twitter.com/willycodexwar) · [Farcaster](https://warpcast.com/willywarrior)

---

**Built for #StacksBuilderRewards March 2026 🏆 · Collect them all! 🎖️**\n## Series\n- Infosec #1-170\n- Glitch Art #201-500\n- Galactic #501-600 (ultra rare)
\n## Series\n- Infosec #1-170\n- Glitch Art #201-500\n- Galactic #501-600 (ultra rare)
