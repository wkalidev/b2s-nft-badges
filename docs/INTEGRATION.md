# Integration Guide

## Check if user has badge
(define-read-only (has-badge (user principal) (token-id uint))
  (is-eq (some user) (nft-get-owner? b2s-badge token-id))
)

## Mint badge (admin only)
(contract-call? 
  'SP1V72500C63KN9E348QDK9X879MASSTN0J3KBQ5N.b2s-badges
  mint-badge recipient badge-id)
