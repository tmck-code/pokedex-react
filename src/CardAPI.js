/**
 * Fetches data from the python API
 * @param {string} url the URL to fetch data from
 * @returns {Promise<any>} the JSON response from the API
 */
export async function fetchData (endpoint, debug=false) {
    let res = await fetch(`http://localhost:8000/${endpoint}`)
    let data = await res.json()
    debug && console.log(`[CardAPI] fetched ${endpoint} from API: ${data}`)
    return data
}

/**
 * Fetches the list of available Card Sets from the API
*/
export function fetchCardSets () {
    return fetchData('card_sets/')
}

/**
 * Fetches the list of Cards that belong to a Card Set from the API
*/
export default function fetchCards(card_set_code) {
    return fetchData(`card_sets/${card_set_code}/cards/`)
}
