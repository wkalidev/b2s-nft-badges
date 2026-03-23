import { useState, useEffect } from 'react'
import { callReadOnlyFunction, cvToJSON, standardPrincipalCV, uintCV } from '@stacks/transactions'
import { StacksMainnet } from '@stacks/network'

const network  = new StacksMainnet()
const CONTRACT = 'SP936YWJPST8GB8FFRCN7CC6P2YR5K6NNBAARQ96'

export function useEligibility(address: string, badgeId: number, userAmount: number) {
  const [eligible, setEligible] = useState(false)
  const [loading, setLoading]   = useState(false)

  useEffect(() => {
    if (!address || !badgeId) return
    setLoading(true)
    callReadOnlyFunction({
      network,
      contractAddress: CONTRACT,
      contractName:    'b2s-badges',
      functionName:    'check-eligibility',
      functionArgs:    [
        standardPrincipalCV(address),
        uintCV(badgeId),
        uintCV(Math.floor(userAmount * 1_000_000)),
      ],
      senderAddress: address,
    })
      .then(r => setEligible(cvToJSON(r).value === true))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [address, badgeId, userAmount])

  return { eligible, loading }
}
