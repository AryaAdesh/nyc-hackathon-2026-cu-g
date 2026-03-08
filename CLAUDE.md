# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev       # Start dev server with HMR (http://localhost:5173)
npm run build     # Production build
npm run preview   # Preview production build
npm run lint      # Run ESLint
```

No test suite is configured.

## Architecture

This is a React + Vite + Three.js app called **generative-thread** — an immersive 3D concept-exploration experience.

### App State Machine (`src/App.jsx`)

The entire application is driven by a linear state machine with these states:

```
ENTRY → GENERATING → EXPERIENCE → GENERATING_WORLD → EXPLORE_WORLD
```

- **ENTRY**: Shows `BreathingOrb` (3D) + `EntryUI` (HTML overlay). User types or speaks a prompt.
- **GENERATING**: Hides entry UI, shows `ParticleTransition` explosion + `LoadingUI` text overlay. Auto-advances after 5 seconds.
- **EXPERIENCE**: Shows `MainExperience` — a scroll-based 3D tunnel with clickable idea nodes.
- **GENERATING_WORLD**: Replays the `ParticleTransition` explosion after a node is clicked.
- **EXPLORE_WORLD**: Placeholder state showing the selected world number.

### 3D Layer vs HTML Overlay Pattern

All 3D content lives inside `<Canvas>` (React Three Fiber). HTML overlays (UI controls, loading text) are rendered outside `<Canvas>` with `position: absolute` and `zIndex: 10`. Some HTML is embedded inside the 3D scene via `@react-three/drei`'s `<Html>` component (used for node info cards in `MainExperience`).

### Key Components

- **`BreathingOrb`** (`src/BreathingOrb.jsx`): Animated distorted sphere using `MeshDistortMaterial`. Shrinks to 0 scale when `isListening` is true to reveal the waveform visualizer.
- **`EntryUI`** (`src/EntryUI.jsx`): HTML overlay with text input + Web Speech API voice recognition. Uses `AudioContext` + `AnalyserNode` to drive a 4-dot waveform visualizer in real time.
- **`ParticleTransition`** (`src/ParticleTransition.jsx`): 30,000-particle explosion using `THREE.Points` with additive blending. Calls `onComplete` after a fixed 5-second timeout.
- **`MainExperience`** (`src/MainExperience.jsx`): Scroll-driven tunnel using `@react-three/drei`'s `ScrollControls`. Camera moves along the Z-axis from z=10 to z=-180. Contains 3 hardcoded `IdeaNode` objects with placeholder concept data.
- **`LoadingUI`** (`src/LoadingUI.jsx`): HTML overlay that cycles through loading phase strings every 1.5s.

### Current Stub Areas

The app is a UI prototype — the prompt text from `EntryUI` is passed to `handlePromptSubmit` but never used (state just transitions to `GENERATING`). The `ideas` array in `MainExperience` is hardcoded; integration with an AI/generative backend is the intended next step.
