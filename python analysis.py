import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


try:
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
   
    base_dir = os.getcwd()

csv_path = os.path.join(base_dir, 'countries of the world.csv')
df = pd.read_csv(csv_path)

numeric_columns = ['Pop. Density (per sq. mi.)', 'Coastline (coast/area ratio)', 
                   'Net migration', 'Infant mortality (per 1000 births)', 
                   'GDP ($ per capita)', 'Literacy (%)', 'Phones (per 1000)',
                   'Arable (%)', 'Crops (%)', 'Other (%)', 'Birthrate', 
                   'Deathrate', 'Agriculture', 'Industry', 'Service']

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.').replace('', np.nan)
        df[col] = pd.to_numeric(df[col], errors='coerce')

df['Country'] = df['Country'].str.strip()
df['Region'] = df['Region'].str.strip()

print("=" * 80)
print("ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ - GLOBAL BUDGET BRAIN (GBB)")
print("=" * 80)
print()


# ΥΠΟΘΕΣΗ 1: GDP per capita vs Βρεφική Θνησιμότητα
print("ΥΠΟΘΕΣΗ 1: Οι χώρες με υψηλότερο GDP per capita έχουν σημαντικά")
print("χαμηλότερα ποσοστά βρεφικής θνησιμότητας")
print("-" * 80)

hyp1_data = df[['Country', 'GDP ($ per capita)', 'Infant mortality (per 1000 births)']].dropna()

print(f"\nΔείγμα: {len(hyp1_data)} χώρες με πλήρη δεδομένα\n")

correlation, p_value = stats.pearsonr(
    hyp1_data['GDP ($ per capita)'], 
    hyp1_data['Infant mortality (per 1000 births)']
)

print(f"Συντελεστής Συσχέτισης Pearson: {correlation:.4f}")
print(f"P-value: {p_value:.2e}")
print(f"Στατιστική Σημαντικότητα: {'ΝΑΙ (p < 0.05)' if p_value < 0.05 else 'ΟΧΙ (p >= 0.05)'}")

gdp_median = hyp1_data['GDP ($ per capita)'].median()
hyp1_data['GDP_Group'] = hyp1_data['GDP ($ per capita)'].apply(
    lambda x: 'Υψηλό GDP' if x >= gdp_median else 'Χαμηλό GDP'
)

high_gdp_mortality = hyp1_data[hyp1_data['GDP_Group'] == 'Υψηλό GDP']['Infant mortality (per 1000 births)']
low_gdp_mortality = hyp1_data[hyp1_data['GDP_Group'] == 'Χαμηλό GDP']['Infant mortality (per 1000 births)']

print(f"\nΜέση Βρεφική Θνησιμότητα:")
print(f"  • Υψηλό GDP (>= ${gdp_median:,.0f}): {high_gdp_mortality.mean():.2f} ανά 1000")
print(f"  • Χαμηλό GDP (< ${gdp_median:,.0f}): {low_gdp_mortality.mean():.2f} ανά 1000")

t_stat, t_pvalue = stats.ttest_ind(high_gdp_mortality, low_gdp_mortality)
print(f"\nT-test: t={t_stat:.4f}, p={t_pvalue:.2e}")

print("\n ΑΠΟΤΕΛΕΣΜΑ ΥΠΟΘΕΣΗΣ 1:")
if correlation < -0.5 and p_value < 0.05:
    print(" ΕΠΑΛΗΘΕΥΕΤΑΙ ΠΛΗΡΩΣ")
    print("   Υπάρχει ισχυρή αρνητική συσχέτιση μεταξύ GDP και βρεφικής θνησιμότητας.")
    print("   Οι πλουσιότερες χώρες έχουν σημαντικά καλύτερα υγειονομικά αποτελέσματα.")
elif correlation < 0 and p_value < 0.05:
    print(" ΕΠΑΛΗΘΕΥΕΤΑΙ")
    print("   Υπάρχει στατιστικά σημαντική αρνητική συσχέτιση.")
else:
    print(" ΔΕΝ ΕΠΑΛΗΘΕΥΕΤΑΙ")

print("\n" + "=" * 80)


# ΥΠΟΘΕΣΗ 2: Δυτική Ευρώπη vs Υποσαχάρια Αφρική
print("\nΥΠΟΘΕΣΗ 2: Οι χώρες της Δυτικής Ευρώπης έχουν σημαντικά υψηλότερο GDP")
print("per capita και χαμηλότερο ποσοστό αγροτικού πληθυσμού από την")
print("Υποσαχάρια Αφρική")
print("-" * 80)

western_europe = df[df['Region'] == 'WESTERN EUROPE']
subsaharan_africa = df[df['Region'] == 'SUB-SAHARAN AFRICA']

print(f"\nΔείγμα:")
print(f"  • Δυτική Ευρώπη: {len(western_europe)} χώρες")
print(f"  • Υποσαχάρια Αφρική: {len(subsaharan_africa)} χώρες")

