output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "aks_cluster" {
  value = azurerm_kubernetes_cluster.aks.name
}