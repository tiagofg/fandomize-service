import os
import uuid
from loguru import logger

from exceptions.custom_exceptions import EmptyUrlError, InvalidStyleError
from services.prompt_loader import load_prompt_map
from core.config import client, settings

async def process_image(
    file_obj,
    filename: str,
    image_style: str,
    additional_details: str,
) -> str:
    prompt_map = load_prompt_map()           
    base_prompt = prompt_map.get(image_style)

    if base_prompt is None:
        valid = ", ".join(prompt_map)
        raise InvalidStyleError(f"Estilo “{image_style}” inválido. Válidos: {valid}")

    tmp_path = os.path.join(settings.tmp_dir, f"{uuid.uuid4().hex}_{filename}")
    file_obj.seek(0)

    with open(tmp_path, "wb") as out:
        out.write(file_obj.read())

    try:
        system_msg = (
            "Você é um assistente que recebe um prompt de estilo de arte e detalhes "
            "adicionais e devolve um prompt único em inglês pronto para edição."
        )

        user_msg = (
            f"Estilo base: {base_prompt}\n"
            f"Detalhes adicionais: {additional_details}\n\n"
            "Combine-os em um único prompt em inglês e retorne somente o prompt final."
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
        logger.info("📝 Prompt final gerado: {}", final_prompt)

        with open(tmp_path, "rb") as img_f:
            edit_resp = client.images.edit(
                model="gpt-image-1",
                image=img_f,
                prompt=final_prompt,
                quality="medium",
            )

        logger.info("🎨 Resposta da edição: {}", edit_resp)
        base64_img = edit_resp.data[0].b64_json
        
        if not base64_img:
            raise EmptyUrlError("A API de edição não retornou imagem válida")

        return base64_img

    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            logger.warning("Falha ao apagar arquivo temporário {}", tmp_path)
