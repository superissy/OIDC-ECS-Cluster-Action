output "name" {
  value = aws_ecs_cluster.owasp-juice-shop.name 
}

output "id" {
  value = aws_ecs_cluster.owasp-juice-shop.id
}

output "name" {
  value = aws_ecs_service.owasp-juice-shop-service.name
}

output "id" {
  value = aws_ecs_service.owasp-juice-shop-service.id
}

output "name" {
  value = aws_ecs_task_definition.owasp_juice_shop_task.name
}

output "id" {
  value = aws_ecs_task_definition.owasp_juice_shop_task.id
}