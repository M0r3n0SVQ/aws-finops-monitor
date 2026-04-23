variable "region" {
  default = "eu-south-2"
}

variable "telegram_bot_token" {
  description = "Token del bot de Telegram"
  sensitive   = true
}

variable "telegram_chat_id" {
  description = "Chat ID de Telegram"
  sensitive   = true
}

variable "finops_access_key" {
  description = "AWS Access Key para Cost Explorer"
  sensitive   = true
}

variable "finops_secret_key" {
  description = "AWS Secret Key para Cost Explorer"
  sensitive   = true
}