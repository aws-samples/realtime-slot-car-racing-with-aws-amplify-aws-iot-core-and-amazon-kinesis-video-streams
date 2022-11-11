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

const { ERRORS, STATUS, RACE_STATES, SUCCESS_MESSAGES, FUNCTION_INPUTS } = require('./utils/constants')
const { getRace, createLapTime } = require('./utils/graphql-statements')

/**
 * Function inputs:
 * raceId: STRING
 * playerId: STRING
 * timeInMilliSec: INT
*/

exports.handler = async (event) => {
  const { values, missingValues } = getFunctionInputs(event)

  if (missingValues.length > 0) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.MISSING_VARIABLE,
      details: `Missing: ${JSON.stringify(missingValues)}`
    }
  }

  // Can skip this step if we don't care about checking the race state
  const currentRace = await getCurrentRace(values[FUNCTION_INPUTS.RACE_ID])
  if (currentRace.status === STATUS.ERROR) { console.log(currentRace); return currentRace }

  // Check if player we're creating laptime for is actually in the race
  if (!currentRace.data.players.items.find(p => p.id === values[FUNCTION_INPUTS.PLAYER_ID])) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.PLAYER_NOT_IN_RACE
    }
  }

  // Create Lap Time Data
  let lapTime;
  try {
    const lapTimeData = {
      timeInMilliSec: values[FUNCTION_INPUTS.TIME_IN_MS],
      playerId: values[FUNCTION_INPUTS.PLAYER_ID],
      raceId: currentRace.data.id
    }
    lapTime = await createLapTime(lapTimeData)
  } catch (error) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.UNABLE_TO_CREATE_LAPTIME,
      details: String(error)
    }
  }
  return {
    status: STATUS.SUCCESS,
    message: SUCCESS_MESSAGES.SUCCESSFULLY_CREATED_LAPTIME,
    details: JSON.stringify(lapTime)
  }
};

// Function go get all the function inputs by names defined in utils/constants.js
const getFunctionInputs = (event) => {
  let variableRoot = event.arguments?.input || event
  var missingValues = []
  var values = {}
  for (const value of Object.values(FUNCTION_INPUTS)) {
    const inputValue = variableRoot[value]
    if (inputValue === null || inputValue === undefined) {
      missingValues.push(value)
    } else {
      values[value] = inputValue
    }
  }
  return {
    values,
    missingValues
  }
}

// Function to fetch the race object by raceId
const getCurrentRace = async (raceId) => {
  let currentRace;
  try {
    const currentRaceData = await getRace(raceId)
    currentRace = currentRaceData.data.getRace
  } catch (error) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.UNABLE_TO_FETCH_RACE_INFO,
      details: String(error)
    }
  }

  if (currentRace === null || currentRace === undefined) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.RACE_DOESNT_EXIST,
    }
  }

  if (currentRace.currentRaceState !== RACE_STATES.GREEN_FLAG) {
    return {
      status: STATUS.ERROR,
      message: ERRORS.RACE_NOT_ONGOING,
    }
  }
  return {
    status: STATUS.SUCCESS,
    data: currentRace
  }
}