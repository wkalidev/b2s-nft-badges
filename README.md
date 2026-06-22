# B2S NFT Achievement Badges

SIP-009 NFT badge system for Base2Stacks ecosystem milestones on Stacks mainnet.

[![CI](https://github.com/wkalidev/b2s-nft-badges/actions/workflows/ci-clarity.yml/badge.svg)](https://github.com/wkalidev/b2s-nft-badges/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**Network:** Stacks Mainnet  
**Contract:** `SP1V72500C63KN9E348QDK9X879MASSTN0J3KBQ5N.b2s-marketplace`

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

## Smart Contracts (Mainnet)

**Deployer:** `SP1V72500C63KN9E348QDK9X879MASSTN0J3KBQ5N`

| Contract | Description |
|----------|-------------|
| `b2s-marketplace` | NFT badge marketplace, 2.5% fee, list/buy/delist |
| `b2s-token-v4` | $B2S payment token used in marketplace |

## Related Repos

| Repo | Description |
|------|-------------|
| [base2stacks-tracker](https://github.com/wkalidev/base2stacks-tracker) | Main DeFi platform — [live app](https://base2stacks-tracker.vercel.app) |
| [b2s-token-contract](https://github.com/wkalidev/b2s-token-contract) | SDK & Clarity contracts — [@wkalidev/b2s-contracts](https://www.npmjs.com/package/@wkalidev/b2s-contracts) |
| [b2s-analytics-dashboard](https://github.com/wkalidev/b2s-analytics-dashboard) | Analytics dashboard components |
| [b2s-staking-interface](https://github.com/wkalidev/b2s-staking-interface) | Staking UI components |
| [stacks-clarity-toolkit](https://github.com/wkalidev/stacks-clarity-toolkit) | Clarity dev toolkit — [@wkalidev/stacks-clarity-toolkit](https://www.npmjs.com/package/@wkalidev/stacks-clarity-toolkit) |

## License

MIT — Built for #StacksBuilderRewards May 2026