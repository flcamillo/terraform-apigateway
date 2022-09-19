# gera uma senha aleatória
resource "random_password" "dbpassword" {
  length           = 16
  special          = false
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# define o segredo que será guardado
resource "aws_secretsmanager_secret_version" "dbuserpassword" {
  secret_id     = aws_secretsmanager_secret.dbuser.id
  secret_string = jsonencode({ "user" : var.db_user, "password" : random_password.dbpassword.result })
}

# define o secretmanager para guardar o segredo
resource "aws_secretsmanager_secret" "dbuser" {
  name = var.db_secret
}
