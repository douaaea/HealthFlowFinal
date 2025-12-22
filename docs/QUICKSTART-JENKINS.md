# HealthFlow CI/CD - Step by Step Setup

## Quick Start: 5-Minute Setup

Follow these steps to get your Jenkins CI/CD pipeline running.

---

## ✅ Step 1: Install Jenkins Plugins

1. Open Jenkins: `http://localhost:8080`
2. Go to **Manage Jenkins** → **Manage Plugins** → **Available**
3. Search and install these plugins:
   - ✅ Git
   - ✅ GitHub
   - ✅ Pipeline
   - ✅ Docker Pipeline
   - ✅ Credentials Binding
4. Click **Install without restart**
5. Wait for installations to complete

---

## ✅ Step 2: Add Credentials

### GitHub Credentials
1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click **(global)** → **Add Credentials**
3. Fill in:
   - **Kind**: Username with password
   - **Username**: Your GitHub username
   - **Password**: [Create GitHub token here](https://github.com/settings/tokens/new) with scopes: `repo`, `admin:repo_hook`
   - **ID**: `github-credentials`
4. Click **Create**

### Docker Hub Credentials
1. Click **Add Credentials** again
2. Fill in:
   - **Kind**: Username with password
   - **Username**: `taoufikjeta`
   - **Password**: Your Docker Hub password
   - **ID**: `dockerhub-credentials`
3. Click **Create**

### PostgreSQL Password
1. Click **Add Credentials** again
2. Fill in:
   - **Kind**: Secret text
   - **Secret**: `qwerty`
   - **ID**: `postgres-password`
3. Click **Create**

![Credentials overview](C:/Users/daham/.gemini/antigravity/brain/78e36cd3-653d-4913-a2ea-ac4310b48bfe/uploaded_image_3_1766414009457.png)

---

## ✅ Step 3: Create Pipeline Job

1. Click **New Item** on Jenkins dashboard
2. Enter name: `HealthFlow-Pipeline`
3. Select **Pipeline**
4. Click **OK**

### Configure the job:

#### General Section
- ✅ **GitHub project**
  - Project URL: `https://github.com/testalgms/HealthFlowFinal/`

![General configuration](C:/Users/daham/.gemini/antigravity/brain/78e36cd3-653d-4913-a2ea-ac4310b48bfe/uploaded_image_0_1766414009457.png)

#### Build Triggers
- ✅ **GitHub hook trigger for GITScm polling**

![Build triggers](C:/Users/daham/.gemini/antigravity/brain/78e36cd3-653d-4913-a2ea-ac4310b48bfe/uploaded_image_0_1766414009457.png)

#### Pipeline Section
- **Definition**: Pipeline script from SCM
- **SCM**: Git
  - **Repository URL**: `https://github.com/testalgms/HealthFlowFinal.git`
  - **Credentials**: `github-credentials`
  - **Branch**: `*/main`
- **Script Path**: `Jenkinsfile`

![Pipeline configuration](C:/Users/daham/.gemini/antigravity/brain/78e36cd3-653d-4913-a2ea-ac4310b48bfe/uploaded_image_1_1766414009457.png)

5. Click **Save**

---

## ✅ Step 4: Setup GitHub Webhook

1. Go to your GitHub repository: `https://github.com/testalgms/HealthFlowFinal/settings/hooks`
2. Click **Add webhook**
3. Configure:
   - **Payload URL**: `http://YOUR_JENKINS_IP:8080/github-webhook/`
     - Example: `http://192.168.1.100:8080/github-webhook/`
     - For public server: `http://jenkins.yourdomain.com:8080/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: ✅ Just the push event
   - **Active**: ✅
4. Click **Add webhook**

> **Note**: If Jenkins is not publicly accessible, use [ngrok](https://ngrok.com/):
> ```bash
> ngrok http 8080
> # Use the https URL provided by ngrok
> ```

---

## ✅ Step 5: Test the Pipeline

### First Manual Build
1. Go to Jenkins → `HealthFlow-Pipeline`
2. Click **Build Now**
3. Watch the build progress in **Console Output**

### Automatic Build (via webhook)
1. Make a change to your repository
   ```bash
   cd c:/Users/daham/Desktop/Fi/HealthFlowFinal
   git add .
   git commit -m "Test Jenkins webhook"
   git push origin main
   ```
2. Jenkins should automatically start building!

---

## ✅ Step 6: Verify Deployment

After successful build, verify services are running:

### Check Docker Containers
```bash
docker ps
```

You should see 9 containers running:
- healthflow-postgres
- healthflow-proxy-fhir
- healthflow-deid
- healthflow-featurizer
- healthflow-ml-predictor
- healthflow-score-api
- healthflow-audit-fairness
- healthflow-api-gateway
- healthflow-dashboard

### Access Services
- **Dashboard**: http://localhost:3002
- **API Gateway**: http://localhost:8085/actuator/health

---

## 🎉 Success!

Your CI/CD pipeline is now fully operational!

Every push to `main` branch will:
1. ✅ Build all services
2. ✅ Run tests
3. ✅ Create Docker images
4. ✅ Push to Docker Hub
5. ✅ Deploy automatically
6. ✅ Run health checks

---

## 🔍 Monitoring Your Pipeline

### View Build Status
- Jenkins Dashboard → Click on build number → **Console Output**

### Check Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f ml-predictor
```

### Health Checks
```bash
# Check all services
curl http://localhost:8085/actuator/health    # API Gateway
curl http://localhost:5000/api/v1/health      # DeID
curl http://localhost:5001/api/v1/health      # Featurizer
curl http://localhost:5002/api/v1/health      # ML Predictor
curl http://localhost:5003/health             # Score API
curl http://localhost:5004/api/v1/health      # Audit Fairness
```

---

## ⚠️ Troubleshooting

### Build fails with "Docker command not found"
**Solution**: Add Jenkins user to docker group
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Webhook not triggering builds
**Solution**: 
1. Check webhook delivery in GitHub (Settings → Webhooks → Recent Deliveries)
2. Ensure Jenkins URL is accessible from GitHub
3. Verify webhook URL ends with `/github-webhook/`

### Maven build fails
**Solution**: Configure Java in Jenkins
1. Manage Jenkins → Global Tool Configuration
2. Add JDK 17

---

## 📚 Next Steps

- Read the full [jenkins-setup-guide.md](./jenkins-setup-guide.md) for advanced configuration
- Set up Slack/Email notifications
- Add integration tests
- Configure staging environment

---

**Quick Reference Card**

| Component | URL | Purpose |
|-----------|-----|---------|
| Jenkins | http://localhost:8080 | CI/CD Server |
| Dashboard | http://localhost:3002 | Web UI |
| API Gateway | http://localhost:8085 | Backend API |
| Docker Hub | hub.docker.com/u/taoufikjeta | Image Registry |
