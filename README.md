# OIDC GitHub Action for Creating a Test ECS Cluster and ECR
This README provides detailed instructions on using the OIDC (OpenID Connect) GitHub Action to create and manage a test Amazon Elastic Container Service (ECS) cluster. This action allows for seamless integration and deployment of containerized applications to AWS ECS using GitHub workflows.

## Prerequisites
Before using this GitHub Action, ensure you have the following:

- An AWS account with appropriate permissions to create and manage ECS clusters.
- A GitHub repository where the workflow will be configured.
- Basic understanding of GitHub Actions, AWS ECS, and Docker.



# Steps and how the OIDC works 
- Register Github as an Identity Provider (OIDC)
- Action requests to generate signed JWT 
- Issues a signed JWT
- Action sends JWT requested role ARN to AWS 
- Validate JWT, Verify that the token is allowed to assume the requested role, and Send a short-lived access token in exchange

# The Github Action pipeline does the following 
- Create a naked test ECS Cluster
- Create an AWS ECR Repository leveraging your GitHub username
