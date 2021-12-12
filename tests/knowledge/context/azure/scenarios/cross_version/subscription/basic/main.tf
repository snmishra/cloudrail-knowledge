locals {
  resource_prefix = "cr3703"

  # Parameters for a new subscription
  billing_account_name    = "doron" # Complete this
  enrollment_account_name = "doron" # Complete this
}

data "azurerm_billing_enrollment_account_scope" "test" {
  count                   = local.billing_account_name == "fake" ? 0 : 1
  billing_account_name    = local.billing_account_name
  enrollment_account_name = local.enrollment_account_name
}

resource "azurerm_subscription" "test" {
  count             = local.billing_account_name == "fake" ? 0 : 1
  subscription_name = "dev_alon"
  alias             = "${local.resource_prefix}-subscription-alias"
  billing_scope_id  = data.azurerm_billing_enrollment_account_scope.test.0.id
  workload          = "Production"
}
