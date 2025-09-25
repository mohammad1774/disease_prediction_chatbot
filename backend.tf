terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "tfstateprodtest1"
    container_name       = "tfstate"
    key                  = "infra.tfstate"
  }

  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}
  provider "azurerm" {
    features {}
  }
