# Deploying Granola.g

This guide covers the deployment process for the Granola.g team building platform.

## Prerequisites

- Docker and Docker Compose installed
- Git access to the repository
- OpenAI API key with function calling capabilities
- Access to desired domain for hosting (optional)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/e2i-uvu/granola.g.git
   cd granola.g
   ```

2. Create environment files:
   ```bash
   # For frontend
   cp frontend/template.env frontend/.env
   ```

3. Edit the `.env` file to include:
   - OpenAI API key
   - Backend authentication credentials
   - Any other required environment variables

## Deployment Options

Granola.g comes with several pre-configured deployment options:

### Development Environment

For local development and testing:

```bash
docker-compose -f development.yaml up -d
```

This configuration:
- Maps local ports to container ports
- Uses less resource-intensive settings
- Enables development-friendly features

### Staging Environment

For pre-production testing:

```bash
docker-compose -f staging.yaml up -d
```

This configuration:
- Includes a Traefik reverse proxy for HTTPS
- Uses more production-like settings
- Can be deployed to a staging server

### Production Environment

For live deployment:

```bash
docker-compose -f production.yaml up -d
```

This configuration:
- Uses optimized resource settings
- Includes full HTTPS with Let's Encrypt integration
- Implements proper logging and monitoring

## Traefik Configuration

For staging and production deployments with HTTPS:

1. Configure your domain in `docker-compose.traefik.yaml`
2. Ensure the Let's Encrypt directory exists and has proper permissions
3. Deploy with:
   ```bash
   docker-compose -f docker-compose.traefik.yaml up -d
   ```

## Updating the Deployment

To update an existing deployment with the latest code:

```bash
git pull
docker-compose -f [chosen-environment].yaml down
docker-compose -f [chosen-environment].yaml up -d --build
```

This rebuilds the containers with any new code changes.

## Troubleshooting

### Container Logs

To view logs for troubleshooting:

```bash
# All containers
docker-compose -f [environment].yaml logs

# Specific container
docker-compose -f [environment].yaml logs go_server
docker-compose -f [environment].yaml logs streamlit
```

### Common Issues

1. **Authentication Failures**: Verify credentials in environment variables
2. **OpenAI API Issues**: Check API key validity and network connectivity
3. **Database Errors**: Ensure volume permissions are correct
4. **Network Issues**: Check that containers can communicate with each other

## Backup and Recovery

To backup the database:

```bash
docker cp granola_go_server:/app/database/database.db ./database-backup.db
```

To restore from backup:

```bash
docker cp ./database-backup.db granola_go_server:/app/database/database.db
```

## Security Considerations

- Keep your OpenAI API key and authentication credentials secure
- Regularly update the Docker images and dependencies
- Use HTTPS in production environments
- Implement proper network security for your deployment server