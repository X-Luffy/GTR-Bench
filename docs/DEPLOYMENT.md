# Deployment Guide

This guide provides instructions for deploying the Human-Level Visual Reasoning Assessment System in various environments.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Modern web browser

### Software Dependencies
- Python package manager (pip or conda)
- Git (for version control)
- Web server (optional, for production)

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd human-level-assessment
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n human-level python=3.9
conda activate human-level
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
streamlit --version
python -c "import cv2, PIL, numpy, pandas; print('All dependencies installed successfully')"
```

### 5. Run Application
```bash
streamlit run app.py
```

## Production Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Prepare Repository**
   - Ensure all files are committed to Git
   - Create `requirements.txt` with exact versions
   - Add `.streamlit/config.toml` for configuration

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure deployment settings
   - Deploy

3. **Configuration File** (`.streamlit/config.toml`)
   ```toml
   [server]
   port = 8501
   headless = true
   enableCORS = false
   enableXsrfProtection = false

   [browser]
   gatherUsageStats = false
   ```

### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run**
   ```bash
   docker build -t human-level-assessment .
   docker run -p 8501:8501 human-level-assessment
   ```

### Option 3: Traditional Server Deployment

1. **Server Setup**
   ```bash
   # Install Python and dependencies
   sudo apt update
   sudo apt install python3 python3-pip python3-venv

   # Create application directory
   sudo mkdir -p /opt/human-level-assessment
   sudo chown $USER:$USER /opt/human-level-assessment
   ```

2. **Application Deployment**
   ```bash
   cd /opt/human-level-assessment
   git clone <repository-url> .
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Systemd Service** (`/etc/systemd/system/human-level.service`)
   ```ini
   [Unit]
   Description=Human Level Assessment System
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/human-level-assessment
   Environment=PATH=/opt/human-level-assessment/venv/bin
   ExecStart=/opt/human-level-assessment/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable human-level
   sudo systemctl start human-level
   ```

### Option 4: Cloud Platform Deployment

#### AWS EC2
1. Launch EC2 instance (t3.medium or larger)
2. Install Docker or Python environment
3. Follow Docker or traditional deployment steps
4. Configure security groups for port 8501

#### Google Cloud Platform
1. Create Compute Engine instance
2. Install application dependencies
3. Use Cloud Run for containerized deployment
4. Configure load balancer if needed

#### Azure
1. Create Virtual Machine or App Service
2. Deploy using Azure Container Instances
3. Configure networking and security

## Configuration

### Environment Variables
```bash
# Optional configuration
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## Data Management

### Data Directory Structure
```
data/
├── outdoor/
│   ├── raw_video/     # Video files
│   ├── crop_video/    # Cropped videos
│   ├── map/          # Map images
│   └── *.json        # Question data
└── indoor/
    ├── raw_video/     # Video files
    ├── crop_video/    # Cropped videos
    ├── map/          # Map images
    └── *.json        # Question data
```

### Data Backup
```bash
# Create backup
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Restore backup
tar -xzf data-backup-YYYYMMDD.tar.gz
```

## Monitoring and Maintenance

### Log Management
```bash
# View application logs
journalctl -u human-level -f

# Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log
```

### Performance Monitoring
- Monitor CPU and memory usage
- Check disk space for video files
- Monitor network traffic
- Set up alerts for service downtime

### Updates
```bash
# Update application
cd /opt/human-level-assessment
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart human-level
```

## Security Considerations

### Network Security
- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting
- Use VPN for sensitive deployments

### Data Security
- Encrypt sensitive data
- Regular security updates
- Access control and authentication
- Audit logging

### Backup Strategy
- Regular data backups
- Test restore procedures
- Off-site backup storage
- Version control for code

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8501
   lsof -i :8501
   # Kill process
   kill -9 <PID>
   ```

2. **Permission Denied**
   ```bash
   # Fix file permissions
   chmod +x app.py
   chown -R $USER:$USER /opt/human-level-assessment
   ```

3. **Missing Dependencies**
   ```bash
   # Reinstall requirements
   pip install --force-reinstall -r requirements.txt
   ```

4. **Video Files Not Found**
   - Check file paths in JSON data
   - Verify file permissions
   - Ensure data directory structure is correct

### Performance Issues
- Increase server resources
- Optimize video file sizes
- Implement caching strategies
- Use CDN for static assets

## Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Deploy multiple instances
- Implement session sharing
- Use external database for state

### Vertical Scaling
- Increase server resources
- Optimize application code
- Use faster storage (SSD)
- Implement caching layers

## Support

For deployment issues:
1. Check application logs
2. Verify system requirements
3. Review configuration files
4. Open GitHub issue with details
