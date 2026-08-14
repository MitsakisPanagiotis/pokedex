BASE_URL: str = "https://pokeapi.co/api/v2/pokemon?limit="
ENDPOINTS: dict[str, str] = {
    "generation_i": f"{BASE_URL}151",
    "generation_ii": f"{BASE_URL}100&offset=151",
    "generation_iii": f"{BASE_URL}135&offset=251",
    "generation_iv": f"{BASE_URL}107&offset=386",
    "generation_v": f"{BASE_URL}156&offset=493",
    "generation_vi": f"{BASE_URL}72&offset=649",
    "generation_vii": f"{BASE_URL}88&offset=721",
    "generation_viii": f"{BASE_URL}96&offset=809",
    "generation_ix": f"{BASE_URL}120&offset=905",
}
