from fastapi import FastAPI, status, Response #, Query
# from typing import Annotated

from word_db import get_original_accented_word, get_random_selectable_word, word_is_in_dictionary, word_has_accents
from word_db.rae_definitions import search_word


word_db = FastAPI()


# def word_definition(word: Annotated[str | None, Query(min_length= 5, max_length=10)] = None):
@word_db.get("/definitions/{word}")
def get_definition(word: str):
    result = { "data": [] }
    result["data"] += _get_definitions_to_add(word)
    original_accented = get_original_accented_word(word)
    if original_accented != word:
        result["data"] += _get_definitions_to_add(original_accented)
    return result
    

@word_db.get("/words/check")
def check_word(word:str, response: Response):
    is_in_db = word_is_in_dictionary(word=word, accents_mode=word_has_accents(word))
    response.status_code = status.HTTP_204_NO_CONTENT if is_in_db else status.HTTP_404_NOT_FOUND


# def get_word(length: Annotated[int, Query(ge=5, le=10)] = 5, accents: bool = False):
@word_db.get("/words/pick")
def get_word(length: int = 5, accents: bool = False):
    return { "word": get_random_selectable_word(length, accents) }



def _get_definitions_to_add(word:str) -> [{str: any}]:
    result = []
    definitions = search_word(word)
    if definitions.definitions and len(definitions.definitions) > 0:
        result.append(definitions)
    return result