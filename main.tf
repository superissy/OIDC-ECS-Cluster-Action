resource "aws_ecs_cluster" "owasp-juice-shop" {
    name = "owasp-juice-shop"
  
}

resource "aws_ecs_task_definition" "owasp_juice_shop_task" {
  family                   = "test"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  container_definitions    = <<TASK_DEFINITION
[
  {
    "name": "iis",
    "image": ${var.image_name},
    "cpu": 1024,
    "memory": 2048,
    "essential": true
  }
]
TASK_DEFINITION
}

data "aws_iam_role" "ecs-service-role" {
    name = "ecsServiceRole"
}

resource "aws_ecs_service" "owasp-juice-shop-service" {
    name = "owasp-juice-shop-service"
    cluster = aws_ecs_cluster.owasp-juice-shop.id
    task_definition = aws_ecs_task_definition.owasp-juice-shop-task.arn
    desired_count = 1
    iam_role = data.aws_iam_role.ecs-service-role.arn
    depends_on = [aws_iam_role_policy.ecs-service-policy]
    load_balancer {
        target_group_arn = aws_lb_target_group.owasp-juice-shop-tg.arn
        container_name = "owasp-juice-shop"
        container_port = 3000
    }
}