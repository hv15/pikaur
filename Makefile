# This file is licensed under GPLv3, see https://www.gnu.org/licenses/

LANGS := fr ru pt de is tr da nl es

LOCALEDIR := locale
POTFILE := $(LOCALEDIR)/pikaur.pot
POFILES := $(addprefix $(LOCALEDIR)/,$(addsuffix .po,$(LANGS)))
POTEMPFILES := $(addprefix $(LOCALEDIR)/,$(addsuffix .po~,$(LANGS)))
MOFILES = $(POFILES:.po=.mo)

MAN_FILE := pikaur.1
MD_MAN_FILE := $(MAN_FILE).md
MANFILES := $(MAN_FILE) $(MD_MAN_FILE)

all: locale man

locale: $(MOFILES)

$(POTFILE):
	find pikaur -type f -name '*.py' -not -name 'argparse.py' \
		| xargs xgettext --language=python --add-comments --sort-output \
			--default-domain=pikaur --from-code=UTF-8 --keyword='_n:1,2' --output=$@

$(LOCALEDIR)/%.po: $(POTFILE)
	test -f $@ || msginit --locale=$* --no-translator --input=$< --output=$@
	msgmerge --update $@ $<

%.mo: %.po
	msgfmt -o $@ $<

clean_man:
	$(RM) $(MANFILES)

clean: clean_man
	$(RM) $(LANGS_MO)
	$(RM) $(POTEMPFILES)

man: clean_man
	cp README.md $(MD_MAN_FILE)
	sed -i -e 's/^##### /### /g' -e 's/^#### /### /g' $(MD_MAN_FILE)
	ronn $(MD_MAN_FILE) --manual="Pikaur manual" -r
	sed -i -e '/travis/d' -e '/Screenshot/d' $(MAN_FILE)

.PHONY: all clean $(POTFILE)
.PRECIOUS: $(LOCALEDIR)/%.po
