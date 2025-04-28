import os
import json
import uuid
import openai

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HERE = os.path.dirname(__file__)

def load_prompt_map():
    """
    Carrega os mapeamentos de estilo dos arquivos JSON e retorna um dict { value: prompt }
    """
    prompt_map = {}

    for fname in [
        "prompts/animations_prompts.json",
        "prompts/games_prompts.json",
        "prompts/live_actions_prompts.json",
        "prompts/others_prompts.json",
    ]:
        path = os.path.join(HERE, fname)

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Arquivo de prompts não encontrado: {path}")

        with open(path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        for entry in entries:
            prompt_map[entry["value"]] = entry["prompt"]

    return prompt_map


PROMPT_MAP = load_prompt_map()

class InvalidStyleError(Exception):
    """Lançada quando o image_style não está no mapeamento"""
    pass

class EmptyUrlError(Exception):
    """Lançada quando a URL retornada pela API de edição é vazia"""
    pass

async def process_image(file_obj, filename: str, image_style: str, additional_details: str) -> str:
    """
    Processa a imagem:
    - Valida o image_style
    - Salva a imagem em disco temporariamente
    - Usa GPT-4.1-mini para combinar o prompt base e detalhes adicionais
    - Chama openai.Image.create_edit com o prompt final
    - Retorna a URL da imagem editada
    """
    base_prompt = PROMPT_MAP.get(image_style)

    if base_prompt is None:
        valid = ", ".join(PROMPT_MAP.keys())
        raise InvalidStyleError(
            f"Estilo '{image_style}' não reconhecido. Valores válidos: {valid}"
        )

    tmp_path = f"/tmp/{uuid.uuid4().hex}_{filename}"
    file_obj.seek(0)

    with open(tmp_path, "wb") as out:
        out.write(file_obj.read())

    try:
        system_msg = (
            "Você é um assistente que recebe um prompt de estilo de arte e detalhes adicionais, "
            "e retorna um prompt único em Inglês, pronto para ser usado na API de edição de imagens."
        )

        user_msg = (
            f"Estilo base: {base_prompt}\n"
            f"Detalhes adicionais: {additional_details}\n\n"
            "Combine-os em um único prompt em Inglês e retorne apenas o texto do prompt final."
        )

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )

        final_prompt = response.choices[0].message.content.strip()

        print(f"Prompt final: {final_prompt}")

        with open(tmp_path, "rb") as img_f:
            edit_resp = client.images.edit(
                model="gpt-image-1",
                image=img_f,
                prompt=final_prompt,
            )

        print(edit_resp)

        base_64_img = edit_resp.data[0].b64_json

        if not isinstance(base_64_img, str) or not base_64_img:
            raise EmptyUrlError("A API de edição não retornou uma imagem válida")

        return base_64_img

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
