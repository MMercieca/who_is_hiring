# Introduction

Sorting through all of the companies in your network to find out which companies are hiring can take a while.  This is also the kind of research that can be outsourced to an LLM.

That is what this script does.

## Basic usage

To find the openings for a single company:

```
python main.py <Company name>
```

To find the openings for a list of companies from a plain text file:

```
python main.py file <companies.txt>
```

For the `companies.txt`, the file contains no headers and lists one company name per line.

When running in file mode, it's helpful to save the output to a log.  That way the `Info` lines can be removed and a CSV of all of the career pages and openings can be generated.

```
python main.py file <filename.txt> >> <output.log>
cat <output.log> | grep -v Info >> output.csv
```

## Requirements

I developed this with Python 3.13. Older versions should work, but I haven't tested them.

Dependencies can be installed with:

```
pip install -r requirements.txt
```

You will also need an [OpenAI API](https://platform.openai.com) key. You can obtain one by:

1. Signing up for hte [OpenAI platform](https://auth.openai.com/create-account)
2. Go to Settings -> Billings
3. Add a credit card and purchase some credits.

### Optional - Enable Google Fallback

If OpenAI can't find the career page, you can optionally have the script search Google for it.

Google isn't enabled by default for two reasons:

1. It's an extra service to set up
2. It costs more than OpenAI, at least right now.

To enable Google fallback, you need a Google API key and a search engine ID (CX ID) from the [Google cloud console](https://cloud.google.com/cloud-console).

To get an API key:

1. Go to the [Google cloud console](https://cloud.google.com/cloud-console)
2. [Set up a new project](https://console.cloud.google.com/projectcreate)
3. Back under APIs and Services, go to Credentials.
4. Click Create credentials (located at the top) and generate a new API key.
5. Copy the API key into the `config.py`

To generate the CX ID, 

1. Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)
2. Click Get Started
3. Give the engine a name and make sure "Search the entire web" is enabled.
4. Create the custom search engine.
5. Copy the CX ID and place it in the `config.py`

Google search fallback is now enabled.