we_gdp = western_europe['GDP ($ per capita)'].dropna()
sa_gdp = subsaharan_africa['GDP ($ per capita)'].dropna()
we_agr = western_europe['Agriculture'].dropna()
sa_agr = subsaharan_africa['Agriculture'].dropna()


if we_gdp.empty or sa_gdp.empty or we_agr.empty or sa_agr.empty:
    print("\n⚠️ Insufficient data for comparison between regions.")
else:
    print("\n💰 ΣΥΓΚΡΙΣΗ GDP PER CAPITA:")
    print(f"\nΔυτική Ευρώπη:")
    print(f"  • Μέσος όρος: ${we_gdp.mean():,.0f}")
    print(f"  • Διάμεσος: ${we_gdp.median():,.0f}")
    print(f"  • Εύρος: ${we_gdp.min():,.0f} - ${we_gdp.max():,.0f}")

    print(f"\nΥποσαχάρια Αφρική:")
    print(f"  • Μέσος όρος: ${sa_gdp.mean():,.0f}")
    print(f"  • Διάμεσος: ${sa_gdp.median():,.0f}")
    print(f"  • Εύρος: ${sa_gdp.min():,.0f} - ${sa_gdp.max():,.0f}")

    u_stat_gdp, p_gdp = stats.mannwhitneyu(we_gdp, sa_gdp, alternative='greater')
    print(f"\nMann-Whitney U test (GDP): U={u_stat_gdp:.0f}, p={p_gdp:.2e}")

    
    print("\n🌾 ΣΥΓΚΡΙΣΗ ΠΟΣΟΣΤΟΥ ΑΓΡΟΤΙΚΟΥ ΤΟΜΕΑ:")
    print(f"\nΔυτική Ευρώπη:")
    print(f"  • Μέσο ποσοστό: {we_agr.mean()*100:.1f}%")
    print(f"  • Διάμεσο: {we_agr.median()*100:.1f}%")
    print(f"  • Εύρος: {we_agr.min()*100:.1f}% - {we_agr.max()*100:.1f}%")

    print(f"\nΥποσαχάρια Αφρική:")
    print(f"  • Μέσο ποσοστό: {sa_agr.mean()*100:.1f}%")
    print(f"  • Διάμεσο: {sa_agr.median()*100:.1f}%")
    print(f"  • Εύρος: {sa_agr.min()*100:.1f}% - {sa_agr.max()*100:.1f}%")

    u_stat_agr, p_agr = stats.mannwhitneyu(we_agr, sa_agr, alternative='less')
    print(f"\nMann-Whitney U test (Γεωργία): U={u_stat_agr:.0f}, p={p_agr:.2e}")

    print("\n📊 ΑΠΟΤΕΛΕΣΜΑ ΥΠΟΘΕΣΗΣ 2:")
    if p_gdp < 0.05 and p_agr < 0.05:
        print(" ✅ ΕΠΑΛΗΘΕΥΕΤΑΙ ΠΛΗΡΩΣ")
        print("   Και οι δύο διαφορές είναι στατιστικά σημαντικές (p < 0.05).")
        print(f"   • Η Δυτική Ευρώπη έχει {we_gdp.mean()/sa_gdp.mean():.1f}x υψηλότερο GDP")
        print(f"   • Η Υποσαχάρια Αφρική έχει {sa_agr.mean()/we_agr.mean():.1f}x υψηλότερο αγροτικό τομέα")
    else:
        parts_verified = []
        if p_gdp < 0.05:
            parts_verified.append("GDP")
        if p_agr < 0.05:
            parts_verified.append("Αγροτικός τομέας")
        
        if parts_verified:
            print(f" ⚠️ ΕΠΑΛΗΘΕΥΕΤΑΙ ΜΕΡΙΚΩΣ ({', '.join(parts_verified)})")
        else:
            print(" ❌ ΔΕΝ ΕΠΑΛΗΘΕΥΕΤΑΙ")

print("\n" + "=" * 80)
print("\n 🎯 ΣΥΜΠΕΡΑΣΜΑΤΑ ΓΙΑ ΤΟ GLOBAL BUDGET BRAIN:")
print("-" * 80)
print("""
1. Η ισχυρή συσχέτιση GDP-Βρεφικής Θνησιμότητας δείχνει ότι η οικονομική 
   ευημερία συνδέεται άμεσα με την ποιότητα των υγειονομικών υπηρεσιών.
   
2. Οι τεράστιες διαφορές μεταξύ Δυτικής Ευρώπης και Υποσαχάριας Αφρικής
   υπογραμμίζουν την ανάγκη για targeted budget optimization.

3. Το GBB μπορεί να βοηθήσει κυβερνήσεις να:
   • Εντοπίσουν inefficiencies στις δαπάνες υγείας
   • Βελτιώσουν την κατανομή πόρων στον αγροτικό τομέα
   • Συγκρίνουν την απόδοσή τους με άλλες χώρες
   • Προτεραιοποιήσουν επενδύσεις για μέγιστο κοινωνικό όφελος
""")
