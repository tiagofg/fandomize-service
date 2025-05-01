import json
import os
from loguru import logger
from functools import lru_cache

HERE = os.path.dirname(__file__)

PROMPT_DIR = os.path.normpath(os.path.join(HERE, os.pardir, os.pardir, "prompts"))

@lru_cache(maxsize=1)
def load_prompt_map() -> dict[str, str]:
    """
    Carrega (uma vez só) os mapeamentos de estilo
    e devolve {value: prompt}.
    """
    prompt_map: dict[str, str] = {}

    for fname in (
        "animations_prompts.json",
        "games_prompts.json",
        "live_actions_prompts.json",
        "others_prompts.json",
    ):
        path = os.path.join(PROMPT_DIR, fname)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo de prompts não encontrado: {path}")
        
        with open(path, encoding="utf-8") as f:
            for entry in json.load(f):
                prompt_map[entry["value"]] = entry["prompt"]

    logger.success("Prompts carregados: {}", len(prompt_map))
    return prompt_map
