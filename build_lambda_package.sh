#!/bin/sh

cd lambda-packaging/
git clean -f -d
pip install trestus -t .
cp ../trestus/templates/scrivito.html trestus/templates
cp ../trestus/templates/trestus.css trestus/templates
cp ../trestus/__init__.py trestus/
cp ../calltrestus.py .
zip -r /tmp/calltrestus.zip *

echo ""
echo "/tmp/calltrestus.zip is now ready to be uploaded to AWS lambda!"
