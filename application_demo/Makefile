# $@	Le nom de la cible
# $<	Le nom de la première dépendance
# $^	La liste des dépendances
# $?	La liste des dépendances plus récentes que la cible
# $*	Le nom du fichier sans suffixe

CC=
CFLAGS=
LDFLAGS=
EXEC=

clean:
	@rm -rf *.pyc *~

mrproper: 
	@find . -name "*.pyc" -exec rm -f {} \; -o -name "*~" -exec rm -f {} \;
