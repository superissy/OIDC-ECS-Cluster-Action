provider "aws" {
  region = "us-east-1"

}

terraform {
  backend "s3" {
    bucket = "xsave-oidc-statefile"
    key    = "tfstate"
    region = "us-east-1"
    
  }
}