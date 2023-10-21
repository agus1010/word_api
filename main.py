from typing import Annotated
from fastapi import FastAPI, Query, Path
from random import randint
import word_db as WordDB
import word_db.rae_definitions as RAE


word_api = FastAPI()


@word_api.get("/pick_word")
def pick_word(
    length: Annotated[int, Query(ge= WordDB.MIN_WORD_LENGTH, le= WordDB.MAX_WORD_LENGTH)] = 5,
    accents: bool = False
):
    accents_key = "accented" if accents else "accentless"
    total_word_count = WordDB.STATS["selectables"][accents_key][str(length)]
    chosen_index = randint(0, total_word_count)
    word = WordDB.get_selectable_word_at_index(index= chosen_index, accented= accents, length= str(length))
    return { "word": word }


@word_api.get("/define/{word:str}")
def define(
    word: Annotated[str, Path(min_length= WordDB.MIN_WORD_LENGTH, max_length= WordDB.MAX_WORD_LENGTH)]
):
    original_accented = WordDB.get_original_accented_word(word)
    rae_word = RAE.search_word(word)
    accented_rae_word = RAE.search_word(original_accented) if original_accented != "" else RAE.RAEWord("", [])
    definitions = []
    if len(rae_word.definitions) > 0:
        definitions.append(rae_word)
    if word != original_accented and len(accented_rae_word.definitions) > 0:
        definitions.append(accented_rae_word)
    return [ rae_w.__dict__ for rae_w in definitions ]