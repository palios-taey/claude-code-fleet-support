PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
LIBDIR ?= $(PREFIX)/lib/claude-code-fleet-support

.PHONY: install

install:
	install -d "$(BINDIR)"
	install -d "$(LIBDIR)"
	rm -rf "$(LIBDIR)/lib"
	cp -R lib "$(LIBDIR)/lib"
	install -m 755 scripts/cf-support-intake "$(BINDIR)/cf-support-intake"
