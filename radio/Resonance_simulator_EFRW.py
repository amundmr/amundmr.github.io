import numpy as np
import matplotlib.pyplot as plt

def calculate_impedance(f_MHz, length_m):
    """
    Approximates the complex feedpoint impedance (Z = R + jX) of an end-fed wire.
    """
    c = 299.792  # Speed of light in Mm/s
    wavelength = c / f_MHz
    beta = 2 * np.pi / wavelength
    
    Z0 = 500  # Characteristic impedance of the wire
    alpha = 0.015 + (0.001 * f_MHz) 
    
    prop_gamma = alpha + 1j * beta
    Z_ant = Z0 / np.tanh(prop_gamma * length_m)
    return Z_ant

def main():
    frequencies = np.linspace(1.5, 30.0, 1000)
    
    # Comparing the "Trap" (40m) and the "Magic" random wire (25.6m)
    lengths_to_test = [25.6, 40.0] 
    
    # Create a figure with 2 stacked subplots
    fig, (ax_x, ax_r) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    for length in lengths_to_test:
        Z_ant = calculate_impedance(frequencies, length)
        
        # Extract Resistance (Real part) and Reactance (Imaginary part)
        R = np.real(Z_ant)
        X = np.imag(Z_ant)
        
        label_str = f'{length}m ({length * 3.28084:.1f} ft)'
        
        # Top Plot: Reactance
        ax_x.plot(frequencies, X, label=label_str, linewidth=2)
        
        # Bottom Plot: Resistance
        ax_r.plot(frequencies, R, label=label_str, linewidth=2)

    # --- Highlight Ham Bands on both plots ---
    ham_bands = {
        '80m': (3.5, 4.0), '60m': (5.33, 5.40), '40m': (7.0, 7.3),
        '30m': (10.1, 10.15), '20m': (14.0, 14.35), '17m': (18.068, 18.168),
        '15m': (21.0, 21.45), '12m': (24.89, 24.99), '10m': (28.0, 29.7)
    }

    for ax in [ax_x, ax_r]:
        for band, (f_min, f_max) in ham_bands.items():
            ax.axvspan(f_min, f_max, color='gray', alpha=0.2)
            if ax == ax_x: # Only put labels on the top plot
                ax.text(f_min + (f_max - f_min)/2, 1500, band, 
                         horizontalalignment='center', verticalalignment='top', 
                         rotation=90, fontsize=8, alpha=0.7)

    # --- Formatting Reactance (Top) ---
    ax_x.set_title('Reactance (X) - Looking for Zero-Crossings (Resonance)', fontsize=14)
    ax_x.set_ylabel('Reactance (Ohms)', fontsize=12)
    ax_x.axhline(y=0, color='r', linestyle='-', alpha=0.8, label='Resonance (X=0)')
    ax_x.set_ylim(-2000, 2000) # Clamp the y-axis to see the zero crossings clearly
    ax_x.grid(True, linestyle='--', alpha=0.5)
    ax_x.legend(loc='lower right')

    # --- Formatting Resistance (Bottom) ---
    ax_r.set_title('Resistance (R) - How hard is it to match?', fontsize=14)
    ax_r.set_xlabel('Frequency (MHz)', fontsize=12)
    ax_r.set_ylabel('Resistance (Ohms) - Log Scale', fontsize=12)
    ax_r.set_yscale('log')
    ax_r.set_ylim(30, 10000)
    ax_r.axhline(y=450, color='g', linestyle='--', alpha=0.5, label='450 Ω (9:1 Target)')
    ax_r.grid(True, which='both', linestyle='--', alpha=0.5)
    ax_r.legend(loc='lower right')

    plt.xlim(1.5, 30)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()