export const getPlayerByUUIDClaim = (players, uuid) => {
  return players.find(player => player.claims?.items[0]?.uuid === uuid)
}

export const getClaim = (player) => {
  return player.claims.items[0] || null
}