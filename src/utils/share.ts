const APP_URL = 'https://base2stacks-tracker.vercel.app'

export function getBadgeShareText(badgeName: string): string {
  return `🏅 Just earned the "${badgeName}" NFT badge on Base2Stacks!\n🎖️ Collect achievements on Stacks mainnet.\n👉 ${APP_URL}\n#B2S #NFT #Stacks`
}

export function getTwitterUrl(text: string): string {
  return `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`
}

export function getFarcasterUrl(text: string): string {
  return `https://warpcast.com/~/compose?text=${encodeURIComponent(text)}`
}
