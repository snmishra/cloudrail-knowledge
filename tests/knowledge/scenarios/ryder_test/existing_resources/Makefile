.PHONY: apply
apply:
	@AWS_PROFILE=indeni terraform apply --auto-approve

.PHONY: init
init:
	@AWS_PROFILE=indeni terraform init

.PHONY: test
test:
	@cloudrail run --auto-approve

.PHONY: destroy
destroy:
	@AWS_PROFILE=indeni terraform destroy
