export function calcFloorPrice(listings: any[]): number {
  const prices = listings
    .filter(l => l.active)
    .map(l => l.price)
  return prices.length > 0 ? Math.min(...prices) : 0
}

export function calcTotalVolume(sales: any[]): number {
  return sales.reduce((sum, s) => sum + s.price, 0)
}

export function formatB2SPrice(price: number): string {
  if (price >= 1000) return `${(price / 1000).toFixed(1)}K B2S`
  return `${price} B2S`
}
