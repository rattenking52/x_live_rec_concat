#!/usr/bin/python3

import argparse
import logging
import sys
from pathlib import Path
from typing import List

import soundfile as sf

logger = logging.getLogger(__name__)

OUTPUT_FILE_NAME = "output.wav"
X_LIVE_RECORDING_FILE_PATTERN = "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] [0-9][0-9].[0-9][0-9].[0-9][0-9].WAV"


def concatenate_wav_files(input_file_paths: List[Path], output_file_path: Path) -> None:
    with sf.SoundFile(input_file_paths[0], 'r') as meta_file:
        if meta_file.subtype != "PCM_32":
            raise NotImplementedError
        else:
            dtype = "int32"

        with sf.SoundFile(output_file_path, 'w', meta_file.samplerate, meta_file.channels, meta_file.subtype,
                          meta_file.endian, "RF64") as output_file:
            for i, input_file_path in enumerate(input_file_paths):
                logger.info(f"Processing file {i + 1}/{len(input_file_paths)} ...")
                with sf.SoundFile(input_file_path, 'r') as input_file:
                    output_file.buffer_write(input_file.buffer_read(dtype=dtype), dtype=dtype)


def parse_args():
    parser = argparse.ArgumentParser(
        description='This script concatenates .wav files produced by a recording done with the X-LIVE.')
    parser.add_argument("input_folder_path", type=Path, help="Input folder path")

    args = parser.parse_args()

    input_folder_path = args.input_folder_path.expanduser().resolve()

    if not input_folder_path.is_dir():
        logger.error(f'Input folder path "{input_folder_path}" is not a directory')
        sys.exit()

    logger.info(f"Input folder path: {input_folder_path}")

    wav_file_paths = sorted(input_folder_path.glob(X_LIVE_RECORDING_FILE_PATTERN))

    if len(wav_file_paths) < 2:
        logger.error("Input folder path does not contain at least two .WAV files")
        sys.exit()

    for wav_file_path in wav_file_paths:
        logger.info(f"Found file: {wav_file_path}")

    output_file_path = input_folder_path / "output.wav"

    if output_file_path.is_file():
        logger.warning(f'Output file "{output_file_path}" will be overwritten')
    else:
        logger.info(f"Output file path: {output_file_path}")

    return wav_file_paths, output_file_path


def main():
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    concatenate_wav_files(*parse_args())
    logger.info(f"Finished successfully")


if __name__ == "__main__":
    main()
