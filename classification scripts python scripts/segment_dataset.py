import os
import soundfile as sf

INPUT_ROOT = os.path.expanduser(
    "~/feeding_dataset"
)

OUTPUT_BASE = (
    "/media/feliciano/Aux/AI_AFS_DATASET"
)

SEGMENTS = [1]

CLASSES = [
    "Class_0_Background",
    "Class_1_PreFeeding",
    "Class_2_Feeding",
    "Class_3_PostFeeding"
]

for seg_len in SEGMENTS:

    output_root = os.path.join(
        OUTPUT_BASE,
        f"feeding_dataset_{seg_len}s"
    )

    for cls in CLASSES:

        os.makedirs(
            os.path.join(
                output_root,
                cls
            ),
            exist_ok=True
        )

for cls in CLASSES:

    source_dir = os.path.join(
        INPUT_ROOT,
        cls
    )

    wavs = [
        f for f in os.listdir(source_dir)
        if f.lower().endswith(".wav")
    ]

    print(
        f"\nProcessing {cls}: {len(wavs)} files"
    )

    for wav in wavs:

        wav_path = os.path.join(
            source_dir,
            wav
        )

        try:

            audio, sr = sf.read(
                wav_path
            )

            if audio.ndim > 1:
                audio = audio.mean(axis=1)

            basename = os.path.splitext(
                wav
            )[0]

            for seg_len in SEGMENTS:

                output_root = os.path.join(
                    OUTPUT_BASE,
                    f"feeding_dataset_{seg_len}s",
                    cls
                )

                samples = (
                    seg_len * sr
                )

                n_segments = (
                    len(audio) // samples
                )

                for i in range(
                    n_segments
                ):

                    segment = audio[
                        i*samples:
                        (i+1)*samples
                    ]

                    outfile = os.path.join(
                        output_root,
                        f"{basename}_seg{i:05d}.wav"
                    )

                    if os.path.exists(
                        outfile
                    ):
                        continue

                    sf.write(
                        outfile,
                        segment,
                        sr
                    )

        except Exception as e:

            print(
                "FAILED:",
                wav,
                e
            )

print("\nDONE")
