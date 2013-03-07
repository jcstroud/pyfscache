include PackageInfo.cfg
include Makefile.inc

RELEASE = $(MAJOR).$(MINOR).$(MICRO)$(TAG)
BUNDLE = $(PACKAGE)-$(RELEASE)
DOCZIP = $(BUNDLE)-docs.zip
DOCPDF = $(PACKAGE).pdf

VERMODULE = $(PACKAGE)/_version.py

DOCS = LICENSE.txt html
PRODUCTS = $(VERMODULE) $(DOCS)

all : sdist

LICENSE.txt :
	$(PYTHON) -c 'exec("import configobj; \
                            p = configobj.ConfigObj(\"PackageInfo.cfg\", \
                                                    list_values=False); \
                            t = open(\"$(LICENSE_TEMPLATE)\").read(); \
                            s = t % p; \
                            open(\"LICENSE.txt\", \"w\").write(s)")'

$(VERMODULE) : scrub
	$(ECHO) '__version__ = "$(RELEASE)"' > $(VERMODULE)

html : $(VERMODULE)
	cd $(DOCDIR) ; rm -rf _build/html ; make html
	mv $(DOCDIR)/_build/html $(HTMLDIR)

$(DOCZIP) : html
	-rm -f $(DOCZIP)
	cd $(HTMLDIR) ; zip -ry $(CURDIR)/$(DOCZIP) *
	mv $(DOCZIP) $(DOCDEST)

pdf : $(VERMODULE)
	cd $(DOCDIR) ; rm -rf _build/latex ; make latexpdf
	mv $(DOCDIR)/_build/latex/$(PACKAGE).pdf $(DOCDEST)/$(DOCPDF)

sdist : $(PRODUCTS)
	-rm dist/$(BUNDLE).tar.gz
	$(PYTHON) setup.py sdist

install : all
	$(PYTHON) setup.py install

build : all
	$(PYTHON) setup.py build

pypi-build-docs : $(DOCZIP)

pypi-upload-docs : html
	python setup.py upload_docs

pypi-upload : all pypi-upload-docs
	$(PYTHON) setup.py sdist upload

test : clean $(VERMODULE)
	$(PYTHON) setup.py test

clean :
	$(ECHO) Cleaning up in `pwd`.
	-rm -rf $(DOCS)
	-rm -rf $(DOCPDF)
	cd $(DOCDIR) ; make clean

prune :
	$(PYTHON) -c 'exec("import phyles; \
                            import logging; \
               logging.basicConfig(level=logging.INFO); \
               phyles.prune([\"*~\", \"*.pyc\", \".*~\"], \
                            doit=True)")'

scrub : clean prune
	-rm -rf dist/ build/ $(PACKAGE).egg-info/
