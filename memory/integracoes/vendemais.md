# Vendemais — Sistema Integrador Interno

## O que é
Sistema web interno do ClubPetro que centraliza dados e oferece ferramentas para os times de Marketing e Comercial. Funcionalidades: mapeamento de mercado, analítico, construção de materiais, habilidades. Não substitui RD nem Kommo — é um centralizador com ferramentas próprias.

## Localização
- **Repo local**: `C:\Users\ClubPetro-123\Documents\vendemais`
- **GitHub**: https://github.com/andrecarvalhaes/vendemais.git
- **Branch principal**: `main`

## Stack
- **Frontend**: React 19 + TypeScript + Vite
- **Backend/DB**: Supabase
- **IA**: Google Generative AI (Gemini)
- **Gráficos**: Chart.js
- **Deploy**: GitHub Pages (Actions → `gh-pages` branch) + Firebase Hosting (`vendemais-3cec3`)

## Estrutura
```
vendemais/
├── src/
│   ├── components/
│   ├── layout/
│   ├── lib/
│   ├── pages/
│   └── App.tsx
├── .github/workflows/deploy.yml
├── firebase.json
├── vite.config.ts
├── package.json
└── index.html
```

## Workflow de Alterações (OBRIGATÓRIO)
1. Criar branch a partir de `main`
2. Fazer as alterações
3. Commit com mensagem descritiva
4. Abrir PR no GitHub com descrição em **português** do que foi feito
5. Retornar link de teste (preview/PR) para André validar
6. Só após aprovação, fazer merge para `main` (que faz deploy automático via GitHub Actions)

## Dev Local
- `npm run dev` — servidor local na porta 3000
- `npm run build` — build para `dist/`
- Requer `GEMINI_API_KEY` no `.env.local`
