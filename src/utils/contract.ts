import { openContractCall } from '@stacks/connect'
import { uintCV, standardPrincipalCV, PostConditionMode, AnchorMode } from '@stacks/transactions'
import { StacksMainnet } from '@stacks/network'

const network  = new StacksMainnet()
const CONTRACT = 'SP1V72500C63KN9E348QDK9X879MASSTN0J3KBQ5N'

export async function callListBadge(badgeId: number, price: number) {
  return openContractCall({
    network,
    contractAddress:   CONTRACT,
    contractName:      'b2s-marketplace',
    functionName:      'list-badge',
    functionArgs:      [uintCV(badgeId), uintCV(Math.floor(price * 1_000_000))],
    postConditionMode: PostConditionMode.Allow,
    anchorMode:        AnchorMode.Any,
  })
}

export async function callBuyBadge(listingId: number) {
  return openContractCall({
    network,
    contractAddress:   CONTRACT,
    contractName:      'b2s-marketplace',
    functionName:      'buy-badge',
    functionArgs:      [uintCV(listingId)],
    postConditionMode: PostConditionMode.Allow,
    anchorMode:        AnchorMode.Any,
  })
}
