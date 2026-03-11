# 🛒 B2S NFT Marketplace

Complete guide to buying and selling achievement badge NFTs on Stacks mainnet.

**Deployer**: `SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96`  
**Status**: ✅ Live on Stacks Mainnet  
**Platform Fee**: 2.5%

---

## 📋 Overview

The B2S Marketplace allows users to buy and sell achievement badges as SIP-009 NFTs. All transactions happen on-chain with transparent pricing — no custodians, no intermediaries.

---

## 🎯 Features

### For Buyers
- 🔍 Browse all available badges
- 💎 Filter by rarity (Common → Legendary)
- 📊 See price history and trends
- ✅ Instant purchase with $B2S tokens
- 🔐 Secure on-chain atomic transactions

### For Sellers
- 💰 List badges at any price (min 1 $B2S)
- 📝 Edit listing price anytime
- ❌ Cancel listings for free
- 💵 Receive 97.5% of sale price
- 📈 Track your sales stats

---

## 🛍️ How to Buy

### Step 1 — Browse
Navigate to the **Marketplace** tab at [base2stacks-tracker.vercel.app](https://base2stacks-tracker.vercel.app).

### Step 2 — Select Badge
Click any badge to view rarity, price, seller address, and listing date.

### Step 3 — Purchase
1. Click **Buy Now**
2. Review transaction details
3. Confirm in Hiro/Leather wallet
4. Badge transfers to your wallet instantly

**Transaction fees:**
- Platform fee: 2.5%
- Gas fee: ~0.001 STX

```
Example:
Badge: Gold Staker (Rare)
Price: 50 $B2S
Platform Fee: 1.25 $B2S (2.5%)
Seller Receives: 48.75 $B2S
```

---

## 💰 How to Sell

1. Go to **My Items** tab
2. Click **Sell Item** on any badge
3. Enter price (min 1 $B2S)
4. Confirm transaction
5. Badge is listed — edit or cancel anytime

```
Example:
Badge: Silver Staker (Uncommon)
Your Price: 25 $B2S
Platform Fee: 0.625 $B2S (2.5%)
You Receive: 24.375 $B2S
```

---

## 💎 Badge Rarities & Floor Prices

| Rarity | Color | Drop Rate | Floor Price |
|---|---|---|---|
| Common | Gray | 50% | ~5 $B2S |
| Uncommon | Green | 30% | ~15 $B2S |
| Rare | Blue | 15% | ~30 $B2S |
| Epic | Purple | 4% | ~75 $B2S |
| Legendary | Gold/Red | 1% | ~200 $B2S |

---

## 🔧 Smart Contract Functions

```clarity
;; Contract: SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-airdrop-v2

;; List badge for sale
(list-badge (badge-id uint) (price uint))
;; Requirements: own the badge, price ≥ 1_000_000 (1 $B2S)

;; Cancel listing
(cancel-listing (listing-id uint))
;; Requirements: must be the seller

;; Buy badge
(buy-badge (listing-id uint))
;; Requirements: sufficient $B2S, cannot buy own listing
;; Effects: atomic transfer — badge + payment in same tx

;; Update price
(update-price (listing-id uint) (new-price uint))

;; Read-only
(get-listing (listing-id uint))
(get-user-stats (user principal))
(calculate-platform-fee (price uint))   ;; → 2.5%
(calculate-seller-amount (price uint))  ;; → price - fee
```

---

## 🔐 Security

- ✅ Ownership verified before listing
- ✅ No double-spending — atomic transactions
- ✅ Platform fee enforced on-chain
- ✅ Cannot buy your own listings
- ✅ Cancel anytime — no lock-up
- ✅ No admin withdrawal of user funds

---

## 🔮 Roadmap

### Phase 2 (Q2 2026)
- [ ] Auction system
- [ ] Offer / counter-offer system
- [ ] Bundle sales (multiple badges)
- [ ] Advanced filters + search

### Phase 3 (Q3 2026)
- [ ] Badge rental system
- [ ] Royalties for original earners
- [ ] Collection showcases
- [ ] Trader achievement badges

---

## 🤝 Support

- 🐛 [Report Issue](https://github.com/wkalidev/b2s-nft-badges/issues)
- 💬 [Farcaster](https://warpcast.com/willywarrior)
- 🐦 [Twitter](https://twitter.com/willycodexwar)

---

**Version**: 1.1.0 · **Updated**: March 2026 · **Network**: Stacks Mainnet