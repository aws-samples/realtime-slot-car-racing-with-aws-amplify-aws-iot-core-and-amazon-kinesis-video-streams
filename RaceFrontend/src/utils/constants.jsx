export const CARS = [
  { color: "green", value: 1, claimable: true },
  { color: "red", value: 2, claimable: true },
  { color: "orange", value: 3, claimable: true },
  { color: "white", value: 4, claimable: true },
  { color: "yellow", value: 5, claimable: true },
  { color: "blue", value: 6, claimable: true },
]

export const RACE_STATES = {
  LOBBY: "lobby",
  PRACTICE: 'practice',
  PENDING: "pending",
  RED_FLAG: "red_flag",
  YELLOW_FLAG: "yellow_flag",
  GREEN_FLAG: "green_flag",
  CHECKERED_FLAG: "checkered_flag",
  ABORTED: "aborted",
  FORMATION_LAPS: "formation_laps"
}

export const CONTROLLER_VISIBLE_STATES = [
  RACE_STATES.PRACTICE,
  RACE_STATES.PENDING,
  RACE_STATES.RED_FLAG,
  RACE_STATES.YELLOW_FLAG,
  RACE_STATES.GREEN_FLAG,
  RACE_STATES.CHECKERED_FLAG,
  RACE_STATES.FORMATION_LAPS
]

export const DRIVING_RACE_STATES = [
  RACE_STATES.PRACTICE,
  RACE_STATES.YELLOW_FLAG,
  RACE_STATES.GREEN_FLAG,
]

export const RACER_ICON = "🏎️"

export const RACE_STATE_ICONS = {
  [RACE_STATES.LOBBY]: "🏨",
  [RACE_STATES.PRACTICE]: "🏎️",
  [RACE_STATES.PENDING]: "⏰",
  [RACE_STATES.RED_FLAG]: "🔴",
  [RACE_STATES.YELLOW_FLAG]: "🟡",
  [RACE_STATES.GREEN_FLAG]: "🟢",
  [RACE_STATES.CHECKERED_FLAG]: "🏁",
  [RACE_STATES.ABORTED]: "❌",
  [RACE_STATES.FORMATION_LAPS]: "🏎️",
}

export const STATUS = {
  ERROR: "ERROR",
  SUCCESS: "SUCCESS"
}

export const CORE_OVERVIEW_ID = 1

export const MQTT_TOPICS = {
  CAR_CONTROL_UPDATE: 'CAR_CONTROL_UPDATE',
  GAME_STATE_UPDATE: 'GAME_STATE_UPDATE'
}

export const RACE_OPERATIONS = {
  INITIALISE: "initialise",
  SET_PRACTICE: "set_practice",
  SET_PENDING: "set_pending",
  TRIGGER_RED_FLAG: "trigger_red_flag",
  TRIGGER_YELLOW_FLAG: "trigger_yellow_flag",
  TRIGGER_GREEN_FLAG: "trigger_green_flag",
  TRIGGER_CHECKERED_FLAG: "trigger_checkered_flag",
  TRIGGER_FORMATION_LAPS: "trigger_formation_laps",
  CREATE_NEW_RACE: "create_new_race",
  ABORT_RACE: "abort_race"
}

export const RACE_CONFIRMATION_MESSAGES = {
  [RACE_OPERATIONS.ABORT_RACE]: "Are you sure you want to abort this race?",
  [RACE_OPERATIONS.CREATE_NEW_RACE]: "Are you sure you want to create a new race?",
  [RACE_OPERATIONS.SET_PRACTICE]: "Are you sure you want to allow drivers to do practice runs?",
  [RACE_OPERATIONS.SET_PENDING]: "Are you sure you want to line up the drivers?",
  [RACE_OPERATIONS.TRIGGER_CHECKERED_FLAG]: "Are you sure you want to finish this race?",
  [RACE_OPERATIONS.TRIGGER_FORMATION_LAPS]: "Are you sure you want to start the formation lap?",
}

export const LAPTIME_TYPE_STRING = "laptime"

export const LEADERBOARD_INDEX_ICONS = ["🥇", "🥈", "🥉"]