# B2S NFT Achievement Badges

NFT badges system for rewarding Base2Stacks ecosystem milestones.

[![NFT](https://img.shields.io/badge/NFT-Badges-purple)](https://stacks.co/)
[![SIP-009](https://img.shields.io/badge/Standard-SIP--009-blue)](https://github.com/stacksgov/sips)

## 🏅 Overview

Earn unique NFT badges by reaching milestones in the Base2Stacks ecosystem. Each badge is a collectible that proves your achievements on-chain.

## 🎖️ Badge Types

### Staking Badges

| Badge | Requirement | Rarity |
|-------|-------------|--------|
| 🥉 Bronze Staker | Stake 100+ $B2S | Common |
| 🥈 Silver Staker | Stake 1,000+ $B2S | Uncommon |
| 🥇 Gold Staker | Stake 10,000+ $B2S | Rare |
| 💎 Diamond Staker | Stake 100,000+ $B2S | Epic |
| 👑 Legendary Staker | Stake 1M+ $B2S | Legendary |

### Activity Badges

| Badge | Requirement | Rarity |
|-------|-------------|--------|
| 🔥 Early Adopter | First 100 users | Legendary |
| ⚡ Active Trader | 100+ transactions | Rare |
| 🎯 Consistent Claimer | 30-day streak | Uncommon |
| 💪 Power User | 1,000+ transactions | Epic |
| 🌟 Community Leader | Top 10 leaderboard | Legendary |

### Special Badges

| Badge | Requirement | Rarity |
|-------|-------------|--------|
| 🚀 Launch Hero | Participated in launch | Legendary |
| 🐛 Bug Hunter | Reported critical bug | Epic |
| 💡 Feature Contributor | Suggested implemented feature | Rare |
| 📚 Documentation Master | Contributed to docs | Uncommon |
| 🎨 Design Wizard | Created official artwork | Epic |

## 🎨 Badge Design

All badges follow SIP-009 NFT standard with:
- **Unique artwork** - Custom designed for each badge
- **Metadata** - On-chain verification
- **Transferable** - Trade on marketplaces
- **Display** - Show off in wallet/profile

## 🚀 Quick Start

### Check Your Badges
```tsx
import { BadgeChecker } from '@b2s/nft-badges';

function MyBadges() {
  const { badges, loading } = useBadges(userAddress);
  
  return (
    <div>
      {badges.map(badge => (
        <BadgeCard key={badge.id} badge={badge} />
      ))}
    </div>
  );
}
```

### Mint Badge
```typescript
import { mintBadge } from '@b2s/nft-badges';

await mintBadge({
  userAddress: 'ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM',
  badgeType: 'gold-staker',
  contractAddress: 'ST936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-badges'
});
```

## 📦 Components

### BadgeGallery

Display all user badges.
```tsx
<BadgeGallery
  userAddress={string}
  showRarity={true}
  filterByType?: 'staking' | 'activity' | 'special'
/>
```

### BadgeCard

Individual badge display.
```tsx
<BadgeCard
  badge={Badge}
  showDetails={true}
  size="medium"
/>
```

### BadgeProgress

Show progress towards next badge.
```tsx
<BadgeProgress
  currentAmount={5000}
  nextBadge="gold-staker"
  requirement={10000}
/>
```

## 🔧 Smart Contract

### Mint Function
```clarity
(define-public (mint-badge (recipient principal) (badge-id uint))
  (begin
    (asserts! (is-eligible recipient badge-id) err-not-eligible)
    (nft-mint? b2s-badge badge-id recipient)
  )
)
```

### Check Eligibility
```clarity
(define-read-only (is-eligible (user principal) (badge-id uint))
  (let ((staked-amount (get-staked-amount user)))
    (>= staked-amount (get-badge-requirement badge-id))
  )
)
```

## 📊 Badge Metadata
```json
{
  "name": "Gold Staker Badge",
  "description": "Awarded for staking 10,000+ $B2S tokens",
  "image": "ipfs://QmXxxx/gold-staker.png",
  "attributes": [
    {
      "trait_type": "Type",
      "value": "Staking"
    },
    {
      "trait_type": "Rarity",
      "value": "Rare"
    },
    {
      "trait_type": "Earned Date",
      "value": "2026-02-08"
    }
  ]
}
```

## 🎯 Earning Criteria

### Automatic Awards

Badges are **automatically minted** when you:
- ✅ Reach staking threshold
- ✅ Complete transaction milestone
- ✅ Achieve streak goal

### Manual Claims

Some badges require **manual claiming**:
- 🐛 Bug reports (verified by team)
- 💡 Feature suggestions (implemented)
- 🎨 Community contributions

## 🔗 Integration

### With Tracker App

Badges are automatically checked in the main tracker:
```tsx
// In base2stacks-tracker
import { BadgeNotification } from '@b2s/nft-badges';

<BadgeNotification
  userAddress={address}
  onNewBadge={(badge) => {
    toast.success(`🎉 New badge earned: ${badge.name}`);
  }}
/>
```

## 🛠️ Development
```bash
# Install
npm install

# Deploy contract
clarinet deploy --testnet

# Run tests
clarinet test
```

## 📖 API Reference

### useBadges Hook
```typescript
const { 
  badges,        // Badge[]
  loading,       // boolean
  refetch        // () => void
} = useBadges(userAddress);
```

### Badge Type
```typescript
interface Badge {
  id: number;
  name: string;
  description: string;
  image: string;
  rarity: 'Common' | 'Uncommon' | 'Rare' | 'Epic' | 'Legendary';
  earnedDate: Date;
  metadata: Record<string, any>;
}
```

## 🎨 Badge Artwork

All badge artwork is:
- 🎨 **Custom designed** - Unique cyberpunk aesthetic
- 📐 **512x512px** - Optimized for display
- 🌈 **Animated** - Special effects for rare badges
- 💾 **IPFS hosted** - Decentralized storage

## 🏆 Leaderboard Integration

Badges contribute to your leaderboard score:
- Common: +10 points
- Uncommon: +25 points
- Rare: +50 points
- Epic: +100 points
- Legendary: +250 points

## 🔮 Future Badges

Coming soon:
- 🎮 Gaming achievements
- 🤝 Referral rewards
- 📈 Trading milestones
- 🌍 Community events
- 🎭 Seasonal badges

## 🔗 Links

- [Main Tracker](https://wkalidev-base2stacks-tracker.vercel.app)
- [Smart Contract](https://github.com/wkalidev/b2s-token-contract)
- [NFT Marketplace](https://gamma.io) (coming soon)

## 🤝 Contributing

See [CONTRIBUTING.md](../base2stacks-tracker/CONTRIBUTING.md)

## 📜 License

MIT License

---

**Built for #StacksBuilderRewards 🏆**

**Collect them all! 🎖️**