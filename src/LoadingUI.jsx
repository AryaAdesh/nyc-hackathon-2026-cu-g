import { useState, useEffect } from 'react';

export default function LoadingUI() {
    const phases = [
        "Synthesizing Narrative...",
        "Orchestrating Multimodal Vectors...",
        "Rendering Nano Banana Assets...",
        "Fabricating Physics..."
    ];

    const [phaseIndex, setPhaseIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setPhaseIndex((prev) => (prev < phases.length - 1 ? prev + 1 : prev));
        }, 1500);
        return () => clearInterval(interval);
    }, [phases.length]);

    return (
        <div style={{
            position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh',
            display: 'flex', justifyContent: 'center', alignItems: 'center',
            zIndex: 10, pointerEvents: 'none', fontFamily: '"Space Grotesk", sans-serif'
        }}>
            <h2 style={{
                color: 'white', fontSize: '28px', fontWeight: '400', letterSpacing: '2px',
                animation: 'pulse 1.5s infinite' // Simple CSS pulse
            }}>
                {phases[phaseIndex]}
            </h2>
        </div>
    );
}