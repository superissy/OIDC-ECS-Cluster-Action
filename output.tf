output "name" {
  value = aws_ecs_cluster.owasp-juice-shop.name
}

output "id" {
  value = aws_ecs_cluster.owasp-juice-shop.id
}

output "arn" {
  value = aws_ecs_task_definition.owasp_juice_shop_task.arn
}
