# Setting Up a Scalable Application in AWS

## Big Picture: Architecture Diagram

### High-Level Components
Below is a high-level architecture of the scalable system in AWS:

```plaintext
                                +--------------------------+
                                |     Users/Clients        |
                                +-----------+--------------+
                                            |
                                            ▼
                        +-------------------+------------------+
                        |   Application Load Balancer (ALB)    |
                        +-------------------+------------------+
                                            |
                   +------------------------+------------------------+
                   |                                                     |
           +-------+-------+                                     +-------+-------+
           |   EKS Cluster  |                                     |  EKS Cluster  |
           |   (Kubernetes) |                                     | (Kubernetes)  |
           | - App Services |                                     | - ML Services |
           | - Vector DB    |                                     | - APIs        |
           +---------------+                                     +---------------+
                   |                                                     |
          +--------+--------+                                  +---------+-------+
          |                 |                                  |                 |
+---------+---------+ +-----+-----+              +-------------+---------+ +-----+-----+
|   Amazon RDS      | |  OpenAI   |              |  Amazon S3             | |   MLflow  |
|   (Postgres)      | |   APIs    |              |  Storage Bucket        | | Tracking  |
+-------------------+ +-----------+              +------------------------+ +-----------+
```

---

## Key AWS Services

### 1. Compute and Orchestration
- **EKS (Elastic Kubernetes Service)**: Hosts your containerized microservices, scalable workloads, and APIs.
- **ECR (Elastic Container Registry)**: Stores Docker images for deployment into EKS.
- **EC2 Auto Scaling Group**: Optional for running services that aren't containerized or for Kubernetes worker nodes.

### 2. Networking
- **ALB (Application Load Balancer)**: Routes traffic from clients to the appropriate services running in EKS.
- **VPC (Virtual Private Cloud)**: Provides a private and secure network for your infrastructure.

### 3. Data Storage
- **Amazon RDS (Relational Database Service)**: Manages your relational database (e.g., PostgreSQL).
- **Amazon S3**: Provides scalable object storage for logs, artifacts, or data used by the app.

### 4. External Services
- **OpenAI**: For LLM and AI service calls.
- **Vector DB**: Use a managed or self-hosted solution (e.g., Pinecone, Weaviate).

### 5. Monitoring and Logging
- **CloudWatch**: Centralized logging and monitoring for application and infrastructure metrics.
- **MLflow**: Tracks machine learning experiments, models, and pipelines (can be hosted in EKS or on EC2).

---

## Step-by-Step Setup

### 1. Networking
- **Set up a VPC**:
  - Use the AWS VPC wizard to create a private network for your app.
  - Include:
    - **Public subnets** for ALB.
    - **Private subnets** for EKS nodes, RDS, and other backend services.
    - **Internet Gateway** for outgoing traffic (e.g., OpenAI API).

```plaintext
VPC:
- Public Subnets: ALB
- Private Subnets: EKS Nodes, RDS, etc.
- Route Table:
  - Public: ALB → Internet Gateway
  - Private: EKS → NAT Gateway → Internet Gateway
```

---

### 2. Compute and Containers

#### **ECR**:
1. Push your Docker images to an ECR repository:
   ```bash
   aws ecr create-repository --repository-name my-app
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t my-app .
   docker tag my-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
   ```

#### **EKS**:
1. Create an EKS cluster:
   ```bash
   eksctl create cluster --name my-cluster --region us-east-1 --nodegroup-name app-nodes
   ```
2. Deploy workloads:
   - Use Kubernetes manifests or Helm charts to deploy services.
   - Example Deployment YAML:
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: app-service
     spec:
       replicas: 3
       selector:
         matchLabels:
           app: my-app
       template:
         metadata:
           labels:
             app: my-app
         spec:
           containers:
           - name: app-container
             image: <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-app:latest
             ports:
             - containerPort: 80
     ```

#### **ALB Integration**:
- Use an ALB ingress controller to route traffic to services:
  ```bash
  kubectl apply -k github.com/aws/eks-charts/alb-ingress-controller
  ```

---

### 3. Storage

#### **Amazon RDS**:
1. Create a Postgres database:
   ```bash
   aws rds create-db-instance --db-instance-identifier my-db --db-instance-class db.t3.medium --engine postgres --allocated-storage 20
   ```
2. Connect your app to RDS using environment variables.

#### **S3**:
- Create an S3 bucket for storage:
  ```bash
  aws s3api create-bucket --bucket my-app-bucket --region us-east-1
  ```

---

### 4. External Services

#### **OpenAI**:
- Store API keys in **AWS Secrets Manager** and access them securely in your app.

#### **Vector DB**:
- Use a managed service (e.g., Pinecone) or deploy a self-hosted vector database (e.g., Weaviate) in EKS.

---

### 5. Monitoring

#### **CloudWatch**:
- Set up logging for EKS workloads:
  ```bash
  aws logs create-log-group --log-group-name /eks/my-app
  ```

#### **MLflow**:
- Deploy MLflow to EKS or host it on an EC2 instance with S3 as the backend for artifacts.

---

## Next Steps

1. **Iterate on Infrastructure**:
   - Deploy incrementally starting with ECR, EKS, and ALB.
2. **Automation**:
   - Use Terraform or AWS CloudFormation to automate infrastructure setup.
3. **CI/CD**:
   - Integrate with AWS CodePipeline for continuous deployment of updates to EKS.

