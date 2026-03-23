export type FilterType = 'all' | 'staking' | 'activity' | 'special'
export type SortType   = 'rarity' | 'id' | 'name'

export function filterBadges(badges: any[], filter: FilterType) {
  if (filter === 'all') return badges
  return badges.filter(b => b.type === filter)
}

export function sortBadges(badges: any[], sort: SortType) {
  const order = { Common: 0, Uncommon: 1, Rare: 2, Epic: 3, Legendary: 4 }
  return [...badges].sort((a, b) => {
    if (sort === 'rarity') return (order[b.rarity] || 0) - (order[a.rarity] || 0)
    if (sort === 'id')     return a.id - b.id
    if (sort === 'name')   return a.name.localeCompare(b.name)
    return 0
  })
}
