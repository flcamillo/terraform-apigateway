variable "lambda_role_name" {
  type        = string
  description = "Nome da role para a lambda"
  default     = "role-lambda-api-user"
}

variable "lambda_policy_name" {
  type        = string
  description = "Nome da policy para a lambda"
  default     = "policy-lambda-api-user"
}

variable "lambda_name" {
  type        = string
  description = "Nome da lambda que vai processar os metodos do API Gateway"
  default     = "api-user"
}

variable "api_gateway_role_name" {
  type        = string
  description = "Nome da role para o api gateway"
  default     = "role-api-gateway-auth"
}

variable "api_gateway_policy_name" {
  type        = string
  description = "Nome da policy para o api gateway"
  default     = "policy-api-gateway-auth"
}

variable "apigateway_name" {
  type        = string
  description = "Nome do API Gateway"
  default     = "auth"
}

variable "lambda_root" {
  type        = string
  description = "Caminho para a pasta onde está todo o conteúdo da lambda"
  default     = "../lambda"
}

variable "swagger_root" {
  type        = string
  description = "Caminho para a pasta onde está o swagger do api gateway"
  default     = "../swagger"
}

variable "db_secret" {
  type        = string
  description = "Nome do segredo que contem o usuário e senha do banco de dados"
  default     = "docdb-user1"
}

variable "db_user" {
  type        = string
  description = "Nome do usuário root do banco de dados"
  default     = "root"
}

variable "db_name" {
  type        = string
  description = "Nome do banco de dados"
  default     = "auth"
}

variable "db_cluster" {
  type        = string
  description = "Nome do cluster do DocumentDB"
  default     = "cluster-auth"
}

variable "db_cluster_instance" {
  type        = string
  description = "Tipo de instâncias do cluster do DocumentDB"
  default     = "db.r6g.large"
}

variable "lambda_vpc_subnet" {
  type        = list(string)
  description = "Lista de identificação de subnets para a lambda poder usar a VPC"
  default     = ["subnet-7beb561d", "subnet-04f5464d", "subnet-6377cf38"]
}

variable "lambda_vpc_sg" {
  type        = list(string)
  description = "Identificação do grupo de segurança da lambda"
  default     = ["sg-9539bae9"]
}
