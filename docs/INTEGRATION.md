# Integration Guide

## Check if user has badge
(define-read-only (has-badge (user principal) (token-id uint))
  (is-eq (some user) (nft-get-owner? b2s-badge token-id))
)

## Mint badge (admin only)
(contract-call? 
  'SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96.b2s-badges
  mint-badge recipient badge-id)
