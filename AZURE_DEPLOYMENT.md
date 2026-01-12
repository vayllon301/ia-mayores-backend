# Azure Web App Deployment Guide

## Prerequisites

- Azure account with an active subscription
- Azure CLI installed (optional, but recommended)

## Deployment Steps

### Option 1: Deploy via Azure Portal

1. **Create Azure Web App**

   - Go to Azure Portal (portal.azure.com)
   - Create a new "Web App" resource
   - Select:
     - Runtime: Python 3.11
     - Operating System: Linux
     - Region: Choose closest to your users

2. **Configure Application Settings**

   - Go to your Web App → Configuration → Application Settings
   - Add the following environment variables:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Configure Startup Command**

   - Go to Configuration → General Settings
   - Set "Startup Command" to:
     ```
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120
     ```
   - Or simply use the startup.txt file content

4. **Deploy Code**

   - Option A: Use GitHub Actions (recommended)

     - Connect your GitHub repository in Deployment Center
     - Azure will auto-generate a workflow file

   - Option B: Local Git deployment

     - Enable Local Git in Deployment Center
     - Push your code to the Azure Git remote

   - Option C: ZIP deployment
     - Zip your project files (exclude venv, **pycache**)
     - Use Azure CLI: `az webapp deployment source config-zip`

### Option 2: Deploy via Azure CLI

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-ia-mayores --location westeurope

# Create App Service plan
az appservice plan create \
  --name plan-ia-mayores \
  --resource-group rg-ia-mayores \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group rg-ia-mayores \
  --plan plan-ia-mayores \
  --name ia-mayores-backend \
  --runtime "PYTHON:3.11"

# Configure startup command
az webapp config set \
  --resource-group rg-ia-mayores \
  --name ia-mayores-backend \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 120"

# Set environment variables
az webapp config appsettings set \
  --resource-group rg-ia-mayores \
  --name ia-mayores-backend \
  --settings OPENAI_API_KEY="your_key_here"

# Deploy code (from local directory)
az webapp up \
  --resource-group rg-ia-mayores \
  --name ia-mayores-backend \
  --runtime "PYTHON:3.11"
```

## Important Configuration

### Environment Variables (Required)

- `OPENAI_API_KEY`: Your OpenAI API key

### Files Included for Azure

- `requirements.txt`: Python dependencies
- `startup.txt`: Startup command for Azure
- `.python_version`: Python version specification
- `.deployment`: Azure deployment configuration

### Testing Your Deployment

Once deployed, test your endpoints:

1. Health check:

   ```
   https://your-app-name.azurewebsites.net/health
   ```

2. Chat endpoint:
   ```bash
   curl -X POST https://your-app-name.azurewebsites.net/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello!"}'
   ```

## Monitoring

- Enable Application Insights for monitoring
- Check logs: Azure Portal → Your Web App → Log stream
- Or use CLI: `az webapp log tail --name ia-mayores-backend --resource-group rg-ia-mayores`

## Scaling

For production workloads, consider:

- Scaling up: Choose a higher-tier App Service plan (B2, B3, S1, etc.)
- Scaling out: Increase number of instances
- Adjust worker count in startup command based on instance size

## Troubleshooting

1. **App not starting**: Check startup logs in Azure Portal
2. **Import errors**: Verify all dependencies in requirements.txt
3. **API key issues**: Verify environment variables are set correctly
4. **Timeout errors**: Increase `--timeout` value in startup command

## Security Best Practices

1. Update CORS origins in `app/main.py` to your frontend domain
2. Enable HTTPS only
3. Use Azure Key Vault for sensitive data
4. Enable authentication if needed
