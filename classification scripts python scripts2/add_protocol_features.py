import librosa
import numpy as np

def protocol_features(y, sr):

    rms = librosa.feature.rms(
        y=y
    )

    spl = 20 * np.log10(
        np.maximum(
            np.abs(y).mean(),
            1e-10
        )
    )

    spectral = np.abs(
        librosa.stft(y)
    )

    band_energy = np.mean(
        spectral
    )

    entropy = -np.sum(
        (spectral / spectral.sum())
        *
        np.log2(
            spectral / spectral.sum()
            + 1e-12
        )
    )

    bursts = np.sum(
        np.abs(y)
        >
        3*np.std(y)
    )

    return {
        "spl": spl,
        "band_energy": band_energy,
        "spectral_entropy": entropy,
        "burst_count": bursts,
        "rms": np.mean(rms)
    }
