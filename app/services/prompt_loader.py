import json
import os
from loguru import logger
from functools import lru_cache

HERE = os.path.dirname(__file__)

@lru_cache(maxsize=1)
def load_prompt_map() -> dict[str, str]:
    """
    Carrega (uma vez só) os mapeamentos de estilo
    e devolve {value: prompt}.
    """
    prompt_map: dict[str, str] = {}
    for fname in (
        "/../../prompts/animations_prompts.json",
        "/../../prompts/games_prompts.json",
        "/../../prompts/live_actions_prompts.json",
        "/../../prompts/others_prompts.json",
    ):
        path = os.path.join(HERE, fname)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo de prompts não encontrado: {path}")
        
        with open(path, encoding="utf-8") as f:
            for entry in json.load(f):
                prompt_map[entry["value"]] = entry["prompt"]

    logger.success("Prompts carregados: {}", len(prompt_map))
    return prompt_map