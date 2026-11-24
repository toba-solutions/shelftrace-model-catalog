# Shelftrace Model Catalog

The public catalog for Shelftrace’s optional cloud classification. It gives the model picker readable names, recommendations, and retirement notices for OpenAI, Claude, Gemini, and Mistral. Catalog updates reach the app after a successful refresh without requiring a new App Store release.

[Browse the catalog](models-v1.json) · [Download the JSON](https://raw.githubusercontent.com/toba-solutions/shelftrace-model-catalog/main/models-v1.json)

## How Shelftrace uses it

In Shelftrace, open **Settings → Intelligence**, choose a provider, and click **Refresh Models**. Shelftrace fetches the public catalog from GitHub and, when you’ve saved an API key, asks the selected provider which models your account can access. The provider determines availability. Shelftrace uses the catalog to annotate and recommend those choices.

The GitHub request is unauthenticated and fetches model metadata only. Shelftrace sends your API key directly to your selected provider for model discovery. Your saved model stays selected when you refresh, and you can enter a custom model ID in the picker.

## Updating the catalog

1. Edit `models-v1.json`. Keep `schemaVersion` at `1` and place each entry under `openai`, `claude`, `gemini`, or `mistral` in `providers`.
2. Use the exact API model ID and keep it unique within its provider. Verify that the model supports Shelftrace’s structured JSON classification before marking it compatible or recommending it.
3. Publish the change to `main`. In Shelftrace, click **Refresh Models** and verify the updated name, recommendation, or notice. GitHub caching can briefly delay changes.

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | Yes | Provider’s API model ID. For Gemini, omit the `models/` prefix. |
| `name` | Yes | Display name in the picker, up to 128 characters. |
| `compatible` | Yes | Boolean indicating whether the model has been verified for structured JSON classification. |
| `recommended` | Yes | Boolean indicating whether Shelftrace should recommend an eligible model. |
| `retiresOn` | No | Announced retirement date in `YYYY-MM-DD` format. |
| `note` | No | Short message shown when the model is selected, up to 240 characters. |
