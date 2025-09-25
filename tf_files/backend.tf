terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "tfstateprodtest1"
    container_name       = "tfstate"
    key                  = "infra.tfstate"
  }
}