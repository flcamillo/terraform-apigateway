# define a configuração das instancias do DocumentDB
resource "aws_docdb_cluster_instance" "instances" {
  count              = 1
  identifier         = "${var.db_cluster}-${count.index}"
  cluster_identifier = aws_docdb_cluster.cluster.id
  instance_class     = var.db_cluster_instance
}

# define a configuração do cluster do DocumentDB
resource "aws_docdb_cluster" "cluster" {
  cluster_identifier      = var.db_cluster
  availability_zones      = ["sa-east-1a", "sa-east-1b", "sa-east-1c"]
  master_username         = var.db_user
  master_password         = random_password.dbpassword.result
  backup_retention_period = 2
  preferred_backup_window = "01:00-05:00"
  skip_final_snapshot     = true
  engine_version          = "4.0.0"
}
