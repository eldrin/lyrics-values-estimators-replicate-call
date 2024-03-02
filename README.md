# Lyrics Value Estimators Replicate API Caller

it calls the [lyrics value estimation](https://replicate.com/eldrin/text-concept-similarity) via python API of [Replicate](https://replicate.com/).


## Installation

```bash
git clone https://github.com/eldrin/lyrics-values-estimators-replicate-call.git
cd lyrics-values-estimators-replicate-call
python3 -m venv lyric_value_replicate_call
source lyric_value_replicate_call/bin/activate
python -m pip install -r requirements.txt
```


## How to use

We need to authenticate to run the repo with API calls. Grab your token from [replicate.com/account](https://replicate.com/account) and set it as an env variable before running the program.

```bash
# we assume we are under the repo root
export REPLICATE_API_TOKEN=xxxx
python main.py config_example.yml
```


## Note

Currently, the script only loop through the permutation of `normalization` and `word_embs` options. It is possible to extend it to any of other parameters (i.e., `alpha`, `apply_idf`, etc.) too. It might be added in the future upon feature request.

Also, **input text should not include comma**. This is a known issue, and will be fixed in the next update.

## How to improve it

We are more than welcome for any issue report and/or pull-requests.


## Contributers

Jaehun Kim


## References

```
TBD
```
