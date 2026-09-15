PYTHON ?= python
.PHONY: help install check test verify demo journeys audit-poc audit-iteration2 integrity
help:
	@echo "install, check, test, verify, demo, journeys, audit-poc, audit-iteration2, integrity"
	@echo "Audits are unresolved acceptance requirements and currently exit nonzero."
install:
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PYTHON) -m pip install -e './collector[test]'
check:
	$(PYTHON) tools/workspace.py check
test:
	$(PYTHON) tools/workspace.py test
verify:
	$(PYTHON) tools/workspace.py verify
demo:
	$(PYTHON) tools/workspace.py demo
journeys:
	$(PYTHON) tools/workspace.py journeys
audit-poc:
	$(PYTHON) tools/workspace.py audit poc
audit-iteration2:
	$(PYTHON) tools/workspace.py audit iteration2
integrity:
	$(PYTHON) tools/verify_manifest.py --strict
