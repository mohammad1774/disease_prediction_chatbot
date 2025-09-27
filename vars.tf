output "acr_login_server" {
  value = azurerm_container_registry.prediction-acr.login_server
}
output "acr_admin_username" {
  value = azurerm_container_registry.prediction-acr.admin_username
}

output "acr_admin_password" {
  value     = azurerm_container_registry.prediction-acr.admin_password
  sensitive = true
}

output "aks_kube_config" {
  value     = azurerm_kubernetes_cluster.prediction-aks.kube_config_raw
  sensitive = true
}

