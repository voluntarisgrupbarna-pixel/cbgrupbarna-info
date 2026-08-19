// Una sola font de contingut per a les 3 llengües. Editar aqui, no en 3 fitxers HTML.
// Aquest fitxer es la prova de concepte que soluciona el problema real:
// /femeni/ i les seves traduccions ja s'han desincronitzat perque cada versio
// es un HTML clonat a ma. Amb aquest patro, nomes hi ha UNA font.

export const locales = ['ca', 'es', 'en'] as const;
export type Locale = (typeof locales)[number];

export const instalacionsUi: Record<Locale, {
  eyebrow: string;
  title: string;
  lede: string;
  ctaMap: string;
  descriptions: Record<string, string>;
  tags: Record<string, string>;
}> = {
  ca: {
    eyebrow: 'El club',
    title: 'Instal·lacions',
    lede: "Sis pistes al Districte de Sant Martí. Quina et toca depèn de l'equip: consulta la fitxa del teu per saber-ho cada setmana.",
    ctaMap: 'Com arribar-hi →',
    tags: { seu: 'Seu principal', pista: 'Pista' },
    descriptions: {
      'la-nau-del-clot': 'El pavelló de referència del club.',
      'escola-provencals': 'Instal·lació esportiva del barri, al Districte de Sant Martí.',
      'la-farigola-del-clot': 'Instal·lació esportiva del barri del Clot.',
      'la-rambleta-del-clot': 'Instal·lació esportiva del barri del Clot.',
      'escola-casas': 'Instal·lació esportiva del barri del Clot.',
      'claror-maritim': "Instal·lació del Complex Esportiu Claror.",
    },
  },
  es: {
    eyebrow: 'El club',
    title: 'Instalaciones',
    lede: 'Seis pistas en el Districte de Sant Martí. Cuál te toca depende del equipo: consulta la ficha del tuyo para saberlo cada semana.',
    ctaMap: 'Cómo llegar →',
    tags: { seu: 'Sede principal', pista: 'Pista' },
    descriptions: {
      'la-nau-del-clot': 'El pabellón de referencia del club.',
      'escola-provencals': 'Instalación deportiva del barrio, en el Districte de Sant Martí.',
      'la-farigola-del-clot': 'Instalación deportiva del barrio del Clot.',
      'la-rambleta-del-clot': 'Instalación deportiva del barrio del Clot.',
      'escola-casas': 'Instalación deportiva del barrio del Clot.',
      'claror-maritim': 'Instalación del Complex Esportiu Claror.',
    },
  },
  en: {
    eyebrow: 'The club',
    title: 'Facilities',
    lede: "Six courts in the Sant Martí district. Which one your child trains at depends on the team: check your team's page to know each week.",
    ctaMap: 'Get directions →',
    tags: { seu: 'Main venue', pista: 'Court' },
    descriptions: {
      'la-nau-del-clot': "The club's main venue.",
      'escola-provencals': 'Neighbourhood sports facility in the Sant Martí district.',
      'la-farigola-del-clot': 'Neighbourhood sports facility in El Clot.',
      'la-rambleta-del-clot': 'Neighbourhood sports facility in El Clot.',
      'escola-casas': 'Neighbourhood sports facility in El Clot.',
      'claror-maritim': 'Court at the Complex Esportiu Claror.',
    },
  },
};
