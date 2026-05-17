# B2S NFT Achievement Badges

SIP-009 NFT badge system for Base2Stacks ecosystem milestones on Stacks mainnet.

[![CI](https://github.com/wkalidev/b2s-nft-badges/actions/workflows/ci-clarity.yml/badge.svg)](https://github.com/wkalidev/b2s-nft-badges/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**Network:** Stacks Mainnet  
**Contract:** `SP1V72500C63KN9E348QDK9X879MASSTN0J3KBQ5N.b2s-airdrop`

## Installation

```bash
npm install @wkalidev/b2s-badges
```

## Badge Types

| Badge | Requirement | Rarity |
|-------|-------------|--------|
| Bronze Staker | 100+ B2S staked | Common |
| Silver Staker | 1,000+ B2S staked | Uncommon |
| Gold Staker | 10,000+ B2S staked | Rare |
| Diamond Staker | 100,000+ B2S staked | Epic |
| Legendary Staker | 1M+ B2S staked | Legendary |

## 567 Unique Badges — 3 Series

| Series | IDs | Theme |
|--------|-----|-------|
| 🔐 Infosec Original | #1–#170 | Cybersecurity, 3 Legendaries |
| 🎨 Glitch Art | #201–#500 | 300 generative glitch badges |
| 🌌 Ultra Rare Galactic | #501–#600 | Galactic / Base / Degen / Stack |

## Usage

```typescript
import { useBadges, BadgeGallery } from '@wkalidev/b2s-badges'

function MyBadges({ address }: { address: string }) {
  const { badges, loading } = useBadges(address)
  return <BadgeGallery badges={badges} showRarity />
}
```

## Development

```bash
clarinet check && clarinet test
npm install && npm run build
```

## Related

- [base2stacks-tracker](https://base2stacks-tracker.vercel.app) — live DeFi platform
- [@wkalidev/b2s-contracts](https://www.npmjs.com/package/@wkalidev/b2s-contracts) — contract SDK

## License

MIT — Built for #StacksBuilderRewards May 2026 🏆