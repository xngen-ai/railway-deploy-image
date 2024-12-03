# railway-deploy-image

GitHub Action for deploying Docker images to Railway services.

## Description

This action allows you to deploy a Docker image to a Railway service using Railway's GraphQL API.

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| `railway_token` | Railway API token | Yes |
| `image_url` | Full Docker image URL with tag | Yes |
| `service_id` | Railway service ID | Yes |
| `environment_id` | Railway environment ID | Yes |

## Usage

~~~yaml
- name: Deploy to Railway
  uses: your-username/railway-deploy-image@v1
  with:
    railway_token: ${{ secrets.RAILWAY_TOKEN }}
    image_url: ${{ steps.image_info.outputs.IMAGE_FULL_NAME }}:${{ steps.image_info.outputs.IMAGE_TAG }}
    service_id: ${{ secrets.RW_SERVICE_ID_DEV }}
    environment_id: ${{ secrets.RW_ENVIRONMENT_ID_DEV }}
~~~

## Example Workflow

~~~yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Add steps to build and push your Docker image
      
      - name: Deploy to Railway
        uses: your-username/railway-deploy-image@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          image_url: ${{ steps.image_info.outputs.IMAGE_FULL_NAME }}:${{ steps.image_info.outputs.IMAGE_TAG }}
          service_id: ${{ secrets.RW_SERVICE_ID_DEV }}
          environment_id: ${{ secrets.RW_ENVIRONMENT_ID_DEV }}
~~~

## License

MIT
