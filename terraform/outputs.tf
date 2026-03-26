output "bastion_public_ip" {
  description = "Public IP of the bastion host"
  value       = azurerm_public_ip.bastion.ip_address
}

output "app_vm_private_ip" {
  description = "Private IP of the app VM"
  value       = azurerm_network_interface.app.private_ip_address
}

output "acr_login_server" {
  description = "ACR login server URL"
  value       = azurerm_container_registry.main.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.main.admin_username
}

output "mysql_host" {
  description = "MySQL server hostname"
  value       = azurerm_mysql_flexible_server.main.fqdn
}