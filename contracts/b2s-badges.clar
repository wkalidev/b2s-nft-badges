;; B2S Achievement Badges NFT Contract
;; SIP-009 compliant NFT for ecosystem achievements

;; Define NFT
(define-non-fungible-token b2s-badge uint)

;; Constants
(define-constant contract-owner tx-sender)
(define-constant err-not-authorized (err u401))
(define-constant err-not-found (err u404))
(define-constant err-already-minted (err u409))
(define-constant err-not-eligible (err u403))

;; Data Variables
(define-data-var last-token-id uint u0)

;; Data Maps
(define-map badge-metadata uint {
  name: (string-ascii 50),
  badge-type: (string-ascii 20),
  rarity: (string-ascii 20),
  requirement: uint
})

(define-map user-badges principal (list 50 uint))

;; Badge Types
;; 1-10: Bronze Staker series
;; 11-20: Silver Staker series
;; 21-30: Gold Staker series
;; 31-40: Activity badges
;; 41-50: Special badges

;; Initialize badge metadata
(map-set badge-metadata u1 {
  name: "Bronze Staker",
  badge-type: "staking",
  rarity: "Common",
  requirement: u100000000 ;; 100 tokens (6 decimals)
})

(map-set badge-metadata u2 {
  name: "Silver Staker",
  badge-type: "staking",
  rarity: "Uncommon",
  requirement: u1000000000 ;; 1000 tokens
})

(map-set badge-metadata u3 {
  name: "Gold Staker",
  badge-type: "staking",
  rarity: "Rare",
  requirement: u10000000000 ;; 10,000 tokens
})

;; Public Functions

;; Mint badge
(define-public (mint-badge (recipient principal) (badge-id uint))
  (let ((token-id (+ (var-get last-token-id) u1)))
    (asserts! (is-eq tx-sender contract-owner) err-not-authorized)
    (asserts! (is-some (map-get? badge-metadata badge-id)) err-not-found)
    (try! (nft-mint? b2s-badge token-id recipient))
    (var-set last-token-id token-id)
    (ok token-id)
  )
)

;; Transfer badge
(define-public (transfer (token-id uint) (sender principal) (recipient principal))
  (begin
    (asserts! (is-eq tx-sender sender) err-not-authorized)
    (nft-transfer? b2s-badge token-id sender recipient)
  )
)

;; Check eligibility (to be called by authorized minter)
(define-read-only (check-eligibility (user principal) (badge-id uint) (user-amount uint))
  (match (map-get? badge-metadata badge-id)
    metadata (>= user-amount (get requirement metadata))
    false
  )
)

;; Get badge info
(define-read-only (get-badge-info (badge-id uint))
  (map-get? badge-metadata badge-id)
)

;; Get token URI
(define-read-only (get-token-uri (token-id uint))
  (ok (some "ipfs://QmXxxx/{id}.json"))
)

;; Get owner
(define-read-only (get-owner (token-id uint))
  (ok (nft-get-owner? b2s-badge token-id))
)

;; Get last token ID
(define-read-only (get-last-token-id)
  (ok (var-get last-token-id))
)