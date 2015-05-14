# to create new translations, run something like
# pybabel init -i messages.pot -d ../../frontend/translations -l fr
# and change 'fr' to whatever you need.

pybabel extract -F babel.cfg -k ___ -o messages.pot ../../