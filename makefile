
NAME = tnotes
CWD = $(shell pwd)

install:
	@ln -sf $(CWD)/tnotes /usr/local/bin/tnotes
	@echo "created symlink: /usr/local/bin/tnotes"

