variable "resource_group_name" {
  type    = string
  default = "cropguard-rg"
}

variable "location" {
  type    = string
  default = "westeurope"
}

variable "admin_username" {
  type    = string
  default = "azureuser"
}

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "db_admin_username" {
  type    = string
  default = "mysqladmin"
}

variable "db_admin_password" {
  type      = string
  sensitive = true
}

variable "allowed_ssh_ip" {
  type    = string
}
