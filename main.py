from typing import Optional, Any
from pathlib import Path
import argparse
import requests

import yaml
import replicate
from tqdm import tqdm


LYRIC_VALUES_REPO="eldrin/text-concept-similarity:24412301b8a071cd50094d9554e0a5716cb337205bf680f99c5e95669bd7d796"


def run(
    config: dict[str, Any],
    out_path: Path,
    out_fn: str = 'output.csv'
) -> Optional[str]:
    """
    """
    n_cases = (
        len(config['options']['normalization']) * 
        len(config['options']['word_embs'])
    )
    lyrics_file = Path(config['data']['input'])
    with tqdm(total=n_cases, ncols=80) as prog:
        for emb in config['options']['word_embs']:
            for norm in config['options']['normalization']:

                # make output path
                out_path_ = out_path / emb / norm
                if not out_path_.exists():
                    out_path_.mkdir(parents=True, exist_ok=True)

                # run and fetch
                output = None
                try:
                    output = replicate.run(
                        LYRIC_VALUES_REPO,
                        input={
                            "text": lyrics_file.open('r'),
                            "alpha": 0.5,
                            "apply_idf": True,
                            "word_embs": emb,
                            "normalization": norm
                        }
                    )
                    assert output is not None, \
                            f"[ERROR] we found empty return from "\
                            f"replicate repo! ({norm}, {emb})"

                    # save 
                    save_output(output,
                                out_path_ / out_fn)

                except Exception as e:
                    print(e)

                prog.update()


def save_output(
    uri: str,
    out_path: Path
) -> None:
    """
    """
    if uri is not None:
        r = requests.get(uri)
        if r.ok:
            with out_path.open('w') as f:
                f.write(r.text)
        else:
            raise ValueError('[ERROR] Could not fetch result from server!')


def parse_arguments():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str,
                        help="the configuration file to fetch results \
                                from replicate lyrics value repo")
    return parser.parse_args()


def main():
    """
    """
    args = parse_arguments()

    # load configuration
    with Path(args.config).open('r') as fp:
        config = yaml.safe_load(fp)

    # setup output path
    out_path = Path(config['data']['output_path'])
    input_stem = Path(config['data']['input']).stem
    out_fn = f'{input_stem}_value_scores.csv'
     
    # we loop through all the params
    run(config, out_path, out_fn) 


if __name__ == "__main__":
    main()
