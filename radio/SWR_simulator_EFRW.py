import numpy as np
import matplotlib.pyplot as plt

def calculate_impedance(f_MHz, length_m):
    """
    Approximates the feedpoint impedance of an end-fed wire.
    Uses a lossy transmission line model to simulate the high/low impedance 
    cycles of a wire antenna across frequencies.
    """
    c = 299.792  # Speed of light in Mm/s
    wavelength = c / f_MHz
    beta = 2 * np.pi / wavelength
    
    # Antenna approximation parameters
    Z0 = 500  # Characteristic impedance of the wire in free space
    # The alpha factor simulates radiation resistance/loss. 
    # It increases slightly with frequency.
    alpha = 0.015 + (0.001 * f_MHz) 
    
    prop_gamma = alpha + 1j * beta
    
    # Impedance of an open-ended transmission line: Z = Z0 * coth(gamma * L)
    # Since numpy doesn't have coth, we use 1/tanh
    Z_ant = Z0 / np.tanh(prop_gamma * length_m)
    return Z_ant

def calculate_swr(Z_ant, Z_system=450):
    """
    Calculates SWR. Default Z_system is 450 ohms, simulating a 50-ohm 
    transceiver looking through a 9:1 UNUN.
    """
    # Reflection coefficient
    refl_coeff = np.abs((Z_ant - Z_system) / (Z_ant + Z_system))
    # SWR formula
    swr = (1 + refl_coeff) / (1 - refl_coeff)
    return swr

def main():
    # Frequency range: 1.5 MHz to 30 MHz (covering 160m to 10m)
    frequencies = np.linspace(1.5, 30.0, 1000)
    
    # Wire lengths to test (in meters)
    # 8.84m (~29ft), 12.5m (~41ft), 21.64m (~71ft) are classic random wire lengths
    lengths_to_test = [8.84, 12.5, 21.64, 25.6] 
    lengths_to_test = [40, 20, 25.6] 
    
    plt.figure(figsize=(12, 6))
    
    # Plot SWR for each length
    for length in lengths_to_test:
        Z_ant = calculate_impedance(frequencies, length)
        swr = calculate_swr(Z_ant, Z_system=450) # 9:1 UNUN assumed
        plt.plot(frequencies, swr, label=f'{length}m ({length * 3.28084:.1f} ft)', linewidth=2)

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

    for band, (f_min, f_max) in ham_bands.items():
        plt.axvspan(f_min, f_max, color='gray', alpha=0.2)
        # Add label for the band slightly above the bottom
        plt.text(f_min + (f_max - f_min)/2, 1.2, band, 
                 horizontalalignment='center', verticalalignment='bottom', 
                 rotation=90, fontsize=8, alpha=0.7)

    # Chart formatting
    plt.title('Approximated SWR of Random Wire Antennas (using 9:1 UNUN)', fontsize=14)
    plt.xlabel('Frequency (MHz)', fontsize=12)
    plt.ylabel('SWR', fontsize=12)
    plt.ylim(1, 15)  # Cap SWR at 15 for readability (tuners usually max out at 10:1)
    plt.xlim(1.5, 30)
    plt.axhline(y=3, color='r', linestyle='--', alpha=0.5, label='SWR 3:1 (Tuner Limit)')
    
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    main()