import pandas as pd
import matplotlib.pyplot as plt

# Načítaj dataset
df = pd.read_csv('SquadLists.csv')

# Filtuj iba útočníkov (FW)
forwards = df[df['Position'] == 'FW']

# 1. TOP 10 Tímov
goals_by_team = forwards.groupby('Team')['Goals'].sum().nlargest(10)

# 2. Priemer výšky útočníkov
avg_height = forwards['Height (cm)'].mean()

# 3. Priemer Goals a Caps
avg_goals = forwards['Goals'].mean()
avg_caps = forwards['Caps'].mean()

print("=" * 60)
print("FOOTBALL ANALYSIS - ÚTOČNÍCI (FW)")
print("=" * 60)
print(f"\n📊 Celkový počet útočníkov: {len(forwards)}")
print(f"📏 Priemerná výška: {avg_height:.1f} cm")
print(f"⚽ Priemer gólov na hráča: {avg_goals:.1f}")
print(f"🎮 Priemer Caps na hráča: {avg_caps:.1f}")
print("\n" + "=" * 60)
print("TOP 10 TÍMOV PODĽA GÓLOV:")
print("=" * 60)
print(goals_by_team)

# Vytvor GRAFY
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Graf 1: TOP 10 tímov
goals_by_team.plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('TOP 10 Tímov podľa Gólov', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Tím')
axes[0, 0].set_ylabel('Počet Gólov')
axes[0, 0].tick_params(axis='x', rotation=45)

# Graf 2: Histogram výšky
axes[0, 1].hist(forwards['Height (cm)'].dropna(), bins=20, color='green', alpha=0.7)
axes[0, 1].set_title('Distribúcia Výšky Útočníkov', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Výška (cm)')
axes[0, 1].set_ylabel('Počet Hráčov')
axes[0, 1].axvline(avg_height, color='red', linestyle='--', label=f'Priemer: {avg_height:.1f}cm')
axes[0, 1].legend()

# Graf 3: Goals vs Caps (Scatter)
axes[1, 0].scatter(forwards['Caps'], forwards['Goals'], alpha=0.6, color='orange')
axes[1, 0].set_title('Góly vs. Skúsenosť (Caps)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Caps (Zápasy)')
axes[1, 0].set_ylabel('Góly')

# Graf 4: Top 10 hráčov
top_players = forwards.nlargest(10, 'Goals')[['Player Name', 'Goals']].set_index('Player Name')
top_players.plot(kind='barh', ax=axes[1, 1], color='purple', legend=False)
axes[1, 1].set_title('TOP 10 Hráčov podľa Gólov', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Počet Gólov')

plt.tight_layout()
plt.savefig('football_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Všetky grafy uložené ako 'football_analysis.png'")
plt.show()