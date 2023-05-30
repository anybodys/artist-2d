.PHONY : \
	infra-lint \
	infra-format \
	infra-test

infra-lint:
	terraform fmt -recursive -check .

infra-format:
	terraform fmt -recursive .

infra-test:
	cd infra/test && go test -v -timeout 30m
