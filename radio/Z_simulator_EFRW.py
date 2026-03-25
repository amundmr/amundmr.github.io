import numpy as np
import matplotlib.pyplot as plt

def calculate_impedance(f_MHz, length_m):
    """
    Approximates the feedpoint impedance of an end-fed wire.
    Uses a lossy transmission line model.
    """
    c = 299.792  # Speed of light in Mm/s
    wavelength = c / f_MHz
    beta = 2 * np.pi / wavelength
    
    # Antenna approximation parameters
    Z0 = 500  # Characteristic impedance of the wire in free space
    alpha = 0.015 + (0.001 * f_MHz) 
    
    prop_gamma = alpha + 1j * beta
    
    # Impedance of an open-ended transmission line
    Z_ant = Z0 / np.tanh(prop_gamma * length_m)
    return Z_ant

def score_length(length_m, ham_bands, target_ohm=450, n_samples=10):
    """
    Score how close a wire length stays to target_ohm across all ham bands.
    Per-band score: 1.0 = perfect match, approaches 0 as |Z| diverges (log scale).
    Returns overall score (0–1) and per-band breakdown.
    """
    band_scores = {}
    for band, (f_min, f_max) in ham_bands.items():
        freqs = np.linspace(f_min, f_max, n_samples)
        Z = calculate_impedance(freqs, length_m)
        avg_Z = np.mean(np.abs(Z))
        # Log-ratio penalty: 0 = perfect, grows with deviation
        log_error = abs(np.log(avg_Z / target_ohm))
        band_scores[band] = round(1.0 / (1.0 + log_error), 3)
    overall = round(np.mean(list(band_scores.values())), 3)
    return overall, band_scores


def main():
    # Frequency range: 1.5 MHz to 30 MHz (covering 160m to 10m)
    frequencies = np.linspace(1.5, 30.0, 1000)

    # Wire lengths to test (in meters)
    lengths_to_test = [8.84, 12.5, 21.64, 25.6]
    lengths_to_test = [40, 25.6]

    plt.figure(figsize=(12, 6))
    
    # Plot Impedance Magnitude for each length
    for length in lengths_to_test:
        Z_ant = calculate_impedance(frequencies, length)
        # We plot the absolute magnitude of the complex impedance |Z|
        plt.plot(frequencies, np.abs(Z_ant), label=f'{length}m ({length * 3.28084:.1f} ft)', linewidth=2)

    # --- Highlight Ham Bands ---
    ham_bands = {
        '160m': (1.8, 2.0),
        '80m': (3.5, 4.0),
        '60m': (5.33, 5.40),
        '40m': (7.0, 7.3),
        '30m': (10.1, 10.15),
        '20m': (14.0, 14.35),
        '17m': (18.068, 18.168),
        '15m': (21.0, 21.45),
        '12m': (24.89, 24.99),
        '10m': (28.0, 29.7)
    }

    # --- Score each length vs 450 Ω target across all ham bands ---
    band_names = list(ham_bands.keys())
    print(f"\n{'Length':<10} {'Score':>7}  " + "  ".join(f"{b:>6}" for b in band_names))
    print("-" * (10 + 9 + 9 * len(band_names)))
    for length in lengths_to_test:
        overall, band_scores = score_length(length, ham_bands)
        band_vals = "  ".join(f"{band_scores[b]:>6.3f}" for b in band_names)
        print(f"{length:<10} {overall:>7.3f}  {band_vals}")
    print()

    for band, (f_min, f_max) in ham_bands.items():
        plt.axvspan(f_min, f_max, color='gray', alpha=0.2)
        # Add label for the band near the top of the plot
        plt.text(f_min + (f_max - f_min)/2, 6000, band, 
                 horizontalalignment='center', verticalalignment='top', 
                 rotation=90, fontsize=8, alpha=0.7)

    # Chart formatting
    plt.title('Approximated Feedpoint Impedance (|Z|) of End-Fed Wires', fontsize=14)
    plt.xlabel('Frequency (MHz)', fontsize=12)
    plt.ylabel('Impedance Magnitude (Ohms) - Log Scale', fontsize=12)
    
    # Using a log scale because impedance swings from ~50 to ~5000+ ohms
    plt.yscale('log')
    plt.ylim(30, 10000)
    plt.xlim(1.5, 30)
    
    # Helpful reference lines
    plt.axhline(y=50, color='r', linestyle='--', alpha=0.5, label='50 Ω (Direct Radio Feed)')
    plt.axhline(y=450, color='g', linestyle='--', alpha=0.5, label='450 Ω (9:1 UNUN Target)')
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='lower right')
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    main()