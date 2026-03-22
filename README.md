# B2S NFT Achievement Badges

SIP-009 NFT badge system for Base2Stacks ecosystem milestones on Stacks mainnet.

[![CI](https://github.com/wkalidev/b2s-nft-badges/actions/workflows/ci-clarity.yml/badge.svg)](https://github.com/wkalidev/b2s-nft-badges/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

**Network:** Stacks Mainnet
**Contract:** SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-airdrop-v2

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

## License

MIT — Built for #StacksBuilderRewards March 2026 🏆
