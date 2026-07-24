// Genera dades mensuals deterministes 2024-01 → 2026-07 (creixement + estacionalitat)
export function buildMonthly(){
  const MONTHS = [];
  for (let y=2024; y<=2026; y++) for (let m=1; m<=12; m++){ if(y===2026&&m>7) break; MONTHS.push([y,m]); }
  // nous seguidors per mes segons estacionalitat (index 1-12): set alt (inscripcions), estiu (campus/3x3), des/ago baix
  const season = {1:34,2:30,3:38,4:33,5:36,6:52,7:58,8:22,9:74,10:48,11:41,12:26};
  const growth = {2024:0.82,2025:1.0,2026:1.18}; // el club creix cada any
  let followers = 1585; // final 2023
  const monthly = {};
  for (const [y,m] of MONTHS){
    const key = `${y}-${String(m).padStart(2,'0')}`;
    const nf = Math.round(season[m]*growth[y]);
    followers += nf;
    const reach = Math.round((season[m]*growth[y])*720 + 16000);
    monthly[key] = {
      followers,
      newFollowers: nf,
      reach,
      profileViews: Math.round(reach*0.13),
      posts: [8,7,9,8,9,11,10,6,13,10,9,7][m-1],
      avgEngagement: +(5.4 + (season[m]/58)*2.6).toFixed(2),
    };
  }
  return monthly;
}
