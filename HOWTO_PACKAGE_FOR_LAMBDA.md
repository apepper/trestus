# Howto Package for Lambda

You need Python 2 installed. On Mac OS X we recommend Homebrew (see [Homebrew](http://brew.sh/)) for this (e.g. `brew install python`).

Once Python is installed call the following shell script, to build the lambda function:

```
./build_lambda_package.sh
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
