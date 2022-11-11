/* Amplify Params - DO NOT EDIT
	API_RACER_GRAPHQLAPIENDPOINTOUTPUT
	API_RACER_GRAPHQLAPIIDOUTPUT
	API_RACER_GRAPHQLAPIKEYOUTPUT
	ENV
	REGION
Amplify Params - DO NOT EDIT */

/**
 * @type {import('@types/aws-lambda').APIGatewayProxyHandler}
 */

const { CARS, ERRORS, STATUS, CORE_OVERVIEW_ID, RACE_STATES, SUCCESS_MESSAGES } = require('./utils/constants')
const {
  getCar,
  createCar,
  createOverview,
  getOverview,
  createRace,
  createPlayer,
  updateOverview,
  updateRace,
} = require('./utils/graphql-statements')

exports.handler = async (event) => {
  const params = event.arguments.input
  if (params.secretPin !== process.env.SECRETPIN) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.INVALID_PIN,
    }
  }

  const { nrOfLaps, raceId } = params.additionalParams

  try {
    switch (params.operation) {
      case 'initialise':                return await initialiseSetup(nrOfLaps)
      case 'set_practice':              return await setRaceState(raceId, RACE_STATES.PRACTICE)
      case 'set_pending':               return await setRaceState(raceId, RACE_STATES.PENDING)
      case 'trigger_red_flag':          return await setRaceState(raceId, RACE_STATES.RED_FLAG)
      case 'trigger_yellow_flag':       return await setRaceState(raceId, RACE_STATES.YELLOW_FLAG)
      case 'trigger_green_flag':        return await setRaceState(raceId, RACE_STATES.GREEN_FLAG)
      case 'trigger_checkered_flag':    return await setRaceState(raceId, RACE_STATES.CHECKERED_FLAG)
      case 'trigger_formation_laps':    return await setRaceState(raceId, RACE_STATES.FORMATION_LAPS)
      case 'abort_race':                return await setRaceState(raceId, RACE_STATES.ABORTED)
      case 'create_new_race':           return await initRace(nrOfLaps)
      default:                          return { status: STATUS.ERROR, message: ERRORS.INVALID_OPERATION }
    }
  } catch (error) {
    return {
      status: STATUS.ERROR,
      message: error.message,
      details: String(error)
    }
  }
};

const initialiseSetup = async () => {
  // Step 1: Create Cars if not exists
  await createCars()

  // Step 2: Create Overview if not exists
  await initOverview()

  return {
    status: STATUS.SUCCESS,
    message: SUCCESS_MESSAGES.SUCCESSFUL_INIT,
  }
}

const createCars = async () => {
  const carData = CARS.map((item) => {
    return {
      id: item.value,
      color: item.color,
      throttle: 0,
      fuelLevel: 100,
      tireWear: 0,
      speed: 0,
      requestLaneSwitch: false,
      brakesOn: false
    }
  })

  for (const car of carData) {
    try {
      const carExists = await getCar(car.id)
      if (carExists.data?.getCar?.id === undefined) {
        await createCar(car)
      }
    } catch (error) {
      console.error(error)
      throw Error(ERRORS.ERROR_CREATING_CAR)
    }
  }
}

const initOverview = async () => {
  try {
    const overviewExists = await getOverview()
    if (overviewExists.data?.getOverview?.id === undefined) {
      await createOverview()
    }
  } catch (error) {
    console.error(error)
    throw Error(ERRORS.ERROR_CREATING_OVERVIEW)
  }
}

const initRace = async (nrOfLaps) => {
  let result;
  try {
    result = await createRace({
      nrOfLaps,
      overviewAllRacesId: CORE_OVERVIEW_ID,
      currentRaceState: RACE_STATES.LOBBY
    })
    const raceId = result.data.createRace.id

    const playerInit = await initPlayers(raceId)
    console.log(playerInit)

    const setLobbyRaceState = await setRaceState(raceId, RACE_STATES.LOBBY)
    console.log(setLobbyRaceState)

    const updateOverview = await updateOverviewRaceId(raceId)
    console.log(updateOverview)

  } catch (error) {
    console.error(error)
    throw Error(ERRORS.ERROR_CREATING_RACE)
  }
  return {
    status: STATUS.SUCCESS,
    message: SUCCESS_MESSAGES.SUCCESSFUL_RACE_INIT,
    details: JSON.stringify(result)
  }
}

const initPlayers = async (raceId) => {
  for (const car of CARS) {
    try {
      await createPlayer({ playerCarId: car.value, racePlayersId: raceId })
    } catch (error) {
      console.error(error)
      throw new Error(ERRORS.ERROR_CREATING_PLAYER)
    }
  }
}

const setRaceState = async (raceId, raceState) => {
  let result;
  try {
    result = await updateRace({ id: raceId, currentRaceState: raceState })
  } catch (error) {
    console.error(error)
    throw Error(ERRORS.ERROR_CREATING_RACE_STATE)
  }
  return {
    status: STATUS.SUCCESS,
    message: SUCCESS_MESSAGES.SUCCESSFUL_STATE_UPDATE,
    details: JSON.stringify(result)
  }
}

const updateOverviewRaceId = async (raceId) => {
  let overview;
  try {
    overview = await updateOverview({ id: CORE_OVERVIEW_ID, overviewCurrentRaceId: raceId })
  } catch (error) {
    console.error(error)
    throw Error(ERRORS.ERROR_UPDATING_RACE_OVERVIEW)
  }
  return {
    status: STATUS.SUCCESS,
    message: SUCCESS_MESSAGES.SUCCESSFUL_OVERVIEW_UPDATE,
    details: JSON.stringify(overview)
  }
}