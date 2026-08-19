// Font unica per a /femeni/ (ca), /es/baloncesto-femenino/ i /en/womens-basketball/.
// Avui aquestes tres pagines ja han divergit perque son 3 HTML separats
// (veure PENDENTS-WEB.md). Aquest fitxer es la prova que, amb aquest patro,
// un canvi es fa un cop i surt correcte als tres idiomes -- FAQ i el seu
// JSON-LD inclosos, que es la part que ningu manté sincronitzada a ma.

export type Locale = 'ca' | 'es' | 'en';

export interface FaqItem { q: string; a: string }

export interface FemeniContent {
  eyebrowHero: string;
  h1: string;
  h1Em: string;
  lede: string;
  ctaPlay: string;
  ctaTeams: string;
  stats: { value: string; label: string }[];
  metode: { eyebrow: string; title: string; intro: string };
  pillars: { n: string; title: string; p1: string; p2: string }[];
  pull: string;
  faqEyebrow: string;
  faqTitle: string;
  faq: FaqItem[];
  closerTitle: string;
  closerP: string;
  ctaInfo: string;
  ctaWhatsapp: string;
  ctaSponsor: string;
}

export const femeni: Record<Locale, FemeniContent> = {
  ca: {
    eyebrowHero: 'El Clot · Barcelona · Des de 1965',
    h1: 'Bàsquet femení ',
    h1Em: 'de veritat',
    lede: "El CB Grup Barna destina el <strong>50% del pressupost</strong> al bàsquet femení quan la mitjana del sector és el 35%. Vuit equips federats, 38 entrenadores i un camí que va de l'Escoleta de 4 anys fins a la Lliga Femenina Endesa. No és una política de quotes: és com està construït el club des de 1965.",
    ctaPlay: 'Vull jugar-hi',
    ctaTeams: 'Els equips 26-27',
    stats: [
      { value: '50%', label: 'Del pressupost, al femení' },
      { value: '38', label: 'Entrenadores actives' },
      { value: '65,5%', label: "De l'staff tècnic són dones" },
      { value: '53,7%', label: "D'audiència femenina a xarxes" },
    ],
    metode: {
      eyebrow: 'El Mètode Barna',
      title: 'Un sistema. No una campanya.',
      intro: "Tres pilars que funcionen alhora i es reforcen entre ells. El club els ha construït de manera orgànica durant sis dècades, i avui són objecte d'estudi acadèmic a la UB-INEFC.",
    },
    pillars: [
      { n: '01', title: 'Inversió paritària', p1: 'El <b>50% del pressupost</b> del club va al bàsquet femení. La mitjana del sector és el 35%.', p2: 'Amb 140.000-160.000 € anuals, això vol dir 70.000-80.000 € al femení. No calen més diners: cal repartir d\'una altra manera els que ja hi ha.' },
      { n: '02', title: 'Pipeline de lideratge', p1: '<b>38 entrenadores actives</b>, el 65,5% de l\'staff tècnic. Entrenen 40 equips cada setmana al Clot.', p2: 'La jugadora que es fa entrenadora — i que entrena equips masculins — canvia la percepció de les nenes, dels nens i de les famílies més que cap campanya d\'igualtat.' },
      { n: '03', title: 'Resposta de la comunitat', p1: 'El <b>53,7% de l\'audiència</b> del club a xarxes són dones. Al bàsquet base, les audiències digitals solen ser un 60-70% masculines.', p2: 'Sense cap campanya dirigida. Quan un club practica la igualtat en comptes de comunicar-la, la comunitat que hi correspon apareix sola.' },
    ],
    pull: '«No les busquem. Ens troben.»',
    faqEyebrow: 'Per a famílies',
    faqTitle: 'Preguntes freqüents',
    faq: [
      { q: 'Quants equips femenins té el club?', a: "La temporada 2026-27 n'hi ha vuit amb competició federada FCBQ, de l'Infantil al Sènior, més els grups d'Escoleta i l'equip d'esport adaptat Barna Màgics. El Sènior Femení A competeix a la Super Copa Femenina." },
      { q: 'La meva filla no ha jugat mai. Pot començar?', a: "Sí. L'Escoleta acull nenes i nens de 4 a 8 anys sense cap experiència prèvia, i a les categories de formació s'entra durant el curs si hi ha plaça. Escriu-nos i et diem què li toca per edat." },
      { q: 'Què costa? Hi ha beques?', a: "El club manté beques socials perquè cap nena es quedi fora per motius econòmics. Explica'ns el cas i ho mirem sense compromís." },
      { q: 'Qui entrena els equips femenins?', a: "38 entrenadores actives, el 65,5% de l'staff tècnic del club. Moltes són exjugadores formades a casa, i entrenen equips femenins, mixtos i també masculins." },
      { q: "On s'entrena i es juga?", a: "A La Nau del Clot, C/ Llacuna 172, dins el Parc del Clot (08018 Barcelona), al Districte de Sant Martí." },
    ],
    closerTitle: 'Aquí hi caben totes',
    closerP: "Tant si vol començar als 4 anys com si busca competir a la Super Copa, hi ha un lloc per a ella. I si la teva empresa vol acompanyar el projecte femení, també.",
    ctaInfo: 'Demanar informació',
    ctaWhatsapp: 'WhatsApp del club',
    ctaSponsor: 'Patrocinar el femení',
  },
  es: {
    eyebrowHero: 'El Clot · Barcelona · Desde 1965',
    h1: 'Baloncesto femenino ',
    h1Em: 'de verdad',
    lede: 'El CB Grup Barna destina el <strong>50% del presupuesto</strong> al baloncesto femenino cuando la media del sector es del 35%. Ocho equipos federados, 38 entrenadoras y un camino que va de la Escoleta de 4 años hasta la Liga Femenina Endesa. No es una política de cuotas: es como está construido el club desde 1965.',
    ctaPlay: 'Quiero jugar',
    ctaTeams: 'Los equipos 26-27',
    stats: [
      { value: '50%', label: 'Del presupuesto, al femenino' },
      { value: '38', label: 'Entrenadoras activas' },
      { value: '65,5%', label: 'Del staff técnico son mujeres' },
      { value: '53,7%', label: 'De audiencia femenina en redes' },
    ],
    metode: {
      eyebrow: 'El Método Barna',
      title: 'Un sistema. No una campaña.',
      intro: 'Tres pilares que funcionan a la vez y se refuerzan entre ellos. El club los ha construido de forma orgánica durante seis décadas, y hoy son objeto de estudio académico en la UB-INEFC.',
    },
    pillars: [
      { n: '01', title: 'Inversión paritaria', p1: 'El <b>50% del presupuesto</b> del club va al baloncesto femenino. La media del sector es del 35%.', p2: 'Con 140.000-160.000 € anuales, eso significa 70.000-80.000 € al femenino. No hacen falta más recursos: hay que repartir de otra manera los que ya hay.' },
      { n: '02', title: 'Pipeline de liderazgo', p1: '<b>38 entrenadoras activas</b>, el 65,5% del staff técnico. Entrenan 40 equipos cada semana en El Clot.', p2: 'La jugadora que se hace entrenadora —y que entrena equipos masculinos— cambia la percepción de las niñas, los niños y las familias más que cualquier campaña de igualdad.' },
      { n: '03', title: 'Respuesta de la comunidad', p1: 'El <b>53,7% de la audiencia</b> del club en redes son mujeres. En el baloncesto base, las audiencias digitales suelen ser un 60-70% masculinas.', p2: 'Sin ninguna campaña dirigida. Cuando un club practica la igualdad en vez de comunicarla, la comunidad correspondiente aparece sola.' },
    ],
    pull: '«No las buscamos. Nos encuentran.»',
    faqEyebrow: 'Para familias',
    faqTitle: 'Preguntas frecuentes',
    faq: [
      { q: '¿Cuántos equipos femeninos tiene el club?', a: 'La temporada 2026-27 hay ocho con competición federada FCBQ, desde Infantil hasta Sénior, más los grupos de Escoleta y el equipo de deporte adaptado Barna Màgics. El Sénior Femenino A compite en la Super Copa Femenina.' },
      { q: 'Mi hija nunca ha jugado. ¿Puede empezar?', a: 'Sí. La Escoleta acoge a niñas y niños de 4 a 8 años sin experiencia previa, y en las categorías de formación se puede entrar durante el curso si hay plaza. Escríbenos y te decimos qué le corresponde por edad.' },
      { q: '¿Qué cuesta? ¿Hay becas?', a: 'El club mantiene becas sociales para que ninguna niña se quede fuera por motivos económicos. Cuéntanos el caso y lo miramos sin compromiso.' },
      { q: '¿Quién entrena a los equipos femeninos?', a: '38 entrenadoras activas, el 65,5% del staff técnico del club. Muchas son exjugadoras formadas en casa, y entrenan equipos femeninos, mixtos y también masculinos.' },
      { q: '¿Dónde se entrena y se juega?', a: 'En La Nau del Clot, C/ Llacuna 172, dentro del Parc del Clot (08018 Barcelona), en el Districte de Sant Martí.' },
    ],
    closerTitle: 'Aquí caben todas',
    closerP: 'Tanto si quiere empezar a los 4 años como si busca competir en la Super Copa, hay un lugar para ella. Y si tu empresa quiere acompañar el proyecto femenino, también.',
    ctaInfo: 'Pedir información',
    ctaWhatsapp: 'WhatsApp del club',
    ctaSponsor: 'Patrocinar el femenino',
  },
  en: {
    eyebrowHero: 'El Clot · Barcelona · Since 1965',
    h1: "Women's basketball ",
    h1Em: 'done right',
    lede: "CB Grup Barna puts <strong>50% of its budget</strong> into women's basketball, when the sector average is 35%. Eight federated teams, 38 coaches, and a pathway from the 4-year-old Escoleta to the Liga Femenina Endesa. It's not a quota policy: it's how the club has been built since 1965.",
    ctaPlay: 'I want to play',
    ctaTeams: 'The 26-27 teams',
    stats: [
      { value: '50%', label: "Of the budget, to women's basketball" },
      { value: '38', label: 'Active coaches' },
      { value: '65.5%', label: 'Of the coaching staff are women' },
      { value: '53.7%', label: 'Female audience on social media' },
    ],
    metode: {
      eyebrow: 'The Barna Method',
      title: 'A system. Not a campaign.',
      intro: 'Three pillars that work together and reinforce each other. The club has built them organically over six decades, and today they are the subject of academic study at UB-INEFC.',
    },
    pillars: [
      { n: '01', title: 'Equal investment', p1: "<b>50% of the club's budget</b> goes to women's basketball. The sector average is 35%.", p2: 'With €140,000-160,000 a year, that means €70,000-80,000 for women\'s basketball. It doesn\'t take more money: it takes distributing what\'s already there differently.' },
      { n: '02', title: 'Leadership pipeline', p1: '<b>38 active coaches</b>, 65.5% of the technical staff. They coach 40 teams every week in El Clot.', p2: "The player who becomes a coach — and who coaches boys' teams too — changes how girls, boys and families see the sport more than any equality campaign." },
      { n: '03', title: 'Community response', p1: "<b>53.7% of the club's audience</b> on social media are women. In youth basketball, digital audiences are usually 60-70% male.", p2: 'Without any targeted campaign. When a club practices equality instead of just talking about it, the community that matches it shows up on its own.' },
    ],
    pull: '"We don\'t look for them. They find us."',
    faqEyebrow: 'For families',
    faqTitle: 'Frequently asked questions',
    faq: [
      { q: 'How many women\'s teams does the club have?', a: 'In the 2026-27 season there are eight competing in the FCBQ federated league, from U-14 to Senior, plus the Escoleta groups and the Barna Màgics adapted-sports team. The Senior Women\'s A team competes in the Super Copa Femenina.' },
      { q: "My daughter has never played. Can she start?", a: 'Yes. The Escoleta welcomes girls and boys aged 4 to 8 with no prior experience, and in the development categories you can join mid-season if there is a spot. Write to us and we\'ll tell you what fits her age.' },
      { q: 'What does it cost? Are there scholarships?', a: 'The club keeps social scholarships so no girl is left out for financial reasons. Tell us your situation and we\'ll look into it, no strings attached.' },
      { q: "Who coaches the women's teams?", a: '38 active coaches, 65.5% of the club\'s technical staff. Many are former players trained at the club, and they coach women\'s, mixed and men\'s teams alike.' },
      { q: 'Where do they train and play?', a: 'At La Nau del Clot, C/ Llacuna 172, inside Parc del Clot (08018 Barcelona), in the Sant Martí district.' },
    ],
    closerTitle: "There's room here for all of them",
    closerP: "Whether she wants to start at age 4 or aims to compete in the Super Copa, there's a place for her. And if your company wants to support the women's project, there's a place for you too.",
    ctaInfo: 'Request information',
    ctaWhatsapp: 'Club WhatsApp',
    ctaSponsor: "Sponsor the women's project",
  },
};
