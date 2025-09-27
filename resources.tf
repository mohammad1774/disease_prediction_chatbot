
provider "azurerm" {
  features {}
}

#Resource Group
resource "azurerm_resource_group" "prediction-rg" {
  name = "disease-prediction-rg"
  location = "canadacentral"
}

#Azure Container Registry
resource "azurerm_container_registry" "prediction-acr" {
  name = "mohammadacr1774"
  resource_group_name = azurerm_resource_group.prediction-rg.name
  location = azurerm_resource_group.prediction-rg.location
  sku = "Basic"
  admin_enabled = true
}

#Azure Kubernetes Cluster 
resource "azurerm_kubernetes_cluster" "prediction-aks" {
  name = "prediction-aks"
  location = azurerm_resource_group.prediction-rg.location
  resource_group_name = azurerm_container_registry.prediction-acr.name
  dns_prefix = "predictionaks"

  default_node_pool {
    name = "default"
    node_count = 2
    vm_size = "Standard_DS2_V2"
  }

  identity {
    type = "SystemAssigned"
  }
}


#Azure k8s pull access 
resource "azurerm_role_assignment" "aks_acr_pull" {
  principal_id = azurerm_kubernetes_cluster.prediction-aks.kubelet_identity[0].object_id
  role_definition_id = "AcrPull"
  scope = azurerm_container_registry.prediction-acr.id
}



