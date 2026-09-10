# Fandomize Service

Fandomize Service is the image-processing API behind [Fandomize Web](https://github.com/tiagofg/fandomize-web). It accepts an uploaded image, a style identifier, and additional instructions, then uses OpenAI models to compose an English editing prompt and generate an edited image.

The API currently exposes one operation: `POST /edit-image`.

## Processing flow

1. FastAPI parses the multipart upload and form fields.
2. The service loads the style prompt from the JSON catalogs in [`prompts/`](prompts/).
3. `gpt-4.1-mini` combines the catalog prompt and additional details into a final English prompt.
4. `gpt-image-1` edits the uploaded image with that prompt at medium quality.
5. The API returns the generated image as a base64 string in `{ "image": "..." }`.

Uploaded files are copied to the configured temporary directory and removed in a `finally` block after processing.

## Technology

- Python 3.13 in the supplied Docker image
- FastAPI and Uvicorn
- OpenAI Python SDK
- Pydantic Settings and python-dotenv
- Loguru with YAML logging configuration

## Requirements

- Python 3.13 recommended to match the container
- An OpenAI API key with access to the configured text and image models

Image editing uses billable external API operations.

## Local setup

Run from the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cat > .env <<'EOF'
OPENAI_API_KEY=replace-with-your-key
EOF
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Pydantic also supports the optional `TMP_DIR` setting. It defaults to `/tmp` and must point to a writable directory.

The prompt loader reads the four tracked JSON catalogs from the repository-root `prompts/` directory. Run the application with the repository contents intact so those files remain available.

## API

### `POST /edit-image`

Send a `multipart/form-data` request with all three fields:

| Field | Type | Description |
| --- | --- | --- |
| `uploaded_image` | File | Source image to edit |
| `image_style` | String | Style value from the prompt catalogs |
| `additional_details` | String | Required, nonempty guidance for the edit |

For example, `pixel-art` is a valid tracked style value:

```bash
curl --request POST http://localhost:8000/edit-image \
  --form 'uploaded_image=@./example.png' \
  --form 'image_style=pixel-art' \
  --form 'additional_details=keep the original background' \
  --output response.json
```

This request calls the configured OpenAI models. A successful response contains base64 image data rather than an image file or URL.

Unknown style values return HTTP 400. The router maps `EmptyUrlError` to HTTP 404; other processing exceptions return HTTP 500. FastAPI validation errors use the framework's standard validation response.

Interactive OpenAPI documentation is available at `/docs` while the application is running.

## Docker and deployment

Build and run the image from the repository root:

```bash
docker build -t fandomize-service .
docker run --rm \
  --publish 127.0.0.1:8000:8000 \
  --env-file .env \
  fandomize-service
```

The image runs Uvicorn as an unprivileged user with four workers and exposes port 8000. It copies both `app/` and `prompts/` into the image.

The included GitHub Actions workflow deploys pushes to `main` over SSH and rebuilds a Compose service named `backend`. The Compose file and host configuration are external to this repository. The workflow does not run automated tests before deployment, and this repository does not currently contain a test suite.

## Current limitations

- Requests invoke synchronous OpenAI SDK methods inside an async route, which can tie up an event-loop worker during long model calls.
- Upload size, file type, and filename are not explicitly validated by application code.
- The API returns potentially large base64 payloads in JSON and does not persist generated images.
- Error responses can include underlying exception text.
- The endpoint has no application-level authentication or rate limiting.
- Style identifiers are fixed by the JSON files in `prompts/`; clients must keep their catalogs aligned with those values.
