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