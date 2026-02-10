;; B2S NFT Marketplace
;; Buy and sell achievement badges

(define-constant contract-owner tx-sender)

;; Error codes
(define-constant err-not-authorized (err u401))
(define-constant err-not-found (err u404))
(define-constant err-already-listed (err u405))
(define-constant err-not-listed (err u406))
(define-constant err-insufficient-funds (err u407))
(define-constant err-invalid-price (err u408))
(define-constant err-not-owner (err u409))

;; Constants
(define-constant platform-fee-percentage u250) ;; 2.5% (250/10000)
(define-constant min-price u1000000) ;; 1 token minimum

;; Data vars
(define-data-var total-listings uint u0)
(define-data-var total-sales uint u0)
(define-data-var total-volume uint u0)

;; Listing structure
(define-map listings uint {
  seller: principal,
  badge-id: uint,
  price: uint,
  listed-at: uint,
  active: bool
})

;; Badge ownership (simplified - would integrate with NFT contract)
(define-map badge-owners {badge-id: uint} principal)

;; Sales history
(define-map sales uint {
  listing-id: uint,
  seller: principal,
  buyer: principal,
  badge-id: uint,
  price: uint,
  sold-at: uint
})

;; User stats
(define-map user-stats principal {
  items-sold: uint,
  items-bought: uint,
  total-earned: uint,
  total-spent: uint
})

;; Public Functions

;; List badge for sale
(define-public (list-badge (badge-id uint) (price uint))
  (let (
    (seller tx-sender)
    (listing-id (+ (var-get total-listings) u1))
    (current-owner (unwrap! (map-get? badge-owners {badge-id: badge-id}) err-not-found))
  )
    ;; Validations
    (asserts! (is-eq seller current-owner) err-not-owner)
    (asserts! (>= price min-price) err-invalid-price)
    
    ;; Create listing
    (map-set listings listing-id {
      seller: seller,
      badge-id: badge-id,
      price: price,
      listed-at: block-height,
      active: true
    })
    
    (var-set total-listings listing-id)
    (ok listing-id)
  )
)

;; Cancel listing
(define-public (cancel-listing (listing-id uint))
  (let (
    (listing (unwrap! (map-get? listings listing-id) err-not-found))
  )
    (asserts! (is-eq tx-sender (get seller listing)) err-not-authorized)
    (asserts! (get active listing) err-not-listed)
    
    ;; Deactivate listing
    (map-set listings listing-id (merge listing {active: false}))
    (ok true)
  )
)

;; Buy badge
(define-public (buy-badge (listing-id uint))
  (let (
    (buyer tx-sender)
    (listing (unwrap! (map-get? listings listing-id) err-not-found))
    (price (get price listing))
    (seller (get seller listing))
    (badge-id (get badge-id listing))
    (platform-fee (/ (* price platform-fee-percentage) u10000))
    (seller-amount (- price platform-fee))
    (sale-id (+ (var-get total-sales) u1))
  )
    ;; Validations
    (asserts! (get active listing) err-not-listed)
    (asserts! (not (is-eq buyer seller)) err-not-authorized)
    
    ;; Transfer badge ownership
    (map-set badge-owners {badge-id: badge-id} buyer)
    
    ;; Deactivate listing
    (map-set listings listing-id (merge listing {active: false}))
    
    ;; Record sale
    (map-set sales sale-id {
      listing-id: listing-id,
      seller: seller,
      buyer: buyer,
      badge-id: badge-id,
      price: price,
      sold-at: block-height
    })
    
    ;; Update stats
    (var-set total-sales sale-id)
    (var-set total-volume (+ (var-get total-volume) price))
    
    ;; Update user stats
    (update-seller-stats seller price)
    (update-buyer-stats buyer price)
    
    (ok sale-id)
  )
)

;; Update price
(define-public (update-price (listing-id uint) (new-price uint))
  (let (
    (listing (unwrap! (map-get? listings listing-id) err-not-found))
  )
    (asserts! (is-eq tx-sender (get seller listing)) err-not-authorized)
    (asserts! (get active listing) err-not-listed)
    (asserts! (>= new-price min-price) err-invalid-price)
    
    (map-set listings listing-id (merge listing {price: new-price}))
    (ok true)
  )
)

;; Private Functions

(define-private (update-seller-stats (seller principal) (amount uint))
  (let (
    (current-stats (default-to 
      {items-sold: u0, items-bought: u0, total-earned: u0, total-spent: u0}
      (map-get? user-stats seller)))
  )
    (map-set user-stats seller {
      items-sold: (+ (get items-sold current-stats) u1),
      items-bought: (get items-bought current-stats),
      total-earned: (+ (get total-earned current-stats) amount),
      total-spent: (get total-spent current-stats)
    })
  )
)

(define-private (update-buyer-stats (buyer principal) (amount uint))
  (let (
    (current-stats (default-to 
      {items-sold: u0, items-bought: u0, total-earned: u0, total-spent: u0}
      (map-get? user-stats buyer)))
  )
    (map-set user-stats buyer {
      items-sold: (get items-sold current-stats),
      items-bought: (+ (get items-bought current-stats) u1),
      total-earned: (get total-earned current-stats),
      total-spent: (+ (get total-spent current-stats) amount)
    })
  )
)

;; Read-only Functions

;; Get listing details
(define-read-only (get-listing (listing-id uint))
  (ok (map-get? listings listing-id))
)

;; Get active listings count
(define-read-only (get-total-listings)
  (ok (var-get total-listings))
)

;; Get total sales
(define-read-only (get-total-sales)
  (ok (var-get total-sales))
)

;; Get total volume
(define-read-only (get-total-volume)
  (ok (var-get total-volume))
)

;; Get sale details
(define-read-only (get-sale (sale-id uint))
  (ok (map-get? sales sale-id))
)

;; Get user stats
(define-read-only (get-user-stats (user principal))
  (ok (map-get? user-stats user))
)

;; Get badge owner
(define-read-only (get-badge-owner (badge-id uint))
  (ok (map-get? badge-owners {badge-id: badge-id}))
)

;; Check if badge is listed
(define-read-only (is-badge-listed (badge-id uint))
  (ok false) ;; Would check all active listings
)

;; Get platform fee for price
(define-read-only (calculate-platform-fee (price uint))
  (ok (/ (* price platform-fee-percentage) u10000))
)

;; Get seller amount after fee
(define-read-only (calculate-seller-amount (price uint))
  (let (
    (fee (/ (* price platform-fee-percentage) u10000))
  )
    (ok (- price fee))
  )
)

;; Admin function to set badge owner (for testing)
(define-public (admin-set-badge-owner (badge-id uint) (owner principal))
  (begin
    (asserts! (is-eq tx-sender contract-owner) err-not-authorized)
    (map-set badge-owners {badge-id: badge-id} owner)
    (ok true)
  )
)