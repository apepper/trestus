# Howto Package for Lambda

Create a folder for the lambda package.

If using Mac OS X and you have Python installed using Homebrew (see [Homebrew](http://brew.sh/)), add a `setup.cfg` file in your `/path/to/lambda-packaging` with the following content. Alternatively put a `.pydistutils.cfg` with the same contents in your `HOME_DIR`.

```
[install]
prefix=
```

Install modules into package folder

```
pip install trestus -t /path/to/lambda-packaging
```

Copy the adjusted files
* `trestus/templates/scrivito.html` into the folder `/path/to/lambda-packaging/trestus/templates/`,
* `trestus/templates/trestus.css` into the folder `/path/to/lambda-packaging/trestus/templates/`,
* `trestus/__init__.py` into the folder `/path/to/lambda-packaging/trestus/`
* `robots.txt` into the folder `/path/to/lambda-packaging/` and
* `calltrestus.py` into the folder `/path/to/lambda-packaging/`.

Change into the package folder and create a zip file containing all contents of the folder

```
zip -r /tmp/calltrestus.zip *
```

Upload that zip file into the lambda function.

## Configuration:

Handler: `calltrestus.calltrestus_handler`

## Environment variables

* `API_KEY`: your encrypted trello API key (with enabled encryption helpers)
  [Get your Trello Application Key](https://trello.com/app-key) (Key)
* `BOARD_ID`: the ID of the board that is the source of your status page
* `BUCKET_NAME`: name of the s3 bucket to host the status page (`dev-scrvt-status.infopark.io`)
* `CUSTOM_TEMPLATE`: path to the custom template you want to use generating the status page  (`templates/scrivito.html`)
* `OUTPUT_PATH`: path to the generated file  (needs to be something in `/tmp` for Lambda since that is the only writable file system in that environment, e.g. `/tmp/index.html`)
* `TOKEN`: your encrypted Trello token (with enabled encryption helpers)
  You have to generate a token for your API key using the link in that app-key page mentioned above, but change the scope to `read` (from `read,write,account`)

# Local Development

For local development :

* Define the following [environment variables](#environment-variables)
* In `calltrestus.py`:
  * uncomment the lines defining `API_KEY` and `TOKEN` from environment
  * comment out the lines defining defining `ENCRYPTED_API_KEY`, `API_KEY`, `ENCRYPTED_TOKEN` and `TOKEN` from `kms`
* Call `python calltrestus.py` to generate the status page from the Trello board and upload the results to S3
* Call `python trestus/__init__.py --board-id $BOARD_ID --key $API_KEY --token $TOKEN --custom-template $CUSTOM_TEMPLATE $OUTPUT_PATH` to only generate the status page from the Trello board
