
PLUGINS=arxiv ieeexplore mathscinet zentralblatt

.PHONY: clean install all test

clean:
	for plg in $(PLUGINS); do cd $$plg; make clean; cd ..; done

all:
	for plg in $(PLUGINS); do cd $$plg; make zip; cd ..;done

links: linknetbib
	for plg in $(PLUGINS); \
	do \
		rm $$plg/src/mysource.py $$plg/src/tags.py; \
		ln libs/mysource.py $$plg/src/mysource.py; \
		ln libs/tags.py $$plg/src/tags.py; \
	done

ifeq ($(OS),Windows_NT)
linknetbib:
	for iplg in $(PLUGINS); \
	do \
		rm $$iplg/src/netbib; \
		cmd //c mklink //D "$$iplg\src\netbib" "libs\netbib"; \
	done

else
linknetbib:
	for iplg in $(PLUGINS); \
	do \
		rm $$iplg/src/netbib; \
		ln -s libs/netbib $$iplg/src/netbib; \
	done
endif

install:
	for plg in $(PLUGINS); do cd $$plg; make install; cd ..; done

uninstall:
	for plg in $(PLUGINS); do cd $$plg; make uninstall; cd ..; done

test:
	for plg in $(PLUGINS); do cd $$plg; make test; cd ..; done

run:
	calibre-debug -g

kill:
	calibre -s

