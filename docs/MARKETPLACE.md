# 🛒 B2S NFT Marketplace

Complete guide to buying and selling achievement badge NFTs.

## 📋 Overview

The B2S Marketplace allows users to buy and sell achievement badges as NFTs. All transactions happen on-chain with transparent pricing and a 2.5% platform fee.

## 🎯 Features

### For Buyers
- 🔍 Browse all available badges
- 💎 Filter by rarity (Common → Legendary)
- 📊 See price history and trends
- ✅ Instant purchase with $B2S tokens
- 🔐 Secure on-chain transactions

### For Sellers
- 💰 List badges at any price (min 1 $B2S)
- 📝 Edit listing price anytime
- ❌ Cancel listings for free
- 💵 Receive 97.5% of sale price
- 📈 Track your sales stats

## 🛍️ How to Buy

### Step 1: Browse Marketplace

Navigate to the **Marketplace** tab to see all available listings.

### Step 2: Select Badge

Click on any badge to view:
- Badge name and description
- Rarity level
- Current price
- Seller address
- Time listed

### Step 3: Purchase

1. Click **Buy Now**
2. Review transaction details
3. Confirm in wallet
4. Badge transfers to your wallet

**Transaction fees:**
- Platform fee: 2.5%
- Gas fee: ~0.001 STX

### Example Purchase
```
Badge: Gold Staker (Epic)
Price: 50 $B2S
Platform Fee: 1.25 $B2S (2.5%)
You Pay: 50 $B2S
Seller Receives: 48.75 $B2S
```

## 💰 How to Sell

### Step 1: View Your Items

Go to **My Items** tab to see all badges you own.

### Step 2: List for Sale

1. Click **Sell Item** on badge
2. Enter your desired price
3. Review platform fee (2.5%)
4. Click **List Item**
5. Confirm transaction

**Minimum price:** 1 $B2S  
**No maximum price!**

### Step 3: Manage Listing

- **Edit Price**: Change price anytime
- **Cancel Listing**: Remove from marketplace
- **View Stats**: Track views and interest

### Example Listing
```
Badge: Silver Staker (Rare)
Your Price: 25 $B2S
Platform Fee: 0.625 $B2S (2.5%)
You Receive: 24.375 $B2S (if sold)
```

## 💎 Badge Rarities

### Common
- Color: Gray
- Drop Rate: 50%
- Floor Price: ~5 $B2S

### Uncommon
- Color: Green
- Drop Rate: 30%
- Floor Price: ~15 $B2S

### Rare
- Color: Blue
- Drop Rate: 15%
- Floor Price: ~30 $B2S

### Epic
- Color: Purple
- Drop Rate: 4%
- Floor Price: ~75 $B2S

### Legendary
- Color: Orange/Red
- Drop Rate: 1%
- Floor Price: ~200 $B2S

## 📊 Marketplace Stats

### Total Volume
Sum of all completed sales in $B2S tokens.

### Floor Price
Lowest listing price currently available.

### Total Sales
Number of successful transactions.

### Active Listings
Current badges available for purchase.

## 🔧 Smart Contract Functions

### Public Functions

#### list-badge
```clarity
(list-badge (badge-id uint) (price uint))
```

List your badge for sale.

**Requirements:**
- You must own the badge
- Price ≥ 1,000,000 (1 $B2S)

**Returns:** Listing ID

#### cancel-listing
```clarity
(cancel-listing (listing-id uint))
```

Remove your listing from marketplace.

**Requirements:**
- You must be the seller
- Listing must be active

#### buy-badge
```clarity
(buy-badge (listing-id uint))
```

Purchase a listed badge.

**Requirements:**
- Sufficient $B2S balance
- Cannot buy your own listing

**Effects:**
- Badge ownership transfers to buyer
- Payment transfers to seller (minus fee)
- Listing becomes inactive

#### update-price
```clarity
(update-price (listing-id uint) (new-price uint))
```

Change listing price.

**Requirements:**
- You must be the seller
- New price ≥ 1 $B2S

### Read-Only Functions

#### get-listing
```clarity
(get-listing (listing-id uint))
```

Get listing details.

#### get-user-stats
```clarity
(get-user-stats (user principal))
```

Get user's marketplace statistics:
- Items sold
- Items bought
- Total earned
- Total spent

#### calculate-platform-fee
```clarity
(calculate-platform-fee (price uint))
```

Calculate 2.5% platform fee for a price.

#### calculate-seller-amount
```clarity
(calculate-seller-amount (price uint))
```

Calculate amount seller receives (price - fee).

## 💡 Trading Tips

### For Buyers

1. **Check Rarity**: Higher rarity = more valuable
2. **Compare Prices**: Don't overpay
3. **Watch Floor Price**: Good indicator of value
4. **Buy Dips**: Prices fluctuate
5. **Hold Legendary**: Rare badges appreciate

### For Sellers

1. **Price Competitively**: Check other listings
2. **Don't Underprice**: Know your badge value
3. **Update Prices**: Adjust based on market
4. **Bundle Deals**: Offer discounts (coming soon)
5. **Promote**: Share listings on social media

## 🔐 Security

### Smart Contract
- ✅ Ownership verification before listing
- ✅ No double-spending possible
- ✅ Atomic transactions (all-or-nothing)
- ✅ Platform fee enforced on-chain
- ✅ No admin withdrawal of user funds

### User Protection
- ✅ Cancel listings anytime
- ✅ Can't buy your own listings
- ✅ Price changes only by seller
- ✅ Transparent transaction history

## 📈 Price History

Track badge values over time:
- Daily average prices
- Volume trends
- Rarity-based pricing
- Historical sales data

## 🎮 Gamification

### Trader Badges (Coming Soon)
- 🥉 Bronze Trader: 10 sales
- 🥈 Silver Trader: 50 sales
- 🥇 Gold Trader: 100 sales
- 💎 Diamond Trader: 500 sales

### Rewards
- Trading volume rewards
- Liquidity provider bonuses
- Market maker incentives

## 🔮 Future Features

### Phase 2
- [ ] Auction system (highest bidder wins)
- [ ] Offers (make offer below asking price)
- [ ] Bundles (sell multiple badges together)
- [ ] Filters (sort by price, rarity, time)
- [ ] Search functionality

### Phase 3
- [ ] Badge rental system
- [ ] Fractional ownership
- [ ] Royalties for original earners
- [ ] Collection showcases
- [ ] Social features (comments, likes)

## 📱 Mobile App (Coming Soon)

Buy and sell badges on the go!

## 🤝 Support

Need help?
- 📚 [Badge Documentation](README.md)
- 🐛 [Report Issue](https://github.com/wkalidev/b2s-nft-badges/issues)
- 💬 [Community Chat](https://warpcast.com/willywarrior)
- 🐦 [Twitter](https://twitter.com/willycodexwar)

## 📜 License

MIT License

---

**Version**: 1.0.0  
**Last Updated**: February 8, 2026  
**Status**: ✅ Live on Testnet  
**Platform Fee**: 2.5%