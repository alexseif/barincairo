# Todo List: Frontend Vite SPA Migration & Refinement

**Topic**: frontend  
**Issue**: vite-refinement  
**Branch**: `frontend`  

- [ ] Task 1.1: Create & checkout `frontend` git branch
- [ ] Task 1.2: Scaffold Vite 6 configuration (`vite.config.ts`), `index.html`, `src/main.tsx`, `src/App.tsx`, and `package.json` scripts
- [ ] Task 2.1: Realign `VenueProperties` interface in `src/lib/api.ts` with Python FastAPI backend schema
- [ ] Task 2.2: Implement zero-fallback API fetching (`VITE_API_URL` / `http://127.0.0.1:8000`)
- [ ] Task 3.1: Build `Header` component with `rem` typography scale
- [ ] Task 3.2: Build `Hero` component with accessible "Wust El Balad" -> "Downtown" tooltip
- [ ] Task 4.1: Refactor `MapLibreMap` with WebGL `useRef` lifecycle cleanup on unmount
- [ ] Task 4.2: Implement mobile styled `<select>` combobox filters (Price & Vibe) for `< 768px` viewports & `min-h-[420px]` height
- [ ] Task 5.1: Build `Carousel` component with sub-header `"Selected for the night"`
- [ ] Task 5.2: Implement 3-bar carousel cycle with Prev (`<`) / Next (`>`) arrows and `1 / 3` tab indicators
- [ ] Task 5.3: Add mobile responsive card layout for venue hero card
- [ ] Task 6.1: Build `GroundRules` 4-rule responsive grid with updated Rule 4 text and `0.75rem` minimum font size
- [ ] Task 6.2: Fix mobile drawer navigation anchor links for smooth scrolling to `#about`
- [ ] Task 7.1: Configure `vitest.config.mts` for Vite/React 19 environment
- [ ] Task 7.2: Implement Vitest test suites (API zero-fallback, Hero tooltip, Carousel switcher, Ground rules grid)
- [ ] Task 7.3: Run `npm run build` and `npm run test` verification pass
