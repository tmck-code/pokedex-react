export async function fetchData (url) {
    let res = await fetch(url)
    let data = await res.json()
    console.log(data)
    return data
}

export function fetchCardSets () {
    return fetchData('http://localhost:8000/card_sets/')
}

export default function fetchCards(card_set_code) {
    return fetchData('http://localhost:8000/card_sets/' + card_set_code + '/cards/')
}

export function fetchCardSet(card_set_code) {
    return fetchData('http://localhost:8000/card_sets/' + card_set_code + '/')
}
