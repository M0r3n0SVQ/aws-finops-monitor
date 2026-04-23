output "lambda_function_name" {
  value = aws_lambda_function.finops_monitor.function_name
}

output "eventbridge_schedule" {
  value = aws_scheduler_schedule.finops_diario.name
}